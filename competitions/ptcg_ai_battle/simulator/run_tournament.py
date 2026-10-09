"""Run repeated local matches and write a small JSON summary."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from collections.abc import Callable, Sequence
from pathlib import Path

from agent.random_agent import RandomAgent
from simulator.cabt_runner import load_deck, run_match, summarize_match

AgentFactory = Callable[[Sequence[int], int | None], Callable[..., list[int]]]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deck", type=Path, required=True)
    parser.add_argument("--games", type=int, default=10)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def run_tournament(
    deck: Sequence[int],
    *,
    games: int = 10,
    seed: int = 0,
    agent0_factory: AgentFactory = RandomAgent,
    agent1_factory: AgentFactory = RandomAgent,
    agent0_label: str = "random",
    agent1_label: str = "random",
) -> dict[str, object]:
    """Run matches between two injectable agent factories."""

    if games <= 0:
        raise ValueError("games must be positive")

    outcomes: Counter[str] = Counter()
    match_summaries: list[dict[str, object]] = []
    errors = 0
    for index in range(games):
        try:
            match_seed = seed + index
            env = run_match(
                deck,
                deck,
                agent0_factory(deck, seed + index * 2),
                agent1_factory(deck, seed + index * 2 + 1),
                seed=match_seed,
            )
            match_summary = summarize_match(env)
            match_summaries.append(match_summary)
            outcomes[str(match_summary["outcome"])] += 1
            if match_summary["outcome"] == "error":
                errors += 1
        except Exception as exc:  # noqa: BLE001 - record failures in evaluation output
            errors += 1
            match_summaries.append({"outcome": "error", "error_type": type(exc).__name__})
            outcomes[f"error:{type(exc).__name__}"] += 1

    completed_games = games - errors
    durations = [
        float(item["average_decision_seconds"])
        for item in match_summaries
        if isinstance(item.get("average_decision_seconds"), (int, float))
    ]
    summary = {
        "agent0": agent0_label,
        "agent1": agent1_label,
        "games": games,
        "completed_games": completed_games,
        "wins_agent0": outcomes["agent0_win"],
        "wins_agent1": outcomes["agent1_win"],
        "draws": outcomes["draw"],
        "errors": errors,
        "outcomes": dict(outcomes),
        "average_decision_seconds": sum(durations) / len(durations) if durations else None,
        "seed": seed,
    }

    return summary


def write_tournament_outputs(summary: dict[str, object], output: Path) -> None:
    """Write the JSON and CSV forms of one tournament summary."""

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    csv_path = output.with_suffix(".csv")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value"])
        for key, value in summary.items():
            writer.writerow([key, json.dumps(value, ensure_ascii=False)])


def main() -> int:
    args = build_parser().parse_args()
    deck = load_deck(args.deck)
    summary = run_tournament(deck, games=args.games, seed=args.seed)
    write_tournament_outputs(summary, args.output)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
