"""Carga de configuración desde variables de entorno (.env)."""
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    api_key: str
    modelo: str
    temperatura: float
    base_url: Optional[str]


def cargar_config() -> Config:
    """Lee el .env y valida lo mínimo necesario para llamar a OpenAI."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key.startswith("sk-..."):
        raise RuntimeError(
            "Falta OPENAI_API_KEY. Copia .env.example a .env y completa tu clave."
        )

    return Config(
        api_key=api_key,
        modelo=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip(),
        temperatura=float(os.getenv("OPENAI_TEMPERATURE", "0")),
        base_url=os.getenv("OPENAI_BASE_URL", "").strip() or None,
    )
