"""Energy-first, attack-second heuristic for exp003."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence

from .action_policy import select_random_options
from .default_deck import DEFAULT_DECK

MAIN_ACTION_SELECT_TYPE = 0
ATTACH_OPTION_TYPE = 8
ATTACK_OPTION_TYPE = 13
END_OPTION_TYPE = 14
ENERGY_CARD_IDS = frozenset({3})


def select_energy_first_options(
    observation: Mapping[str, object],
    rng: random.Random,
    energy_card_ids: frozenset[int] = ENERGY_CARD_IDS,
) -> list[int]:
    """Attach a hand energy before attacking when the board allows it."""

    select = observation.get("select")
    if not isinstance(select, Mapping) or select.get("type") != MAIN_ACTION_SELECT_TYPE:
        return select_random_options(observation, rng)

    options = select.get("option", [])
    if not isinstance(options, Sequence) or isinstance(options, (str, bytes)):
        return []

    current = observation.get("current")
    if isinstance(current, Mapping) and current.get("energyAttached") is False:
        energy_attach_indices = _energy_attach_indices(current, options, energy_card_ids)
        if energy_attach_indices:
            return _sample_candidates(
                select, energy_attach_indices, len(options), rng, observation
            )

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


def _energy_attach_indices(
    current: Mapping[str, object],
    options: Sequence[object],
    energy_card_ids: frozenset[int],
) -> list[int]:
    """Find attach options whose hand index points to a configured energy card."""

    players = current.get("players")
    your_index = current.get("yourIndex")
    if (
        not isinstance(players, Sequence)
        or isinstance(players, (str, bytes))
        or not isinstance(your_index, int)
        or not 0 <= your_index < len(players)
    ):
        return []

    player = players[your_index]
    if not isinstance(player, Mapping):
        return []
    hand = player.get("hand")
    if not isinstance(hand, Sequence) or isinstance(hand, (str, bytes)):
        return []

    candidates: list[int] = []
    for option_index, option in enumerate(options):
        if not isinstance(option, Mapping) or option.get("type") != ATTACH_OPTION_TYPE:
            continue
        hand_index = option.get("index")
        if not isinstance(hand_index, int) or not 0 <= hand_index < len(hand):
            continue
        card = hand[hand_index]
        if isinstance(card, Mapping) and card.get("id") in energy_card_ids:
            candidates.append(option_index)

    active_candidates = [
        index for index in candidates if isinstance(options[index], Mapping) and options[index].get("inPlayIndex") == 0
    ]
    return active_candidates or candidates


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


class EnergyFirstAgent:
    """Callable exp003 agent with isolated tie-breaking randomness."""

    def __init__(
        self,
        deck: Sequence[int] = DEFAULT_DECK,
        seed: int | None = None,
        energy_card_ids: frozenset[int] = ENERGY_CARD_IDS,
    ) -> None:
        if len(deck) != 60:
            raise ValueError("A CABT deck must contain exactly 60 card IDs")
        self.deck = list(deck)
        self.rng = random.Random(seed)
        self.energy_card_ids = energy_card_ids

    def __call__(
        self,
        observation: Mapping[str, object],
        configuration: Mapping[str, object] | None = None,
    ) -> list[int]:
        if observation.get("select") is None:
            return list(self.deck)
        return select_energy_first_options(observation, self.rng, self.energy_card_ids)
