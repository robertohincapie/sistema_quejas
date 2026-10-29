"""Construcción del LLM (OpenAI) y de la cadena clasificadora con salida estructurada."""
from typing import Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

from quejas.config import cargar_config
from quejas.prompts import crear_prompt
from quejas.schemas import ClasificacionQueja


def crear_modelo() -> ChatOpenAI:
    cfg = cargar_config()
    return ChatOpenAI(
        model=cfg.modelo,
        temperature=cfg.temperatura,
        api_key=cfg.api_key,
        base_url=cfg.base_url,
    )


def construir_clasificador(llm: Optional[BaseChatModel] = None) -> Runnable:
    """prompt | LLM con salida estructurada.

    Entrada de la cadena : {"texto_usuario": str}
    Salida de la cadena  : instancia de ClasificacionQueja (validada por Pydantic)

    method="json_schema" + strict=True usa Structured Outputs de OpenAI, el mismo
    mecanismo que tu "response_format" con "strict": true.
    """
    llm = llm or crear_modelo()
    llm_estructurado = llm.with_structured_output(
        ClasificacionQueja, method="json_schema", strict=True
    )
    return crear_prompt() | llm_estructurado
