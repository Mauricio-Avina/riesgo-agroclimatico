"""Comprobar la última versión registrada de cada archivo restaurado, sin modificar bronce."""
import csv
from hashlib import file_digest

from src import config


def main():
    with config.MANIFIESTO.open(encoding="utf-8-sig", newline="") as entrada:
        versiones = {r["archivo"]: r["sha256"] for r in csv.DictReader(entrada)}
    if not versiones:
        raise SystemExit("El manifiesto no contiene archivos.")
    diferencias = []
    for nombre, esperado in versiones.items():
        archivo = config.BRONCE / nombre
        if not archivo.is_file():
            diferencias.append(f"Falta {nombre}")
            continue
        with archivo.open("rb") as datos:
            if file_digest(datos, "sha256").hexdigest() != esperado:
                diferencias.append(f"Huella distinta en {nombre}")
    if diferencias:
        raise SystemExit("\n".join(diferencias))
    print(f"Coinciden las {len(versiones)} huellas de bronce.")


if __name__ == "__main__":
    main()
