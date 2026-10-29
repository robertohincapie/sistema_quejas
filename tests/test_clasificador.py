"""Pruebas de schema y prompt (sin llamadas de red)."""
import json
from pathlib import Path

import pytest
from langchain_openai import ChatOpenAI
from pydantic import ValidationError

from quejas.llm import construir_clasificador
from quejas.prompts import crear_prompt
from quejas.schemas import ClasificacionQueja

RUTA_SCHEMA = Path(__file__).parent.parent / "docs" / "clasificacion_quejas.schema.json"


def test_schema_pydantic_coincide_con_el_json_schema_original():
    original = json.loads(RUTA_SCHEMA.read_text(encoding="utf-8"))["schema"]
    generado = ClasificacionQueja.model_json_schema()

    assert set(generado["properties"]) == set(original["properties"])
    assert set(generado["required"]) == set(original["required"])
    assert generado["additionalProperties"] is False

    for campo in ("departamento", "prioridad"):
        assert generado["properties"][campo]["enum"] == original["properties"][campo]["enum"]


def test_rechaza_valores_fuera_del_enum():
    with pytest.raises(ValidationError):
        ClasificacionQueja(resumen="x", departamento="ventas", prioridad="alto")
    with pytest.raises(ValidationError):
        ClasificacionQueja(resumen="x", departamento="soporte", prioridad="urgente")


def test_rechaza_campos_extra():
    with pytest.raises(ValidationError):
        ClasificacionQueja(
            resumen="x", departamento="soporte", prioridad="bajo", extra="no permitido"
        )


def test_prompt_formatea_aunque_el_usuario_escriba_llaves():
    mensajes = crear_prompt().format_messages(texto_usuario='Error {"codigo": 500}')
    assert len(mensajes) == 2
    assert 'Error {"codigo": 500}' in mensajes[1].content


def test_cadena_se_construye_con_json_schema_estricto():
    # Clave falsa: construir la cadena no hace llamadas de red.
    llm = ChatOpenAI(model="gpt-4o-mini", api_key="sk-prueba")
    cadena = construir_clasificador(llm)
    assert cadena is not None
