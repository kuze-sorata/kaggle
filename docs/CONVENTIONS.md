# 規約

## フォルダの役割

- ルートの `workspace_notes/`
  - 生の思考メモ置き場
  - 日本語のメモ、ちょっとした気づき、途中のアイデア、ラフな下書きに使う
  - 内容が未完成でもよい

- ルートの `workspace_experiments/`
  - ワークスペース横断の実験まとめ置き場
  - コンペ横断の比較や、共有ベンチマーク、後で見返したい結果を置く
  - 短く、比較しやすく書く

- ルートの `docs/`
  - 安定したドキュメントと運用ルール置き場
  - 規約、手順、参照資料を置く
  - 下書き置き場にはしない
  - 共通の進め方は `docs/kaggle_workflow.md` と `docs/codex_collaboration.md` にまとめる

- コンペ配下の `experiments/`
  - `competitions/<competition_name>/experiments/` の中で使う
  - そのコンペ固有の実験履歴、比較、メモを置く
  - `index.md` と `expXXX.md` で管理する

## 書き方の方針

- コード、ファイル名、ディレクトリ名、公開向け文書は英語を基本にする
- `workspace_notes/` と実験メモでは、日本語を自由に使ってよい
- `competitions/<competition_name>/experiments/` の本文は日本語を基本にする
- 1つのファイルは 1 つの目的に集中させる
- 識別子、コード、機械可読な見出しの中で、日本語と英語を混ぜすぎない

## 実験メモ

- 短く、まとまっていない途中メモは `workspace_notes/` に置く
- 後で比較したい結果は `workspace_experiments/` に置く
- コンペごとの実験履歴は `competitions/<competition_name>/experiments/` に置く
- `experiments/index.md` を、そのコンペの実験履歴の一覧として扱う
- `expXXX.md` を、その実験の一次情報として扱う
- 実験ログの書式は `docs/experiment_log_template.md` を基準にする

## コミットメッセージ

- コミットメッセージは日本語を基本にする
- 件名は変更の主旨が分かる短い文にする
- 本文では、何を変更したかを箇条書きで残す
- あとで GitHub の履歴を見返したときに、変更意図が分かる書き方にする

## 例

- `workspace_notes/2026-05-22_feature_ideas.md`
- `workspace_experiments/lgbm_vs_catboost.md`
- `docs/workflow.md`
- `competitions/titanic/experiments/index.md`
- `competitions/titanic/experiments/exp001.md`
