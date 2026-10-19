"""Submission entry point for the current action-exhaustion baseline."""

from __future__ import annotations

from collections.abc import Mapping

from agent.baseline_agent import baseline_agent


def agent(
    observation: Mapping[str, object],
    configuration: Mapping[str, object] | None = None,
) -> list[int]:
    """Return a selection following the current exp005 baseline policy."""

    return baseline_agent(observation, configuration)


def main(
    observation: Mapping[str, object],
    configuration: Mapping[str, object] | None = None,
) -> list[int]:
    """Alias used by local code and the Kaggle submission wrapper."""

    return agent(observation, configuration)
