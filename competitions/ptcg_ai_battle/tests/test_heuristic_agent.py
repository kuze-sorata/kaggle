import random

from experiments.exp002.agent.heuristic_agent import select_heuristic_options


def test_attack_is_preferred_in_main_action_menu() -> None:
    observation = {
        "select": {
            "type": 0,
            "option": [{"type": 14}, {"type": 13}, {"type": 8}],
            "minCount": 0,
            "maxCount": 1,
        }
    }

    assert select_heuristic_options(observation, random.Random(0)) == [1]


def test_end_is_avoided_when_no_attack_is_available() -> None:
    observation = {
        "select": {
            "type": 0,
            "option": [{"type": 14}, {"type": 8}],
            "minCount": 0,
            "maxCount": 1,
        }
    }

    assert select_heuristic_options(observation, random.Random(0)) == [1]


def test_non_main_action_selection_keeps_random_baseline_behavior() -> None:
    observation = {
        "select": {
            "type": 1,
            "option": [{"type": 3}, {"type": 3}, {"type": 3}],
            "minCount": 1,
            "maxCount": 1,
        }
    }

    selected = select_heuristic_options(observation, random.Random(0))
    assert len(selected) == 1
    assert selected[0] in {0, 1, 2}
