from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent

if load_dotenv is not None:
    load_dotenv(BASE_DIR / ".env")


def is_ai_enabled() -> bool:
    use_ai = os.getenv("USE_AI", "false").lower() == "true"
    api_key = os.getenv("OPENAI_API_KEY")
    return use_ai and bool(api_key)


def get_model_name() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def get_client() -> Optional[OpenAI]:
    if not is_ai_enabled():
        return None
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_responses_json(prompt: str) -> dict:
    client = get_client()
    if client is None:
        raise RuntimeError("AI is not enabled. Set OPENAI_API_KEY and USE_AI=true.")

    response = client.responses.create(
        model=get_model_name(),
        input=prompt,
        text={"format": {"type": "json_object"}},
    )

    text = getattr(response, "output_text", None)
    if not text:
        raise RuntimeError("Model did not return output_text.")
    return json.loads(text)