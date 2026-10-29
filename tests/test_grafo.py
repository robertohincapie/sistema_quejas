"""Pruebas del grafo con un LLM falso (no consumen API ni requieren .env)."""
import pytest
from langchain_core.runnables import RunnableLambda

from quejas.grafo import construir_grafo
from quejas.schemas import ClasificacionQueja, EstadoQueja


def _ejecutar(departamento: str, prioridad: str, respuesta_encargado: bool = False):
    """Corre el grafo completo con clasificador falso y entradas simuladas."""
    llamadas_al_encargado = []

    def encargado(resumen, depto, prio):
        llamadas_al_encargado.append((resumen, depto, prio))
        return respuesta_encargado

    clasificador = RunnableLambda(
        lambda _: ClasificacionQueja(
            resumen="Resumen de prueba.", departamento=departamento, prioridad=prioridad
        )
    )
    grafo = construir_grafo(
        clasificador=clasificador,
        fn_pedir_queja=lambda: "texto de prueba",
        fn_preguntar_encargado=encargado,
    )
    estado = EstadoQueja.model_validate(grafo.invoke(EstadoQueja()))
    return estado, llamadas_al_encargado


@pytest.mark.parametrize(
    "departamento", ["facturacion", "cobranza", "servicio_al_cliente", "soporte"]
)
def test_enrutamiento_por_departamento(departamento):
    estado, _ = _ejecutar(departamento, "bajo")
    assert estado.departamento_atendido == departamento
    assert any(linea.startswith(f"[{departamento}]") for linea in estado.historial)


@pytest.mark.parametrize("prioridad", ["bajo", "medio"])
def test_prioridad_no_alta_no_consulta_al_encargado(prioridad):
    estado, llamadas = _ejecutar("soporte", prioridad)
    assert llamadas == []
    assert estado.llamar_usuario is None
    assert "sin llamada" in estado.resultado


def test_prioridad_alta_y_encargado_dice_si():
    estado, llamadas = _ejecutar("cobranza", "alto", respuesta_encargado=True)
    assert len(llamadas) == 1
    assert llamadas[0][1:] == ("cobranza", "alto")
    assert estado.llamar_usuario is True
    assert any(linea.startswith("[llamar_usuario]") for linea in estado.historial)
    assert "se llamará al usuario" in estado.resultado


def test_prioridad_alta_y_encargado_dice_no():
    estado, llamadas = _ejecutar("soporte", "alto", respuesta_encargado=False)
    assert len(llamadas) == 1
    assert estado.llamar_usuario is False
    assert not any(linea.startswith("[llamar_usuario]") for linea in estado.historial)
    assert "no llamar" in estado.resultado


def test_historial_acumula_en_orden():
    estado, _ = _ejecutar("facturacion", "alto", respuesta_encargado=True)
    etiquetas = [linea.split("]")[0] + "]" for linea in estado.historial]
    assert etiquetas == [
        "[capturar_queja]",
        "[clasificar_queja]",
        "[facturacion]",
        "[consultar_encargado]",
        "[llamar_usuario]",
        "[cerrar_caso]",
    ]


def test_texto_precargado_omite_la_pregunta():
    def no_deberia_llamarse():
        raise AssertionError("No se debía preguntar la queja")

    clasificador = RunnableLambda(
        lambda x: ClasificacionQueja(
            resumen=x["texto_usuario"], departamento="soporte", prioridad="bajo"
        )
    )
    grafo = construir_grafo(clasificador=clasificador, fn_pedir_queja=no_deberia_llamarse)
    estado = EstadoQueja.model_validate(grafo.invoke(EstadoQueja(texto_usuario="ya viene")))
    assert estado.clasificacion.resumen == "ya viene"
