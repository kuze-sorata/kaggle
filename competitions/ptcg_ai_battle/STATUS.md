# PTCG AI Battle Challenge Status

このファイルは、コンペ作業の現在地、実験番号、担当範囲を共有するためのハブです。

## Current Baseline

- Baseline experiment: `exp005`
- Baseline deck: `experiments/exp005/decks/exp005_deck.csv`
- Local evaluation: `completed (400 matches, 0 errors; exp005 beat random in 174/200 seat-balanced matches)`
- Kaggle submission: `not started`

## Current Direction

- 合法手を安定して返し、準備行動を攻撃より先に行うexp005 baselineを実装済み。
- 固定デッキで自己対戦と複数ベースライン対戦を同一条件で比較する。
- exp002〜exp004の単純な行動優先・選択個数変更は、exp001 random baselineを下回った。
- exp005は攻撃前に準備行動を使い切る方針で、random相手に席順合算87%（174/200）を記録し、新baselineに昇格した。
- 次はデッキ候補や行動評価を追加し、exp005を基準に比較する。

## Experiment ID Reservation

- Next available experiment id: `exp006`
- Reserved: none

## Active Assignments

- Owner: `User`
  - Reserved experiment: none
  - Status: `exp005 completed; baseline promoted to exp005; next work starts at exp006`

## Workflow

1. 実験開始前にこのファイルで `expXXX` を予約する。
2. Notebook、提出物、実験ログは同じ実験番号で管理する。
3. 実験結果は `experiments/expXXX.md` に短く事実ベースで記録する。
4. 実験固有のAIコード、デッキ、観測スキーマ、生成物は
   `experiments/expXXX/` に保存する。
5. ベースラインの昇格とこのファイルの更新は親エージェントが担当する。
