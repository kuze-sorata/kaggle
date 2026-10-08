# PTCG AI Battle Challenge Status

このファイルは、コンペ作業の現在地、実験番号、担当範囲を共有するためのハブです。

## Current Baseline

- Baseline experiment: `TBD`
- Baseline deck: `TBD`
- Local evaluation: `not started`
- Kaggle submission: `not started`

## Current Direction

- まずは合法手を安定して返せる最小エージェントを実装する。
- 固定デッキで自己対戦と複数ベースライン対戦を再現可能にする。
- その後、ヒューリスティック、探索、相手の不完全情報推定を順に比較する。

## Experiment ID Reservation

- Next available experiment id: `exp001`
- Reserved: none

## Active Assignments

- Owner: `User`
  - Reserved experiment: none
  - Status: `not started`

## Workflow

1. 実験開始前にこのファイルで `expXXX` を予約する。
2. Notebook、提出物、実験ログは同じ実験番号で管理する。
3. 実験結果は `experiments/expXXX.md` に短く事実ベースで記録する。
4. ベースラインの昇格とこのファイルの更新は親エージェントが担当する。
