# house_prices

Kaggle competition: House Prices - Advanced Regression Techniques

## Current State

- `exp001`: Codex-generated broad EDA is done.
- `exp002`: reserved for user-written EDA before baseline modeling.
- Baseline modeling has not started yet.

## Working Policy

- EDA is the user's main learning and hypothesis-generation process.
- In `exp002`, the user writes the exploratory code and investigates the data until the behavior of the target, important features, missing values, categories, train/test shift, and outliers feels understandable.
- Codex can help as a reviewer, discussion partner, or notebook-debugging assistant during EDA.
- After `exp002`, baseline creation and repeated one-change-at-a-time hypothesis validation can be standardized with Codex.

## Setup

```powershell
cd C:\Users\21td031\dev\kaggle
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Documents

- Shared status: `STATUS.md`
- Experiment index: `experiments/index.md`
- Current EDA plan: `experiments/exp002.md`
- Task list: `TODO.md`
