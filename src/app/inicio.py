"""Aplicación local para productores y personal técnico."""
from html import escape

import streamlit as st

from src import config
from src.app.cliente import SinServicio, aviso_copia, copia, pedir
from src.app.pages import tecnico

st.set_page_config(page_title="Maíz | Riesgo municipal", page_icon="🌽", layout="wide", initial_sidebar_state="collapsed")


def productor(entrada, locales):
    try:
        if locales:
            raise SinServicio
        f = pedir("/ficha", entrada)
        pdf = pedir("/boletin/" + entrada["cvegeo"], pdf=True)
    except SinServicio:
        datos = locales or copia()
        if not locales:
            aviso_copia(datos)
        f = next((f for f in datos["fichas"] if all(f[k] == v for k,v in entrada.items())), None)
        if not f:
            st.info("Esta consulta no está en la copia local.")
            return
        ruta = config.BOLETINES / (entrada["cvegeo"] + ".pdf")
        pdf = ruta.read_bytes() if ruta.exists() else None
    signo, nombre, color = config.NIVELES[f["prediccion"]["nivel"]]
    a,b = st.columns([1.15,1], gap="large")
    with a:
        st.html(f"""<div class="tarjeta" style="border-left-color:{color}">
          <span class="meta">{escape(f['municipio'])} · {escape(f['modalidad'])}</span>
          <h2 style="color:{color}">{signo} Riesgo {nombre.lower()}</h2>
          <p class="frecuencia">{escape(f['frecuencia'])}</p>
          <p>temporadas parecidas podrían perder más del 10 % de la superficie sembrada.</p>
          <small>Datos al {escape(f['fecha_datos'])}  ·  {escape(f['aviso'])}</small></div>""")
        if pdf:
            st.download_button("Descargar boletín municipal · PDF", pdf,
                               file_name=f"boletin-{entrada['cvegeo']}-{entrada['anio']}.pdf", mime="application/pdf")
            st.caption("Para imprimir · Etapa de llenado · Modalidades disponibles del municipio.")
    with b:
        st.subheader("Qué hacer en la parcela")
        st.write(f["recomendacion"])
        st.caption("Orientación propia basada en " + f["fuente_recomendacion"])
        st.markdown("**" + f["origen"] + "**")
        for factor in f["factores"]:
            st.markdown("• " + factor)
        if f["prediccion"]["anios_analogos"]:
            st.caption("Las etapas pendientes se estiman con temporadas históricas. Los aportes resumen esos escenarios.")


def aplicacion():
    st.html("""<style>.stMainBlockContainer{max-width:1120px;padding-top:2rem}
    h1,h2,h3{letter-spacing:-.025em}.meta{font-weight:650;letter-spacing:.03em}
    .tarjeta{background:#eaf0e6;border-left:6px solid;border-radius:7px;padding:20px 24px;margin-bottom:12px}
    .tarjeta h2{font-size:2.3rem;margin:8px 0}.tarjeta p{margin:0 0 10px}.tarjeta .frecuencia{font-size:1.65rem;font-weight:680}
    .tarjeta small{color:#344b40}</style>""")
    st.title("Riesgo de pérdida de maíz")
    st.caption(f"Primavera–verano · Ciclo {config.CICLO_DEMO} · Reconstrucción retrospectiva")
    modo = st.radio("Modo de consulta", ["Productor", "Técnico"], horizontal=True)
    locales = None
    try:
        catalogo = pedir("/municipios")
    except SinServicio:
        locales = copia()
        aviso_copia(locales)
        catalogo = locales["catalogo"]
    c1,c2,c3,c4 = st.columns([1,1.65,1,1.2])
    estado = c1.selectbox("Estado", list(config.ESTADOS_NOMBRE), index=1, format_func=config.ESTADOS_NOMBRE.get)
    municipios = {m["cvegeo"]:m for m in sorted(catalogo,key=lambda m:m["municipio"]) if m["cvegeo"].startswith(estado)}
    clave = c2.selectbox("Municipio", list(municipios), format_func=lambda k: municipios[k]["municipio"])
    modalidades = municipios[clave]["modalidades"]
    modalidad = c3.selectbox("Modalidad", modalidades, index=modalidades.index("Temporal") if "Temporal" in modalidades else 0)
    etapa = c4.selectbox("Etapa observada", list(config.ETAPAS), index=3,
                         format_func=lambda v:config.NOMBRES_ETAPA[v].capitalize())
    entrada = dict(cvegeo=clave,modalidad=modalidad,anio=config.CICLO_DEMO,ultima_etapa=etapa)
    if modo == "Productor":
        productor(entrada, locales)
    elif locales:
        st.info("El historial, las explicaciones técnicas y el simulador requieren el servicio local. Las fichas y los boletines están disponibles en el modo Productor.")
    else:
        try:
            tecnico.mostrar(entrada, modalidades)
        except SinServicio:
            st.warning("Se interrumpió el servicio local. Vuelve a consultar o abre la ficha guardada en el modo Productor.")


st.navigation([st.Page(aplicacion, title="Consulta municipal")], position="hidden").run()
