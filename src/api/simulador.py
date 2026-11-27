"""Contrastes pareados sobre tres temporadas históricas de un municipio."""
from functools import lru_cache

import numpy as np
import pandas as pd

from src import config
from src.api.servicio import SinDatos
from src.features.ventanas import calcular_ventanas, fechas_por_etapa
from src.models.evaluacion import clasificar
from src.models.explicacion import etiqueta
from src.models.objetivo import predictores


class Simulador:
    def __init__(self, servicio):
        self.servicio = servicio
        datos = servicio.datos
        self.historia = datos.loc[datos.anio.le(max(config.ANIOS_MODELO["validacion"]))]
        columnas = [v for v in (*config.FIJAS_MODELO, *config.CLIMA_MODELO) if v not in config.CATEGORICAS_MODELO]
        self.limites = datos.loc[datos.anio.isin(config.ANIOS_MODELO["entrenamiento"]), columnas].quantile(
            [0.01, 0.10, 0.90, 0.99])
        self.perdida_ha = {}
        for modalidad, filas in self.historia.groupby("modalidad"):
            valor = filas.valor_produccion_pesos_de_2025.sum() / filas.sembrada_ha.sum()
            severidad = filas.loc[filas.perdida.eq(1), "siniestralidad"].mean()
            self.perdida_ha[modalidad] = float(valor * severidad)

    @lru_cache(maxsize=8)
    def diario(self, clave):
        datos = pd.read_parquet(config.PLATA / "clima_diario.parquet", filters=[("cvegeo", "=", clave)])
        return datos.set_index("fecha").sort_index()

    def analogos(self, grupo):
        if grupo.empty:
            raise SinDatos("El municipio carece de historial para la modalidad actual.")
        lluvia = grupo.set_index("anio")[[f"lluvia_{e}_mm" for e in config.ETAPAS]].sum(axis=1).sort_index()
        return {nombre: int((lluvia - lluvia.quantile(q)).abs().idxmin()) for nombre, q in config.CLIMAS_SIM.items()}

    def matriz(self, clave, palanca, anio):
        h = self.historia
        base = h.loc[h.cvegeo.eq(clave) & h.modalidad.eq(palanca.modalidad.value) & h.anio.eq(anio)].copy()
        if base.empty:
            raise SinDatos(f"{palanca.modalidad.value} carece de registro en el municipio para {anio}.")
        fechas = fechas_por_etapa(f"{anio}-{palanca.fecha}")
        indicadores = calcular_ventanas(self.diario(clave), anio, fechas)
        if pd.isna(list(indicadores.values())).any():
            raise SinDatos("El clima diario está incompleto para la ventana solicitada.")
        for col, valor in indicadores.items():
            base[col] = valor
        return predictores(base, "completa")

    def fuera(self, fila):
        return [dict(variable=etiqueta(v), valor=float(fila[v]), p01=float(self.limites.at[.01,v]),
                     p99=float(self.limites.at[.99,v])) for v in self.limites
                if not self.limites.at[.01,v] <= fila[v] <= self.limites.at[.99,v]]

    def tornado(self, base):
        nombres = list(config.DIRECCIONES_RF07)
        filas = []
        for v in nombres:
            for q in (.10, .90):
                alternativa = base.copy()
                alternativa[v] = self.limites.at[q, v]
                filas.append(alternativa)
        probs = self.servicio.calibrado.predict_proba(pd.concat(filas))[:, 1].reshape(-1, 2)
        return sorted([dict(variable=etiqueta(v), p10=round(float(a),4), p90=round(float(b),4),
                            cambio_pp=round(float(b-a)*100,2)) for v,(a,b) in zip(nombres, probs)],
                      key=lambda r: -abs(r["cambio_pp"]))

    def consultar(self, entrada):
        clave = entrada.cvegeo
        grupo = self.historia.loc[self.historia.cvegeo.eq(clave)]
        anios = self.analogos(grupo.loc[grupo.modalidad.eq(entrada.actual.modalidad.value)])
        resultados, tornado = [], []
        for caso, palanca in zip("ABC", [entrada.actual, entrada.alternativa_b, entrada.alternativa_c]):
            modalidad = palanca.modalidad.value
            for clima, anio in anios.items():
                matriz = self.matriz(clave, palanca, anio)
                p = float(self.servicio.calibrado.predict_proba(matriz)[0,1])
                nivel = str(clasificar(np.array([p]), self.servicio.costos)[0])
                resultados.append(dict(caso=caso, clima=clima, anio=anio, modalidad=modalidad, fecha=palanca.fecha,
                                       probabilidad=round(p,4), nivel=nivel, perdida_esperada_ha=round(p*self.perdida_ha[modalidad],2),
                                       fuera_de_rango=self.fuera(matriz.iloc[0])))
                if caso == "A" and clima == "Normal":
                    tornado = self.tornado(matriz)
        return dict(resultados=resultados, tornado=tornado, aviso=config.AVISO_SIMULACION,
                    perdida_condicional_ha=self.perdida_ha, unidad="MXN de 2025 por hectárea")
