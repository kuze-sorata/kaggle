# titanic

## 位置づけ

このディレクトリは `Titanic` コンペ固有の実装と実験履歴を置く場所です。進め方そのものは [docs/kaggle_workflow.md](/home/sora/dev/kaggle/docs/kaggle_workflow.md) を参照し、Codex への依頼方法は [docs/codex_collaboration.md](/home/sora/dev/kaggle/docs/codex_collaboration.md) を参照します。

問題設定の整理は [problem_understanding.md](/home/sora/dev/kaggle/competitions/titanic/problem_understanding.md) を起点にします。

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
- 並列で実験を進める場合は、最初に `STATUS.md` を見て現在の baseline、予約済み実験番号、担当範囲を確認する
- 並列運用の共通ルールはリポジトリルートの `AGENTS.md` を参照する

## 現在の運用ルール

- `exp001` は真の baseline として扱う
- `exp001` の baseline は、生の 7 列 `Pclass`, `Sex`, `Age`, `SibSp`, `Parch`, `Fare`, `Embarked` を使う
- baseline では `Title`、`HasCabin`、`FamilySize` などの追加特徴量はまだ使わない
- 現在の正式版では `Title`、`FamilyGroup`、`SexPclass` を採用済み特徴量として `src/features.py` に反映している
- `notebooks/` では EDA や 1 仮説ずつの試作を行う
- 試して良かったものだけ `src/train.py` と、必要なら `src/features.py` に反映する
- `src/train.py` は「今の正式学習版」、`src/predict.py` は「今の正式提出版」として上書き運用する
- `src/features.py` は採用済み特徴量だけを残す場所として扱う
- 試しただけの特徴量ロジックは `features.py` に入れず、notebook と `experiments/` に残す
- モデル保存時は必ず `--model-path` を付けて、実験番号付きの成果物名を明示する
- 提出生成時は必ず `--model-path` と `--output` を付けて、実験番号付きの提出 CSV を明示する
- 特徴量は `採用候補`、`保留候補`、`却下候補` の3つで扱う
- 単独で強く効いたものを先に採用候補とする
- 単独では弱いが相互作用がありそうなものは保留候補として残し、後で再評価する
- 全組み合わせの総当たりはせず、基本は「現在のベスト構成」に 1 変更ずつ足して比較する

## 推奨する命名ルール

- notebook: `expXXX_<topic>.ipynb`
- model: `models/expXXX_<topic>.joblib`
- submission: `submissions/expXXX_<topic>.csv`
- experiment log: `experiments/expXXX.md`

例:

- `notebooks/exp003_title.ipynb`
- `models/exp003_title.joblib`
- `submissions/exp003_title.csv`
- `experiments/exp003.md`
