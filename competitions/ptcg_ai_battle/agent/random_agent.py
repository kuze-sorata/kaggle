"""Random baseline agent for local CABT matches."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence

from agent.action_policy import select_random_options
from agent.default_deck import DEFAULT_DECK


class RandomAgent:
    """Callable random agent with an isolated random-number generator."""

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
        """Select an action; CABT may also pass its configuration mapping."""

        if observation.get("select") is None:
            return list(self.deck)
        return select_random_options(observation, self.rng)


def random_agent(
    observation: Mapping[str, object],
    configuration: Mapping[str, object] | None = None,
) -> list[int]:
    """Kaggle-compatible entry point using process-global randomness."""

    if observation.get("select") is None:
        return list(DEFAULT_DECK)
    return select_random_options(observation, random)
