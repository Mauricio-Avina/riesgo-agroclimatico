"""Contratos de las cinco tablas de plata y del maestro, sin modificar los datos."""
import pandas as pd
import pandera.pandas as pa

from src import config

C = pa.Check
clave = pa.Column(str, [C.str_matches(r"^\d{5}$"),
                        C(lambda s: s.str[:2].isin(config.ESTADOS_MODELO), name="estado_del_piloto")])
anio = pa.Column(int, C.isin(list(config.ANIOS)))
modalidad = pa.Column(str, C.isin(config.MODALIDADES))
llave = ["cvegeo", "anio", "modalidad"]


def numero(regla=None, nullable=False):
    """Admite valores numéricos enteros o reales sin convertir la tabla."""
    reglas = [C(lambda s: pd.api.types.is_numeric_dtype(s), name="tipo_numerico")]
    if regla is not None:
        reglas.append(regla)
    return pa.Column(checks=reglas, nullable=nullable)


def columnas_fecha():
    """Permite las resoluciones datetime soportadas por pandas."""
    return pa.Column(checks=C(lambda s: pd.api.types.is_datetime64_any_dtype(s), name="fecha"))


agr = dict(cvegeo=clave, anio=anio, modalidad=modalidad)
for col in ["sembrada_ha", "cosechada_ha", "siniestrada_ha", "produccion_t",
            "rendimiento_t_ha", "precio_pesos_t", "valor_produccion_pesos"]:
    agr[col] = numero(C.ge(0), col in {"precio_pesos_t", "rendimiento_t_ha"})
agr["siniestralidad"] = numero(C.in_range(0, 1), True)
superficie = C(lambda d: d.cosechada_ha.le(d.sembrada_ha) & d.siniestrada_ha.le(d.sembrada_ha),
               name="superficies_no_superan_la_sembrada")
geo = dict(cvegeo=clave, municipio=pa.Column(str), latitud=numero(C.in_range(-90, 90)),
           longitud=numero(C.in_range(-180, 180)), area_km2=numero(C.gt(0)))
soc = dict(cvegeo=clave, marginacion_2020=numero(), grado_marginacion_2020=pa.Column(str))
eco = dict(anio=anio, inpc=numero(C.gt(0)), factor_pesos_constantes=numero(C.gt(0)))
altitud = numero(C.ne(-999))
diario = dict(altitud_celda_m=altitud, cvegeo=clave, fecha=columnas_fecha(), tmax=numero(C.ne(-999), True),
              tmin=numero(C.ne(-999), True), lluvia=numero(C.ge(0), True),
              radiacion=numero(C.ge(0), True), humedad=numero(C.in_range(0, 100), True))
inicio = pd.Timestamp(config.ANIO_INICIAL, 1, 1)
fin = pd.Timestamp(config.ANIO_FINAL, 12, 31)


def calendario_completo(d):
    """La unicidad municipio-fecha y estos límites aseguran un calendario sin huecos."""
    return (d.fecha.between(inicio, fin).all() and d.fecha.eq(d.fecha.dt.normalize()).all()
            and d.groupby("cvegeo").size().eq((fin - inicio).days + 1).all() and d.cvegeo.nunique() == config.MUNICIPIOS_ESPERADOS)


comunes = {**agr, **geo, **soc, **eco, "altitud_celda_m": altitud, "fecha_siembra_escenario": columnas_fecha()}
for etapa, (primero, ultimo) in config.ETAPAS.items():
    for col in [f"lluvia_{etapa}_mm", f"radiacion_{etapa}_mj_m2_dia", f"gdd_{etapa}"]:
        comunes[col] = numero(C.ge(0), True)
    comunes[f"racha_seca_{etapa}_dias"] = numero(C.in_range(0, ultimo - primero + 1), True)
for col, etapa in [("calor_floracion_dias", "floracion"), ("helada_llenado_dias", "llenado")]:
    primero, ultimo = config.ETAPAS[etapa]
    comunes[col] = numero(C.in_range(0, ultimo - primero + 1), True)
for col in ["precio_pesos_t", "valor_produccion_pesos"]:
    comunes[f"{col}_de_{config.ANIO_BASE_PRECIOS}"] = numero(C.ge(0), col == "precio_pesos_t")

municipales = C(lambda d: len(d) == config.MUNICIPIOS_ESPERADOS, name="municipios_esperados")
ESQUEMAS = {
    "siap_maiz_pv": pa.DataFrameSchema(agr, unique=llave, checks=superficie, strict=True),
    "municipios": pa.DataFrameSchema(geo, unique=["cvegeo"], checks=municipales, strict=True),
    "clima_diario": pa.DataFrameSchema(diario, unique=["cvegeo", "fecha"], strict=True,
        checks=[C(lambda d: d.tmax.ge(d.tmin) | d.tmax.isna() | d.tmin.isna(), name="maxima_al_menos_minima"),
                C(calendario_completo)]),
    "inpc": pa.DataFrameSchema(eco, unique=["anio"], checks=C(lambda d: len(d) == len(config.ANIOS)), strict=True),
    "marginacion": pa.DataFrameSchema(soc, unique=["cvegeo"], checks=municipales, strict=True),
    "dataset_maestro": pa.DataFrameSchema(comunes, unique=llave, strict=True,
        checks=[superficie, C(lambda d: d.isna().mean().lt(.05).all(), name="RF02_faltantes_por_columna")]),
}
