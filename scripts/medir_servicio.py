"""Latencias extremo a extremo con una API local ya iniciada. Ejecutar desde la raíz."""
from statistics import mean
from time import perf_counter
import json

import requests

from src import config


def medir(sesion, ruta, entrada, cantidad):
    url = config.API_LOCAL + ruta
    sesion.post(url,json=entrada,timeout=30).raise_for_status()
    duraciones = []
    for _ in range(cantidad):
        inicio = perf_counter()
        respuesta = sesion.post(url,json=entrada,timeout=30)
        respuesta.raise_for_status()
        respuesta.json()
        duraciones.append((perf_counter() - inicio) * 1000)
    return dict(consultas=cantidad, media_ms=mean(duraciones), minimo_ms=min(duraciones), maximo_ms=max(duraciones))


def main():
    actual = {"modalidad":"Temporal", "fecha":"06-15"}
    consulta = dict(cvegeo="11032",actual=actual,alternativa_b=actual | {"fecha":"07-01"},
                    alternativa_c=actual | {"modalidad":"Riego"})
    with requests.Session() as sesion:
        sesion.trust_env=False
        return {"prediccion":medir(sesion,"/prediccion",config.EJEMPLO_API,100),
                "simulacion":medir(sesion,"/simulacion",consulta,10)}


if __name__ == "__main__":
    print(json.dumps(main(),indent=2))
