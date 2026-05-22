"""Titanic コンペ用の設定."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    project_name: str = "titanic"
    data_dir: Path = Path("data")
    model_dir: Path = Path("models")
    submission_dir: Path = Path("submissions")
    log_dir: Path = Path("logs")
    train_file: str = "train.csv"
    test_file: str = "test.csv"
    target_col: str = "Survived"
    id_col: str = "PassengerId"
    random_state: int = 42
    valid_size: float = 0.2
    n_splits: int = 5
    model_filename: str = "titanic_baseline_lr.joblib"
    submission_filename: str = "baseline_submission.csv"


def get_config() -> Config:
    return Config()
