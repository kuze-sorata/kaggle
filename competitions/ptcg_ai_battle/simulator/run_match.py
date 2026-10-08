"""Run one local random-vs-random CABT match."""

from __future__ import annotations

import argparse
from pathlib import Path

from agent.random_agent import RandomAgent
from simulator.cabt_runner import load_deck, run_match, summarize_match


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deck", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--render", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    deck = load_deck(args.deck)
    env = run_match(
        deck,
        deck,
        RandomAgent(deck, args.seed),
        RandomAgent(deck, args.seed + 1),
        seed=args.seed,
    )
    if args.render:
        args.render.parent.mkdir(parents=True, exist_ok=True)
        args.render.write_text(env.render(mode="html"), encoding="utf-8")
    print(summarize_match(env))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
