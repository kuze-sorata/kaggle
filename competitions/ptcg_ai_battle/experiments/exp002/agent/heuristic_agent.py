"""Attack-first, end-avoidance heuristic for exp002."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence

from .action_policy import select_random_options
from .default_deck import DEFAULT_DECK

MAIN_ACTION_SELECT_TYPE = 0
ATTACK_OPTION_TYPE = 13
END_OPTION_TYPE = 14


def select_heuristic_options(
    observation: Mapping[str, object],
    rng: random.Random,
) -> list[int]:
    """Prefer attacks, then any non-end action, for the main action menu."""

    select = observation.get("select")
    if not isinstance(select, Mapping) or select.get("type") != MAIN_ACTION_SELECT_TYPE:
        return select_random_options(observation, rng)

    options = select.get("option", [])
    if not isinstance(options, Sequence) or isinstance(options, (str, bytes)):
        return []

    attack_indices = [
        index for index, option in enumerate(options)
        if isinstance(option, Mapping) and option.get("type") == ATTACK_OPTION_TYPE
    ]
    if attack_indices:
        return _sample_candidates(select, attack_indices, len(options), rng, observation)

    non_end_indices = [
        index for index, option in enumerate(options)
        if isinstance(option, Mapping) and option.get("type") != END_OPTION_TYPE
    ]
    if non_end_indices:
        return _sample_candidates(select, non_end_indices, len(options), rng, observation)

    return select_random_options(observation, rng)


def _sample_candidates(
    select: Mapping[str, object],
    candidates: list[int],
    option_count: int,
    rng: random.Random,
    observation: Mapping[str, object],
) -> list[int]:
    """Sample the allowed number of candidates while preserving legal bounds."""

    min_count = _bounded_int(select.get("minCount"), default=0)
    max_count = min(_bounded_int(select.get("maxCount"), default=min_count), option_count)
    count = min(max_count, len(candidates))
    if count < min_count:
        return select_random_options(observation, rng)
    return rng.sample(candidates, count) if count else []


def _bounded_int(value: object, *, default: int) -> int:
    if isinstance(value, bool):
        return default
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default


class HeuristicAgent:
    """Callable exp002 agent with isolated randomness for tie-breaking."""

    def __init__(self, deck: Sequence[int] = DEFAULT_DECK, seed: int | None = None) -> None:
        if len(deck) != 60:
            raise ValueError("A CABT deck must contain exactly 60 card IDs")
        self.deck = list(deck)
        self.rng = random.Random(seed)

    def __call__(
        self,
        observation: Mapping[str, object],
        configuration: Mapping[str, object] | None = None,
    ) -> list[int]:
        if observation.get("select") is None:
            return list(self.deck)
        return select_heuristic_options(observation, self.rng)
