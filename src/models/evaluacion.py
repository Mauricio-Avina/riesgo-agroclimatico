"""Calibración temporal y verificación pareada frente a la climatología actualizada."""
from itertools import product

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.frozen import FrozenEstimator
from sklearn.metrics import average_precision_score, roc_auc_score

from src import config
from src.models.busqueda import CLAVES, Climatologia, entradas


def umbrales(historia, deflactor):
    """Costo incremental y beneficio marginal entre calendarios de auxilio publicados."""
    valor = historia.valor_produccion_pesos_de_2025.sum() / historia.sembrada_ha.sum()
    filas = []
    for color, (inicial, final) in config.ACCIONES_RIEGO.items():
        costo = (final - inicial) * config.COSTO_AUXILIO * deflactor
        fraccion = (config.T_HA_AUXILIO[final] - config.T_HA_AUXILIO[inicial]) / config.T_HA_AUXILIO[config.BASE_AUXILIOS]
        perdida_evitable = valor * fraccion
        filas.append(dict(color=color, auxilios_inicial=inicial, auxilios_final=final,
                          costo_ha_2025=costo, valor_ha_2025=valor, fraccion_protegida=fraccion,
                          perdida_evitable_ha_2025=perdida_evitable, umbral=costo/perdida_evitable))
    return pd.DataFrame(filas)


def puntuaciones(y, p, ref):
    """Brier y habilidad, precisión promedio y área ROC para una misma muestra."""
    bs = np.mean((y - p) ** 2)
    bs_ref = np.mean((y - ref) ** 2)
    dos_clases = np.unique(y).size == 2
    return np.array([bs, 1 - bs / bs_ref if bs_ref else np.nan,
                     average_precision_score(y, p) if y.any() else np.nan,
                     roc_auc_score(y, p) if dos_clases else np.nan])


def intervalos(y, p, ref, anios):
    """Bootstrap exacto de cinco años: comprimir remuestras con igual multiplicidad."""
    bloques = [np.flatnonzero(anios == a) for a in np.unique(anios)]
    n = len(bloques)
    # Una sola temporada no admite estimar incertidumbre entre años.
    if n < 2:
        return np.full((2, len(config.METRICAS)), np.nan), np.zeros(len(config.METRICAS), dtype=int)
    patrones, frecuencia = np.unique(np.sort(list(product(range(n), repeat=n)), axis=1),
                                     axis=0, return_counts=True)
    replicas = []
    for patron in patrones:
        idx = np.concatenate([bloques[j] for j in patron])
        replicas.append(puntuaciones(y[idx], p[idx], ref[idx]))
    muestra = np.repeat(replicas, frecuencia, axis=0)
    return np.nanquantile(muestra, config.CUANTILES_IC, axis=0), np.isfinite(muestra).sum(axis=0)


def evaluar_corte(tabla, horizonte, nombre, corte, grupo):
    """Reportar denominadores y réplicas válidas junto a cada estimación."""
    y, p, ref = (tabla[c].to_numpy() for c in ("perdida", "p", "referencia"))
    valores = puntuaciones(y, p, ref)
    limites, validas = intervalos(y, p, ref, tabla.anio.to_numpy())
    fila = dict(horizonte=horizonte, modelo=nombre, corte=corte, grupo=grupo, filas=len(y),
                perdidas=y.sum(), prevalencia=y.mean(), prob_media=p.mean(),
                brier_sin_calibrar=np.mean((y-tabla.cruda.to_numpy())**2),
                brier_referencia=np.mean((y-ref)**2))
    for i, metrica in enumerate(config.METRICAS):
        fila.update({metrica: valores[i], metrica+"_ic_inf": limites[0,i],
                     metrica+"_ic_sup": limites[1,i], metrica+"_replicas": validas[i]})
    return fila


def calibrar_evaluar(partes, modelos, ganador, horizonte, referencia):
    """Congelar ajustes; usar validación para Platt y prueba exclusivamente para verificación."""
    validacion, prueba = partes["validacion"], partes["prueba"]
    filas, control = [], []
    for nombre, modelo in modelos.items():
        xv = entradas(validacion, nombre, horizonte)
        xp = entradas(prueba, nombre, horizonte)
        # FrozenEstimator.fit es inerte. El único bloque produce una puntuación por
        # fila de validación sin introducir particiones aleatorias ni reajustar el árbol.
        bloque = np.arange(len(xv))
        calibrado = CalibratedClassifierCV(FrozenEstimator(modelo), method="sigmoid",
                                           cv=[(bloque, bloque)], ensemble=False)
        calibrado.fit(xv, validacion.perdida)
        joblib.dump(calibrado, config.ARTEFACTOS / f"{horizonte}_{nombre}_platt.joblib")
        control.append(dict(horizonte=horizonte, modelo=nombre, filas=len(xv),
                            perdidas=validacion.perdida.sum(), observada=validacion.perdida.mean(),
                            prob_media=calibrado.predict_proba(xv)[:,1].mean()))
        tabla = prueba.assign(p=calibrado.predict_proba(xp)[:,1], cruda=modelo.predict_proba(xp)[:,1],
                              referencia=referencia)
        if nombre == ganador:
            final = tabla
        cortes = [("total", "Todos", tabla)]
        for columna in ("modalidad", "anio"):
            cortes.extend((columna, grupo, t) for grupo, t in tabla.groupby(columna))
        filas.extend(evaluar_corte(t, horizonte, nombre, corte, grupo) for corte, grupo, t in cortes)
    return pd.DataFrame(filas), pd.DataFrame(control), final


def referencia_actualizada(historia, prueba):
    """Congelar la referencia de BSS con la información disponible al iniciar 2021."""
    modelo = Climatologia().fit(historia[CLAVES], historia.perdida)
    joblib.dump(modelo, config.ARTEFACTOS / "referencia_preprueba.joblib")
    return modelo.predict_proba(prueba[CLAVES])[:,1]


def clasificar(probabilidad, costos):
    """Asignar verde, amarillo o rojo con la misma regla estricta que la auditoría."""
    cortes = costos.set_index("color").umbral
    amarillo, rojo = cortes["amarillo"], cortes["rojo"]
    if not 0 < amarillo < rojo < 1:
        raise ValueError("La relación costo–pérdida no produce dos umbrales operativos ordenados")
    return np.select([probabilidad > rojo, probabilidad > amarillo],
                     ["rojo", "amarillo"], default="verde")


def avisos(t, umbral):
    """Un aviso se activa al superar el punto de indiferencia económica."""
    alerta, evento = t.p.gt(umbral), t.perdida.eq(1)
    aciertos = (alerta & evento).sum()
    return dict(filas=len(t), perdidas=evento.sum(), avisos=alerta.sum(), aciertos=aciertos,
                falsas_alarmas=(alerta & ~evento).sum(), falsas_alarmas_por_anio=(alerta & ~evento).sum()/t.anio.nunique(),
                sensibilidad=aciertos/evento.sum() if evento.any() else np.nan,
                precision=aciertos/alerta.sum() if alerta.any() else np.nan)


def semaforo(t, costos, horizonte):
    """Evaluar los dos umbrales acumulativos en el periodo y en cada año."""
    filas = []
    for accion in costos.itertuples():
        for periodo, sub in [("Todos", t), *t.groupby("anio")]:
            filas.append(dict(horizonte=horizonte, periodo=periodo, umbral=accion.umbral,
                              nivel=accion.color, **avisos(sub, accion.umbral)))
    return pd.DataFrame(filas)


def confiabilidad(t, horizonte, nombre, ruta):
    """Comparar cada curva con la diagonal en cinco grupos equipoblados."""
    fig, ax = plt.subplots(figsize=(6.8,4.6), layout="constrained")
    ax.plot([0,1], [0,1], "--", color="gray", label="Calibración ideal")
    for col, etiqueta in [("cruda","Sin calibrar"), ("p","Con Platt")]:
        obs, estim = calibration_curve(t.perdida, t[col], n_bins=config.GRUPOS_CONFIABILIDAD, strategy="quantile")
        ax.plot(estim, obs, "o-", label=etiqueta)
    ax.set(xlabel="Probabilidad media pronosticada", ylabel="Proporción de pérdidas observada",
           xlim=(0,1), ylim=(0,1), title=f"Confiabilidad en 2021–2025 · {nombre}")
    ax.legend(); fig.savefig(ruta, dpi=config.DPI_MODELOS); plt.close(fig)
