# 実験一覧

| Experiment | 内容 | Status | 結論 |
|---|---|---|---|
| `exp001` | CABT起動・ランダムAI自己対戦 | complete | 100試合完走、エラー0件。代表実行ではagent0 56勝、agent1 44勝、引き分け0。成果物: `experiments/exp001/` |
| `exp002` | 攻撃優先・終了回避ヒューリスティック | complete | 4条件×100試合を完走。heuristicのrandom対戦勝率は席順合算で4%（8/200）、exp001をbaselineとして維持。成果物: `experiments/exp002/` |
| `exp003` | エネルギー付与優先ヒューリスティック | complete | random対戦は席順合算で18%（36/200）。exp002を大幅に上回ったが、exp001をbaselineとして維持。成果物: `experiments/exp003/` |
| `exp004` | 選択個数ランダム化 | complete | count-randomはmax-count randomに対して席順合算71/200勝（35.5%）。全400試合でエラー0件、baselineはexp001のまま維持。成果物: `experiments/exp004/` |
| `exp005` | 攻撃・番終了前に可能な行動を使い切る | complete | 準備行動を優先する方針はrandomに席順合算174/200勝（87%）。全400試合でエラー0件。exp005を新baselineに昇格。成果物: `experiments/exp005/` |
