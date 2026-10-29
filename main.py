"""Punto de entrada por línea de comandos.

Uso:
    python main.py                      # pregunta la queja por consola
    python main.py --texto "No puedo entrar a mi cuenta"
    python main.py --mermaid            # imprime el grafo en Mermaid (no usa OpenAI)
"""
import argparse

from quejas.grafo import construir_grafo
from quejas.schemas import EstadoQueja


def main() -> None:
    parser = argparse.ArgumentParser(description="Clasificador de quejas con LangGraph")
    parser.add_argument("--texto", default="", help="Queja como argumento (omite la pregunta).")
    parser.add_argument(
        "--mermaid", action="store_true", help="Imprime el diagrama Mermaid del grafo y termina."
    )
    args = parser.parse_args()

    if args.mermaid:
        # Dummy: solo para dibujar, no se llama al LLM. Evita exigir OPENAI_API_KEY.
        from langchain_core.runnables import RunnableLambda

        grafo = construir_grafo(clasificador=RunnableLambda(lambda _: None))
        print(grafo.get_graph().draw_mermaid())
        return

    grafo = construir_grafo()
    resultado = grafo.invoke(EstadoQueja(texto_usuario=args.texto))
    estado = EstadoQueja.model_validate(resultado)

    print("\n================ RESULTADO ================")
    print(f"Resumen     : {estado.clasificacion.resumen}")
    print(f"Departamento: {estado.clasificacion.departamento}")
    print(f"Prioridad   : {estado.clasificacion.prioridad}")
    print(f"Decisión    : {estado.resultado}")
    print("\n--- Traza de nodos ---")
    for linea in estado.historial:
        print(linea)


if __name__ == "__main__":
    main()
