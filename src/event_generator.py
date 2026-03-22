from __future__ import annotations

import json
from pathlib import Path

from src.ai_client import is_ai_enabled, call_responses_json
from src.data_models import EventPayload
from src.fallback_data import FALLBACK_EVENTS
from src.game_state import random_seed_choice

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_DIR / "prompts" / "event_prompt.txt"


def _load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def generate_event(game: dict) -> EventPayload:
    if not is_ai_enabled():
        return EventPayload(**random_seed_choice(FALLBACK_EVENTS))

    prompt = _load_prompt().format(
        game_state=json.dumps(
            {
                "turn": game["turn"],
                "team_type": game["team_type"],
                "trust": game["trust"],
                "safety": game["safety"],
                "performance": game["performance"],
                "transparency": game["transparency"],
                "attrition_risk": game["attrition_risk"],
                "faction_risk": game["faction_risk"],
                "misconduct_risk": game["misconduct_risk"],
                "flags": game["flags"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        difficulty=game["difficulty"],
    )
    payload = call_responses_json(prompt)
    return EventPayload(**payload)
