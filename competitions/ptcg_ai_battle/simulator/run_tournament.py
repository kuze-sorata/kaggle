"""Run repeated local matches and write a small JSON summary."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from agent.random_agent import RandomAgent
from simulator.cabt_runner import load_deck, run_match, summarize_match


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deck", type=Path, required=True)
    parser.add_argument("--games", type=int, default=10)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.games <= 0:
        raise ValueError("--games must be positive")
    deck = load_deck(args.deck)
    outcomes: Counter[str] = Counter()
    match_summaries: list[dict[str, object]] = []
    errors = 0
    for index in range(args.games):
        try:
            match_seed = args.seed + index
            env = run_match(
                deck,
                deck,
                RandomAgent(deck, args.seed + index * 2),
                RandomAgent(deck, args.seed + index * 2 + 1),
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

    completed_games = args.games - errors
    durations = [
        float(item["average_decision_seconds"])
        for item in match_summaries
        if isinstance(item.get("average_decision_seconds"), (int, float))
    ]
    summary = {
        "agent0": "random",
        "agent1": "random",
        "games": args.games,
        "completed_games": completed_games,
        "wins_agent0": outcomes["agent0_win"],
        "wins_agent1": outcomes["agent1_win"],
        "draws": outcomes["draw"],
        "errors": errors,
        "outcomes": dict(outcomes),
        "average_decision_seconds": sum(durations) / len(durations) if durations else None,
        "seed": args.seed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    csv_path = args.output.with_suffix(".csv")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value"])
        for key, value in summary.items():
            writer.writerow([key, json.dumps(value, ensure_ascii=False)])
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
