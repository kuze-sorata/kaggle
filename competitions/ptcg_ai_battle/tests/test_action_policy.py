from agent.action_policy import first_legal_option, select_random_options
from agent.default_deck import DEFAULT_DECK
from agent.random_agent import RandomAgent


def test_random_selection_respects_option_bounds() -> None:
    observation = {"select": {"option": ["a", "b", "c"], "minCount": 1, "maxCount": 2}}
    selected = select_random_options(observation, __import__("random").Random(0))
    assert len(selected) == 2
    assert len(set(selected)) == len(selected)
    assert all(0 <= index < 3 for index in selected)


def test_empty_or_missing_selection_is_safe() -> None:
    assert select_random_options({}, __import__("random").Random(0)) == []
    assert first_legal_option({"select": {"option": []}}) == []


def test_initial_observation_returns_a_60_card_deck() -> None:
    selected = RandomAgent(DEFAULT_DECK, seed=0)({"select": None})
    assert selected == list(DEFAULT_DECK)
    assert len(selected) == 60
