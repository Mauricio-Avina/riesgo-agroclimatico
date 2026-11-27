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
MUNICIPIOS_ESPERADOS = 64  # Cobertura conjunta de D-004.
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

PESO_PREVIA = 2
COMBINACIONES = 20
ARBOLES = 90
ITER_LOGISTICA = 800
ITER_RED = 250
PROCESOS = 3
ORDEN_DESEMPATE = ("climatologia", "logistica", "bosque", "boosting", "red")
ESPACIOS_BUSQUEDA = {
    "logistica": {"C": [10 ** (i / 4) for i in range(-12, 12)]},
    "bosque": {"max_depth": [3, 5, 8, None], "min_samples_leaf": [2, 5, 10, 20],
               "max_features": ["sqrt", 0.5, 0.8]},
    "boosting": {"learning_rate": [0.025, 0.05, 0.1], "max_leaf_nodes": [5, 9, 15, 25],
                 "min_samples_leaf": [10, 20, 40], "l2_regularization": [0.1, 1, 5]},
    "red": {"alpha": [0.0001, 0.001, 0.01, 0.1], "learning_rate_init": [0.001, 0.003, 0.01],
            "hidden_layer_sizes": [(12,), (24,), (16, 8), (32, 12)]},
}

METRICAS = ("brier", "bss", "pr_auc", "roc_auc")
CUANTILES_IC = (0.025, 0.975)
GRUPOS_CONFIABILIDAD = 5
DPI_MODELOS = 300
MIN_EVENTOS_EQUIDAD = 20
BRECHA_SENSIBILIDAD = 0.10
ANIO_COSTO_AUXILIO = 2024
COSTO_AUXILIO = 600  # MXN/ha, INIFAP, 29-04-2024, Sinaloa.
FUENTE_COSTO = "https://www.gob.mx/inifap/articulos/recomendaciones-para-el-manejo-del-riego-normal-y-deficitario-de-maiz"
# Sifuentes Ibarra et al., Tecnologías de riego bajo condiciones de escasez de agua en maíz,
# cuadro 5, p. 15. Rendimientos experimentales por calendario, no eficacia municipal.
FUENTE_RESPUESTA = "https://www.fps.org.mx/portal/index.php/component/phocadownload/category/30-granos-y-flores?download=66:tecnologias-de-riego-bajo-condiciones-de-escasez-de-agua-en-maiz"
BASE_AUXILIOS = 2
T_HA_AUXILIO = {2: 6.79, 3: 9.73, 5: 10.62}
ACCIONES_RIEGO = {"amarillo": (2, 3), "rojo": (3, 5)}

GRUPOS_EQUIDAD = ("modalidad", "estado", "grado_marginacion_2020")
TOLERANCIA_SHAP = 1e-5
N_GLOBAL, N_LOCAL, N_TEXTO = 10, 7, 3
ANIO_CASO = 2023
NOMBRES_VARIABLES = {"lluvia_": "Lluvia", "racha_seca_": "Racha seca", "gdd_": "Grados día",
                     "radiacion_": "Radiación", "calor_": "Días de calor", "helada_": "Días de helada",
                     "sembrada_ha": "Superficie sembrada (ha)", "marginacion_2020": "Índice de marginación",
                     "modalidad_": "Modalidad", "estado_": "Estado", "latitud": "Latitud",
                     "longitud": "Longitud", "area_km2": "Área municipal (km²)", "altitud_celda_m": "Altitud (m)"}

NOMBRES_ETAPA = {"siembra": "siembra", "vegetativo": "crecimiento vegetativo",
                 "floracion": "floración", "llenado": "llenado"}
UNIDADES_CLIMA = {"mm": "mm", "dias": "días", "mj_m2_dia": "MJ/m²/día"}

PREFIJO_API = "/v1"
CUANTILES_ANALOGOS = (0.10, 0.90)
EJEMPLO_API = {"cvegeo": "11032", "modalidad": "Temporal", "anio": 2023,
               "ultima_etapa": "llenado"}
