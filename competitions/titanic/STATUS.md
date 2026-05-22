# Titanic Parallel Run Status

## Purpose

このファイルは、複数の Codex やサブエージェントで並列に仮説検証するときの共有ハブとして使う。  
会話ではなく、このファイルを最新の作業前提として扱う。

## Current Baseline

- Baseline experiment: `exp007`
- Baseline feature set: `Title`, `FamilyGroup`, `SexPclass`
- Baseline CV: `0.83614`
- Baseline LB: `0.77511`
- Baseline status: `official current baseline`

## Experiment ID Reservation

- Next available experiment id: `exp009`
- Reservation rule:
  - 実験を始める前に、この欄で番号を予約する
  - 1 つの実験番号を複数の Codex で共有しない
  - notebook, submission, experiment log は同じ実験番号でそろえる

## Active Assignments

- Owner: `Codex-A`
  - Reserved experiment: `exp009`
  - Hypothesis: `TBD`
  - Write scope: `notebooks/exp009_*.ipynb`, `experiments/exp009.md`, `submissions/exp009_*.csv`
  - Status: `open`

- Owner: `Codex-B`
  - Reserved experiment: `exp010`
  - Hypothesis: `TBD`
  - Write scope: `notebooks/exp010_*.ipynb`, `experiments/exp010.md`, `submissions/exp010_*.csv`
  - Status: `open`

## Decision Rules

- 各 Codex は、原則として notebook と experiment log までを担当する
- `src/features.py`, `src/train.py`, `src/predict.py` の正式更新は親担当だけが行う
- 新しい仮説は、現在の baseline に対して 1 変更だけ加えて比較する
- 採用判断は CV を主とし、LB は補助として扱う
- 実験完了後は `experiments/index.md` を更新してから次に進む

## Handoff Format

- Result summary:
  - Experiment: `expXXX`
  - Hypothesis: `...`
  - CV mean/std: `...`
  - LB: `...` or `TBD`
  - Decision: `adopt` / `hold` / `reject`
  - Notes: `...`

## Current Notes

- `exp008` は `FareBand` を検証したが、CV `0.82827` で baseline を更新しなかった
- 現在の正式な比較基準は引き続き `exp007`
- 次の候補は `AgeBand`, `TicketGroupSize` など、`exp007` に別情報を足す仮説
