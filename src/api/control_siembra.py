"""Compara por etapa los dos modelos y la política de la API en idénticas observaciones."""
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from src import config
from src.api.esquemas import Solicitud
from src.api.servicio import Servicio
from src.models.busqueda import CLAVES
from src.models.evaluacion import puntuaciones


def main():
    servicio = Servicio()
    prueba = servicio.historia.loc[servicio.historia.anio.isin(config.ANIOS_MODELO["prueba"])]
    original = joblib.load(config.ARTEFACTOS / "completa_boosting_platt.joblib")
    referencia = servicio.referencia.predict_proba(prueba[CLAVES])[:, 1]
    filas = []
    for etapa in config.ETAPAS:
        matrices = []
        for caso in prueba.itertuples(index=False):
            solicitud = Solicitud(cvegeo=caso.cvegeo, modalidad=caso.modalidad,
                                  anio=caso.anio, ultima_etapa=etapa)
            matriz, _ = servicio.escenarios(solicitud)
            matrices.append(matriz)
        cortes = np.cumsum([len(m) for m in matrices])[:-1]
        x = pd.concat(matrices, ignore_index=True)
        tabla = prueba[["cvegeo","modalidad","anio","perdida"]].copy()
        tabla["etapa"] = etapa
        tabla["climatologia"] = referencia
        for version, modelo in [("original",original), ("restringido",servicio.calibrado)]:
            p = modelo.predict_proba(x)[:, 1]
            tabla[version] = [v.mean() for v in np.split(p, cortes)]
        fuente = "climatologia" if etapa == "siembra" else "restringido"
        # La evaluación compara los puntajes sin redondear. El contrato redondea al devolverlos.
        tabla["api"] = tabla[fuente]
        tabla["api_publicada"] = tabla["api"].round(4)
        filas.append(tabla)
    datos = pd.concat(filas,ignore_index=True)
    datos.to_csv(config.REPORTES / "prediccion_por_etapa.csv", index=False)
    resumen = []
    for etapa, t in datos.groupby("etapa",sort=False):
        for grupo, g in [("Todos",t), *t.groupby("modalidad")]:
            for version in ["original","restringido","climatologia","api","api_publicada"]:
                bs,bss,ap,roc = puntuaciones(g.perdida.to_numpy(),g[version].to_numpy(),g.climatologia.to_numpy())
                resumen.append(dict(etapa=etapa,grupo=grupo,version=version,filas=len(g),perdidas=g.perdida.sum(),
                                    brier=bs,bss=bss,pr_auc=ap,roc_auc=roc))
    pd.DataFrame(resumen).to_csv(config.REPORTES / "metricas_por_etapa.csv", index=False)


if __name__ == "__main__":
    with threadpool_limits(1):
        main()
