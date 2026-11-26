"""Promedios anuales del INPC general mensual, serie 865541 de INEGI."""
import json
import logging

import pandas as pd

from src import config
from src.etl.archivos import descargar, guardar_parquet
from src.registro import configurar_registro

log = logging.getLogger(__name__)
URL = "https://www.inegi.org.mx/app/indicesdeprecios/servicios/CalculadoraAjaxInteraccion.asmx/DatosIniciales"
MESES = "ene feb mar abr may jun jul ago sep oct nov dic".split()


def main():
    consulta = json.dumps({"idSerie": "865541", "esquema": "INP"}).encode()
    ruta = descargar(URL, config.BRONCE / "inegi" / "inpc_865541_mensual.json",
                     lambda b: json.loads(b)["d"], cuerpo_json=consulta)
    filas = []
    for entrada in json.loads(ruta.read_bytes())["d"]:
        periodo, indice = entrada.split("&")
        mes, anio = periodo.lower().split("-")
        if int(anio) in config.ANIOS:
            filas.append((int(anio), MESES.index(mes) + 1, float(indice)))
    meses = pd.DataFrame(filas, columns=["anio", "mes", "inpc"])
    calendario = pd.MultiIndex.from_product([config.ANIOS, range(1, 13)], names=["anio", "mes"])
    if not meses.set_index(["anio", "mes"]).sort_index().index.equals(calendario) or not meses.inpc.gt(0).all():
        raise ValueError("Serie mensual INPC incompleta, duplicada o con índices inválidos")
    anual = meses.groupby("anio", as_index=False).agg(inpc=("inpc", "mean"))
    base = anual.loc[anual.anio.eq(config.ANIO_BASE_PRECIOS), "inpc"].item()
    anual["factor_pesos_constantes"] = base / anual.inpc
    guardar_parquet(anual, config.PLATA / "inpc.parquet")
    log.info("INPC: %d meses; %d medias anuales; año base %d.", len(meses), len(anual), config.ANIO_BASE_PRECIOS)


if __name__ == "__main__":
    configurar_registro()
    main()
