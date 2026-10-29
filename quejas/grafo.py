"""Construcción y compilación del grafo LangGraph."""
from typing import Callable, Optional

from langchain_core.runnables import Runnable
from langgraph.graph import END, START, StateGraph

from quejas.consola import consultar_encargado as consultar_encargado_consola
from quejas.consola import pedir_queja as pedir_queja_consola
from quejas.llm import construir_clasificador
from quejas.nodos import (
    crear_nodo_capturar_queja,
    crear_nodo_clasificador,
    crear_nodo_consultar_encargado,
    nodo_cerrar_caso,
    nodo_cobranza,
    nodo_facturacion,
    nodo_llamar_usuario,
    nodo_servicio_al_cliente,
    nodo_soporte,
)
from quejas.routers import (
    enrutar_llamada,
    enrutar_por_departamento,
    enrutar_por_prioridad,
)
from quejas.schemas import DEPARTAMENTOS, EstadoQueja


def construir_grafo(
    clasificador: Optional[Runnable] = None,
    fn_pedir_queja: Callable[[], str] = pedir_queja_consola,
    fn_preguntar_encargado: Callable[[str, str, str], bool] = consultar_encargado_consola,
):
    """Arma y compila el grafo.

    Las dependencias externas (LLM y entradas) se inyectan por parámetro:
    así el mismo grafo corre con OpenAI + input() en producción y con
    funciones falsas en las pruebas.
    """
    if clasificador is None:
        clasificador = construir_clasificador()

    g = StateGraph(EstadoQueja)

    # --- Nodos ---
    g.add_node("capturar_queja", crear_nodo_capturar_queja(fn_pedir_queja))
    g.add_node("clasificar_queja", crear_nodo_clasificador(clasificador))
    g.add_node("facturacion", nodo_facturacion)
    g.add_node("cobranza", nodo_cobranza)
    g.add_node("servicio_al_cliente", nodo_servicio_al_cliente)
    g.add_node("soporte", nodo_soporte)
    g.add_node("consultar_encargado", crear_nodo_consultar_encargado(fn_preguntar_encargado))
    g.add_node("llamar_usuario", nodo_llamar_usuario)
    g.add_node("cerrar_caso", nodo_cerrar_caso)

    # --- Aristas ---
    g.add_edge(START, "capturar_queja")
    g.add_edge("capturar_queja", "clasificar_queja")

    # Enrutamiento 1: por departamento
    g.add_conditional_edges(
        "clasificar_queja",
        enrutar_por_departamento,
        {depto: depto for depto in DEPARTAMENTOS},
    )

    # Enrutamiento 2: por prioridad (desde cada departamento)
    for depto in DEPARTAMENTOS:
        g.add_conditional_edges(
            depto,
            enrutar_por_prioridad,
            {"consultar_encargado": "consultar_encargado", "cerrar_caso": "cerrar_caso"},
        )

    # Enrutamiento 3: decisión del encargado
    g.add_conditional_edges(
        "consultar_encargado",
        enrutar_llamada,
        {"llamar_usuario": "llamar_usuario", "cerrar_caso": "cerrar_caso"},
    )

    g.add_edge("llamar_usuario", "cerrar_caso")
    g.add_edge("cerrar_caso", END)

    return g.compile()
