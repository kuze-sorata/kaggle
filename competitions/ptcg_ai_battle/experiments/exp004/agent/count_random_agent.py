"""Random baseline that also randomizes the number of selected options."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence

from .default_deck import DEFAULT_DECK


def select_count_random_options(
    observation: Mapping[str, object],
    rng: random.Random,
) -> list[int]:
    """Select a random legal count, then a random combination of indices."""

    select = observation.get("select")
    if not isinstance(select, Mapping):
        return []

    options = select.get("option", [])
    if not isinstance(options, Sequence) or isinstance(options, (str, bytes)):
        return []
    option_count = len(options)
    if option_count == 0:
        return []

    min_count = _bounded_int(select.get("minCount"), default=0)
    max_count = _bounded_int(select.get("maxCount"), default=min_count)
    max_count = min(max_count, option_count)
    min_count = min(min_count, max_count)
    count = rng.randint(min_count, max_count)
    return rng.sample(range(option_count), count) if count else []


def _bounded_int(value: object, *, default: int) -> int:
    if isinstance(value, bool):
        return default
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default


class CountRandomAgent:
    """Callable count-random agent with isolated randomness."""

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
        return select_count_random_options(observation, self.rng)
