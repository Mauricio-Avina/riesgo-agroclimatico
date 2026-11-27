"""Comparación retrospectiva D-027 con hiperparámetros y particiones de D-019 a D-023."""
import joblib
import numpy as np
import pandas as pd
import shap
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
from threadpoolctl import threadpool_limits

from src import config
from src.models.busqueda import CLAVES
from src.models.evaluacion import clasificar, confiabilidad, evaluar_corte, semaforo
from src.models.explicacion import equidad, explicar
from src.models.objetivo import cargar, grupos, predictores


def ajustar(partes, original):
    modelo = clone(original)
    modelo.named_steps["preparar"].set_output(transform="pandas")
    modelo.set_params(modelo__monotonic_cst=config.DIRECCIONES_RF07)
    train, val = partes["entrenamiento"], partes["validacion"]
    modelo.fit(predictores(train, "completa"), train.perdida)
    bloque = np.arange(len(val))
    calibrado = CalibratedClassifierCV(FrozenEstimator(modelo), method="sigmoid",
                                       cv=[(bloque, bloque)], ensemble=False)
    calibrado.fit(predictores(val, "completa"), val.perdida)
    joblib.dump(calibrado, config.ARTEFACTOS / "completa_boosting_monotono_platt.joblib")
    return modelo, calibrado


def direcciones(x, prueba, modelo, calibrado, version):
    """Separar asociación entre filas de la respuesta manteniendo el resto fijo."""
    mat = modelo.named_steps["preparar"].transform(x)
    variables = modelo.named_steps["preparar"].get_feature_names_out()
    exp = shap.TreeExplainer(modelo.named_steps["modelo"])(mat)
    aportes = pd.DataFrame(exp.values, columns=variables, index=x.index)
    caso = prueba.cvegeo.eq(config.EJEMPLO_API["cvegeo"]) & prueba.modalidad.eq("Temporal") & prueba.anio.eq(2023)
    for col, signo in config.DIRECCIONES_RF07.items():
        cortes = np.unique(np.quantile(x[col], np.linspace(0, 1, 11)))
        probabilidades = [calibrado.predict_proba(x.assign(**{col: v}))[:, 1] for v in cortes]
        delta = signo * np.diff(probabilidades, axis=0)
        yield dict(version=version, variable=col, signo_esperado=signo,
                   spearman_shap=x[col].corr(aportes[col], method="spearman"),
                   valor_caso=x.loc[caso, col].item(), shap_caso=aportes.loc[caso, col].item(),
                   comparaciones=delta.size, inversiones=int((delta < -1e-12).sum()))


def main():
    partes = grupos(cargar())
    t = partes["prueba"]
    x = predictores(t, "completa")
    ref = joblib.load(config.ARTEFACTOS / "referencia_preprueba.joblib").predict_proba(t[CLAVES])[:, 1]
    original = joblib.load(config.ARTEFACTOS / "completa_boosting.joblib")
    original_platt = joblib.load(config.ARTEFACTOS / "completa_boosting_platt.joblib")
    restringido, platt = ajustar(partes, original)
    costos = pd.read_csv(config.REPORTES / "costos_semaforo.csv")
    amarillo = costos.set_index("color").at["amarillo", "umbral"]
    equidad_grupos, signos, metricas, quintiles, alertas = [], [], [], [], []
    for version, arbol, cal in [("original", original, original_platt), ("restringido", restringido, platt)]:
        p = cal.predict_proba(x)[:, 1]
        tabla = t.assign(p=p, cruda=arbol.predict_proba(x)[:, 1], referencia=ref, color=clasificar(p, costos))
        for corte, grupo, sub in [("total","Todos",tabla), ("sensibilidad","Sin 2023",tabla.loc[tabla.anio.ne(2023)]),
                                  *(("modalidad",g,s) for g,s in tabla.groupby("modalidad"))]:
            metricas.append(evaluar_corte(sub,"completa",version,corte,grupo))
        equidad_grupos.append(equidad(tabla, amarillo, "completa", nivel="amarillo").assign(version=version))
        alertas.append(semaforo(tabla, costos, "completa").assign(version=version))
        signos.extend(direcciones(x,t,arbol,cal,version))
        for i, (_, g) in enumerate(tabla.groupby(pd.qcut(tabla.p, 5, duplicates="drop"), observed=True),1):
            quintiles.append(dict(version=version,quintil=i,n=len(g),pronostico=g.p.mean(),observado=g.perdida.mean()))
        if version == "restringido":
            confiabilidad(tabla,"completa",version,config.FIGURAS / "fig_revision_confiabilidad.png")
            ranking, caso = explicar(tabla, arbol, "boosting", "completa", "_restringido")
            ranking.to_csv(config.REPORTES / "importancia_shap_restringido.csv", index=False)
            pd.DataFrame([caso]).to_csv(config.REPORTES / "caso_shap_restringido.csv", index=False)
    # La auditoría principal incluye ambos horizontes. El rojo original conserva su archivo histórico.
    pron = pd.read_csv(config.REPORTES / "pronosticos_prueba.csv", dtype={"cvegeo": str})
    claves = ["cvegeo", "modalidad", "anio"]
    temprano = t.merge(pron.loc[pron.horizonte.eq("prefloracion"), [*claves, "p"]],
                       on=claves, how="left", validate="one_to_one")
    if temprano.p.isna().any():
        raise ValueError("Faltan predicciones de prefloración para auditar al amarillo.")
    audit_temprana = equidad(temprano, amarillo, "prefloracion", nivel="amarillo").assign(version="original")
    pd.concat([*equidad_grupos, audit_temprana]).to_csv(config.REPORTES / "equidad.csv", index=False)
    for nombre, resultado in [("revision_modelos", pd.DataFrame(metricas)), ("revision_direcciones", pd.DataFrame(signos)),
                              ("revision_equidad", pd.concat(equidad_grupos)), ("revision_quintiles", pd.DataFrame(quintiles)),
                              ("revision_alertas", pd.concat(alertas))]:
        resultado.to_csv(config.REPORTES / (nombre + ".csv"), index=False)


if __name__ == "__main__":
    with threadpool_limits(1):
        main()
