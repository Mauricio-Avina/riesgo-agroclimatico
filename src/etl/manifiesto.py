"""Procedencia y versiones de los archivos descargados en la capa bronce."""

import argparse
import csv
import hashlib
import logging
import os
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import date
from pathlib import Path

from src import config
from src.registro import configurar_registro

log = logging.getLogger(__name__)
CAMPOS = ("archivo", "url", "fecha_descarga", "sha256")


@contextmanager
def _bloquear(manifiesto: Path) -> Iterator[None]:
    """Serializa la lectura y actualización del CSV entre procesos ETL."""
    with manifiesto.with_suffix(".lock").open("a+b") as bloqueo:
        if os.name == "nt":
            import msvcrt

            bloqueo.seek(0)
            msvcrt.locking(bloqueo.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(bloqueo, fcntl.LOCK_EX)
        yield  # Cerrar el archivo libera el bloqueo en ambos sistemas.


def registrar_descarga(ruta: Path | str, url: str) -> bool:
    """Registra una descarga de bronce. Devuelve True si agrega una versión."""
    ruta = Path(ruta).resolve()
    archivo = ruta.relative_to(config.BRONCE).as_posix()
    with ruta.open("rb") as datos:
        huella = hashlib.file_digest(datos, "sha256").hexdigest()

    manifiesto = config.MANIFIESTO
    with _bloquear(manifiesto):
        filas = []
        if manifiesto.exists() and manifiesto.stat().st_size:
            with manifiesto.open(encoding="utf-8-sig", newline="") as entrada:
                lector = csv.DictReader(entrada, strict=True)
                if lector.fieldnames != list(CAMPOS):
                    raise ValueError(f"Encabezado inesperado en {manifiesto.name}")
                filas = list(lector)

        versiones = [fila["sha256"] for fila in filas if fila["archivo"] == archivo]
        if huella in versiones:
            log.info(
                "%s ya registrado con SHA-256 %s. Se conservan %d filas.",
                archivo, huella, len(filas),
            )
            return False

        nueva = {
            "archivo": archivo,
            "url": url,
            "fecha_descarga": date.today().isoformat(),
            "sha256": huella,
        }
        # Publicar el CSV completo evita dejar una fila a medias si falla la escritura.
        descriptor, temporal = tempfile.mkstemp(dir=manifiesto.parent, suffix=".tmp")
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as salida:
                escritor = csv.DictWriter(salida, fieldnames=CAMPOS)
                escritor.writeheader()
                escritor.writerows(filas)
                escritor.writerow(nueva)
            os.replace(temporal, manifiesto)
        finally:
            Path(temporal).unlink(missing_ok=True)

        if versiones:
            log.info(
                "Nueva versión de %s. SHA-256 anterior %s, actual %s.",
                archivo, versiones[-1], huella,
            )
        log.info(
            "Manifiesto: %d filas leídas, %d después de registrar %s.",
            len(filas), len(filas) + 1, archivo,
        )
        return True


def main() -> None:
    """Registra un archivo ya descargado desde la línea de comandos."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ruta", type=Path, help="Ruta del archivo descargado en data/bronce")
    parser.add_argument("url", help="URL de origen de la descarga")
    args = parser.parse_args()
    registrar_descarga(args.ruta, args.url)


if __name__ == "__main__":
    configurar_registro()
    main()
