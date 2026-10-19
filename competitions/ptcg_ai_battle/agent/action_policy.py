"""Small, defensive helpers for selecting CABT option indices."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence

MAIN_ACTION_SELECT_TYPE = 0
ATTACK_OPTION_TYPE = 13
END_OPTION_TYPE = 14


def select_random_options(
    observation: Mapping[str, object],
    rng: random.Random,
) -> list[int]:
    """Return a valid random selection for a CABT observation.

    CABT exposes options as a list and asks for between ``minCount`` and
    ``maxCount`` distinct option indices.  The official example selects
    ``maxCount`` options; doing the same keeps this baseline deterministic in
    shape while respecting the actual bounds in the observation.
    """

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

    # Selecting the maximum allowed number follows the official sample agent.
    count = max_count
    return rng.sample(range(option_count), count) if count else []


def first_legal_option(observation: Mapping[str, object]) -> list[int]:
    """Return the first available option as a deterministic fallback."""

    select = observation.get("select")
    if not isinstance(select, Mapping):
        return []
    options = select.get("option", [])
    if not isinstance(options, Sequence) or isinstance(options, (str, bytes)):
        return []
    if not options:
        return []
    return [0]


def select_setup_before_end_options(
    observation: Mapping[str, object],
    rng: random.Random,
) -> list[int]:
    """Use available setup actions before attacking or ending the turn."""

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
        return _sample_candidates(select, setup_indices, len(options), rng, observation)

    attack_indices = [
        index
        for index, option in enumerate(options)
        if isinstance(option, Mapping) and option.get("type") == ATTACK_OPTION_TYPE
    ]
    if attack_indices:
        return _sample_candidates(select, attack_indices, len(options), rng, observation)

    end_indices = [
        index
        for index, option in enumerate(options)
        if isinstance(option, Mapping) and option.get("type") == END_OPTION_TYPE
    ]
    if end_indices:
        return _sample_candidates(select, end_indices, len(options), rng, observation)

    return select_random_options(observation, rng)


def _sample_candidates(
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
