"""Cierres agrícolas municipales. Unidades del diccionario SIAP 2003–2025."""
import logging
import math
import re
import unicodedata

import pandas as pd

from src import config
from src.etl.archivos import descargar, guardar_parquet
from src.registro import configurar_registro

log = logging.getLogger(__name__)
BASE = "https://nube.agricultura.gob.mx/index.php?view="
MEDIDAS = {"sembrada": "sembrada_ha", "cosechada": "cosechada_ha", "siniestrada": "siniestrada_ha",
           "volumenproduccion": "produccion_t", "rendimiento": "rendimiento_t_ha",
           "preciomediorural": "precio_pesos_t", "valorproduccion": "valor_produccion_pesos"}
CLAVE = ["cvegeo", "anio", "modalidad"]


def normalizar(nombre):
    """Uniforma encabezados históricos de los cierres."""
    texto = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", texto.strip().lower()).strip("_")


def leer_anio(anio, auditoria=None):
    """Lee un cierre nacional y selecciona el alcance del piloto."""
    url = f"{BASE}10AE434F-A2158368-A120BC5A-EDF4AFAA&ANIO={anio}"
    ruta = descargar(url, config.BRONCE / "siap" / f"Cierre_agricola_mun_{anio}.csv")
    tabla = pd.read_csv(ruta, encoding="latin-1", dtype=str)
    tabla.columns = [normalizar(nombre) for nombre in tabla.columns]
    tabla = tabla.rename(columns={"precio": "preciomediorural", "nomcultivo_sin_um": "nomcultivo"})
    seleccion = (tabla.idestado.str.zfill(2).isin(config.ESTADOS_MODELO)
                 & tabla.idcultivo.eq(str(config.ID_CULTIVO)) & tabla.nomcicloproductivo.eq(config.CICLO)
                 & tabla.nommodalidad.isin(config.MODALIDADES))
    filas = tabla.loc[seleccion].copy()
    if auditoria is not None:
        entrada = tabla.rename(columns={**MEDIDAS, "nommodalidad": "modalidad"})
        entrada["cvegeo"] = entrada.idestado.str.zfill(2) + entrada.idmunicipio.str.zfill(3)
        auditoria.entrada("SIAP", entrada[CLAVE + list(MEDIDAS.values())])
    if filas.empty or not filas.anio.eq(str(anio)).all() or not filas.nomcultivo.eq(config.CULTIVO).all():
        raise ValueError(f"Revisar catálogo y cobertura del cierre {anio}")
    log.info("SIAP %d: %d filas leídas, %d después del filtro.", anio, len(tabla), len(filas))
    return filas


def main(auditoria=None):
    """Integra los cierres agrícolas del periodo delimitado."""
    descargar(BASE + "5D24F995-E734D711-1EA6F8D2-9D1387D7",
              config.BRONCE / "siap" / "Diccionario_agricola_2003_a_2025.xlsx")
    tabla = pd.concat([leer_anio(anio, auditoria) for anio in config.ANIOS], ignore_index=True)
    tabla["cvegeo"] = tabla.idestado.str.zfill(2) + tabla.idmunicipio.str.zfill(3)
    tabla = tabla.rename(columns={"nommodalidad": "modalidad", **MEDIDAS})[CLAVE + list(MEDIDAS.values())]
    tabla["anio"] = pd.to_numeric(tabla.anio)
    for columna in MEDIDAS.values():
        valores = tabla[columna].str.strip()
        agrupados = valores.str.contains(",", na=False)
        if not valores[agrupados].str.fullmatch(r"-?\d{1,3}(?:,\d{3})+(?:\.\d+)?").all():
            raise ValueError(f"Separador numérico no reconocido en {columna}")
        tabla[columna] = pd.to_numeric(valores.str.replace(",", "", regex=False))
    if tabla.duplicated(CLAVE).any() or not tabla.cvegeo.str.fullmatch(r"\d{5}").all():
        raise ValueError("Clave SIAP duplicada o inválida. Revisar los registros de origen.")
    superficies = tabla[["sembrada_ha", "cosechada_ha", "siniestrada_ha"]]
    if superficies.isna().any().any() or (superficies < 0).any().any() or (
            superficies[["cosechada_ha", "siniestrada_ha"]].gt(tabla.sembrada_ha, axis=0).any().any()):
        raise ValueError("Superficie ausente o fuera del intervalo permitido")
    tabla["siniestralidad"] = tabla.siniestrada_ha.div(tabla.sembrada_ha.where(tabla.sembrada_ha > 0))
    referencia = tabla.loc[tabla.cvegeo.str.startswith("22") & tabla.anio.eq(2025), "sembrada_ha"].sum()
    if not math.isclose(referencia, config.SEMBRADA_QRO_2025_HA, rel_tol=0, abs_tol=0.005):
        raise ValueError(f"El cruce con la delimitación de Querétaro difiere: {referencia} ha")
    guardar_parquet(tabla.sort_values(CLAVE), config.PLATA / "siap_maiz_pv.parquet")
    log.info("SIAP: %d filas únicas; %d con sembrada cero; Querétaro 2025 %.2f ha.",
             len(tabla), tabla.sembrada_ha.eq(0).sum(), referencia)


if __name__ == "__main__":
    configurar_registro()
    main()
