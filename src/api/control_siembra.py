"""Compara por etapa los dos modelos y la política de la API en idénticas observaciones."""
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from src import config
from src.api.esquemas import Solicitud
from src.api.servicio import Servicio
from src.models.busqueda import CLAVES
from src.models.evaluacion import clasificar, puntuaciones


def main():
    servicio = Servicio()
    prueba = servicio.historia.loc[servicio.historia.anio.isin(config.ANIOS_MODELO["prueba"])]
    original = joblib.load(config.ARTEFACTOS / "completa_boosting_platt.joblib")
    historica = joblib.load(config.ARTEFACTOS / "referencia_preprueba.joblib")
    referencia = historica.predict_proba(prueba[CLAVES])[:, 1]
    platt, _, _ = servicio.climas_siembra[servicio.inicio_prueba]
    climatologia_platt = platt.predict_proba(prueba[CLAVES])[:, 1]
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
        tabla["climatologia_platt"] = climatologia_platt
        for version, modelo in [("original",original), ("restringido",servicio.calibrado)]:
            p = modelo.predict_proba(x)[:, 1]
            tabla[version] = [v.mean() for v in np.split(p, cortes)]
        fuente = "climatologia_platt" if etapa == "siembra" else "restringido"
        # La evaluación compara los puntajes sin redondear. El contrato redondea al devolverlos.
        tabla["api"] = tabla[fuente]
        tabla["api_publicada"] = tabla["api"].round(4)
        filas.append(tabla)
    datos = pd.concat(filas,ignore_index=True)
    datos.to_csv(config.REPORTES / "prediccion_por_etapa.csv", index=False)
    claves = ["cvegeo", "modalidad", "anio"]
    siembra = datos.loc[datos.etapa.eq("siembra")].merge(
        datos.loc[datos.etapa.eq("llenado"), [*claves, "api"]].rename(columns={"api": "p_llenado"}),
        on=claves, validate="one_to_one", how="left")
    if siembra.p_llenado.isna().any():
        raise ValueError("Falta la predicción de llenado para una observación de siembra.")
    cierre = clasificar(siembra.p_llenado, servicio.costos)
    alertas = []
    for fuente in ["climatologia", "climatologia_platt"]:
        color = clasificar(siembra[fuente], servicio.costos)
        rojo = color == "rojo"
        aviso = color != "verde"
        alertas.append(dict(fuente=fuente, filas=len(siembra), perdidas=siembra.perdida.sum(),
                            prob_media=siembra[fuente].mean(), avisos=aviso.sum(),
                            aciertos_aviso=siembra.loc[aviso,"perdida"].sum(), rojos=rojo.sum(),
                            aciertos_rojos=siembra.loc[rojo,"perdida"].sum(),
                            rojo_a_amarillo=(rojo & (cierre == "amarillo")).sum(),
                            rojo_a_verde=(rojo & (cierre == "verde")).sum()))
    pd.DataFrame(alertas).to_csv(config.REPORTES / "alertas_siembra.csv", index=False)
    resumen = []
    for etapa, t in datos.groupby("etapa",sort=False):
        for grupo, g in [("Todos",t), *t.groupby("modalidad")]:
            for version in ["original","restringido","climatologia","climatologia_platt","api","api_publicada"]:
                bs,bss,ap,roc = puntuaciones(g.perdida.to_numpy(),g[version].to_numpy(),g.climatologia.to_numpy())
                resumen.append(dict(etapa=etapa,grupo=grupo,version=version,filas=len(g),perdidas=g.perdida.sum(),
                                    brier=bs,bss=bss,pr_auc=ap,roc_auc=roc))
    pd.DataFrame(resumen).to_csv(config.REPORTES / "metricas_por_etapa.csv", index=False)


if __name__ == "__main__":
    with threadpool_limits(1):
        main()
