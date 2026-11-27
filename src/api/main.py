"""API REST del piloto, ejecutable con uvicorn src.api.main:app."""
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from src.api.esquemas import Simulacion
from src.api.fichas import ficha
from src.api.simulador import Simulador
from src import config
from src.api.esquemas import Clave, ErrorAPI, Explicacion, Municipio, Prediccion, Salud, Solicitud
from src.api.servicio import Servicio, SinDatos


@asynccontextmanager
async def lifespan(app):
    app.state.servicio = Servicio()
    app.state.simulador = Simulador(app.state.servicio)
    yield
    del app.state.servicio


app = FastAPI(title="Riesgo de pérdida de maíz", version="1.0", lifespan=lifespan,
              description="Piloto municipal de Guanajuato y Querétaro. En siembra se informa la climatología calibrada con Platt. Desde vegetativo se emplea el modelo restringido con años análogos.")
errores = {404: {"model": ErrorAPI, "description": "Sin cobertura o historial"},
           422: {"model": ErrorAPI, "description": "Datos de entrada inválidos"}}
router = APIRouter(prefix=config.PREFIJO_API)


@app.exception_handler(SinDatos)
async def sin_datos(request, exc):
    return JSONResponse(status_code=404, content={"detalle": str(exc)})


@app.exception_handler(RequestValidationError)
async def invalida(request, exc):
    campos = ", ".join(dict.fromkeys(str(e["loc"][-1]) for e in exc.errors()))
    return JSONResponse(status_code=422, content={"detalle": "Solicitud inválida. Revise los campos indicados: " + campos + "."})


@router.get("/salud", response_model=Salud, summary="Consultar disponibilidad")
def salud(request: Request):
    return {"estado": "disponible", "modelo": request.app.state.servicio.nombre}


@router.get("/municipios", response_model=list[Municipio], responses=errores, summary="Consultar municipios")
def municipios(request: Request, cvegeo: Clave | None = None):
    return request.app.state.servicio.municipios(cvegeo)


@router.post("/prediccion", response_model=Prediccion, responses=errores, summary="Estimar el riesgo de pérdida")
def prediccion(entrada: Solicitud, request: Request):
    return request.app.state.servicio.prediccion(entrada)


@router.post("/explicacion", response_model=Explicacion, responses=errores, summary="Explicar una estimación")
def explicacion(entrada: Solicitud, request: Request):
    return request.app.state.servicio.explicacion(entrada)


@router.post("/simulacion", responses=errores, summary="Comparar fechas y modalidades")
def simular(entrada: Simulacion, request: Request):
    return request.app.state.simulador.consultar(entrada)


@router.post("/ficha", responses=errores, summary="Consultar la ficha del productor")
def ver_ficha(entrada: Solicitud, request: Request):
    return ficha(request.app.state.servicio, entrada)


@router.post("/explicacion/completa", response_model=Explicacion, responses=errores)
def explicacion_completa(entrada: Solicitud, request: Request):
    return request.app.state.servicio.explicacion(entrada, vista="tecnica")


@router.get("/historial/{cvegeo}", responses=errores, summary="Consultar cierres agrícolas públicos")
def historial(cvegeo: Clave, request: Request):
    servicio = request.app.state.servicio
    servicio.municipios(cvegeo)
    filas = servicio.datos.loc[servicio.datos.cvegeo.eq(cvegeo), list(config.CAMPOS_PUBLICOS)]
    publicas = filas.astype(object).where(filas.notna(), None)
    return dict(filas=publicas.to_dict("records"), unidades=config.CAMPOS_PUBLICOS, fuente="SIAP, cierre agrícola municipal",
                fecha="Cierres de " + str(filas.anio.min()) + " a " + str(filas.anio.max()))


@router.get("/boletin/{cvegeo}", responses=errores, response_class=FileResponse, summary="Descargar el boletín municipal")
def boletin(cvegeo: Clave, request: Request):
    request.app.state.servicio.municipios(cvegeo)
    ruta = config.BOLETINES / f"{cvegeo}.pdf"
    if not ruta.is_file():
        raise SinDatos("El boletín municipal todavía no está disponible.")
    return FileResponse(ruta, media_type="application/pdf", filename=f"boletin-{cvegeo}-{config.CICLO_DEMO}.pdf")


app.include_router(router)
