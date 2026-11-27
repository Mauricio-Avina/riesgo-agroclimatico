from datetime import date

import altair as alt
import pandas as pd
import streamlit as st

from src import config
from src.app.cliente import pedir


def historial(entrada):
    respuesta = pedir("/historial/" + entrada["cvegeo"])
    tabla = pd.DataFrame(respuesta["filas"])
    tabla = tabla.loc[tabla.modalidad.eq(entrada["modalidad"])].copy()
    anios = st.select_slider("Intervalo de años", options=sorted(tabla.anio.unique()),
                            value=(tabla.anio.min(), tabla.anio.max()))
    tabla = tabla.loc[tabla.anio.between(*anios)]
    st.caption(f"{respuesta['fuente']} · {respuesta['fecha']} · Fracción siniestrada = superficie siniestrada / sembrada.")
    tabla = tabla.rename(columns={k:f"{k} ({v})" for k,v in respuesta["unidades"].items()})
    st.dataframe(tabla, hide_index=True, width="stretch")
    descarga = tabla.assign(fuente=respuesta["fuente"], corte=respuesta["fecha"]).to_csv(index=False)
    st.download_button("Descargar datos públicos · CSV", descarga.encode("utf-8-sig"), "historial-municipal.csv", "text/csv")


def explicacion(entrada):
    x = pedir("/explicacion/completa", entrada)
    st.metric("Probabilidad calibrada", f"{x['prediccion']['probabilidad']:.1%}")
    if x["factores"]:
        st.caption(f"Aportes en {x['escala']}. Base {x['base']:.3f}. Salida media {x['salida_media']:.3f}.")
        st.dataframe(pd.DataFrame(x["factores"]), hide_index=True, width="stretch")
    else:
        st.write(x["texto"])


def simulador(entrada, modalidades):
    st.caption("Compara la pérdida esperada por hectárea en las mismas tres temporadas históricas del municipio.")
    with st.form("alternativas"):
        columnas = st.columns(3)
        palancas = {}
        for idx, (campo, titulo, dia) in enumerate([("actual","A · Siembra actual",15),("alternativa_b","B · Alternativa",22),
                                                    ("alternativa_c","C · Alternativa",29)]):
            with columnas[idx]:
                st.markdown("**" + titulo + "**")
                mod = st.selectbox("Modalidad " + titulo[0], modalidades, index=modalidades.index(entrada["modalidad"]),key=campo+"m")
                anio = entrada["anio"]
                fecha = st.date_input("Siembra " + titulo[0],date(anio,6,dia),min_value=date(anio,6,1),max_value=date(anio,7,15),
                                      format="DD/MM/YYYY",key=campo+"f")
                palancas[campo] = {"modalidad":mod, "fecha":fecha.strftime("%m-%d")}
        ejecutar = st.form_submit_button("Comparar escenarios", type="primary")
    consulta = {"cvegeo":entrada["cvegeo"], **palancas}
    if ejecutar:
        st.session_state["sim_resultado"] = (consulta, pedir("/simulacion", consulta))
    guardado = st.session_state.get("sim_resultado")
    if not guardado or guardado[0] != consulta:
        return
    x = guardado[1]
    st.write(x["aviso"])
    filas = pd.DataFrame(x["resultados"])
    vista = filas.drop(columns="fuera_de_rango").copy()
    vista["nivel"] = vista.nivel.map(lambda v: config.NIVELES[v][1])
    vista.columns = ["Opción","Clima","Año","Modalidad","Siembra (mes-día)","Probabilidad","Nivel","Pérdida (MXN/ha)"]
    st.subheader("Pérdida esperada por hectárea")
    st.caption("Pesos de 2025 · Menor pérdida esperada indica la opción más favorable para ese clima.")
    st.bar_chart(vista,x="Clima",y="Pérdida (MXN/ha)",color="Opción",stack=False)
    st.dataframe(vista, hide_index=True, width="stretch")
    avisos = [dict(Opción=r["caso"],Clima=r["clima"],**a) for r in x["resultados"] for a in r["fuera_de_rango"]]
    if avisos:
        with st.expander(f"Extrapolación · {len(avisos)} valores fuera del intervalo de entrenamiento (P1–P99)"):
            st.dataframe(avisos,hide_index=True)
    st.subheader("Sensibilidad de la opción A")
    st.caption("Clima normal · Cambio en puntos porcentuales al pasar del percentil 10 al 90 de cada variable, manteniendo las demás fijas.")
    tornado = pd.DataFrame(x["tornado"]).sort_values("cambio_pp")
    grafico = alt.Chart(tornado).mark_bar(color="#326951").encode(
        y=alt.Y("variable:N", title=None, sort=alt.SortField("cambio_pp"), axis=alt.Axis(labelLimit=330)),
        x=alt.X("cambio_pp:Q", title="Cambio de probabilidad (puntos porcentuales)"),
        tooltip=[alt.Tooltip("variable:N", title="Variable"), alt.Tooltip("p10:Q", title="Prob. en P10",format=".2%"),
                 alt.Tooltip("p90:Q", title="Prob. en P90",format=".2%"), alt.Tooltip("cambio_pp:Q", title="Cambio (pp)")])
    st.altair_chart(grafico.properties(height=310), width="stretch")


def mostrar(entrada, modalidades):
    seccion = st.radio("Consulta técnica", ["Historial y descarga","Explicación","Simulador"],horizontal=True)
    st.subheader(seccion)
    if seccion == "Historial y descarga":
        historial(entrada)
    elif seccion == "Explicación":
        explicacion(entrada)
    else:
        simulador(entrada, modalidades)
