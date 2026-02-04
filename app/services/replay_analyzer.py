from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass
class Step:
    t: int
    action: str
    reward: float = 0.0
    legal: bool = True
    info: Dict[str, Any] | None = None


def analyze(steps: List[Step]) -> Dict[str, Any]:
    failures = Counter()
    swing: List[Tuple[int, float]] = []

    prev_action = None
    repeat_streak = 0
    cum = 0.0
    prev_cum = 0.0

    for s in steps:
        if not s.legal:
            failures["illegal_move"] += 1
        if s.action.lower() in ("timeout", "timed_out"):
            failures["timeout"] += 1
        if s.action.lower() in ("noop", "no_op"):
            failures["noop"] += 1

        if prev_action == s.action:
            repeat_streak += 1
        else:
            repeat_streak = 0
        if repeat_streak >= 2:
            failures["repeated_action"] += 1

        cum += float(s.reward)
        delta = cum - prev_cum
        swing.append((s.t, abs(delta)))
        prev_cum = cum
        prev_action = s.action

    swing.sort(key=lambda x: x[1], reverse=True)
    top_swing = [{"t": t, "magnitude": mag} for t, mag in swing[:5]]

    return {
        "steps": len(steps),
        "total_reward": cum,
        "failure_modes": dict(failures),
        "top_swing_moments": top_swing,
    }


def compare(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    # Compare summary dicts from analyze.
    return {
        "delta_total_reward": a.get("total_reward", 0) - b.get("total_reward", 0),
        "delta_steps": a.get("steps", 0) - b.get("steps", 0),
        "failure_mode_delta": _delta_counter(a.get("failure_modes", {}), b.get("failure_modes", {})),
    }


def _delta_counter(a: Dict[str, int], b: Dict[str, int]) -> Dict[str, int]:
    keys = set(a) | set(b)
    return {k: int(a.get(k, 0)) - int(b.get(k, 0)) for k in sorted(keys)}


def aggregate(summaries: List[Dict[str, Any]]) -> Dict[str, Any]:
    failures = Counter()
    total_reward = 0.0
    steps = 0
    for s in summaries:
        total_reward += float(s.get("total_reward", 0.0))
        steps += int(s.get("steps", 0))
        failures.update(s.get("failure_modes", {}))
    return {
        "matches": len(summaries),
        "total_reward": total_reward,
        "total_steps": steps,
        "failure_modes": dict(failures),
    }
