from pathlib import Path

import pytest

from simulator.cabt_runner import load_deck


def test_deck_loader_requires_60_cards() -> None:
    deck = Path("tests") / "_invalid_deck.csv"
    deck.write_text("1\n" * 59, encoding="utf-8")
    try:
        with pytest.raises(ValueError, match="60"):
            load_deck(deck)
    finally:
        deck.unlink(missing_ok=True)
