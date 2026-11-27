"""API REST del piloto, ejecutable con uvicorn src.api.main:app."""
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src import config
from src.api.esquemas import Clave, ErrorAPI, Explicacion, Municipio, Prediccion, Salud, Solicitud
from src.api.servicio import Servicio, SinDatos


@asynccontextmanager
async def lifespan(app):
    app.state.servicio = Servicio()
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


app.include_router(router)
