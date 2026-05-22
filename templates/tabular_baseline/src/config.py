"""Central configuration for the tabular baseline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    project_name: str = "tabular_baseline"
    data_dir: Path = Path("data")
    model_dir: Path = Path("models")
    submission_dir: Path = Path("submissions")
    log_dir: Path = Path("logs")
    train_file: str = "train.csv"
    test_file: str = "test.csv"
    target_col: str = "target"
    id_col: str = "id"
    task: str = "classification"
    random_state: int = 42
    valid_size: float = 0.2
    model_filename: str = "model.joblib"
    feature_columns: list[str] = field(default_factory=list)


def get_config() -> Config:
    return Config()

