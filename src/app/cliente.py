"""El navegador consulta el servicio local. La copia guardada solo se usa al perder la API."""
import json
import requests
import streamlit as st

from src import config


class SinServicio(Exception):
    pass


def pedir(ruta, entrada=None, pdf=False):
    try:
        with requests.Session() as sesion:
            sesion.trust_env = False
            r = sesion.request("GET" if entrada is None else "POST", config.API_LOCAL + ruta, json=entrada, timeout=(1, 25))
    except (requests.ConnectionError, requests.Timeout) as exc:
        raise SinServicio from exc
    if r.status_code != 200:
        st.error(r.json().get("detalle", "La consulta no se pudo completar."))
        st.stop()
    return r.content if pdf else r.json()


@st.cache_data(show_spinner=False)
def leer_copia(modificada):
    return json.loads(config.FICHA_LOCAL.read_text(encoding="utf-8"))


def copia():
    if not config.FICHA_LOCAL.exists():
        st.error("Aún no hay una copia local. Ejecuta actualizar.bat en la computadora de la cooperativa.")
        st.stop()
    return leer_copia(config.FICHA_LOCAL.stat().st_mtime_ns)


def aviso_copia(datos):
    st.warning(f"Modo sin conexión: datos del {datos['generado']} · Ciclo {datos['ciclo']}.")
