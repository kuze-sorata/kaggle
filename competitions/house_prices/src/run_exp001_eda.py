"""Run broad EDA for House Prices exp001 and save artifacts."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / "logs" / ".matplotlib"))

import matplotlib.pyplot as plt
import nbformat as nbf
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import ks_2samp


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs" / "exp001"
NOTEBOOK_PATH = ROOT / "notebooks" / "exp001_eda.ipynb"
TARGET = "SalePrice"
ID_COL = "Id"


def ensure_dirs() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(DATA_DIR / "train.csv")
    test = pd.read_csv(DATA_DIR / "test.csv")
    return train, test


def build_overview(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    saleprice = train[TARGET]
    overview = pd.DataFrame(
        [
            ("train_rows", len(train)),
            ("train_columns", train.shape[1]),
            ("test_rows", len(test)),
            ("test_columns", test.shape[1]),
            ("numeric_columns", len(train.select_dtypes(include=np.number).columns)),
            ("categorical_columns", len(train.select_dtypes(exclude=np.number).columns)),
            ("target_mean", round(float(saleprice.mean()), 4)),
            ("target_median", round(float(saleprice.median()), 4)),
            ("target_std", round(float(saleprice.std()), 4)),
            ("target_skew", round(float(saleprice.skew()), 4)),
            ("target_log_skew", round(float(np.log1p(saleprice).skew()), 4)),
        ],
        columns=["metric", "value"],
    )
    return overview


def build_missing_summary(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    for column in sorted(set(train.columns) | set(test.columns)):
        train_missing = float(train[column].isna().mean() * 100) if column in train.columns else np.nan
        test_missing = float(test[column].isna().mean() * 100) if column in test.columns else np.nan
        rows.append(
            {
                "column": column,
                "train_missing_pct": round(train_missing, 2),
                "test_missing_pct": round(test_missing, 2),
                "missing_gap_pct": round(abs(train_missing - test_missing), 2),
            }
        )
    missing = pd.DataFrame(rows).sort_values(
        by=["train_missing_pct", "test_missing_pct"],
        ascending=False,
    )
    return missing


def build_numeric_correlations(train: pd.DataFrame) -> pd.DataFrame:
    numeric = train.select_dtypes(include=np.number).drop(columns=[ID_COL], errors="ignore")
    corr = numeric.corr(numeric_only=True)[TARGET].drop(labels=[TARGET]).sort_values(key=np.abs, ascending=False)
    return corr.rename("correlation").reset_index().rename(columns={"index": "feature"})


def build_categorical_summary(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | int | str]] = []
    categorical_cols = train.select_dtypes(exclude=np.number).columns.tolist()
    for column in categorical_cols:
        train_counts = train[column].fillna("__MISSING__").value_counts(normalize=True)
        top_value = str(train_counts.index[0])
        rows.append(
            {
                "feature": column,
                "train_unique": int(train[column].nunique(dropna=True)),
                "test_unique": int(test[column].nunique(dropna=True)),
                "train_missing_pct": round(float(train[column].isna().mean() * 100), 2),
                "test_missing_pct": round(float(test[column].isna().mean() * 100), 2),
                "top_train_value": top_value,
                "top_train_share_pct": round(float(train_counts.iloc[0] * 100), 2),
            }
        )
    summary = pd.DataFrame(rows).sort_values(
        by=["train_unique", "train_missing_pct"],
        ascending=[False, False],
    )
    return summary


def build_numeric_shift_summary(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | str]] = []
    numeric_cols = [col for col in train.select_dtypes(include=np.number).columns if col != TARGET]
    for column in numeric_cols:
        train_series = train[column].dropna()
        test_series = test[column].dropna()
        ks_stat, p_value = ks_2samp(train_series, test_series)
        rows.append(
            {
                "feature": column,
                "train_mean": round(float(train_series.mean()), 4),
                "test_mean": round(float(test_series.mean()), 4),
                "train_std": round(float(train_series.std()), 4),
                "test_std": round(float(test_series.std()), 4),
                "ks_stat": round(float(ks_stat), 4),
                "p_value": round(float(p_value), 6),
            }
        )
    return pd.DataFrame(rows).sort_values(by="ks_stat", ascending=False)


def build_categorical_shift_summary(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | int | str]] = []
    categorical_cols = train.select_dtypes(exclude=np.number).columns.tolist()
    for column in categorical_cols:
        train_dist = train[column].fillna("__MISSING__").value_counts(normalize=True)
        test_dist = test[column].fillna("__MISSING__").value_counts(normalize=True)
        all_levels = train_dist.index.union(test_dist.index)
        train_aligned = train_dist.reindex(all_levels, fill_value=0.0)
        test_aligned = test_dist.reindex(all_levels, fill_value=0.0)
        tv_distance = 0.5 * np.abs(train_aligned - test_aligned).sum()
        rows.append(
            {
                "feature": column,
                "train_levels": int(train[column].nunique(dropna=True)),
                "test_levels": int(test[column].nunique(dropna=True)),
                "tv_distance": round(float(tv_distance), 4),
                "top_train_level": str(train_aligned.idxmax()),
                "top_test_level": str(test_aligned.idxmax()),
            }
        )
    return pd.DataFrame(rows).sort_values(by="tv_distance", ascending=False)


def build_outlier_summary(train: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float | int | str]] = []
    for column in ["SalePrice", "GrLivArea", "LotArea", "TotalBsmtSF", "GarageArea"]:
        series = train[column].dropna()
        q1 = float(series.quantile(0.25))
        q3 = float(series.quantile(0.75))
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        mask = (train[column] < lower) | (train[column] > upper)
        rows.append(
            {
                "feature": column,
                "q1": round(q1, 4),
                "q3": round(q3, 4),
                "iqr": round(iqr, 4),
                "lower_bound": round(lower, 4),
                "upper_bound": round(upper, 4),
                "outlier_count": int(mask.sum()),
                "outlier_pct": round(float(mask.mean() * 100), 2),
            }
        )

    special_mask = (train["GrLivArea"] > 4000) & (train["SalePrice"] < 300000)
    rows.append(
        {
            "feature": "GrLivArea_gt_4000_and_SalePrice_lt_300000",
            "q1": np.nan,
            "q3": np.nan,
            "iqr": np.nan,
            "lower_bound": np.nan,
            "upper_bound": np.nan,
            "outlier_count": int(special_mask.sum()),
            "outlier_pct": round(float(special_mask.mean() * 100), 2),
        }
    )
    return pd.DataFrame(rows)


def save_dataframe(df: pd.DataFrame, name: str) -> None:
    df.to_csv(LOG_DIR / f"{name}.csv", index=False)


def plot_target_distribution(train: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(train[TARGET], kde=True, ax=axes[0], color="#1f77b4")
    axes[0].set_title("SalePrice distribution")
    axes[0].set_xlabel("SalePrice")

    sns.histplot(np.log1p(train[TARGET]), kde=True, ax=axes[1], color="#ff7f0e")
    axes[1].set_title("log1p(SalePrice) distribution")
    axes[1].set_xlabel("log1p(SalePrice)")

    fig.tight_layout()
    fig.savefig(LOG_DIR / "target_distribution.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_missing_summary(missing_summary: pd.DataFrame) -> None:
    top_missing = missing_summary.head(15).copy()
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(top_missing))
    width = 0.4
    ax.bar(x - width / 2, top_missing["train_missing_pct"], width=width, label="train", color="#4c78a8")
    ax.bar(x + width / 2, top_missing["test_missing_pct"], width=width, label="test", color="#f58518")
    ax.set_xticks(x)
    ax.set_xticklabels(top_missing["column"], rotation=70, ha="right")
    ax.set_ylabel("Missing %")
    ax.set_title("Top missing columns")
    ax.legend()
    fig.tight_layout()
    fig.savefig(LOG_DIR / "missing_summary.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_numeric_correlations(correlations: pd.DataFrame) -> None:
    top_corr = correlations.head(15).copy().iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(top_corr["feature"], top_corr["correlation"], color="#54a24b")
    ax.set_title("Top absolute correlations with SalePrice")
    ax.set_xlabel("Correlation")
    fig.tight_layout()
    fig.savefig(LOG_DIR / "numeric_correlations.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_top_numeric_scatter(train: pd.DataFrame, correlations: pd.DataFrame) -> None:
    top_features = correlations.head(6)["feature"].tolist()
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    for ax, feature in zip(axes.flat, top_features, strict=False):
        sns.scatterplot(data=train, x=feature, y=TARGET, alpha=0.5, s=18, ax=ax)
        ax.set_title(feature)
    fig.tight_layout()
    fig.savefig(LOG_DIR / "top_numeric_scatter.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_categorical_boxplots(train: pd.DataFrame) -> None:
    features = ["Neighborhood", "KitchenQual", "ExterQual", "BsmtQual", "GarageFinish", "MSZoning"]
    fig, axes = plt.subplots(3, 2, figsize=(16, 16))
    for ax, feature in zip(axes.flat, features, strict=False):
        top_levels = train[feature].fillna("__MISSING__").value_counts().head(8).index
        subset = train[train[feature].fillna("__MISSING__").isin(top_levels)].copy()
        subset[feature] = subset[feature].fillna("__MISSING__")
        sns.boxplot(data=subset, x=feature, y=TARGET, ax=ax, order=list(top_levels))
        ax.set_title(feature)
        ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(LOG_DIR / "categorical_boxplots.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_shift_summaries(numeric_shift: pd.DataFrame, categorical_shift: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    top_numeric = numeric_shift.head(12).copy().iloc[::-1]
    axes[0].barh(top_numeric["feature"], top_numeric["ks_stat"], color="#e45756")
    axes[0].set_title("Top numeric train/test shifts")
    axes[0].set_xlabel("KS statistic")

    top_categorical = categorical_shift.head(12).copy().iloc[::-1]
    axes[1].barh(top_categorical["feature"], top_categorical["tv_distance"], color="#72b7b2")
    axes[1].set_title("Top categorical train/test shifts")
    axes[1].set_xlabel("TV distance")

    fig.tight_layout()
    fig.savefig(LOG_DIR / "train_test_shift.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def write_summary_markdown(
    overview: pd.DataFrame,
    missing: pd.DataFrame,
    correlations: pd.DataFrame,
    numeric_shift: pd.DataFrame,
    categorical_shift: pd.DataFrame,
    outliers: pd.DataFrame,
) -> None:
    def as_code_block(df: pd.DataFrame) -> str:
        return "```\n" + df.to_string(index=False) + "\n```"

    overview_map = dict(zip(overview["metric"], overview["value"], strict=False))
    high_missing = missing.query("train_missing_pct >= 40")[["column", "train_missing_pct", "test_missing_pct"]].head(8)
    top_corr = correlations.head(8)
    top_num_shift = numeric_shift.head(8)[["feature", "ks_stat", "train_mean", "test_mean"]]
    top_cat_shift = categorical_shift.head(8)[["feature", "tv_distance", "top_train_level", "top_test_level"]]
    outlier_focus = outliers[["feature", "outlier_count", "outlier_pct"]]

    lines = [
        "# exp001 EDA Summary",
        "",
        "## Overview",
        "",
        f"- Train shape: {int(overview_map['train_rows'])} rows x {int(overview_map['train_columns'])} columns",
        f"- Test shape: {int(overview_map['test_rows'])} rows x {int(overview_map['test_columns'])} columns",
        f"- Numeric columns: {int(overview_map['numeric_columns'])}",
        f"- Categorical columns: {int(overview_map['categorical_columns'])}",
        f"- SalePrice skew: {overview_map['target_skew']}",
        f"- log1p(SalePrice) skew: {overview_map['target_log_skew']}",
        "",
        "## High missing columns",
        "",
        as_code_block(high_missing),
        "",
        "## Top numeric correlations with SalePrice",
        "",
        as_code_block(top_corr),
        "",
        "## Strong train/test numeric shifts",
        "",
        as_code_block(top_num_shift),
        "",
        "## Strong train/test categorical shifts",
        "",
        as_code_block(top_cat_shift),
        "",
        "## Outlier summary",
        "",
        as_code_block(outlier_focus),
        "",
        "## Initial implications",
        "",
        "- `SalePrice` is strongly right-skewed, and `log1p` largely stabilizes the target distribution.",
        "- Several columns have structural missingness (`PoolQC`, `MiscFeature`, `Alley`, `Fence`, `FireplaceQu`), so missingness itself may be informative.",
        "- `OverallQual`, `GrLivArea`, `GarageCars`, `GarageArea`, `TotalBsmtSF`, and `1stFlrSF` are strong starting points for the first baseline.",
        "- Some features show train/test distribution gaps, so aggressive hand-tuned thresholds should be treated carefully.",
        "- A small number of very large houses look like outlier candidates and should be tracked explicitly before model comparison.",
        "",
    ]
    (LOG_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def build_notebook() -> None:
    cells = [
        nbf.v4.new_markdown_cell(
            "# exp001 - Broad EDA for House Prices\n\n"
            "この Notebook は `src/run_exp001_eda.py` の生成物です。"
            "主な集計結果は `logs/exp001/` に保存されています。"
        ),
        nbf.v4.new_code_cell(
            "from pathlib import Path\n"
            "import pandas as pd\n"
            "import numpy as np\n\n"
            "ROOT = Path('..').resolve()\n"
            "DATA_DIR = ROOT / 'data'\n"
            "LOG_DIR = ROOT / 'logs' / 'exp001'\n\n"
            "train = pd.read_csv(DATA_DIR / 'train.csv')\n"
            "test = pd.read_csv(DATA_DIR / 'test.csv')\n"
            "train.shape, test.shape"
        ),
        nbf.v4.new_markdown_cell(
            "## Saved summary tables\n\n"
            "- `overview.csv`\n"
            "- `missing_summary.csv`\n"
            "- `numeric_correlations.csv`\n"
            "- `categorical_summary.csv`\n"
            "- `numeric_shift_summary.csv`\n"
            "- `categorical_shift_summary.csv`\n"
            "- `outlier_summary.csv`\n"
        ),
        nbf.v4.new_code_cell(
            "pd.read_csv(LOG_DIR / 'overview.csv')"
        ),
        nbf.v4.new_code_cell(
            "pd.read_csv(LOG_DIR / 'missing_summary.csv').head(15)"
        ),
        nbf.v4.new_code_cell(
            "pd.read_csv(LOG_DIR / 'numeric_correlations.csv').head(15)"
        ),
        nbf.v4.new_code_cell(
            "pd.read_csv(LOG_DIR / 'numeric_shift_summary.csv').head(12)"
        ),
        nbf.v4.new_code_cell(
            "pd.read_csv(LOG_DIR / 'categorical_shift_summary.csv').head(12)"
        ),
        nbf.v4.new_markdown_cell(
            "## Saved figures\n\n"
            "### Target distribution\n"
            "![target_distribution](../logs/exp001/target_distribution.png)\n\n"
            "### Missing summary\n"
            "![missing_summary](../logs/exp001/missing_summary.png)\n\n"
            "### Numeric correlations\n"
            "![numeric_correlations](../logs/exp001/numeric_correlations.png)\n\n"
            "### Top numeric scatter\n"
            "![top_numeric_scatter](../logs/exp001/top_numeric_scatter.png)\n\n"
            "### Categorical boxplots\n"
            "![categorical_boxplots](../logs/exp001/categorical_boxplots.png)\n\n"
            "### Train/Test shift summary\n"
            "![train_test_shift](../logs/exp001/train_test_shift.png)\n"
        ),
        nbf.v4.new_markdown_cell(
            "## Notes\n\n"
            "- この段階ではモデル学習は行わず、広めの EDA に集中する。\n"
            "- 次の `exp002` 以降で、ここで見えた欠損処理・対数変換・強相関特徴を baseline に落とし込む。"
        ),
    ]
    notebook = nbf.v4.new_notebook(cells=cells)
    nbf.write(notebook, NOTEBOOK_PATH)


def main() -> None:
    ensure_dirs()
    train, test = load_data()

    overview = build_overview(train, test)
    missing = build_missing_summary(train, test)
    correlations = build_numeric_correlations(train)
    categorical = build_categorical_summary(train, test)
    numeric_shift = build_numeric_shift_summary(train, test)
    categorical_shift = build_categorical_shift_summary(train, test)
    outliers = build_outlier_summary(train)

    save_dataframe(overview, "overview")
    save_dataframe(missing, "missing_summary")
    save_dataframe(correlations, "numeric_correlations")
    save_dataframe(categorical, "categorical_summary")
    save_dataframe(numeric_shift, "numeric_shift_summary")
    save_dataframe(categorical_shift, "categorical_shift_summary")
    save_dataframe(outliers, "outlier_summary")

    sns.set_theme(style="whitegrid")
    plot_target_distribution(train)
    plot_missing_summary(missing)
    plot_numeric_correlations(correlations)
    plot_top_numeric_scatter(train, correlations)
    plot_categorical_boxplots(train)
    plot_shift_summaries(numeric_shift, categorical_shift)
    write_summary_markdown(overview, missing, correlations, numeric_shift, categorical_shift, outliers)
    build_notebook()


if __name__ == "__main__":
    main()
