"""Small, defensive helpers for selecting CABT option indices."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence


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


def _bounded_int(value: object, *, default: int) -> int:
    if isinstance(value, bool):
        return default
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default
