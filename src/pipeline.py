"""Reconstruye y verifica las capas derivadas del piloto."""
import logging

import pandas as pd

from src import config
from src.etl import clima, economia, municipios, siap, sociedad
from src.etl.calidad import Auditoria
from src.etl.esquemas import ESQUEMAS
from src.features import oro
from src.registro import configurar_registro

log = logging.getLogger(__name__)


def main():
    """Ejecuta las fuentes en orden y publica el reporte tras validar los seis productos."""
    auditoria = Auditoria()
    for etapa in (siap, municipios, clima, economia, sociedad, oro):
        etapa.main(auditoria)
    tablas = {}
    for nombre, esquema in ESQUEMAS.items():
        capa = config.ORO if nombre == "dataset_maestro" else config.PLATA
        tabla = pd.read_parquet(capa / f"{nombre}.parquet")
        esquema.validate(tabla)
        tablas[nombre] = tabla
        log.info("%s: esquema válido; %d filas.", nombre, len(tabla))
    auditoria.publicar(tablas)


if __name__ == "__main__":
    configurar_registro()
    main()
