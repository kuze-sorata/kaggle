"""Thin wrapper around the official kaggle-environments CABT environment."""

from __future__ import annotations

import random
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

from kaggle_environments import make

Agent = Callable[[dict[str, Any]], list[int]]


def load_deck(path: Path) -> list[int]:
    """Load one card ID per line from a deck CSV/text file."""

    values: list[int] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        value = line.strip()
        if not value:
            continue
        try:
            values.append(int(value))
        except ValueError as exc:
            raise ValueError(f"Invalid card ID at {path}:{line_number}: {value!r}") from exc
    if len(values) != 60:
        raise ValueError(f"A CABT deck must contain 60 card IDs; got {len(values)} in {path}")
    return values


def run_match(
    deck0: Sequence[int],
    deck1: Sequence[int],
    agent0: Agent,
    agent1: Agent,
    seed: int | None = None,
) -> Any:
    """Run one CABT match and return the Kaggle environment object."""

    if len(deck0) != 60 or len(deck1) != 60:
        raise ValueError("Both CABT decks must contain exactly 60 card IDs")
    if seed is not None:
        # Fix the Python-level RNG. The native CABT engine also has internal
        # randomness and does not expose a seed parameter in this SDK version.
        random.seed(seed)
    env = make("cabt", configuration={"decks": [list(deck0), list(deck1)]})
    env.run([agent0, agent1])
    return env


def summarize_match(env: Any) -> dict[str, Any]:
    """Extract stable, evaluation-friendly fields from a CABT environment."""

    statuses = [player["status"] for player in env.state]
    rewards = [player.get("reward") for player in env.state]
    if all(status == "DONE" for status in statuses):
        if rewards[0] == 1:
            outcome = "agent0_win"
        elif rewards[1] == 1:
            outcome = "agent1_win"
        else:
            outcome = "draw"
    else:
        outcome = "error"

    durations = list(_find_durations(env.logs))
    return {
        "outcome": outcome,
        "statuses": statuses,
        "rewards": rewards,
        "result": getattr(env, "result", None),
        "steps": len(env.steps),
        "decision_count": len(durations),
        "average_decision_seconds": (
            sum(durations) / len(durations) if durations else None
        ),
    }


def _find_durations(value: object):
    if isinstance(value, Mapping):
        duration = value.get("duration")
        if isinstance(duration, (int, float)):
            yield float(duration)
        for child in value.values():
            yield from _find_durations(child)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for child in value:
            yield from _find_durations(child)
