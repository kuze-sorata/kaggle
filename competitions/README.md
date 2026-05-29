# コンペ一覧

ここには、各 Kaggle コンペごとの作業フォルダを置きます。

進め方の共通ルールは `docs/kaggle_workflow.md` と `docs/codex_collaboration.md` を参照します。

## コンペフォルダの中身

- `data/`: コンペのデータ
- `notebooks/`: 探索用 Notebook
- `src/`: 学習と推論のコード
- `models/`: ローカル保存のモデル成果物
- `submissions/`: 提出ファイル
- `experiments/`: 実験一覧と詳細ログ
- `TODO.md`: やること一覧
- `README.md`: そのコンペ固有の実行手順と補足

## スコープの考え方

- `workspace_notes/`、`workspace_experiments/`、`docs/` は、ワークスペース全体向けの置き場
- コンペごとの反復作業は、対応するコンペフォルダの `experiments/` に置く

## 基本運用

- 進行は共通フローに沿って進める
- 実験ログの書式は `docs/experiment_log_template.md` を基準にする
- コンペ固有 README には、データ配置、実行コマンド、固有注意点だけを書く
