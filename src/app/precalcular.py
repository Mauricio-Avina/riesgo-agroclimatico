"""Publicar una instantánea completa después de generar y comprobar todos sus boletines."""
from datetime import date
import json
import logging
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from threadpoolctl import threadpool_limits

from src import config
from src.api.esquemas import Solicitud
from src.api.fichas import ficha
from src.api.servicio import Servicio
from src.app.boletines import escribir

log = logging.getLogger(__name__)


def main():
    servicio = Servicio()
    catalogo = servicio.municipios()
    fecha = date.today().isoformat()
    fichas = []
    config.ARTEFACTOS.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=config.ARTEFACTOS) as carpeta:
        staging = Path(carpeta)
        for m in catalogo:
            municipales = []
            for modalidad in m["modalidades"]:
                for etapa in config.ETAPAS:
                    entrada = Solicitud(cvegeo=m["cvegeo"], modalidad=modalidad, anio=config.CICLO_DEMO, ultima_etapa=etapa)
                    f = ficha(servicio, entrada)
                    fichas.append(f)
                    if etapa == "llenado":
                        municipales.append(f)
            escribir(staging / (m["cvegeo"] + ".pdf"), municipales)
        archivo = staging / config.FICHA_LOCAL.name
        archivo.write_text(json.dumps(dict(generado=fecha, ciclo=config.CICLO_DEMO, modelo=servicio.nombre,
                                            catalogo=catalogo, fichas=fichas), ensure_ascii=False), encoding="utf-8")
        config.BOLETINES.mkdir(exist_ok=True)
        for pdf in staging.glob("*.pdf"):
            os.replace(pdf, config.BOLETINES / pdf.name)
        os.replace(archivo, config.FICHA_LOCAL)
    log.info("%d fichas y %d boletines publicados", len(fichas), len(catalogo))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s: %(message)s")
    logging.getLogger("fontTools").setLevel(logging.WARNING)
    with threadpool_limits(limits=1):
        main()
