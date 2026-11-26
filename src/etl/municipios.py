"""Puntos interiores y superficie municipal del Marco Geoestadístico del INEGI."""
import json
import logging

import geopandas as gpd
import pandas as pd

from src import config
from src.etl.archivos import descargar, guardar_parquet
from src.registro import configurar_registro

log = logging.getLogger(__name__)


def main():
    partes = []
    for estado in config.ESTADOS_MODELO:
        url = f"https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/{estado}"
        ruta = descargar(url, config.BRONCE / "inegi" / f"mgem_{estado}.geojson")
        geografia = gpd.read_file(ruta)
        if geografia.crs is None or not geografia.cvegeo.str.startswith(estado).all():
            raise ValueError(f"Cartografía sin referencia o con claves ajenas a {estado}")
        poligonos = geografia.to_crs(6933)
        puntos = poligonos.representative_point()
        if not puntos.within(poligonos.geometry).all():
            raise ValueError("Hay puntos fuera de sus municipios")
        puntos = puntos.to_crs(4326)
        partes.append(pd.DataFrame(dict(cvegeo=geografia.cvegeo, municipio=geografia.nomgeo,
                                        latitud=puntos.y, longitud=puntos.x,
                                        area_km2=poligonos.area / 1e6)))
    tabla = pd.concat(partes).sort_values("cvegeo").reset_index(drop=True)
    if tabla.cvegeo.duplicated().any() or len(tabla) != 64:
        raise ValueError("Se esperaban 64 municipios distintos")
    # La elevación es la de la celda POWER. Se incorpora después de la descarga.
    alturas = []
    for clave in tabla.cvegeo:
        ruta = config.BRONCE / "power" / f"{clave}.json"
        alturas.append(json.loads(ruta.read_bytes())["geometry"]["coordinates"][2] if ruta.exists() else None)
    tabla["altitud_celda_m"] = pd.array(alturas, dtype="Float64")
    guardar_parquet(tabla, config.PLATA / "municipios.parquet")
    log.info("Municipios: %d polígonos y %d puntos interiores.", len(tabla), len(tabla))


if __name__ == "__main__":
    configurar_registro()
    main()
