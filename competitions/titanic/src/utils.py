"""Titanic 用の共通ユーティリティ."""

from __future__ import annotations

import random
from pathlib import Path

import joblib
import numpy as np


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def save_model(model, path: str | Path) -> Path:
    path = Path(path)
    ensure_dir(path.parent)
    joblib.dump(model, path)
    return path


def load_model(path: str | Path):
    return joblib.load(path)
