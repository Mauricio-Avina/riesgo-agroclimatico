"""Reproduce el contraste del pronóstico con solo siembra frente a la referencia de prueba."""
import joblib
import pandas as pd

from src import config
from src.api.esquemas import Solicitud
from src.api.servicio import Servicio
from src.models.busqueda import CLAVES


def main():
    servicio = Servicio()
    prueba = servicio.historia.loc[servicio.historia.anio.isin(config.ANIOS_MODELO["prueba"])]
    referencia = joblib.load(config.ARTEFACTOS / "referencia_preprueba.joblib")
    clima = referencia.predict_proba(prueba[CLAVES])[:, 1]
    filas = []
    for caso, historica in zip(prueba.itertuples(index=False), clima, strict=True):
        solicitud = Solicitud(cvegeo=caso.cvegeo, modalidad=caso.modalidad, anio=caso.anio,
                              ultima_etapa="siembra")
        pronostico = servicio.prediccion(solicitud)
        p = pronostico["probabilidad"]
        filas.append(dict(cvegeo=caso.cvegeo, modalidad=caso.modalidad, anio=caso.anio,
                          p_siembra=p, escenarios=pronostico["escenarios"], climatologia=historica,
                          diferencia_absoluta=abs(p - historica)))
    pd.DataFrame(filas).to_csv(config.REPORTES / "control_api_siembra.csv", index=False)


if __name__ == "__main__":
    main()
