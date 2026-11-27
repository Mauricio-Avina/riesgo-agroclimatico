"""Consulta del piloto municipal con trayectorias de clima histórico y TreeSHAP."""
import joblib
import numpy as np
import pandas as pd
import shap

from src import config
from src.models.busqueda import CLAVES, Climatologia
from src.models.evaluacion import ajustar_platt, clasificar
from src.models.explicacion import etiqueta
from src.models.objetivo import cargar, predictores


class SinDatos(LookupError):
    """La clave, la observación o el historial requerido no tienen cobertura."""


class Servicio:
    def __init__(self):
        datos = cargar()
        self.datos = datos
        self.historia = datos[["cvegeo", "municipio", "anio", "perdida", *config.FIJAS_MODELO, *config.CLIMA_MODELO]]
        self.catalogo = (datos.groupby(["cvegeo", "municipio"], as_index=False)
                         .modalidad.agg(lambda s: sorted(s.unique())).rename(columns={"modalidad": "modalidades"}))
        self.nombre = "boosting_monotono"
        self.inicio_prueba = min(config.ANIOS_MODELO["prueba"])
        self.climas_siembra = self.cargar_climatologias()
        self.calibrado = joblib.load(config.ARTEFACTOS / f"completa_{self.nombre}_platt.joblib")
        # El estimador congelado es el mismo árbol que produjo las probabilidades.
        self.modelo = self.calibrado.estimator.estimator
        self.preparar = self.modelo.named_steps["preparar"]
        self.explicador = shap.TreeExplainer(self.modelo.named_steps["modelo"])
        self.costos = pd.read_csv(config.REPORTES / "costos_semaforo.csv")

    def cargar_climatologias(self):
        """Preparar al iniciar los pronósticos de siembra con historia disponible en cada corte."""
        fin_base = max(config.ANIOS_MODELO["entrenamiento"])
        fin_platt = max(config.ANIOS_MODELO["validacion"])
        operativo = joblib.load(config.ARTEFACTOS / "completa_climatologia_platt.joblib")
        modelos = {self.inicio_prueba: (operativo, fin_base, fin_platt)}
        # Cortes retrospectivos: al menos un año de ajuste y uno posterior para Platt.
        anios = sorted(self.historia.anio.unique())
        for anio in anios:
            if anio >= self.inicio_prueba:
                break
            anteriores = [a for a in anios if a < anio]
            if len(anteriores) < 2:
                continue
            n_cal = min(len(config.ANIOS_MODELO["validacion"]), len(anteriores) - 1)
            base = self.historia.loc[self.historia.anio.isin(anteriores[:-n_cal])]
            cal = self.historia.loc[self.historia.anio.isin(anteriores[-n_cal:])]
            if min(base.perdida.nunique(), cal.perdida.nunique()) < 2:
                continue
            crudo = Climatologia().fit(base[CLAVES], base.perdida)
            modelo = ajustar_platt(crudo, cal[CLAVES], cal.perdida)
            modelos[anio] = (modelo, base.anio.max(), cal.anio.max())
        return modelos

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
        if corte not in self.climas_siembra or not (grupo & historico.anio.lt(corte)).any():
            raise SinDatos("Falta historia anterior para estimar y calibrar el riesgo de siembra.")
        modelo, fin_base, fin_cal = self.climas_siembra[corte]
        local = historico.loc[grupo & historico.anio.le(fin_base)]
        consulta = historico.loc[grupo & historico.anio.eq(solicitud.anio), CLAVES]
        p = float(modelo.predict_proba(consulta)[0, 1])
        nivel = str(clasificar(np.array([p]), self.costos)[0])
        pron = dict(fuente="climatologia", probabilidad=round(p, 4), nivel=nivel, p10=None, p90=None,
                    escenarios=0, anios_analogos=[])
        if local.empty:
            base = f"La referencia de siembra emplea la frecuencia histórica de {modalidad.lower()}."
        else:
            base = (f"Hasta {fin_base}, hubo pérdida en {int(local.perdida.sum())} de {len(local)} ciclos "
                    f"municipales de {modalidad.lower()}. La tasa se suavizó con la historia de esa modalidad.")
        texto = (f"{base} Se calibró con Platt en {fin_base + 1}–{fin_cal}. "
                 f"El riesgo calibrado en siembra es {p:.1%} y el aviso es {nivel}.")
        return pron, texto

    def prediccion(self, solicitud):
        if solicitud.ultima_etapa.value == "siembra":
            return self.referencia_siembra(solicitud)[0]
        return self.resumir(*self.escenarios(solicitud))

    def explicacion(self, solicitud, vista="resumen"):
        """Promediar atribuciones crudas sobre exactamente los mismos escenarios que la predicción."""
        if solicitud.ultima_etapa.value == "siembra":
            pron, texto = self.referencia_siembra(solicitud)
            return dict(prediccion=pron, escala="probabilidad climatológica calibrada con Platt", base=pron["probabilidad"],
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
        senales = []
        elegibles = aportes.reindex([*config.DIRECCIONES_RF07, "modalidad"]) if vista == "productor" else aportes
        cantidad = len(elegibles) if vista == "tecnica" else config.N_TEXTO
        for var in elegibles.abs().nlargest(cantidad).index:
            valor = float(aportes[var])
            observado = (str(matriz[var].iloc[0]) if var in config.CATEGORICAS_MODELO
                         else f"{matriz[var].mean():.1f}")
            factores.append(dict(variable=etiqueta(var), valor=observado,
                                 direccion="eleva" if valor > 0 else "reduce" if valor < 0 else "neutra",
                                 aporte=valor))
            senales.append(f"{etiqueta(var)} = {observado} ({factores[-1]['direccion']})")
        texto = (f"El riesgo estimado es {pronostico['probabilidad']:.1%} y el aviso es {pronostico['nivel']}. "
                 f"Los mayores aportes respecto de la base del modelo fueron {', '.join(senales)}.")
        if anios:
            texto += " Los valores y aportes resumen los escenarios históricos."
        return dict(prediccion=pronostico, escala=escala, base=float(base),
                    salida_media=float(base+aportes.sum()), factores=factores, texto=texto)
