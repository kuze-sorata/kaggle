# Parent Agent Behavior

## Role

親エージェントは、並列実験の司令塔として振る舞う。  
自分で全部実装するのではなく、状態管理、分担、統合、採用判断を主に担当する。

## Must Read First

1. `AGENTS.md`
2. `competitions/<competition_name>/STATUS.md`
3. 必要なら `experiments/index.md`

## Responsibilities

- 現在の baseline を確認して固定する
- 次に使う実験番号を予約する
- 子エージェントごとに担当仮説と write scope を分ける
- 同じ `expXXX` を複数の子に割り当てない
- 子の結果を回収して比較する
- 採用判断を行う
- 採用した変更だけを `src/features.py`, `src/train.py`, `src/predict.py` に反映する
- `STATUS.md` の baseline と予約情報を更新する

## Reservation Workflow

1. `STATUS.md` の baseline、`Next available experiment id`、`Active Assignments` を確認する
2. 新しい仮説ごとに連番の experiment id を予約する
3. `Active Assignments` に owner、仮説、write scope、status を書く
4. `Next available experiment id` を次の未使用番号へ進める
5. その内容を前提として子エージェントへ指示を渡す
6. 子の完了後、結果を `STATUS.md` に反映し、assignment を closed にするか削除する
7. 採用仮説があれば baseline を更新し、正式コードへ反映する

## Default Work Split

- 親が触るもの:
  - `competitions/<competition_name>/STATUS.md`
  - `competitions/<competition_name>/src/features.py`
  - `competitions/<competition_name>/src/train.py`
  - `competitions/<competition_name>/src/predict.py`
  - 最終的な `experiments/index.md` の整合確認

- 子が触るもの:
  - `notebooks/expXXX_*.ipynb`
  - `experiments/expXXX.md`
  - `submissions/expXXX_*.csv`

## Rules

- 新しい仮説は、現在の baseline に対して 1 変更だけ加えて比較させる
- 子に曖昧な依頼をしない
- 子ごとに experiment id、仮説、write scope を明示する
- 親が `STATUS.md` を更新する前に子へ新しい experiment id を口頭だけで渡さない
- 同じ仮説を複数の子に渡す場合も、experiment id は必ず分ける
- 子が同じ正式コードを触らないようにする
- 実験の詳細実装を子に任せても、採用判断と正式反映は親が引き取る

## Child Prompt Requirements

子に渡す指示には、最低限次を含めること。

- 現在の baseline
- 担当する experiment id
- 仮説名
- 書き込み可能なファイル範囲
- `STATUS.md` 上の assignment owner 名
- `src/` を触らないこと
- 先に `AGENTS.md` と `STATUS.md` を読むこと

## Success Condition

- 並列で複数仮説を試しても、baseline、実験番号、正式コード更新責任が一意に保たれていること
