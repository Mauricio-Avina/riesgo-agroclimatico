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
SEMBRADA_QRO_2025_HA = 77805.45
ESTACIONES_SMN = (("gto", "11001", "Abasolo", "11001"), ("qro", "22004", "El Batán", "22006"))
UMBRAL_PERDIDA = 0.10
ID_CULTIVO = 7490000
ANIO_BASE_PRECIOS = 2025
SIEMBRA_MES_DIA = (6, 15)
# Días desde la siembra, extremos incluidos. Escenario regional de D-008.
ETAPAS = {"siembra": (0, 6), "vegetativo": (7, 59),
          "floracion": (60, 79), "llenado": (80, 114)}

# Módulo 3. Decisiones D-019 a D-024.
ARTEFACTOS = RAIZ / "artefactos"
ANIOS_MODELO = {"entrenamiento": range(2003, 2018), "validacion": range(2018, 2021),
                "prueba": range(2021, 2026)}
INICIOS_PLIEGUE = (2008, 2010, 2012, 2014, 2016)
ANIOS_POR_PLIEGUE = 2
HORIZONTES = {"completa": tuple(ETAPAS), "prefloracion": ("siembra", "vegetativo")}
CATEGORICAS_MODELO = ("modalidad", "estado")
FIJAS_MODELO = ("sembrada_ha", "latitud", "longitud", "area_km2", "altitud_celda_m",
                "marginacion_2020", *CATEGORICAS_MODELO)
CLIMA_MODELO = tuple(col for etapa in ETAPAS for col in
                     (f"lluvia_{etapa}_mm", f"racha_seca_{etapa}_dias", f"gdd_{etapa}",
                      f"radiacion_{etapa}_mj_m2_dia")) + ("calor_floracion_dias", "helada_llenado_dias")
EXCLUIDAS_MODELO = ("cosechada_ha", "siniestrada_ha", "produccion_t", "rendimiento_t_ha",
                    "precio_pesos_t", "valor_produccion_pesos", "siniestralidad", "perdida",
                    "precio_pesos_t_de_2025", "valor_produccion_pesos_de_2025", "cvegeo",
                    "municipio", "anio", "fecha_siembra_escenario", "inpc",
                    "factor_pesos_constantes", "grado_marginacion_2020")
