# PTCG AI Battle Challenge Status

このファイルは、コンペ作業の現在地、実験番号、担当範囲を共有するためのハブです。

## Current Baseline

- Baseline experiment: `exp001`
- Baseline deck: `experiments/exp001/decks/exp001_deck.csv`
- Local evaluation: `completed (100 random-vs-random matches, 0 errors)`
- Kaggle submission: `not started`

## Current Direction

- 合法手を安定して返せるランダムベースラインを実装済み。
- 固定デッキで自己対戦と複数ベースライン対戦を同一条件で比較する。
- exp002の攻撃優先・終了回避ヒューリスティックは評価済みだが、baselineを下回った。
- exp003のエネルギー付与優先はexp002を上回ったが、random baselineには届かなかった。
- exp004の選択個数ランダム化はmax-count randomに対して席順合算35.5%（71/200）で、baselineを下回った。
- 次は付与先・攻撃対象・カード効果を考慮した行動評価を比較する。

## Experiment ID Reservation

- Next available experiment id: `exp005`
- Reserved: none

## Active Assignments

- Owner: `User`
  - Reserved experiment: none
  - Status: `exp004 completed; baseline remains exp001; next work starts at exp005`

## Workflow

1. 実験開始前にこのファイルで `expXXX` を予約する。
2. Notebook、提出物、実験ログは同じ実験番号で管理する。
3. 実験結果は `experiments/expXXX.md` に短く事実ベースで記録する。
4. 実験固有のAIコード、デッキ、観測スキーマ、生成物は
   `experiments/expXXX/` に保存する。
5. ベースラインの昇格とこのファイルの更新は親エージェントが担当する。
