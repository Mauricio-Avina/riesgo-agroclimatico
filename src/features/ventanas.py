"""Indicadores por etapa. La fecha de siembra y los límites se pueden mover."""
import pandas as pd

from src import config


def fechas_por_etapa(fecha_siembra, etapas=None):
    origen = pd.Timestamp(fecha_siembra)
    if etapas is None:
        etapas = config.ETAPAS
    return {etapa: (origen + pd.Timedelta(days=inicio), origen + pd.Timedelta(days=fin))
            for etapa, (inicio, fin) in etapas.items()}


def calcular_ventanas(serie, anio, fechas):
    """Serie de un municipio indexada por fecha; intervalos diarios inclusivos.

    Cada indicador requiere sus propios insumos completos, incluso en años bisiestos.
    Se permiten etapas que terminen en el año siguiente.
    """
    if not fechas or min(pd.Timestamp(inicio) for inicio, _ in fechas.values()).year != anio:
        raise ValueError("El inicio del ciclo debe pertenecer al año agrícola indicado")
    if not serie.index.is_unique:
        raise ValueError("La serie diaria tiene fechas duplicadas")
    indicadores = {}
    for etapa, (inicio, fin) in fechas.items():
        dias = pd.date_range(inicio, fin)
        if dias.empty:
            raise ValueError(f"Ventana invertida: {etapa}")
        tramo = serie.reindex(dias)
        lluvia = tramo.lluvia
        indicadores[f"lluvia_{etapa}_mm"] = lluvia.sum(min_count=len(dias))
        secos = lluvia.lt(1)
        indicadores[f"racha_seca_{etapa}_dias"] = (
            int(secos.groupby((~secos).cumsum()).sum().max()) if lluvia.notna().all() else float("nan"))
        gdd = (tramo.tmax.clip(10, 30) + tramo.tmin.clip(10, 30)) / 2 - 10
        indicadores[f"gdd_{etapa}"] = gdd.sum(min_count=len(dias))
        indicadores[f"radiacion_{etapa}_mj_m2_dia"] = tramo.radiacion.mean(skipna=False)
        if etapa == "floracion":
            indicadores["calor_floracion_dias"] = (
                int(tramo.tmax.gt(30).sum()) if tramo.tmax.notna().all() else float("nan"))
        if etapa == "llenado":
            indicadores["helada_llenado_dias"] = (
                int(tramo.tmin.lt(0).sum()) if tramo.tmin.notna().all() else float("nan"))
    return indicadores
