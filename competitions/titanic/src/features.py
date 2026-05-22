"""Accepted Titanic feature engineering only."""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


TITLE_NORMALIZATION = {
    "Mlle": "Miss",
    "Ms": "Miss",
    "Mme": "Mrs",
    "Lady": "Rare",
    "Countess": "Rare",
    "Dona": "Rare",
    "Dr": "Rare",
    "Rev": "Rare",
    "Col": "Rare",
    "Major": "Rare",
    "Capt": "Rare",
    "Sir": "Rare",
    "Don": "Rare",
    "Jonkheer": "Rare",
    "Master": "Master",
    "Miss": "Miss",
    "Mr": "Mr",
    "Mrs": "Mrs",
}


class TitanicFeatureEngineer(BaseEstimator, TransformerMixin):
    """Minimal feature transformer for accepted features only.

    Start from a pass-through implementation.
    Add columns here only after notebook validation and CV comparison.
    """

    def fit(self, X: pd.DataFrame, y: Any = None) -> "TitanicFeatureEngineer":
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        title = df["Name"].fillna("").astype(str).str.extract(r",\s*([^\.]+)\.", expand=False)
        df["Title"] = title.fillna("Rare").map(lambda x: TITLE_NORMALIZATION.get(x, "Rare")).astype(str)
        family_size = df["SibSp"].fillna(0) + df["Parch"].fillna(0) + 1
        df["FamilyGroup"] = pd.cut(
            family_size,
            bins=[0, 1, 4, 100],
            labels=["alone", "small", "large"],
            right=True,
        ).astype(str)
        df["SexPclass"] = (
            df["Sex"].fillna("missing").astype(str) + "_" + df["Pclass"].fillna(-1).astype(int).astype(str)
        )
        return df.drop(columns=["Name"])
