"""Ejecutar con python -m src.models desde la raíz del repositorio."""
import logging

import pandas as pd
from threadpoolctl import threadpool_limits

from src import config
from src.models.busqueda import entrenar
from src.models.evaluacion import calibrar_evaluar, clasificar, confiabilidad, referencia_actualizada, semaforo, umbrales
from src.models.explicacion import equidad, explicar
from src.models.objetivo import cargar, grupos
from src.models.revision import main as revisar_rf07

log = logging.getLogger(__name__)


def main():
    """Fijar los dos ganadores antes de evaluar y explicar la prueba reservada."""
    config.ARTEFACTOS.mkdir(exist_ok=True)
    config.FIGURAS.mkdir(parents=True, exist_ok=True)
    datos = cargar()
    por_anio = datos.groupby("anio").perdida.agg(filas="size", perdidas="sum")
    por_anio["lluvia_floracion_temporal_mm"] = (datos.loc[datos.modalidad.eq("Temporal")]
                                                .groupby("anio").lluvia_floracion_mm.mean())
    por_anio["filas_temporal"] = datos.loc[datos.modalidad.eq("Temporal")].groupby("anio").size()
    partes = grupos(datos)
    ajustes = {h: entrenar(partes["entrenamiento"], h) for h in config.HORIZONTES}
    historia = pd.concat([partes["entrenamiento"], partes["validacion"]])
    factores = pd.read_parquet(config.PLATA / "inpc.parquet").set_index("anio")
    costos = umbrales(historia, factores.at[config.ANIO_COSTO_AUXILIO, "factor_pesos_constantes"])
    ref = referencia_actualizada(historia, partes["prueba"])
    rojo = costos.loc[costos.color.eq("rojo"), "umbral"].item()
    salidas = {"costos_semaforo": [costos], "diagnostico_temporal": [por_anio.reset_index()]}
    for h, (modelos, ganador, busqueda) in ajustes.items():
        log.info("%s · ganador fijado: %s", h, ganador)
        metricas, calibracion, t = calibrar_evaluar(partes, modelos, ganador, h, ref)
        t = t.assign(color=clasificar(t.p, costos))
        pronosticos = t[["cvegeo", "municipio", "anio", "modalidad", "perdida", "cruda", "p", "color"]].assign(horizonte=h, modelo=ganador)
        sufijo = "" if h == "completa" else "_" + h
        confiabilidad(t, h, ganador, config.FIGURAS / f"fig_3_5_2_confiabilidad{sufijo}.png")
        ranking, caso = explicar(t, modelos[ganador], ganador, h, sufijo)
        resultados = dict(busqueda_modelos=busqueda, metricas_modelos=metricas, calibracion=calibracion,
                          semaforo=semaforo(t,costos,h), equidad_rojo=equidad(t,rojo,h), importancia_shap=ranking,
                          caso_shap=pd.DataFrame([caso]), pronosticos_prueba=pronosticos)
        for nombre, tabla in resultados.items():
            salidas.setdefault(nombre, []).append(tabla)
    for nombre, tablas in salidas.items():
        pd.concat(tablas, ignore_index=True).to_csv(config.REPORTES / f"{nombre}.csv", index=False)

    revisar_rf07()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s: %(message)s")
    with threadpool_limits(limits=1):
        main()
