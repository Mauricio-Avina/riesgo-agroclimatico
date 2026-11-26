"""Índice y grado de marginación municipal de CONAPO, corte 2020."""
import logging

import pandas as pd

from src import config
from src.etl.archivos import descargar, guardar_parquet
from src.registro import configurar_registro

log = logging.getLogger(__name__)


def main():
    url = "https://raw.githubusercontent.com/IndiceMx/IM_2020/main/IMM_2020.xlsx"
    ruta = descargar(url, config.BRONCE / "conapo" / "IMM_2020.xlsx")
    tabla = pd.read_excel(ruta, sheet_name="IMM_2020", dtype={"CVE_MUN": str},
                          usecols=["CVE_MUN", "IM_2020", "GM_2020"])
    tabla = tabla.rename(columns={"CVE_MUN": "cvegeo", "IM_2020": "marginacion_2020",
                                  "GM_2020": "grado_marginacion_2020"})
    tabla["cvegeo"] = tabla.cvegeo.str.zfill(5)
    tabla = tabla.loc[tabla.cvegeo.str[:2].isin(config.ESTADOS_MODELO)].copy()
    tabla["marginacion_2020"] = pd.to_numeric(tabla.marginacion_2020)
    if len(tabla) != 64 or tabla.cvegeo.duplicated().any() or tabla.isna().any().any():
        raise ValueError("Revisar claves y cobertura de la marginación")
    guardar_parquet(tabla.sort_values("cvegeo"), config.PLATA / "marginacion.parquet")
    log.info("CONAPO: %d municipios con índice y grado de 2020.", len(tabla))


if __name__ == "__main__":
    configurar_registro()
    main()
