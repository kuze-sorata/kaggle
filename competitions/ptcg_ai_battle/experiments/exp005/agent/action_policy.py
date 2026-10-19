"""Action policy for exp005: use setup actions before attacking or ending."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence

from experiments.exp001.agent.action_policy import select_random_options

MAIN_ACTION_SELECT_TYPE = 0
ATTACK_OPTION_TYPE = 13
END_OPTION_TYPE = 14


def select_exp005_options(
    observation: Mapping[str, object],
    rng: random.Random,
) -> list[int]:
    """Exhaust non-ending main actions, then attack, then end the turn.

    Follow-up choices caused by an action keep exp001's max-count random policy.
    Among setup actions, choices are random so this experiment isolates the
    decision to defer attack/end while a non-ending action remains available.
    """

    select = observation.get("select")
    if not isinstance(select, Mapping) or select.get("type") != MAIN_ACTION_SELECT_TYPE:
        return select_random_options(observation, rng)

    options = select.get("option", [])
    if not isinstance(options, Sequence) or isinstance(options, (str, bytes)):
        return []

    setup_indices = [
        index
        for index, option in enumerate(options)
        if isinstance(option, Mapping)
        and option.get("type") not in (ATTACK_OPTION_TYPE, END_OPTION_TYPE)
    ]
    if setup_indices:
        return _sample_allowed(select, setup_indices, len(options), rng, observation)

    attack_indices = [
        index
        for index, option in enumerate(options)
        if isinstance(option, Mapping) and option.get("type") == ATTACK_OPTION_TYPE
    ]
    if attack_indices:
        return _sample_allowed(select, attack_indices, len(options), rng, observation)

    end_indices = [
        index
        for index, option in enumerate(options)
        if isinstance(option, Mapping) and option.get("type") == END_OPTION_TYPE
    ]
    if end_indices:
        return _sample_allowed(select, end_indices, len(options), rng, observation)

    return select_random_options(observation, rng)


def _sample_allowed(
    select: Mapping[str, object],
    candidates: list[int],
    option_count: int,
    rng: random.Random,
    observation: Mapping[str, object],
) -> list[int]:
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
