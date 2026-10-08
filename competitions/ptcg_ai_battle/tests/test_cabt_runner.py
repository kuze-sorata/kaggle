from pathlib import Path

from agent.random_agent import RandomAgent
from simulator.cabt_runner import load_deck, run_match, summarize_match


def test_random_agents_complete_one_cabt_match() -> None:
    deck = load_deck(Path("decks/exp001_deck.csv"))
    env = run_match(deck, deck, RandomAgent(deck, 0), RandomAgent(deck, 1), seed=0)
    summary = summarize_match(env)
    assert summary["outcome"] in {"agent0_win", "agent1_win", "draw"}
    assert summary["steps"] > 1
