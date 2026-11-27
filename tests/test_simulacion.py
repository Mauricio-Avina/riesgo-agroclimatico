"""Equivalencia con oro, cobertura, sensibilidad y operación local."""
import json
import unittest

from fastapi.testclient import TestClient
import numpy as np
from threadpoolctl import threadpool_limits

from src import config
from src.api.esquemas import Palanca
from src.api.fichas import frecuencia
from src.api.main import app


class PruebaSimulacion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.limites = threadpool_limits(limits=1)
        cls.addClassCleanup(cls.limites.restore_original_limits)
        cls.c = TestClient(app)
        cls.c.__enter__()
        cls.addClassCleanup(cls.c.__exit__, None, None, None)
        cls.p = dict(modalidad="Temporal", fecha="06-15")
        cls.entrada = dict(cvegeo="11032",actual=cls.p,alternativa_b=cls.p | {"fecha":"07-01"},
                           alternativa_c=cls.p | {"modalidad":"Riego"})

    def test_control_pareado_y_tornado(self):
        x = self.c.post("/v1/simulacion",json=self.entrada)
        self.assertEqual(x.status_code,200,x.text)
        d=x.json(); filas=d["resultados"]
        self.assertEqual([r["anio"] for r in filas],[2005,2006,2004]*3)
        self.assertEqual(len(d["tornado"]),10)
        for r in filas[:3]:
            y=self.c.post("/v1/prediccion",json=dict(cvegeo="11032",modalidad="Temporal",anio=r["anio"],ultima_etapa="llenado")).json()
            self.assertEqual((r["probabilidad"],r["nivel"]),(y["probabilidad"],y["nivel"]))

    def test_banda_de_fechas_y_limites(self):
        sim = app.state.simulador
        for fecha, primero, ultimo in [("06-01","06-01","06-02"),("06-15","06-14","06-16"),("07-15","07-14","07-15")]:
            palanca = Palanca(modalidad="Temporal", fecha=fecha)
            matriz = sim.matriz("11032", palanca, 2005)
            p, banda = sim.banda_fecha("11032", palanca, 2005, matriz)
            self.assertEqual((banda["desde"], banda["hasta"]), (primero, ultimo))
            self.assertLessEqual(banda["minimo"], round(p,4))
            self.assertLessEqual(round(p,4), banda["maximo"])

    def test_variables_y_extremos(self):
        sim=app.state.simulador
        oro=sim.historia.query("cvegeo=='11032' and anio==2005 and modalidad=='Temporal'").iloc[0]
        original=sim.matriz("11032",Palanca(**self.p),2005).iloc[0]
        cols=list(config.CLIMA_MODELO)
        np.testing.assert_array_equal(oro[cols].values,original[cols].values)
        movida=sim.matriz("11032",Palanca(**(self.p | {"fecha":"07-01"})),2005).iloc[0]
        self.assertTrue((movida[cols]!=original[cols]).any())
        extremo=original.copy(); extremo["lluvia_siembra_mm"]=99999
        self.assertTrue(any(a["valor"]==99999 for a in sim.fuera(extremo)))

    def test_contratos(self):
        sin_riego=next(m for m in self.c.get("/v1/municipios").json() if m["modalidades"]==["Temporal"])
        self.assertEqual(self.c.post("/v1/simulacion",json=self.entrada | {"cvegeo":sin_riego["cvegeo"]}).status_code,404)
        self.assertEqual(self.c.post("/v1/simulacion",json=self.entrada | {"actual":self.p | {"fecha":"06-31"}}).status_code,422)
        for clave,esperado in [("99999",404),("abc",422)]:
            self.assertEqual(self.c.get("/v1/boletin/"+clave).status_code,esperado)
        self.assertEqual(frecuencia(.04),"4 de cada 100")
        self.assertEqual(frecuencia(.004),"Menos de 1 de cada 100")

    def test_historial_incluye_rendimiento_sin_observacion(self):
        h = app.state.servicio.datos
        clave = h.loc[h.rendimiento_t_ha.isna(), "cvegeo"].iloc[0]
        respuesta = self.c.get("/v1/historial/" + clave)
        self.assertEqual(respuesta.status_code, 200)
        filas = respuesta.json()["filas"]
        self.assertEqual(set(filas[0]), set(config.CAMPOS_PUBLICOS))
        self.assertTrue(any(r["rendimiento_t_ha"] is None for r in filas))

    def test_copia_generada(self):
        if not config.FICHA_LOCAL.exists():
            self.skipTest("Ejecutar el precalculado para probar la distribución instalada.")
        datos=json.loads(config.FICHA_LOCAL.read_text(encoding="utf-8"))
        llaves={(f["cvegeo"],f["modalidad"],f["ultima_etapa"]) for f in datos["fichas"]}
        self.assertEqual(len(llaves),len(datos["fichas"]))
        self.assertEqual(len(llaves),sum(len(m["modalidades"]) for m in datos["catalogo"])*len(config.ETAPAS))
        for f in datos["fichas"]:
            self.assertEqual(len(f["factores"]),3)
        for m in datos["catalogo"]:
            b=self.c.get("/v1/boletin/"+m["cvegeo"])
            self.assertEqual(b.status_code,200)
            self.assertTrue(b.content.startswith(b"%PDF"))
