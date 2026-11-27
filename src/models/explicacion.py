"""Explicaciones aditivas del árbol sin calibrar y sensibilidad por grupo."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

from src import config
from src.models.objetivo import predictores
from src.models.evaluacion import avisos


def etiqueta(variable):
    """Nombre que puede leer el técnico, conservando la etapa y la unidad."""
    for prefijo, nombre in config.NOMBRES_VARIABLES.items():
        if variable.startswith(prefijo):
            resto = variable[len(prefijo):].strip("_")
            if not resto:
                return nombre
            etapa, _, unidad = resto.partition("_")
            if etapa in config.ETAPAS:
                etapa = config.NOMBRES_ETAPA[etapa]
                unidad = config.UNIDADES_CLIMA.get(unidad, "")
                return f"{nombre} en {etapa}" + (f" ({unidad})" if unidad else "")
            return f"{nombre} {resto}"
    return variable.replace("_", " ").capitalize()


def equidad(t, rojo, horizonte):
    """Auditar la oportunidad de aviso entre quienes experimentaron pérdida."""
    filas = []
    for dimension in config.GRUPOS_EQUIDAD:
        for grupo, sub in t.groupby(dimension, dropna=False):
            conteos = avisos(sub, rojo)
            filas.append(dict(horizonte=horizonte, dimension=dimension, grupo=grupo,
                              proporcion_observada=sub.perdida.mean(), prob_media=sub.p.mean(),
                              brier=((sub.perdida-sub.p)**2).mean(), umbral_rojo=rojo, **conteos,
                              interpretacion="no concluyente" if conteos["perdidas"] < config.MIN_EVENTOS_EQUIDAD
                              else "descriptiva"))
    tabla = pd.DataFrame(filas)
    mejor = tabla.groupby("dimension").sensibilidad.transform("max")
    return tabla.assign(diferencia_con_mejor=mejor-tabla.sensibilidad,
                        revisar=(mejor-tabla.sensibilidad).gt(config.BRECHA_SENSIBILIDAD))


def barras(nombres, valores, titulo, eje, ruta):
    """Gráfico horizontal con texto suficiente para los nombres climáticos."""
    fig, ax = plt.subplots(figsize=(8.3, 5.3), layout="constrained")
    ax.barh([etiqueta(x) for x in nombres], valores,
            color=np.where(np.asarray(valores) >= 0, "#276680", "#b65736"))
    ax.axvline(0, color="#303030", linewidth=0.7)
    ax.set(xlabel=eje)
    if titulo:
        ax.set_title(titulo)
    fig.savefig(ruta, dpi=config.DPI_MODELOS); plt.close(fig)


def explicar(t, modelo, nombre, horizonte, sufijo):
    """Explicar en prueba, en la escala nativa de la clase pérdida, y verificar la suma."""
    if nombre not in {"bosque", "boosting"}:
        raise ValueError("El ganador no es de árboles. Revisar el método de explicación antes de seguir.")
    x = predictores(t, horizonte)
    preparar, arbol = modelo.named_steps["preparar"], modelo.named_steps["modelo"]
    m = preparar.transform(x)
    variables = np.asarray(preparar.get_feature_names_out())
    expl = shap.TreeExplainer(arbol)(m)
    if nombre == "bosque":
        contrib, base = expl.values[:,:,1], expl.base_values[:,1]
        pred = modelo.predict_proba(x)[:,1]
        escala = "probabilidad sin calibrar"
    else:
        contrib, base = expl.values, np.asarray(expl.base_values).reshape(-1)
        pred = modelo.decision_function(x)
        escala = "logaritmo de momios"
    if not np.allclose(base + contrib.sum(axis=1), pred, atol=config.TOLERANCIA_SHAP):
        raise ValueError("Las contribuciones y la base no reconstruyen la salida del árbol")
    ranking = pd.Series(np.mean(abs(contrib), axis=0), index=variables).sort_values(ascending=False)
    fig = config.FIGURAS
    prefijo = "fig_3_5_2_shap_"
    top = ranking.head(config.N_GLOBAL).sort_values()
    barras(top.index, top.values, "",
           "Media de la contribución absoluta · " + escala, fig / f"{prefijo}global{sufijo}.png")
    caso = t.loc[t.anio.eq(config.ANIO_CASO) & t.modalidad.eq("Temporal") & t.perdida.eq(1)]
    if caso.empty:
        caso = t.loc[t.perdida.eq(1)]
    i = caso.p.idxmax()
    aportes = pd.Series(contrib[i], index=variables)
    # La prosa reúne las categorías one-hot de la misma variable en su suma exacta.
    for variable in config.CATEGORICAS_MODELO:
        columnas = [c for c in aportes.index if c.startswith(variable + "_")]
        total = aportes[columnas].sum()
        aportes = aportes.drop(columnas)
        aportes[variable] = total
    orden = aportes.abs().nlargest(config.N_LOCAL).index[::-1]
    nivel = t.at[i,"color"]
    barras(orden, aportes[orden], f"{t.at[i,'municipio']} · {t.at[i,'modalidad']} {t.at[i,'anio']}",
           "Contribución a la predicción · " + escala, fig / f"{prefijo}local{sufijo}.png")
    principales = aportes.abs().nlargest(config.N_TEXTO).index
    frases = []
    for var in principales:
        sentido = "elevó" if aportes[var] > 0 else "redujo"
        if var == "modalidad":
            descripcion = "La siembra de " + t.at[i,"modalidad"].lower()
        elif var == "estado":
            descripcion = "La ubicación en el estado " + t.at[i,"estado"]
        elif var.startswith("lluvia_"):
            etapa = var.split("_")[1].replace("floracion", "floración")
            descripcion = f"La lluvia acumulada en {etapa} ({t.at[i,var]:.1f} mm)"
        elif var.startswith("racha_seca_"):
            etapa = config.NOMBRES_ETAPA[var.split("_")[2]]
            descripcion = f"La racha de {int(t.at[i,var])} días secos en {etapa}"
        else:
            descripcion = f"{etiqueta(var)} ({t.at[i,var]:.2f})"
        frases.append(f"{descripcion} {sentido} la estimación")
    mensaje = (f"En {t.at[i,'municipio']}, {t.at[i,'modalidad'].lower()}, el aviso de {t.at[i,'anio']} "
               f"quedó en {nivel}, con una probabilidad calibrada de {100*t.at[i,'p']:.1f} %. "
               + ". ".join(f[0].upper()+f[1:] for f in frases) + ". "
               "Son las señales que más pesaron en el modelo. La lluvia y los días secos de la misma "
               "etapa comparten información. El cierre agrícola registró una pérdida.")
    local = dict(horizonte=horizonte, modelo=nombre, cvegeo=t.at[i,"cvegeo"], municipio=t.at[i,"municipio"],
                 anio=t.at[i,"anio"], modalidad=t.at[i,"modalidad"], perdida=t.at[i,"perdida"],
                 nivel=nivel, prob_calibrada=t.at[i,"p"], escala=escala, base=base[i],
                 salida=pred[i], texto=mensaje)
    return ranking.rename_axis("variable").reset_index(name="media_abs_shap").assign(horizonte=horizonte), local
