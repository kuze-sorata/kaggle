"""Generate predictions from a trained model."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from config import get_config
from utils import ensure_dir, load_model


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--model-path", default=None)
    parser.add_argument("--output", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cfg = get_config()
    if args.data_dir:
        cfg.data_dir = Path(args.data_dir)

    model_path = Path(args.model_path) if args.model_path else cfg.model_dir / cfg.model_filename
    output_path = Path(args.output) if args.output else ensure_dir(cfg.submission_dir) / "submission.csv"

    test_path = cfg.data_dir / cfg.test_file
    df = pd.read_csv(test_path)
    ids = df[cfg.id_col] if cfg.id_col in df.columns else pd.Series(range(len(df)), name=cfg.id_col)

    model = load_model(model_path)
    predictions = model.predict(df)

    submission = pd.DataFrame({cfg.id_col: ids, cfg.target_col: predictions})
    ensure_dir(output_path.parent)
    submission.to_csv(output_path, index=False)
    print(f"Saved submission to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

