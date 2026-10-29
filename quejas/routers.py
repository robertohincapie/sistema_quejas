"""Funciones de enrutamiento (aristas condicionales).

Reciben el estado y devuelven la CLAVE del siguiente nodo.
No modifican el estado.
"""
from quejas.schemas import EstadoQueja


def enrutar_por_departamento(state: EstadoQueja) -> str:
    """clasificar_queja -> uno de los cuatro nodos de departamento."""
    return state.clasificacion.departamento


def enrutar_por_prioridad(state: EstadoQueja) -> str:
    """Nodo de departamento -> consulta al encargado (si es alto) o cierre."""
    if state.clasificacion.prioridad == "alto":
        return "consultar_encargado"
    return "cerrar_caso"


def enrutar_llamada(state: EstadoQueja) -> str:
    """consultar_encargado -> llamada al usuario o cierre."""
    return "llamar_usuario" if state.llamar_usuario else "cerrar_caso"
