"""Nodo 7: consulta al encargado (solo para prioridad alta)."""
from typing import Callable

from quejas.schemas import EstadoQueja


def crear_nodo_consultar_encargado(
    preguntar_encargado: Callable[[str, str, str], bool],
):
    """Fábrica: recibe la función (resumen, departamento, prioridad) -> bool."""

    def consultar_encargado(state: EstadoQueja) -> dict:
        c = state.clasificacion
        llamar = preguntar_encargado(c.resumen, c.departamento, c.prioridad)
        return {
            "llamar_usuario": llamar,
            "historial": [
                f"[consultar_encargado] Decisión del encargado: "
                f"{'llamar al usuario' if llamar else 'no llamar al usuario'}"
            ],
        }

    return consultar_encargado
