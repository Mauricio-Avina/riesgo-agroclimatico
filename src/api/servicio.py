"""Consulta del piloto municipal con trayectorias de clima histórico y TreeSHAP."""
import joblib
import numpy as np
import pandas as pd
import shap

from src import config
from src.models.busqueda import CLAVES, Climatologia
from src.models.evaluacion import clasificar
from src.models.explicacion import etiqueta
from src.models.objetivo import cargar, predictores


class SinDatos(LookupError):
    """La clave, la observación o el historial requerido no tienen cobertura."""


class Servicio:
    def __init__(self):
        datos = cargar()
        self.historia = datos[["cvegeo", "municipio", "anio", "perdida", *config.FIJAS_MODELO, *config.CLIMA_MODELO]]
        self.catalogo = (datos.groupby(["cvegeo", "municipio"], as_index=False)
                         .modalidad.agg(lambda s: sorted(s.unique())).rename(columns={"modalidad": "modalidades"}))
        self.nombre = "boosting_monotono"
        self.inicio_prueba = min(config.ANIOS_MODELO["prueba"])
        self.referencia = joblib.load(config.ARTEFACTOS / "referencia_preprueba.joblib")
        self.calibrado = joblib.load(config.ARTEFACTOS / f"completa_{self.nombre}_platt.joblib")
        # El estimador congelado es el mismo árbol que produjo las probabilidades.
        self.modelo = self.calibrado.estimator.estimator
        self.preparar = self.modelo.named_steps["preparar"]
        self.explicador = shap.TreeExplainer(self.modelo.named_steps["modelo"])
        self.costos = pd.read_csv(config.REPORTES / "costos_semaforo.csv")

    def municipios(self, cvegeo=None):
        """Consultar el catálogo, incluidas las modalidades realmente presentes."""
        filas = self.catalogo if cvegeo is None else self.catalogo[self.catalogo.cvegeo.eq(cvegeo)]
        if filas.empty:
            raise SinDatos("El municipio no pertenece al catálogo del piloto.")
        return filas.to_dict("records")

    def escenarios(self, solicitud):
        """Mantener fijos el perfil actual y el clima observado. Cada año aporta un futuro completo."""
        grupo = self.historia.loc[self.historia.cvegeo.eq(solicitud.cvegeo)
                                  & self.historia.modalidad.eq(solicitud.modalidad.value)]
        fila = grupo.loc[grupo.anio.eq(solicitud.anio)]
        if fila.empty:
            raise SinDatos("No hay datos para ese municipio, modalidad y año.")
        etapas = list(config.ETAPAS)
        pendientes = etapas[etapas.index(solicitud.ultima_etapa.value) + 1:]
        if not pendientes:
            return predictores(fila, "completa"), []
        analogos = grupo.loc[grupo.anio.lt(solicitud.anio)].sort_values("anio")
        if analogos.empty:
            raise SinDatos("No hay años anteriores para completar las etapas pendientes.")
        columnas = [c for c in config.CLIMA_MODELO if any(e in c.split("_") for e in pendientes)]
        matriz = fila.iloc[np.zeros(len(analogos), dtype=int)].reset_index(drop=True)
        for col in columnas:
            matriz[col] = analogos[col].to_numpy()
        return predictores(matriz, "completa"), analogos.anio.to_list()

    def resumir(self, matriz, anios):
        """Clasificar la media calibrada; los percentiles describen la dispersión entre escenarios."""
        probabilidades = self.calibrado.predict_proba(matriz)[:, 1]
        media = float(probabilidades.mean())
        p10, p90 = np.quantile(probabilidades, config.CUANTILES_ANALOGOS)
        return dict(fuente=self.nombre, probabilidad=round(media, 4), nivel=str(clasificar(np.array([media]), self.costos)[0]),
                    p10=round(float(p10), 4), p90=round(float(p90), 4), escenarios=len(matriz), anios_analogos=anios)

    def referencia_siembra(self, solicitud):
        clave = solicitud.cvegeo
        modalidad = solicitud.modalidad.value
        historico = self.historia
        grupo = historico.cvegeo.eq(clave) & historico.modalidad.eq(modalidad)
        if not (grupo & historico.anio.eq(solicitud.anio)).any():
            raise SinDatos("No hay datos para ese municipio, modalidad y año.")
        corte = min(solicitud.anio, self.inicio_prueba)
        previos = historico.loc[historico.anio.lt(corte)]
        local = previos.loc[previos.cvegeo.eq(clave) & previos.modalidad.eq(modalidad)]
        if local.empty:
            raise SinDatos("No hay años anteriores para estimar la frecuencia municipal.")
        referencia = self.referencia if corte == self.inicio_prueba else Climatologia().fit(previos[CLAVES], previos.perdida)
        p = float(referencia.predict_proba(local[CLAVES].iloc[:1])[0, 1])
        nivel = str(clasificar(np.array([p]), self.costos)[0])
        pron = dict(fuente="climatologia", probabilidad=round(p, 4), nivel=nivel, p10=None, p90=None,
                    escenarios=0, anios_analogos=[])
        texto = (f"Al cierre de {corte-1}, hubo pérdida en {int(local.perdida.sum())} de {len(local)} "
                 f"ciclos municipales de {modalidad.lower()}. La tasa se suaviza con {config.PESO_PREVIA:g} "
                 f"ciclos equivalentes a la frecuencia de esa modalidad. Riesgo histórico: {p:.1%}.")
        return pron, texto

    def prediccion(self, solicitud):
        if solicitud.ultima_etapa.value == "siembra":
            return self.referencia_siembra(solicitud)[0]
        return self.resumir(*self.escenarios(solicitud))

    def explicacion(self, solicitud):
        """Promediar atribuciones crudas sobre exactamente los mismos escenarios que la predicción."""
        if solicitud.ultima_etapa.value == "siembra":
            pron, texto = self.referencia_siembra(solicitud)
            return dict(prediccion=pron, escala="frecuencia histórica suavizada", base=pron["probabilidad"],
                        salida_media=pron["probabilidad"], factores=[], texto=texto)
        matriz, anios = self.escenarios(solicitud)
        pronostico = self.resumir(matriz, anios)
        exp = self.explicador(self.preparar.transform(matriz))
        valores = exp.values
        base = float(np.mean(exp.base_values))
        escala = "logaritmo de momios sin calibrar"
        aportes = pd.Series(valores.mean(axis=0), index=self.preparar.get_feature_names_out())
        for var in config.CATEGORICAS_MODELO:
            indicadores = [c for c in aportes.index if c.startswith(var+"_")]
            aporte = aportes[indicadores].sum()
            aportes = aportes.drop(indicadores)
            aportes[var] = aporte
        factores = []
        for var in aportes.abs().nlargest(config.N_TEXTO).index:
            valor = float(aportes[var])
            factores.append(dict(variable=etiqueta(var),
                                 direccion="eleva" if valor > 0 else "reduce" if valor < 0 else "neutra",
                                 aporte=valor))
        senales = ", ".join(f["variable"]+" ("+f["direccion"]+")" for f in factores)
        texto = (f"El riesgo estimado es {pronostico['probabilidad']:.1%} y el aviso es {pronostico['nivel']}. "
                 f"Las señales que más pesaron en el modelo fueron {senales}.")
        return dict(prediccion=pronostico, escala=escala, base=float(base),
                    salida_media=float(base+aportes.sum()), factores=factores, texto=texto)
