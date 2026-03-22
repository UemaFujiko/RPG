from __future__ import annotations

import json
from pathlib import Path

from src.ai_client import is_ai_enabled, call_responses_json
from src.data_models import EventPayload, JudgeResult
from src.fallback_data import FALLBACK_JUDGMENTS

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_PATH = BASE_DIR / "prompts" / "judge_prompt.txt"


def _load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def judge_choice(game: dict, event: EventPayload, choice: str) -> JudgeResult:
    if not is_ai_enabled():
        fallback = FALLBACK_JUDGMENTS.get(choice)
        if fallback is None:
            fallback = {
                "effects": {"trust": 0, "safety": 0, "performance": 0, "transparency": 0, "attrition_risk": 0, "faction_risk": 0, "misconduct_risk": 0},
                "reason": "既定判定がないため、変化なしで処理した。",
                "lesson": "固定イベント拡張時は、この選択肢の判定を追加してください。",
                "new_flags": {},
            }
        return JudgeResult(**fallback)

    prompt = _load_prompt().format(
        game_state=json.dumps(
            {
                "turn": game["turn"],
                "team_type": game["team_type"],
                "difficulty": game["difficulty"],
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
        event_payload=event.model_dump_json(indent=2),
        player_choice=choice,
    )
    result = call_responses_json(prompt)
    return JudgeResult(**result)
