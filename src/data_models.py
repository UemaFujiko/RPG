from __future__ import annotations

from typing import List, Dict
from pydantic import BaseModel, Field


class NPC(BaseModel):
    name: str
    role: str
    stance: str
    dialogue: str = ""


class EventPayload(BaseModel):
    event_title: str
    summary: str
    risk_tags: List[str] = Field(default_factory=list)
    npcs: List[NPC] = Field(default_factory=list)
    choices: List[str] = Field(default_factory=list)
    gm_hint: str = ""


class JudgeResult(BaseModel):
    effects: Dict[str, int]
    reason: str
    lesson: str
    new_flags: Dict[str, bool] = Field(default_factory=dict)
