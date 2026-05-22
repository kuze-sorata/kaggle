# 表形式ベースラインテンプレート

表形式データの Kaggle コンペを始めるときの標準テンプレートです。

## 構成

- `data/`: ローカルのコンペデータ
- `notebooks/`: 探索や簡単な確認
- `src/`: 学習と推論のコード
- `models/`: 学習済み成果物の保存先
- `submissions/`: 生成した提出ファイル
- `logs/`: 実行ログ
- `notes/`: コンペ固有のラフメモ
- `experiments/`: コンペ固有の実験まとめ
- `docs/`: コンペ固有の安定した参照資料

## 進め方

1. `data/` にコンペデータを置く
2. `src/config.py` でデータセット固有の設定を調整する
3. `src/train.py` で学習を実行する
4. `src/predict.py` で提出ファイルを作る
5. 結果は `experiment_log.md` に残す
