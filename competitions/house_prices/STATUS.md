# house_prices Parallel Run Status

## Purpose

このファイルは、複数の Codex やサブエージェントで並列に作業するときの共有ハブです。
会話履歴ではなく、このファイルを最新の作業前提として扱います。

## Current Baseline

- Baseline experiment: `TBD`
- Baseline feature set: `TBD`
- Baseline CV: `TBD`
- Baseline LB: `TBD`
- Baseline status: `not started`

## Current Direction

- `exp001` では Codex 生成の broad EDA を実施済み。
- ただし、EDA はデータ理解と仮説生成の土台になるため、以後の正式な仮説検証に入る前に、ユーザー自身がコードを書いて納得いくまで探索する。
- `exp002` は「自分で手を動かす EDA」として扱う。
- baseline 作成、特徴量追加、CV 比較、提出ファイル作成などの定型プロセスは、`exp002` の後に Codex で定型化してよい。

## Experiment ID Reservation

- Next available experiment id: `exp003`
- Reserved:
  - `exp001`: Codex-generated broad EDA, done.
  - `exp002`: user-written deep EDA, reserved / in progress.

## Active Assignments

- Owner: `User`
  - Reserved experiment: `exp002`
  - Hypothesis: `EDA should be written manually to deepen data understanding before baseline modeling.`
  - Write scope: `notebooks/exp002.ipynb`, `experiments/exp002.md`, optional `logs/exp002/`
  - Status: `reserved`

## Parent Workflow

1. 作業開始前に `Current Baseline` と `Experiment ID Reservation` を確認する。
2. 新しい実験は親エージェントが `Active Assignments` に予約してから始める。
3. notebook、submission、experiment log は同じ実験番号でそろえる。
4. 子エージェントは割り当てられた実験番号だけを使う。
5. 実験完了後、親エージェントが `STATUS.md` と `experiments/index.md` を更新する。

## Decision Rules

- 各 Codex は原則として notebook と experiment log までを担当する。
- `src/` の正式更新は担当を 1 つに決めてから行う。
- 新しい仮説は、現在の baseline に対して 1 変更ずつ比較する。
- 採用判断は CV を主とし、LB は補助として扱う。
- EDA から出た観察は、後続の仮説として `experiments/expXXX.md` または `TODO.md` に残す。

## Handoff Format

- Result summary:
  - Experiment: `expXXX`
  - Hypothesis: `...`
  - CV mean/std: `...`
  - LB: `...` or `TBD`
  - Decision: `adopt` / `hold` / `reject`
  - Notes: `...`

## Current Notes

- `exp001` で broad EDA は完了済み。
- `SalePrice` は強い右歪みがあり、`log1p(SalePrice)` が baseline の自然な候補。
- 強い相関を持つ特徴量は `OverallQual`, `GrLivArea`, `GarageCars`, `GarageArea`, `TotalBsmtSF`, `1stFlrSF` など。
- 高欠損列は、単純欠損ではなく構造的な情報を持つ可能性がある。
- `GrLivArea > 4000` かつ `SalePrice < 300000` の典型的な外れ値候補が 2 件ある。
- 次の優先作業は `exp002` で、ユーザー自身が EDA を書いてデータ理解を深めること。
