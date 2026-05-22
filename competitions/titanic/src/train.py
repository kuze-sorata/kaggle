"""Titanic の学習と検証."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

from config import get_config
from features import TitanicFeatureEngineer
from preprocess import build_preprocessor
from utils import ensure_dir, save_model, set_seed, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default=None, help="データディレクトリ")
    parser.add_argument("--model-path", default=None, help="保存先モデルパス")
    parser.add_argument("--cv-folds", type=int, default=None, help="CV の分割数")
    return parser.parse_args()


def build_model(random_state: int) -> VotingClassifier:
    estimators = [
        (
            "lr",
            LogisticRegression(
                max_iter=3000,
                C=0.7,
                solver="lbfgs",
                random_state=random_state,
            ),
        ),
        (
            "rf",
            RandomForestClassifier(
                n_estimators=500,
                min_samples_leaf=2,
                random_state=random_state,
                n_jobs=-1,
            ),
        ),
        (
            "hgb",
            HistGradientBoostingClassifier(
                learning_rate=0.05,
                max_depth=3,
                max_iter=250,
                random_state=random_state,
            ),
        ),
    ]
    return VotingClassifier(estimators=estimators, voting="soft", weights=[2, 2, 3])


def build_pipeline(random_state: int) -> Pipeline:
    return Pipeline(
        steps=[
            ("features", TitanicFeatureEngineer()),
            ("preprocess", build_preprocessor()),
            ("model", build_model(random_state)),
        ]
    )


def main() -> int:
    args = parse_args()
    cfg = get_config()
    if args.data_dir:
        cfg.data_dir = Path(args.data_dir)
    if args.cv_folds:
        cfg.n_splits = args.cv_folds

    set_seed(cfg.random_state)

    train_path = cfg.data_dir / cfg.train_file
    df = pd.read_csv(train_path)
    y = df[cfg.target_col].astype(int)
    X = df.drop(columns=[cfg.target_col])

    pipeline = build_pipeline(cfg.random_state)
    cv = StratifiedKFold(n_splits=cfg.n_splits, shuffle=True, random_state=cfg.random_state)
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring="accuracy", n_jobs=-1)

    pipeline.fit(X, y)

    model_dir = ensure_dir(cfg.model_dir)
    model_path = Path(args.model_path) if args.model_path else model_dir / cfg.model_filename
    save_model(pipeline, model_path)

    report = [
        "Titanic 学習結果",
        f"CV mean: {scores.mean():.5f}",
        f"CV std: {scores.std():.5f}",
        f"CV folds: {cfg.n_splits}",
        f"Model path: {model_path}",
    ]
    write_text(cfg.log_dir / "train_report.txt", "\n".join(report) + "\n")

    print("\n".join(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
