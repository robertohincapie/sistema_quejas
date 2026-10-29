"""Modelos Pydantic: salida estructurada del LLM y estado compartido del grafo."""
import operator
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

# Valores permitidos (idénticos a los enum del json_schema en docs/).
Departamento = Literal["facturacion", "cobranza", "servicio_al_cliente", "soporte"]
Prioridad = Literal["bajo", "medio", "alto"]

DEPARTAMENTOS: tuple[str, ...] = (
    "facturacion",
    "cobranza",
    "servicio_al_cliente",
    "soporte",
)


class ClasificacionQueja(BaseModel):
    """Salida estructurada del nodo clasificador.

    Equivale al json_schema "clasificacion_quejas" (strict, sin campos extra).
    """

    model_config = ConfigDict(extra="forbid")

    resumen: str = Field(
        description="Resumen breve, objetivo y concreto de la solicitud."
    )
    departamento: Departamento = Field(
        description="Departamento responsable de atender la solicitud."
    )
    prioridad: Prioridad = Field(
        description="Nivel de prioridad según el impacto en la continuidad del servicio."
    )


class EstadoQueja(BaseModel):
    """Estado que viaja por el grafo.

    Cada nodo recibe una instancia de este modelo (entrada) y devuelve un
    diccionario con SOLO los campos que quiere actualizar (salida).
    `historial` usa un reducer (operator.add): los nodos agregan líneas sin
    pisar las anteriores.
    """

    texto_usuario: str = ""
    clasificacion: Optional[ClasificacionQueja] = None
    departamento_atendido: Optional[str] = None
    llamar_usuario: Optional[bool] = None
    resultado: Optional[str] = None
    historial: Annotated[list[str], operator.add] = Field(default_factory=list)
