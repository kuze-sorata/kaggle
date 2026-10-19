"""Exp005 agent that uses available setup actions before attacking or ending."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence

from experiments.exp001.agent.default_deck import DEFAULT_DECK
from .action_policy import select_exp005_options


class ExhaustAgent:
    """Callable exp005 agent with isolated randomness for tie-breaking."""

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
        return select_exp005_options(observation, self.rng)
