"""Accepted Titanic feature engineering only."""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class TitanicFeatureEngineer(BaseEstimator, TransformerMixin):
    """Minimal feature transformer for accepted features only.

    Start from a pass-through implementation.
    Add columns here only after notebook validation and CV comparison.
    """

    def fit(self, X: pd.DataFrame, y: Any = None) -> "TitanicFeatureEngineer":
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return X.copy()
