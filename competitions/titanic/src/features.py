"""Titanic 用の特徴量作成."""

from __future__ import annotations

import re
from typing import Any

import numpy as np
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
    """Titanic の素性を DataFrame で整形する."""

    def __init__(self) -> None:
        self.age_median_ = 0.0
        self.fare_median_ = 0.0
        self.embarked_mode_ = "S"
        self.title_age_medians_: dict[str, float] = {}
        self.ticket_group_sizes_: dict[str, int] = {}

    @staticmethod
    def _clean_text(series: pd.Series, default: str = "Unknown") -> pd.Series:
        return series.fillna(default).astype(str).replace({"": default})

    @staticmethod
    def _extract_title(name: pd.Series) -> pd.Series:
        title = name.fillna("").astype(str).str.extract(r",\s*([^\.]+)\.", expand=False)
        title = title.fillna("Rare").map(lambda x: TITLE_NORMALIZATION.get(x, "Rare"))
        return title.astype(str)

    @staticmethod
    def _extract_ticket_prefix(ticket: pd.Series) -> pd.Series:
        prefix = ticket.fillna("").astype(str).str.replace(r"\d+", "", regex=True)
        prefix = prefix.str.replace(r"[./]", "", regex=True).str.strip()
        prefix = prefix.replace("", "NONE")
        return prefix.str.upper()

    @staticmethod
    def _extract_cabin_deck(cabin: pd.Series) -> pd.Series:
        deck = cabin.fillna("").astype(str).str[0]
        deck = deck.replace("", "U").replace("n", "U")
        return deck.str.upper()

    def fit(self, X: pd.DataFrame, y: Any = None) -> "TitanicFeatureEngineer":
        df = X.copy()
        df["Title"] = self._extract_title(df["Name"])

        self.age_median_ = float(pd.to_numeric(df["Age"], errors="coerce").median())
        self.fare_median_ = float(pd.to_numeric(df["Fare"], errors="coerce").median())
        embarked = self._clean_text(df["Embarked"], default="S")
        self.embarked_mode_ = str(embarked.mode(dropna=True).iloc[0]) if not embarked.empty else "S"

        title_age = pd.to_numeric(df["Age"], errors="coerce").groupby(df["Title"]).median()
        self.title_age_medians_ = {
            str(title): float(value)
            for title, value in title_age.items()
            if pd.notna(value)
        }

        ticket_counts = self._clean_text(df["Ticket"], default="UNKNOWN").value_counts()
        self.ticket_group_sizes_ = {str(ticket): int(count) for ticket, count in ticket_counts.items()}
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()

        df["Title"] = self._extract_title(df["Name"])
        df["Pclass"] = self._clean_text(df["Pclass"].astype("Int64").astype(str), default="Unknown")
        df["Sex"] = self._clean_text(df["Sex"], default="Unknown")
        df["Embarked"] = self._clean_text(df["Embarked"], default=self.embarked_mode_)
        df["CabinDeck"] = self._extract_cabin_deck(df["Cabin"])
        df["TicketPrefix"] = self._extract_ticket_prefix(df["Ticket"])

        df["SibSp"] = pd.to_numeric(df["SibSp"], errors="coerce").fillna(0)
        df["Parch"] = pd.to_numeric(df["Parch"], errors="coerce").fillna(0)
        df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
        df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
        df["HasCabin"] = (df["Cabin"].notna()).astype(int)

        df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce").fillna(self.fare_median_)
        df["FarePerPerson"] = df["Fare"] / df["FamilySize"].replace(0, 1)
        df["FareLog"] = np.log1p(df["Fare"].clip(lower=0))

        age = pd.to_numeric(df["Age"], errors="coerce")
        title_age = df["Title"].map(self.title_age_medians_)
        age = age.fillna(title_age)
        age = age.fillna(self.age_median_)
        df["Age"] = age
        df["AgeBand"] = pd.cut(
            df["Age"],
            bins=[-np.inf, 12, 18, 25, 35, 45, 60, np.inf],
            labels=["child", "teen", "young_adult", "adult", "mid_age", "senior", "elder"],
            right=False,
        ).astype(str)

        ticket_key = self._clean_text(df["Ticket"], default="UNKNOWN")
        df["TicketGroupSize"] = ticket_key.map(self.ticket_group_sizes_).fillna(1).astype(int)

        drop_columns = [col for col in ["Name", "Ticket", "Cabin"] if col in df.columns]
        df = df.drop(columns=drop_columns)

        if "PassengerId" in df.columns:
            df = df.drop(columns=["PassengerId"])

        return df

