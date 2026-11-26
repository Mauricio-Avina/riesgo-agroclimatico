"""Rutas del proyecto y alcance del piloto de maíz (decisiones D-003 y D-004)."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data"
BRONCE = DATOS / "bronce"
PLATA = DATOS / "plata"
ORO = DATOS / "oro"
REPORTES = RAIZ / "reports"
FIGURAS = REPORTES / "figures"
MANIFIESTO = BRONCE / "manifiesto.csv"
REGISTRO_ETL = REPORTES / "etl.log"

ESTADO_PILOTO = "22"  # Querétaro (D-003)
ESTADOS_MODELO = ("11", ESTADO_PILOTO)  # Guanajuato y Querétaro (D-004)
ANIO_INICIAL = 2003
ANIO_FINAL = 2025
ANIOS = range(ANIO_INICIAL, ANIO_FINAL + 1)
CULTIVO = "Maíz grano"
CICLO = "Primavera-Verano"
MODALIDADES = ("Riego", "Temporal")
SEMILLA = 42
ID_CULTIVO = 7490000
ANIO_BASE_PRECIOS = 2025
SIEMBRA_MES_DIA = (6, 15)
# Días desde la siembra, extremos incluidos. Escenario regional de D-008.
ETAPAS = {"siembra": (0, 6), "vegetativo": (7, 59),
          "floracion": (60, 79), "llenado": (80, 114)}
