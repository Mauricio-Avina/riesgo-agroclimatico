"""Contrato tipado de las cuatro operaciones del piloto."""
from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from src import config

Clave = Annotated[str, Field(pattern=r"^[0-9]{5}$", description="Clave municipal INEGI de cinco dígitos")]
Modalidad = Enum("Modalidad", {m: m for m in config.MODALIDADES}, type=str)
Etapa = Enum("Etapa", {e: e for e in config.ETAPAS}, type=str)


class Solicitud(BaseModel):
    model_config = ConfigDict(extra="forbid", json_schema_extra={"examples": [config.EJEMPLO_API]})
    cvegeo: Clave
    modalidad: Modalidad
    anio: int = Field(strict=True, ge=config.ANIO_INICIAL, le=config.ANIO_FINAL)
    ultima_etapa: Etapa


class Salud(BaseModel):
    estado: str
    modelo: str


class Municipio(BaseModel):
    cvegeo: Clave
    municipio: str
    modalidades: list[Modalidad]


class Prediccion(BaseModel):
    fuente: Literal["climatologia", "boosting_monotono"] = Field(
        description="Climatología con Platt en siembra y boosting restringido con Platt desde vegetativo.")
    probabilidad: float
    nivel: Literal["verde", "amarillo", "rojo"]
    p10: float | None
    p90: float | None
    escenarios: int
    anios_analogos: list[int]


class Factor(BaseModel):
    variable: str
    valor: str
    direccion: Literal["eleva", "reduce", "neutra"]
    aporte: float


class Explicacion(BaseModel):
    prediccion: Prediccion
    escala: str
    base: float
    salida_media: float
    factores: list[Factor]
    texto: str


class ErrorAPI(BaseModel):
    detalle: str

class Palanca(BaseModel):
    model_config = ConfigDict(extra="forbid")
    modalidad: Modalidad
    fecha: str = Field(pattern=r"^(06-(0[1-9]|[12][0-9]|30)|07-(0[1-9]|1[0-5]))$",
                       description="Mes-día, del 1 de junio al 15 de julio del año análogo.")


class Simulacion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    cvegeo: Clave
    actual: Palanca
    alternativa_b: Palanca
    alternativa_c: Palanca
