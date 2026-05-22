# titanic

## 位置づけ

このディレクトリは `Titanic` コンペ固有の実装と実験履歴を置く場所です。進め方そのものは [docs/kaggle_workflow.md](/home/sora/dev/kaggle/docs/kaggle_workflow.md) を参照し、Codex への依頼方法は [docs/codex_collaboration.md](/home/sora/dev/kaggle/docs/codex_collaboration.md) を参照します。

## 使い方

1. Kaggle から `train.csv` と `test.csv` を `data/` に置く
2. `python src/train.py` で学習する
3. `python src/predict.py` で提出ファイルを作る
4. 実験は `docs/experiment_log_template.md` の書式に沿って `experiments/index.md` と `experiments/expXXX.md` に残す
5. やることは `TODO.md` に残す

## 実験管理

- `experiments/index.md` は全実験の一覧
- `experiments/expXXX.md` は各実験の詳細ログ
- `notebooks/` は探索・EDA・仮説検証用
- `src/` は正式採用した再利用可能コード
- `submissions/` は提出ファイル
- `models/` は学習済みモデル
- `data/` は Git 管理しない
