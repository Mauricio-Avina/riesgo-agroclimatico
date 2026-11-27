"""Contrato HTTP y conservación de la información disponible en cada horizonte."""
import unittest
from unittest.mock import patch

import joblib
import numpy as np
from fastapi.testclient import TestClient

from src import config
from src.api.esquemas import Solicitud
from src.api.main import app
from src.models.objetivo import cargar, predictores


class PruebaAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)
        cls.cliente.__enter__()
        cls.addClassCleanup(cls.cliente.__exit__, None, None, None)
        cls.ejemplo = config.EJEMPLO_API.copy()
        cls.datos = cargar()

    def post(self, ruta="prediccion", **cambios):
        return self.cliente.post("/v1/"+ruta, json=self.ejemplo | cambios)

    def test_catalogo_y_salud(self):
        self.assertEqual(self.cliente.get("/v1/salud").status_code, 200)
        catalogo = self.cliente.get("/v1/municipios").json()
        self.assertEqual(len(catalogo), config.MUNICIPIOS_ESPERADOS)
        self.assertEqual(sum(len(m["modalidades"]) for m in catalogo), 121)
        m = next(m for m in catalogo if len(m["modalidades"]) == 1)
        falta = next(v for v in config.MODALIDADES if v not in m["modalidades"])
        self.assertEqual(self.post(cvegeo=m["cvegeo"], modalidad=falta).status_code, 404)

    def test_errores(self):
        for ruta in ["prediccion","explicacion"]:
            self.assertEqual(self.post(ruta, cvegeo="99999").status_code, 404)
            for invalido in [dict(cvegeo="1103"),dict(ultima_etapa="otoño"),dict(modalidad="otro")]:
                resp = self.post(ruta, **invalido)
                self.assertEqual(resp.status_code, 422)
                self.assertIn("Solicitud inválida", resp.json()["detalle"])

    def test_llenado(self):
        e = self.ejemplo
        fila = self.datos.loc[
            self.datos.cvegeo.eq(e["cvegeo"]) & self.datos.modalidad.eq(e["modalidad"]) & self.datos.anio.eq(e["anio"])]
        pron = self.post(ultima_etapa="llenado").json()
        nombre = self.cliente.get("/v1/salud").json()["modelo"]
        modelo = joblib.load(config.ARTEFACTOS / f"completa_{nombre}_platt.joblib")
        esperado = modelo.predict_proba(predictores(fila,"completa"))[0,1]
        self.assertEqual(pron["probabilidad"], round(float(esperado), 4))
        self.assertEqual(pron["p10"], pron["p90"])
        self.assertEqual(pron["escenarios"], 1)

    def test_analogos_y_explicacion(self):
        peticion = self.ejemplo | {"ultima_etapa":"vegetativo"}
        a = self.post(ultima_etapa="vegetativo").json()
        self.assertEqual(a, self.post(ultima_etapa="vegetativo").json())
        self.assertTrue(all(y < peticion["anio"] for y in a["anios_analogos"]))
        s = app.state.servicio
        x, anios = s.escenarios(Solicitud(**peticion))
        self.assertEqual(x.lluvia_siembra_mm.nunique(), 1)
        hist = self.datos.loc[self.datos.cvegeo.eq(peticion["cvegeo"]) & self.datos.modalidad.eq(peticion["modalidad"])].set_index("anio")
        np.testing.assert_array_equal(x.lluvia_llenado_mm.to_numpy(), hist.loc[anios].lluvia_llenado_mm.to_numpy())
        # En un ciclo abierto, el clima posterior aún puede carecer de valor.
        historia = s.historia.copy()
        piloto = (historia.cvegeo.eq(peticion["cvegeo"]) & historia.modalidad.eq(peticion["modalidad"])
                  & historia.anio.eq(peticion["anio"]))
        historia.loc[piloto, "lluvia_llenado_mm"] = np.nan
        with patch.object(s, "historia", historia):
            self.assertEqual(a, self.post(ultima_etapa="vegetativo").json())
        probs = s.calibrado.predict_proba(x)[:,1]
        np.testing.assert_array_equal([a["probabilidad"], a["p10"], a["p90"]],
                                      np.round([probs.mean(), *np.quantile(probs,config.CUANTILES_ANALOGOS)], 4))
        b = self.post("explicacion", ultima_etapa="vegetativo").json()
        self.assertEqual(a,b["prediccion"])
        self.assertEqual(len(b["factores"]),config.N_TEXTO)
        self.assertEqual(self.post(anio=config.ANIO_INICIAL,ultima_etapa="vegetativo").status_code,404)

    def test_siembra_es_historia_disponible(self):
        from src.models.busqueda import CLAVES, Climatologia
        for anio in [2012, 2021, 2025]:
            pron = self.post(ultima_etapa="siembra", anio=anio).json()
            antes = self.datos.loc[self.datos.anio.lt(min(anio, min(config.ANIOS_MODELO["prueba"])))]
            consulta = antes.loc[antes.cvegeo.eq(self.ejemplo["cvegeo"]) & antes.modalidad.eq(self.ejemplo["modalidad"]), CLAVES].iloc[:1]
            ref = Climatologia().fit(antes[CLAVES], antes.perdida).predict_proba(consulta)[0, 1]
            self.assertEqual(pron["probabilidad"], round(float(ref), 4))
            self.assertEqual((pron["fuente"], pron["escenarios"], pron["p10"], pron["p90"]), ("climatologia", 0, None, None))
            exp = self.post("explicacion", ultima_etapa="siembra", anio=anio).json()
            self.assertEqual(exp["prediccion"], pron)
            self.assertEqual(exp["factores"], [])
        self.assertEqual(self.post(ultima_etapa="siembra", anio=config.ANIO_INICIAL).status_code, 404)

    def test_direcciones_rf07(self):
        modelo = app.state.servicio.calibrado
        x = predictores(self.datos.tail(100), "completa")
        for nombre, signo in config.DIRECCIONES_RF07.items():
            minimo, maximo = self.datos[nombre].min(), self.datos[nombre].max()
            p = [modelo.predict_proba(x.assign(**{nombre: v}))[:, 1] for v in np.linspace(minimo, maximo, 8)]
            self.assertTrue((signo * np.diff(p, axis=0) >= -1e-12).all())
