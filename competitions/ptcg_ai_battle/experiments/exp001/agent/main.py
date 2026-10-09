"""Submission entry point.

This is intentionally a safe random baseline.  Strategy code will be added
only after the simulator and evaluation harness are verified.
"""

from __future__ import annotations

from collections.abc import Mapping

from agent.random_agent import random_agent


def agent(
    observation: Mapping[str, object],
    configuration: Mapping[str, object] | None = None,
) -> list[int]:
    """Return a legal-shaped selection for the current observation."""

    return random_agent(observation, configuration)


def main(
    observation: Mapping[str, object],
    configuration: Mapping[str, object] | None = None,
) -> list[int]:
    """Alias used by local code and the Kaggle submission wrapper."""

    return agent(observation, configuration)
