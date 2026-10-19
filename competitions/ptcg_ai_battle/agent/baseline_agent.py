"""Current submission baseline that exhausts setup actions before attacking."""

from __future__ import annotations

import random
from collections.abc import Mapping

from agent.action_policy import select_setup_before_end_options
from agent.default_deck import DEFAULT_DECK


def baseline_agent(
    observation: Mapping[str, object],
    configuration: Mapping[str, object] | None = None,
) -> list[int]:
    """Return the exp005 policy action using process-global randomness."""

    if observation.get("select") is None:
        return list(DEFAULT_DECK)
    return select_setup_before_end_options(observation, random)
