"""Compare current max-count random with count-random selection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent.random_agent import RandomAgent
from simulator.cabt_runner import load_deck
from simulator.run_tournament import run_tournament, write_tournament_outputs

from .agent.count_random_agent import CountRandomAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deck",
        type=Path,
        default=Path(__file__).parent / "decks" / "exp004_deck.csv",
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
        ("random_vs_random", RandomAgent, RandomAgent, "max_count_random", "max_count_random"),
        ("count_random_vs_random", CountRandomAgent, RandomAgent, "count_random", "max_count_random"),
        ("random_vs_count_random", RandomAgent, CountRandomAgent, "max_count_random", "count_random"),
        ("count_random_vs_count_random", CountRandomAgent, CountRandomAgent, "count_random", "count_random"),
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
        write_tournament_outputs(summary, args.output_dir / f"exp004_{name}.json")
        all_summaries[name] = summary

    print(json.dumps(all_summaries, ensure_ascii=False, indent=2))
    return 0 if all(summary["errors"] == 0 for summary in all_summaries.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
