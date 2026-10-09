import random

from experiments.exp004.agent.count_random_agent import select_count_random_options


def test_count_random_selection_respects_bounds_and_distinct_indices() -> None:
    observation = {
        "select": {
            "option": ["a", "b", "c", "d"],
            "minCount": 1,
            "maxCount": 3,
        }
    }

    selected = select_count_random_options(observation, random.Random(0))
    assert 1 <= len(selected) <= 3
    assert len(selected) == len(set(selected))
    assert all(0 <= index < 4 for index in selected)


def test_count_random_selection_uses_fixed_count_when_bounds_match() -> None:
    observation = {
        "select": {
            "option": ["a", "b", "c"],
            "minCount": 2,
            "maxCount": 2,
        }
    }

    selected = select_count_random_options(observation, random.Random(0))
    assert len(selected) == 2


def test_count_random_selection_can_return_empty_when_optional() -> None:
    observation = {
        "select": {
            "option": ["a", "b"],
            "minCount": 0,
            "maxCount": 0,
        }
    }

    assert select_count_random_options(observation, random.Random(0)) == []
