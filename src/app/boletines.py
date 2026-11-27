"""Boletín de una página por municipio, legible también en escala de grises."""
from fpdf import FPDF

from src import config


def escribir(ruta, fichas):
    pdf = FPDF(format="A4")
    pdf.set_margins(17, 15, 17)
    pdf.set_auto_page_break(True, 13)
    pdf.add_font("DejaVu", fname=str(config.FUENTES_TIPOGRAFICAS / "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", style="B", fname=str(config.FUENTES_TIPOGRAFICAS / "DejaVuSans-Bold.ttf"))
    pdf.add_page()

    def linea(texto, tam=10, alto=5.5, fuerte=False, color="#233c36"):
        pdf.set_font("DejaVu", "B" if fuerte else "", tam)
        pdf.set_text_color(color)
        pdf.multi_cell(0, alto, texto, new_x="LMARGIN", new_y="NEXT")

    f = fichas[0]
    pdf.set_title(f"Boletín de maíz · {f['municipio']}")
    linea("BOLETÍN MUNICIPAL   /   MAÍZ GRANO", 10, 7, True, "#306651")
    linea(f["municipio"], 23, 12, True)
    linea(f"{config.ESTADOS_NOMBRE[f['cvegeo'][:2]]}  ·  Ciclo {f['anio']}  ·  Reconstrucción retrospectiva")
    linea(f"Etapa de llenado   |   Datos al {f['fecha_datos']}")
    pdf.ln(3)
    for f in fichas:
        nivel = f["prediccion"]["nivel"]
        icono, palabra, color = config.NIVELES[nivel]
        linea(f"{f['modalidad']}    {icono}  Riesgo {palabra.lower()}", 15, 8, True, color)
        linea(f"{f['frecuencia']} temporadas similares podrían superar el 10 % de superficie sembrada siniestrada.", 11, 6)
        linea(f["origen"], 9, 5, True)
        for item in f["factores"]:
            linea("•  " + item, 9, 4.8)
        linea(f["recomendacion"], 10, 5.3, True)
        linea("Orientación propia basada en " + f["fuente_recomendacion"], 8, 4.2)
        pdf.ln(4)
    linea(config.AVISO + " La estimación corresponde al municipio y modalidad. Contrástala con las condiciones de tu parcela.", 9, 5)
    linea("Datos agrícolas del SIAP y clima de NASA POWER. Piloto de Guanajuato y Querétaro.", 8, 4.5)
    if pdf.page_no() != 1:
        raise ValueError("El boletín municipal excede una página.")
    pdf.output(str(ruta))
