"""Train a simple tabular baseline model."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.pipeline import Pipeline

from config import get_config
from features import split_feature_types
from preprocess import build_preprocessor
from utils import ensure_dir, save_model, set_seed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--target-col", default=None)
    parser.add_argument("--task", choices=["classification", "regression"], default=None)
    return parser.parse_args()


def build_estimator(task: str, random_state: int):
    if task == "regression":
        return Ridge(alpha=1.0, random_state=random_state)
    return LogisticRegression(max_iter=1000, random_state=random_state, n_jobs=-1)


def main() -> int:
    args = parse_args()
    cfg = get_config()
    if args.data_dir:
        cfg.data_dir = Path(args.data_dir)
    if args.target_col:
        cfg.target_col = args.target_col
    if args.task:
        cfg.task = args.task

    set_seed(cfg.random_state)

    train_path = cfg.data_dir / cfg.train_file
    df = pd.read_csv(train_path)
    y = df[cfg.target_col]
    numeric_features, categorical_features = split_feature_types(df, cfg.target_col, cfg.id_col)
    X = df.drop(columns=[cfg.target_col], errors="ignore")

    model = Pipeline(
        steps=[
            ("preprocess", build_preprocessor(numeric_features, categorical_features)),
            ("model", build_estimator(cfg.task, cfg.random_state)),
        ]
    )

    model.fit(X, y)
    model_path = ensure_dir(cfg.model_dir) / cfg.model_filename
    save_model(model, model_path)
    print(f"Saved model to {model_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
