# PTCG AI Battle Challenge Status

このファイルは、コンペ作業の現在地、実験番号、担当範囲を共有するためのハブです。

## Current Baseline

- Baseline experiment: `exp001`
- Baseline deck: `decks/exp001_deck.csv`
- Local evaluation: `completed (100 random-vs-random matches, 0 errors)`
- Kaggle submission: `not started`

## Current Direction

- 合法手を安定して返せるランダムベースラインを実装済み。
- 固定デッキで自己対戦と複数ベースライン対戦を同一条件で比較する。
- その後、ヒューリスティック、探索、相手の不完全情報推定を順に比較する。

## Experiment ID Reservation

- Next available experiment id: `exp002`
- Reserved: none

## Active Assignments

- Owner: `User`
  - Reserved experiment: none
  - Status: `exp001 completed; next work starts at exp002`

## Workflow

1. 実験開始前にこのファイルで `expXXX` を予約する。
2. Notebook、提出物、実験ログは同じ実験番号で管理する。
3. 実験結果は `experiments/expXXX.md` に短く事実ベースで記録する。
4. ベースラインの昇格とこのファイルの更新は親エージェントが担当する。
