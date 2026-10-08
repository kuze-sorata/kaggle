"""Capture the observations actually exposed to both local agents."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from agent.random_agent import RandomAgent
from simulator.cabt_runner import load_deck, run_match, summarize_match


class RecordingAgent:
    """Record only the observation and action visible to one agent."""

    def __init__(self, agent: RandomAgent) -> None:
        self.agent = agent
        self.observations: list[dict[str, Any]] = []
        self.actions: list[list[int]] = []

    def __call__(self, observation: dict[str, Any], configuration: dict[str, Any]) -> list[int]:
        self.observations.append(copy.deepcopy(observation))
        action = self.agent(observation, configuration)
        self.actions.append(list(action))
        return action


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deck", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    deck = load_deck(args.deck)
    agent0 = RecordingAgent(RandomAgent(deck, args.seed))
    agent1 = RecordingAgent(RandomAgent(deck, args.seed + 1))
    env = run_match(deck, deck, agent0, agent1, seed=args.seed)
    payload = {
        "match": summarize_match(env),
        "players": [
            {"observations": agent0.observations, "actions": agent0.actions},
            {"observations": agent1.observations, "actions": agent1.actions},
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload["match"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
