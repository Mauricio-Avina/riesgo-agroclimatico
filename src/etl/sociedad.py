"""Índice y grado de marginación municipal de CONAPO, corte 2020."""
import logging

import pandas as pd

from src import config
from src.etl.archivos import descargar, guardar_parquet
from src.registro import configurar_registro

log = logging.getLogger(__name__)


def leer_municipios(ruta, auditoria=None):
    """Extrae claves, índices y grados de la hoja municipal de CONAPO."""
    tabla = pd.read_excel(ruta, sheet_name="IMM_2020", dtype={"CVE_MUN": str},
                          usecols=["CVE_MUN", "IM_2020", "GM_2020"])
    tabla = tabla.rename(columns={"CVE_MUN": "cvegeo", "IM_2020": "marginacion_2020",
                                  "GM_2020": "grado_marginacion_2020"})
    if auditoria is not None:
        auditoria.entrada("CONAPO", tabla)
    tabla["cvegeo"] = tabla.cvegeo.str.zfill(5)
    tabla = tabla.loc[tabla.cvegeo.str[:2].isin(config.ESTADOS_MODELO)].copy()
    tabla["marginacion_2020"] = pd.to_numeric(tabla.marginacion_2020)
    if len(tabla) != 64 or tabla.cvegeo.duplicated().any() or tabla.isna().any().any():
        raise ValueError("Revisar claves y cobertura de la marginación")
    return tabla.sort_values("cvegeo").reset_index(drop=True)


def main(auditoria=None):
    """Selecciona el índice y el grado publicados por CONAPO."""
    url = "https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Municipio/IMM_2020.xlsx"
    ruta = descargar(url, config.BRONCE / "conapo" / "oficial" / "IMM_2020.xlsx")
    tabla = leer_municipios(ruta, auditoria)
    primera_copia = config.BRONCE / "conapo" / "IMM_2020.xlsx"
    if primera_copia.exists():
        pd.testing.assert_frame_equal(tabla, leer_municipios(primera_copia), check_exact=True)
        log.info("CONAPO: coincidieron los índices y grados de los %d municipios en ambas ediciones.", len(tabla))
    guardar_parquet(tabla.sort_values("cvegeo"), config.PLATA / "marginacion.parquet")
    log.info("CONAPO: %d municipios con índice y grado de 2020.", len(tabla))


if __name__ == "__main__":
    configurar_registro()
    main()
