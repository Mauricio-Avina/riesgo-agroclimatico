"""Series diarias de NASA POWER en un punto interior por municipio."""
import json
import logging
import time
from urllib.parse import urlencode

import pandas as pd

from src import config
from src.etl.archivos import descargar, guardar_parquet
from src.etl import municipios
from src.registro import configurar_registro

log = logging.getLogger(__name__)
VARIABLES = {"T2M_MAX": "tmax", "T2M_MIN": "tmin", "PRECTOTCORR": "lluvia",
             "ALLSKY_SFC_SW_DWN": "radiacion", "RH2M": "humedad"}


def descargar_municipio(cvegeo, lat, lon):
    ruta = config.BRONCE / "power" / f"{cvegeo}.json"
    params = dict(parameters=",".join(VARIABLES), community="AG", latitude=round(lat, 6),
                  longitude=round(lon, 6), start=f"{config.ANIO_INICIAL}0101",
                  end=f"{config.ANIO_FINAL}1231", format="JSON")
    url = "https://power.larc.nasa.gov/api/temporal/daily/point?" + urlencode(params)
    if ruta.exists():
        lon_guardada, lat_guardada, *_ = json.loads(ruta.read_bytes())["geometry"]["coordinates"]
        if abs(lon_guardada - lon) > 0.001 or abs(lat_guardada - lat) > 0.001:
            raise ValueError(f"El punto de {cvegeo} difiere del usado en la descarga guardada")
    else:
        time.sleep(2)
    return descargar(url, ruta, lambda b: json.loads(b)["properties"]["parameter"])


def json_a_tabla(ruta):
    datos = json.loads(ruta.read_bytes())
    serie = pd.DataFrame(datos["properties"]["parameter"])[list(VARIABLES)].rename(columns=VARIABLES)
    serie.index = pd.to_datetime(serie.index, format="%Y%m%d")
    dias = pd.date_range(f"{config.ANIO_INICIAL}-01-01", f"{config.ANIO_FINAL}-12-31")
    if not serie.index.sort_values().equals(dias):
        raise ValueError(f"Calendario incompleto en {ruta.name}")
    serie = serie.sort_index().replace(-999, float("nan"))
    if (serie.tmax < serie.tmin).any() or (serie.lluvia < 0).any():
        raise ValueError(f"Temperaturas o lluvias imposibles en {ruta.name}")
    serie = serie.rename_axis("fecha").reset_index()
    serie.insert(0, "cvegeo", ruta.stem)
    return serie


def cotejar_lluvia(clima):
    """Compara la celda municipal con una estación del SMN en cada estado."""
    filas = []
    for estado, estacion, nombre, cvegeo in [("gto", "11001", "Abasolo", "11001"),
                                             ("qro", "22004", "El Batán", "22006")]:
        archivo = f"nor9120_{estacion}.txt"
        url = f"https://smn.conagua.gob.mx/tools/RESOURCES/Normales_Climatologicas/Normales9120/{estado}/{archivo}"
        ruta = descargar(url, config.BRONCE / "smn" / archivo)
        seccion = ruta.read_text(encoding="utf-8").split("\nPRECIPITACIÓN\n", 1)[1]
        normal = float(next(linea for linea in seccion.splitlines() if linea.startswith("NORMAL")).split()[-1])
        serie = clima.loc[clima.cvegeo.eq(cvegeo)].set_index("fecha").lluvia
        anuales = serie.groupby(serie.index.year).agg(["sum", "count", "size"])
        completos = anuales.loc[anuales["count"].eq(anuales["size"]), "sum"]
        for fin in [2020, config.ANIO_FINAL]:
            periodo = completos.loc[config.ANIO_INICIAL:fin]
            promedio = periodo.mean()
            filas.append(dict(cvegeo=cvegeo, estacion=estacion, nombre=nombre, inicio_power=config.ANIO_INICIAL,
                              fin_power=fin, anios_completos=len(periodo), power_mm=promedio,
                              smn_1991_2020_mm=normal, diferencia_mm=promedio - normal,
                              diferencia_pct=100 * (promedio / normal - 1)))
    pd.DataFrame(filas).to_csv(config.REPORTES / "cotejo_lluvia_smn.csv", index=False, float_format="%.2f")


def main():
    tabla = pd.read_parquet(config.PLATA / "municipios.parquet")
    partes = []
    for fila in tabla.itertuples(index=False):
        ruta = descargar_municipio(fila.cvegeo, fila.latitud, fila.longitud)
        partes.append(json_a_tabla(ruta))
    clima = pd.concat(partes, ignore_index=True)
    if clima.duplicated(["cvegeo", "fecha"]).any():
        raise ValueError("Clave municipio-día duplicada")
    guardar_parquet(clima, config.PLATA / "clima_diario.parquet")
    log.info("Clima: nulos por variable %s.", clima[list(VARIABLES.values())].isna().sum().to_dict())
    municipios.main()
    cotejar_lluvia(clima)
    log.info("Clima: %d días-municipio de %d series.", len(clima), len(tabla))


if __name__ == "__main__":
    configurar_registro()
    main()
