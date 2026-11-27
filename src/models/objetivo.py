"""Evento de pérdida y disponibilidad de predictores en cada horizonte."""
import numpy as np
import pandas as pd

from src import config


def cargar():
    """Leer oro en orden estable y derivar únicamente el estado y el evento."""
    datos = pd.read_parquet(config.ORO / "dataset_maestro.parquet")
    datos = datos.sort_values(["anio", "cvegeo", "modalidad"]).reset_index(drop=True)
    if datos["siniestralidad"].isna().any():
        raise ValueError("La etiqueta tiene valores desconocidos")
    return datos.assign(estado=datos.cvegeo.str[:2],
                        perdida=datos.siniestralidad.gt(config.UMBRAL_PERDIDA).astype(int))


def predictores(datos, horizonte):
    """Seleccionar por lista positiva y detener el ajuste ante datos incompletos."""
    clima = [col for col in config.CLIMA_MODELO
             if any(etapa in col.split("_") for etapa in config.HORIZONTES[horizonte])]
    matriz = datos.loc[:, [*config.FIJAS_MODELO, *clima]].copy()
    matriz["altitud_celda_m"] = matriz.altitud_celda_m.astype(float)
    if matriz.isna().any().any():
        raise ValueError("Hay predictores sin valor")
    return matriz


def grupos(datos):
    """Separar años completos antes de cualquier ajuste."""
    return {nombre: datos.loc[datos.anio.isin(anios)].reset_index(drop=True)
            for nombre, anios in config.ANIOS_MODELO.items()}


def pliegues(entrenamiento):
    """Índices posicionales para una ventana de entrenamiento creciente."""
    for inicio in config.INICIOS_PLIEGUE:
        antes = entrenamiento.anio < inicio
        despues = entrenamiento.anio.between(inicio, inicio + config.ANIOS_POR_PLIEGUE - 1)
        yield np.flatnonzero(antes), np.flatnonzero(despues)
