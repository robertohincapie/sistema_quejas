"""Nodo 1: captura de la queja del usuario."""
from typing import Callable

from quejas.schemas import EstadoQueja


def crear_nodo_capturar_queja(pedir_queja: Callable[[], str]):
    """Fábrica: recibe la función que obtiene el texto (por ahora, input())."""

    def capturar_queja(state: EstadoQueja) -> dict:
        # Si el estado ya trae texto (p. ej. python main.py --texto "..."), no se pregunta.
        texto = state.texto_usuario.strip() or pedir_queja()
        return {
            "texto_usuario": texto,
            "historial": [f"[capturar_queja] Texto recibido ({len(texto)} caracteres)."],
        }

    return capturar_queja
