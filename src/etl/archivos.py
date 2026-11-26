"""Descargas con procedencia y publicación atómica de tablas."""
import logging
import os
import tempfile
import time
from http.client import IncompleteRead
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.etl.manifiesto import registrar_descarga

log = logging.getLogger(__name__)


def descargar(url, ruta, validar=None, cuerpo_json=None):
    """Conserva la primera copia íntegra; un fallo de red no deja archivos parciales."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if not ruta.is_file():
        for intento in range(3):
            try:
                peticion = Request(url, data=cuerpo_json)
                if cuerpo_json is not None:
                    peticion.add_header("Content-Type", "application/json")
                with urlopen(peticion, timeout=120) as respuesta:
                    contenido = respuesta.read()
                if not contenido or contenido.lstrip().lower().startswith((b"<!doctype html", b"<html")):
                    raise ValueError(f"Respuesta inesperada para {ruta.name}")
                if validar:
                    validar(contenido)
                break
            except (URLError, TimeoutError, ConnectionError, IncompleteRead) as error:
                if intento == 2 or isinstance(error, HTTPError) and error.code < 500 and error.code != 429:
                    raise
                time.sleep(2 ** (intento + 1))
        with tempfile.NamedTemporaryFile(dir=ruta.parent, delete=False) as archivo:
            temporal = Path(archivo.name)
            try:
                archivo.write(contenido)
            except BaseException:
                archivo.close()
                temporal.unlink(missing_ok=True)
                raise
        try:
            temporal.replace(ruta)
        finally:
            temporal.unlink(missing_ok=True)
    registrar_descarga(ruta, url)
    return ruta


def guardar_parquet(tabla, ruta):
    """Sustituye el resultado solamente después de completar su escritura."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fd, temporal = tempfile.mkstemp(dir=ruta.parent, suffix=".parquet")
    os.close(fd)
    try:
        tabla.to_parquet(temporal, index=False)
        os.replace(temporal, ruta)
    finally:
        Path(temporal).unlink(missing_ok=True)
