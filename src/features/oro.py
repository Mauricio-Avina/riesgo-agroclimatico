"""Integra cinco tablas de plata a la granularidad observada en SIAP."""
import logging

import pandas as pd

from src import config
from src.etl.archivos import guardar_parquet
from src.etl.siap import CLAVE
from src.features.ventanas import calcular_ventanas, fechas_por_etapa
from src.registro import configurar_registro

log = logging.getLogger(__name__)


def unir(tabla, dimension, llaves, nombre):
    resultado = tabla.merge(dimension, on=llaves, how="left", validate="many_to_one", indicator=True)
    faltan = resultado["_merge"].eq("left_only")
    log.info("Cruce %s: %d filas antes, %d después; %d municipios sin correspondencia.",
             nombre, len(tabla), len(resultado), resultado.loc[faltan, "cvegeo"].nunique())
    if faltan.any() or len(resultado) != len(tabla):
        raise ValueError(f"Cobertura o multiplicidad inesperada en {nombre}")
    return resultado.drop(columns="_merge")


def main():
    oro = pd.read_parquet(config.PLATA / "siap_maiz_pv.parquet")
    clima = pd.read_parquet(config.PLATA / "clima_diario.parquet")
    registros = []
    for clave, diario in clima.groupby("cvegeo"):
        serie = diario.set_index("fecha").sort_index()
        for anio in config.ANIOS:
            siembra = pd.Timestamp(anio, *config.SIEMBRA_MES_DIA)
            indicadores = calcular_ventanas(serie, anio, fechas_por_etapa(siembra))
            registros.append(dict(cvegeo=clave, anio=anio, fecha_siembra_escenario=siembra, **indicadores))
    oro = unir(oro, pd.DataFrame(registros), ["cvegeo", "anio"], "clima por etapa")
    for nombre, llave in [("municipios", "cvegeo"), ("marginacion", "cvegeo"), ("inpc", "anio")]:
        oro = unir(oro, pd.read_parquet(config.PLATA / f"{nombre}.parquet"), [llave], nombre)
    for nominal in ["precio_pesos_t", "valor_produccion_pesos"]:
        oro[f"{nominal}_de_{config.ANIO_BASE_PRECIOS}"] = oro[nominal] * oro.factor_pesos_constantes
    if oro.duplicated(CLAVE).any():
        raise ValueError("El maestro tiene claves repetidas")
    guardar_parquet(oro.sort_values(CLAVE), config.ORO / "dataset_maestro.parquet")
    faltantes = oro.isna().sum().rename("nulos").to_frame()
    faltantes["filas"] = len(oro)
    faltantes["porcentaje_nulos"] = 100 * faltantes.nulos / len(oro)
    faltantes.rename_axis("columna").to_csv(config.REPORTES / "calidad_oro.csv", float_format="%.4f")
    log.info("Oro: %d filas, %d columnas, %d celdas nulas.", len(oro), len(oro.columns), faltantes.nulos.sum())


if __name__ == "__main__":
    configurar_registro()
    main()
