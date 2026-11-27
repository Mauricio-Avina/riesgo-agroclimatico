"""Textos compartidos por consulta, copia local y boletín impreso."""
from datetime import date

from src import config
from src.features.ventanas import fechas_por_etapa


def frecuencia(p):
    if p == 0:
        return "0 de cada 100"
    if p < .01:
        return "Menos de 1 de cada 100"
    if p > .99 and p < 1:
        return "Más de 99 de cada 100"
    cien = int(p * 100 + .5)
    return f"{cien // 10} de cada 10" if cien % 10 == 0 else f"{cien} de cada 100"


def ficha(servicio, entrada):
    exp = servicio.explicacion(entrada, vista="productor")
    pron = exp["prediccion"]
    etapa, modalidad = entrada.ultima_etapa.value, entrada.modalidad.value
    fecha = date(entrada.anio, *config.SIEMBRA_MES_DIA)
    corte = fechas_por_etapa(fecha)[etapa][1].date().isoformat()
    if etapa == "siembra":
        _, fin_base, fin_cal = servicio.climas_siembra[min(entrada.anio,servicio.inicio_prueba)]
        h = servicio.historia
        local = h.loc[h.cvegeo.eq(entrada.cvegeo) & h.modalidad.eq(modalidad) & h.anio.le(fin_base)]
        factores = [f"Historia municipal hasta {fin_base}: {int(local.perdida.sum())} pérdidas en {len(local)} ciclos.",
                    f"La referencia incorpora la frecuencia histórica de {modalidad.lower()}.",
                    f"Ajuste de la probabilidad con los resultados de {fin_base+1} a {fin_cal}."]
        origen = "Referencia histórica calibrada"
    else:
        frases = {"eleva":"aumentó la estimación", "reduce":"redujo la estimación", "neutra":"sin cambio"}
        factores = []
        for factor in exp["factores"]:
            nombre = factor["variable"]
            if nombre == "Modalidad":
                nombre = f"Modalidad de {modalidad.lower()}"
            factores.append(f"{nombre} · {frases[factor['direccion']]}")
        origen = "Qué influyó frente al riesgo de referencia del modelo"
    return dict(**entrada.model_dump(mode="json"), municipio=servicio.municipios(entrada.cvegeo)[0]["municipio"],
                fecha_datos=corte, prediccion=pron, frecuencia=frecuencia(pron["probabilidad"]), factores=factores,
                origen=origen, recomendacion=config.RECOMENDACIONES[modalidad][pron["nivel"]],
                fuente_recomendacion=config.FUENTE_TEMPORAL if modalidad=="Temporal" else "INIFAP (2024), manejo del riego normal y deficitario de maíz.",
                fuente_url=None if modalidad=="Temporal" else config.FUENTE_COSTO, aviso=config.AVISO)
