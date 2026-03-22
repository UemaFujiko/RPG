from __future__ import annotations

import random
import streamlit as st

DEFAULT_STATE = {
    "turn": 1,
    "max_turns": 10,
    "trust": 60,
    "safety": 60,
    "performance": 50,
    "transparency": 50,
    "attrition_risk": 20,
    "faction_risk": 15,
    "misconduct_risk": 15,
    "history": [],
    "current_event": None,
    "game_over": False,
    "difficulty": "標準",
    "use_ai": False,
    "team_type": "コンサル会社",
    "flags": {
        "evidence_collected": False,
        "victim_protected": False,
        "leadership_alerted": False,
    },
}


STAT_KEYS = [
    "trust",
    "safety",
    "performance",
    "transparency",
    "attrition_risk",
    "faction_risk",
    "misconduct_risk",
]


def init_state() -> None:
    if "game" not in st.session_state:
        st.session_state.game = DEFAULT_STATE.copy()
        st.session_state.game["history"] = []
        st.session_state.game["flags"] = DEFAULT_STATE["flags"].copy()


def reset_state() -> None:
    for k in list(st.session_state.keys()):
        if k == "game":
            del st.session_state[k]
    init_state()


def get_game() -> dict:
    return st.session_state.game


def clamp(val: int, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, val))


def apply_judgment(judgment: dict, choice: str) -> None:
    game = get_game()
    effects = judgment.get("effects", {})
    for key in STAT_KEYS:
        game[key] = clamp(game[key] + int(effects.get(key, 0)))

    for flag, value in judgment.get("new_flags", {}).items():
        game["flags"][flag] = bool(value)

    event = game.get("current_event") or {}
    game["history"].append(
        {
            "turn": game["turn"],
            "event_title": event.get("event_title", "Unknown Event"),
            "choice": choice,
            "effects": effects,
            "reason": judgment.get("reason", ""),
            "lesson": judgment.get("lesson", ""),
        }
    )

    game["turn"] += 1
    game["current_event"] = None
    update_game_over()


def update_game_over() -> None:
    game = get_game()
    if game["turn"] > game["max_turns"]:
        game["game_over"] = True
    if game["trust"] <= 0 or game["safety"] <= 0:
        game["game_over"] = True
    if game["attrition_risk"] >= 100 or game["misconduct_risk"] >= 100:
        game["game_over"] = True


def final_rank() -> str:
    game = get_game()
    score = (
        game["trust"] + game["safety"] + game["performance"] + game["transparency"]
        - game["attrition_risk"] - game["faction_risk"] - game["misconduct_risk"]
    )
    if score >= 180:
        return "S: 高信頼・高防衛"
    if score >= 130:
        return "A: 安定運営"
    if score >= 80:
        return "B: 維持可能だが脆弱"
    if score >= 30:
        return "C: 分断リスク高"
    return "D: 崩壊寸前"


def random_seed_choice(options: list[dict]) -> dict:
    return random.choice(options)
