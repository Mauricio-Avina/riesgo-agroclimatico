"""Comparación de aprendizaje supervisado con climatología históricamente disponible."""
import json
import logging

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from threadpoolctl import threadpool_limits

from src import config
from src.models.objetivo import pliegues, predictores

log = logging.getLogger(__name__)
CLAVES = ["cvegeo", "modalidad"]


class Climatologia(ClassifierMixin, BaseEstimator):
    """Frecuencia por celda retraída hacia la tasa de su modalidad."""
    def fit(self, X, y):
        historia = X[CLAVES].assign(evento=np.asarray(y))
        self.modalidad_ = historia.groupby("modalidad").evento.mean()
        self.global_ = historia.evento.mean()
        celdas = historia.groupby(CLAVES).evento.agg(["sum", "count"])
        previa = celdas.index.get_level_values("modalidad").map(self.modalidad_)
        self.tasas_ = (celdas["sum"] + config.PESO_PREVIA * previa) / (celdas["count"] + config.PESO_PREVIA)
        self.classes_ = np.unique(y)
        return self

    def predict_proba(self, X):
        p = self.tasas_.reindex(pd.MultiIndex.from_frame(X[CLAVES])).to_numpy()
        respaldo = X.modalidad.map(self.modalidad_).fillna(self.global_)
        p = np.where(np.isnan(p), respaldo, p)
        return np.column_stack([1 - p, p])


def entradas(datos, nombre, horizonte):
    """La clave municipal se usa exclusivamente para consultar la referencia."""
    return datos[CLAVES] if nombre == "climatologia" else predictores(datos, horizonte)


def protocolo(nombre, columnas):
    """El escalado y las categorías se aprenden dentro de cada pliegue."""
    modelos = {
        "logistica": LogisticRegression(class_weight="balanced", max_iter=config.ITER_LOGISTICA),
        "bosque": RandomForestClassifier(n_estimators=config.ARBOLES, class_weight="balanced_subsample",
                                          random_state=config.SEMILLA, n_jobs=1),
        "boosting": HistGradientBoostingClassifier(class_weight="balanced", early_stopping=False,
                                                   random_state=config.SEMILLA),
        "red": MLPClassifier(early_stopping=True, max_iter=config.ITER_RED, random_state=config.SEMILLA),
    }
    numericas = [c for c in columnas if c not in config.CATEGORICAS_MODELO]
    transformar = ColumnTransformer([
        ("num", StandardScaler() if nombre in ("logistica", "red") else "passthrough", numericas),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), list(config.CATEGORICAS_MODELO)),
    ], verbose_feature_names_out=False)
    return Pipeline([("preparar", transformar), ("modelo", modelos[nombre])])


def entrenar(datos, horizonte):
    """Buscar y guardar los mejores ajustes usando exclusivamente entrenamiento."""
    cortes = list(pliegues(datos))
    x = predictores(datos, horizonte)
    y = datos.perdida
    filas = []
    modelos = {}
    for nombre in ("climatologia", *config.ESPACIOS_BUSQUEDA):
        log.info("%s · %s", horizonte, nombre)
        if nombre == "climatologia":
            modelo = Pipeline([("modelo", Climatologia())])
            claves = datos[CLAVES]
            puntajes = []
            for antes, despues in cortes:
                modelo.fit(claves.iloc[antes], y.iloc[antes])
                p = modelo.predict_proba(claves.iloc[despues])[:, 1]
                puntajes.append(average_precision_score(y.iloc[despues], p))
            modelo.fit(claves, y)
            parametros = {}
        else:
            espacio = {"modelo__" + k: v for k, v in config.ESPACIOS_BUSQUEDA[nombre].items()}
            buscador = RandomizedSearchCV(protocolo(nombre, x.columns), espacio, cv=cortes,
                                          n_iter=config.COMBINACIONES, scoring="average_precision",
                                          random_state=config.SEMILLA, error_score="raise", n_jobs=config.PROCESOS)
            with joblib.parallel_config(backend="loky", inner_max_num_threads=1), threadpool_limits(1):
                buscador.fit(x, y)
            modelo = buscador.best_estimator_
            parametros = buscador.best_params_
            puntajes = [buscador.cv_results_[f"split{i}_test_score"][buscador.best_index_]
                        for i in range(len(cortes))]
        modelos[nombre] = modelo
        joblib.dump(modelo, config.ARTEFACTOS / f"{horizonte}_{nombre}.joblib")
        for (antes, despues), ap in zip(cortes, puntajes, strict=True):
            bloque = datos.iloc[despues]
            filas.append(dict(horizonte=horizonte, modelo=nombre, inicio=bloque.anio.min(),
                              fin=bloque.anio.max(), n_entrenamiento=len(antes), filas=len(bloque),
                              perdidas=bloque.perdida.sum(), azar=bloque.perdida.mean(), ap=ap,
                              media_ap=np.mean(puntajes), de_ap=np.std(puntajes),
                              parametros=json.dumps(parametros, sort_keys=True)))
    mejores = {r["modelo"]: r["media_ap"] for r in filas}
    ganador = max(config.ORDEN_DESEMPATE, key=mejores.get)
    return modelos, ganador, pd.DataFrame(filas).assign(seleccionado=lambda t: t.modelo.eq(ganador))
