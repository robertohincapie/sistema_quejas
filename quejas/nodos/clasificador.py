"""Nodo 2: clasificación con LLM (salida estructurada)."""
from langchain_core.runnables import Runnable

from quejas.schemas import EstadoQueja


def crear_nodo_clasificador(cadena: Runnable):
    """Fábrica: recibe la cadena `prompt | llm.with_structured_output(...)`."""

    def clasificar_queja(state: EstadoQueja) -> dict:
        clasificacion = cadena.invoke({"texto_usuario": state.texto_usuario})
        return {
            "clasificacion": clasificacion,
            "historial": [
                "[clasificar_queja] "
                f"departamento={clasificacion.departamento}, "
                f"prioridad={clasificacion.prioridad}"
            ],
        }

    return clasificar_queja
