"""Nodos 3-6: un nodo por departamento.

Aquí cada nodo solo simula la atención del caso (registra qué haría). En un
sistema real, cada uno podría crear un ticket, llamar a una API, abrir una
tarea en el CRM, etc.
"""
from quejas.schemas import EstadoQueja


def _atender(state: EstadoQueja, departamento: str, accion: str) -> dict:
    c = state.clasificacion
    return {
        "departamento_atendido": departamento,
        "historial": [
            f"[{departamento}] {accion} | prioridad={c.prioridad} | resumen: {c.resumen}"
        ],
    }


def nodo_facturacion(state: EstadoQueja) -> dict:
    return _atender(state, "facturacion", "Revisión de facturas y cargos del usuario")


def nodo_cobranza(state: EstadoQueja) -> dict:
    return _atender(state, "cobranza", "Revisión de estado de cuenta y obligaciones vencidas")


def nodo_servicio_al_cliente(state: EstadoQueja) -> dict:
    return _atender(state, "servicio_al_cliente", "Asignación a un asesor de atención")


def nodo_soporte(state: EstadoQueja) -> dict:
    return _atender(state, "soporte", "Apertura de ticket técnico")
