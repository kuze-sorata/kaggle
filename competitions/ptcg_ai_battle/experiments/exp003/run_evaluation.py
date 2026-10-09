"""Evaluate exp003 against random and exp002 baselines."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent.random_agent import RandomAgent
from experiments.exp002.agent.heuristic_agent import HeuristicAgent
from simulator.cabt_runner import load_deck
from simulator.run_tournament import run_tournament, write_tournament_outputs

from .agent.energy_agent import EnergyFirstAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deck",
        type=Path,
        default=Path(__file__).parent / "decks" / "exp003_deck.csv",
    )
    parser.add_argument("--games", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent / "outputs",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    deck = load_deck(args.deck)
    scenarios = [
        ("random_vs_random", RandomAgent, RandomAgent, "random", "random"),
        ("exp002_vs_random", HeuristicAgent, RandomAgent, "exp002", "random"),
        ("energy_first_vs_random", EnergyFirstAgent, RandomAgent, "energy_first", "random"),
        ("random_vs_energy_first", RandomAgent, EnergyFirstAgent, "random", "energy_first"),
        ("energy_first_vs_exp002", EnergyFirstAgent, HeuristicAgent, "energy_first", "exp002"),
        ("energy_first_vs_energy_first", EnergyFirstAgent, EnergyFirstAgent, "energy_first", "energy_first"),
    ]

    all_summaries: dict[str, dict[str, object]] = {}
    for name, agent0, agent1, label0, label1 in scenarios:
        summary = run_tournament(
            deck,
            games=args.games,
            seed=args.seed,
            agent0_factory=agent0,
            agent1_factory=agent1,
            agent0_label=label0,
            agent1_label=label1,
        )
        write_tournament_outputs(summary, args.output_dir / f"exp003_{name}.json")
        all_summaries[name] = summary

    print(json.dumps(all_summaries, ensure_ascii=False, indent=2))
    return 0 if all(summary["errors"] == 0 for summary in all_summaries.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
