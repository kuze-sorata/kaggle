"""Feature helpers for tabular data."""

from __future__ import annotations

import pandas as pd


def split_feature_types(df: pd.DataFrame, target_col: str, id_col: str | None = None) -> tuple[list[str], list[str]]:
    excluded = {target_col}
    if id_col is not None and id_col in df.columns:
        excluded.add(id_col)

    feature_df = df.drop(columns=[col for col in excluded if col in df.columns])
    numeric_features = feature_df.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_features = feature_df.columns.difference(numeric_features).tolist()
    return numeric_features, categorical_features

