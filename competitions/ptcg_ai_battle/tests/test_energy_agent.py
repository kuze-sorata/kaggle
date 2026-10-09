import random

from experiments.exp003.agent.energy_agent import select_energy_first_options


def _observation(*, energy_attached: bool, hand_ids: list[int], options: list[dict]) -> dict:
    return {
        "current": {
            "energyAttached": energy_attached,
            "yourIndex": 0,
            "players": [{"hand": [{"id": card_id} for card_id in hand_ids]}],
        },
        "select": {
            "type": 0,
            "option": options,
            "minCount": 1,
            "maxCount": 1,
        },
    }


def test_energy_attachment_is_preferred_before_attack() -> None:
    observation = _observation(
        energy_attached=False,
        hand_ids=[3],
        options=[
            {"type": 13, "attackId": 1044},
            {"type": 8, "index": 0, "inPlayIndex": 0},
            {"type": 14},
        ],
    )

    assert select_energy_first_options(observation, random.Random(0)) == [1]


def test_attack_is_preferred_after_energy_is_already_attached() -> None:
    observation = _observation(
        energy_attached=True,
        hand_ids=[3],
        options=[
            {"type": 13, "attackId": 1044},
            {"type": 8, "index": 0, "inPlayIndex": 0},
            {"type": 14},
        ],
    )

    assert select_energy_first_options(observation, random.Random(0)) == [0]


def test_attack_is_used_when_no_energy_is_available() -> None:
    observation = _observation(
        energy_attached=False,
        hand_ids=[1262],
        options=[
            {"type": 13, "attackId": 1044},
            {"type": 8, "index": 0, "inPlayIndex": 0},
            {"type": 14},
        ],
    )

    assert select_energy_first_options(observation, random.Random(0)) == [0]
