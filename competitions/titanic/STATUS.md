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

- Next available experiment id: `exp015`
- Reservation rule:
  - 親エージェントが実験を始める前に、この欄で番号を予約する
  - 1 つの実験番号を複数の Codex で共有しない
  - notebook, submission, experiment log は同じ実験番号でそろえる
  - 子エージェントは自分で experiment id を採番しない

## Parent Workflow

1. 親が `Current Baseline` と `Next available experiment id` を確認する
2. 親が `Active Assignments` に owner、仮説、write scope、status を記入する
3. 親が `Next available experiment id` を次の未使用番号へ進める
4. 子は `Active Assignments` の割り当てを確認してから着手する
5. 子は notebook、submission、experiment log を更新し、結果を親へ返す
6. 親が `STATUS.md`、`experiments/index.md`、必要なら `src/` を更新する

## Active Assignments

- None

### Assignment Template

- Owner: `Codex-A`
  - Reserved experiment: `exp010`
  - Hypothesis: `add AgeBand on top of exp007`
  - Write scope: `notebooks/exp010_ageband.ipynb`, `experiments/exp010.md`, `submissions/exp010_ageband.csv`
  - Status: `reserved`

- Owner: `Codex-B`
  - Reserved experiment: `exp011`
  - Hypothesis: `add TicketGroupSize on top of exp007`
  - Write scope: `notebooks/exp011_ticketgroupsize.ipynb`, `experiments/exp011.md`, `submissions/exp011_ticketgroupsize.csv`
  - Status: `reserved`

### Status Labels

- `reserved`: 親が予約し、まだ子が実行を始めていない
- `running`: 子が実験中
- `done`: 子が notebook と experiment log を更新し、親への返却待ちまたは返却済み
- `closed`: 親が結果を回収し、台帳反映まで完了した

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

- `exp008` は `FareBand` を `Title + FamilyGroup` に追加したが、CV `0.82827` で baseline を更新しなかった
- `exp009` は `FareBand` を `exp007` に追加したが、CV `0.83275` で baseline を更新しなかった
- `exp010` は `AgeBand` を `exp007` に追加したが、CV `0.83053` で baseline を更新しなかった
- `exp011` は `TicketGroupSize` を `exp007` に追加したが、CV `0.83501` で baseline を更新しなかった
- `exp012` は `RandomForest` へ置き換えたが、CV `0.80808` で baseline を大きく下回った
- `exp013` は `CatBoost` へ置き換え、CV `0.83839` で `exp007` をわずかに上回ったが、LB `0.75598` で悪化した
- `exp014` で `exp007` と `exp013` を複数 seed と holdout で見直した結果、`exp013` の優位は安定しなかった
- 現在の正式な比較基準は引き続き `exp007`
- 次の候補は、`exp007` を一区切りとするか、別モデル比較をやるなら複数 seed 前提で再設計すること
