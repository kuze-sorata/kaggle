# 表形式ベースラインテンプレート

表形式データの Kaggle コンペを始めるときの標準テンプレートです。

## 構成

- `data/`: ローカルのコンペデータ
- `notebooks/`: 探索や簡単な確認
- `src/`: 学習と推論のコード
- `models/`: 学習済み成果物の保存先
- `submissions/`: 生成した提出ファイル
- `logs/`: 実行ログ
- `experiments/`: 実験一覧と詳細ログ
- `TODO.md`: やること一覧

## 進め方

1. `data/` にコンペデータを置く
2. `src/config.py` でデータセット固有の設定を調整する
3. `src/train.py` で学習を実行する
4. `src/predict.py` で提出ファイルを作る
5. `experiments/index.md` と `experiments/expXXX.md` に結果を残す
6. `TODO.md` に残タスクを書く

