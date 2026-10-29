"""Nodos 8-9: llamada al usuario (simulada) y cierre del caso."""
from quejas.schemas import EstadoQueja


def nodo_llamar_usuario(state: EstadoQueja) -> dict:
    return {
        "historial": ["[llamar_usuario] Llamada al usuario programada (simulada)."],
    }


def nodo_cerrar_caso(state: EstadoQueja) -> dict:
    c = state.clasificacion
    depto = state.departamento_atendido

    if state.llamar_usuario:
        resultado = f"Caso derivado a {depto} (prioridad {c.prioridad}); se llamará al usuario."
    elif c.prioridad == "alto":
        resultado = (
            f"Caso derivado a {depto} (prioridad alto); "
            "el encargado decidió no llamar al usuario."
        )
    else:
        resultado = f"Caso registrado en {depto} (prioridad {c.prioridad}); sin llamada."

    return {
        "resultado": resultado,
        "historial": ["[cerrar_caso] Caso cerrado."],
    }
