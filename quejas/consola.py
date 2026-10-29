"""Entradas por línea de comandos.

Están separadas de los nodos para poder reemplazarlas más adelante (web, chat,
API...) o inyectar funciones falsas en las pruebas.
"""


def pedir_queja() -> str:
    """Pregunta al usuario por su queja o petición (repite si la deja vacía)."""
    while True:
        texto = input("\n¿Cuál es su queja o petición? > ").strip()
        if texto:
            return texto
        print("Por favor escriba algo.")


def consultar_encargado(resumen: str, departamento: str, prioridad: str) -> bool:
    """Pregunta al encargado si se debe llamar al usuario (s/n)."""
    print("\n--- CASO DE PRIORIDAD ALTA ---")
    print(f"Departamento: {departamento}")
    print(f"Prioridad   : {prioridad}")
    print(f"Resumen     : {resumen}")
    while True:
        respuesta = input("¿Se debe llamar al usuario? [s/n] > ").strip().lower()
        if respuesta in {"s", "si", "sí", "y", "yes"}:
            return True
        if respuesta in {"n", "no"}:
            return False
        print("Responda 's' o 'n'.")
