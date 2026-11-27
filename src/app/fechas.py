"""Fechas para las pantallas y el boletín, independientes del idioma de Windows."""
from datetime import date

MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre")


def fecha_larga(iso):
    dia = date.fromisoformat(iso)
    return f"{dia.day} de {MESES[dia.month - 1]} de {dia.year}"
