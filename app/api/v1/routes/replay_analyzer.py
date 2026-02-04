from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.replay_analyzer import Step, aggregate, analyze, compare

router = APIRouter(prefix="/v1", tags=["replay-analyzer"])


class StepIn(BaseModel):
    t: int
    action: str
    reward: float = 0.0
    legal: bool = True
    info: Dict[str, Any] = Field(default_factory=dict)


class AnalyzeIn(BaseModel):
    steps: List[StepIn]


class CompareIn(BaseModel):
    a: AnalyzeIn
    b: AnalyzeIn


class AggregateIn(BaseModel):
    matches: List[AnalyzeIn]


@router.post("/analyze")
def api_analyze(body: AnalyzeIn) -> Dict[str, Any]:
    steps = [Step(t=s.t, action=s.action, reward=s.reward, legal=s.legal, info=s.info) for s in body.steps]
    return {"analysis": analyze(steps)}


@router.post("/compare")
def api_compare(body: CompareIn) -> Dict[str, Any]:
    a_steps = [Step(t=s.t, action=s.action, reward=s.reward, legal=s.legal, info=s.info) for s in body.a.steps]
    b_steps = [Step(t=s.t, action=s.action, reward=s.reward, legal=s.legal, info=s.info) for s in body.b.steps]
    a_sum = analyze(a_steps)
    b_sum = analyze(b_steps)
    return {"a": a_sum, "b": b_sum, "delta": compare(a_sum, b_sum)}


@router.post("/aggregate")
def api_aggregate(body: AggregateIn) -> Dict[str, Any]:
    sums = []
    for m in body.matches:
        steps = [Step(t=s.t, action=s.action, reward=s.reward, legal=s.legal, info=s.info) for s in m.steps]
        sums.append(analyze(steps))
    return {"summary": aggregate(sums)}
