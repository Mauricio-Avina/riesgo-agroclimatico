"""Configuración común del registro para los puntos de entrada del proyecto."""

import logging

from src import config


def configurar_registro() -> None:
    """Envía los mensajes a la consola y conserva el historial entre ejecuciones."""
    config.REGISTRO_ETL.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config.REGISTRO_ETL, mode="a", encoding="utf-8"),
        ],
    )
