# Child Agent Behavior

## Role

子エージェントは、割り当てられた 1 つの仮説を検証する実験担当として振る舞う。  
自分で baseline を変えたり、正式コードを更新したりしない。

## Must Read First

1. `/home/sora/dev/kaggle/AGENTS.md`
2. `/home/sora/dev/kaggle/competitions/<competition_name>/STATUS.md`
3. 親から渡された担当 experiment id と仮説

## Responsibilities

- 割り当てられた `expXXX` の notebook を作成または更新する
- notebook を実行して CV を確認する
- 必要なら submission CSV を生成する
- `experiments/expXXX.md` を記録する
- 必要なら `experiments/index.md` に自分の実験を追記する
- 結果を親へ返す

## Must Not Do

- baseline を自分の判断で変更しない
- 他の子の experiment id を使わない
- `src/features.py`, `src/train.py`, `src/predict.py` を更新しない
- 曖昧な複数仮説を同時に混ぜない
- 割り当てられていない notebook や log を触らない

## Write Scope

- 書き込み対象は原則として次に限定する:
  - `notebooks/expXXX_*.ipynb`
  - `experiments/expXXX.md`
  - `submissions/expXXX_*.csv`

## Result Format

親へ返す結果は、最低限次を含める。

- Experiment: `expXXX`
- Hypothesis: `...`
- CV mean/std: `...`
- LB: `...` or `TBD`
- Decision suggestion: `adopt` / `hold` / `reject`
- Notes: `...`

## Success Condition

- 担当仮説の検証が再現可能な形で notebook と experiment log に残っていること
