# Child Agent Behavior

## Role

子エージェントは、割り当てられた 1 つの仮説を検証する実験担当として振る舞う。  
自分で baseline を変えたり、正式コードを更新したりしない。

## Must Read First

1. `AGENTS.md`
2. `competitions/<competition_name>/STATUS.md`
3. 親から渡された担当 experiment id と仮説

## Responsibilities

- 割り当てられた `expXXX` の notebook を作成または更新する
- notebook を実行して CV を確認する
- 必要なら submission CSV を生成する
- `experiments/expXXX.md` を記録する
- 結果を親へ返す

## Start Checklist

1. `AGENTS.md` と `STATUS.md` を読む
2. 自分の owner 名、experiment id、仮説、write scope が `STATUS.md` にあることを確認する
3. baseline と比較対象を確認する
4. 割り当て範囲外のファイルを触らないことを確認する

## Must Not Do

- baseline を自分の判断で変更しない
- 自分で新しい experiment id を採番しない
- 他の子の experiment id を使わない
- `src/features.py`, `src/train.py`, `src/predict.py` を更新しない
- 曖昧な複数仮説を同時に混ぜない
- 割り当てられていない notebook や log を触らない
- `STATUS.md` の baseline、`Next available experiment id`、他の assignment を更新しない

## Write Scope

- 書き込み対象は原則として次に限定する:
- `notebooks/expXXX_*.ipynb`
- `experiments/expXXX.md`
- `submissions/expXXX_*.csv`

## Handoff To Parent

- 実験完了後は、結果サマリを親に返してから次の実験に進む
- `experiments/index.md` と `STATUS.md` の最終整合は親が担当する

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
