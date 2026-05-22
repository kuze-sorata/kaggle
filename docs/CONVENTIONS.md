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

- コンペ配下の `notes/` / `experiments/` / `docs/`
  - `competitions/<competition_name>/` の中で使う
  - そのコンペ固有の作業場所として扱う
  - ワークスペース全体の資料とは分ける

## 書き方の方針

- コード、ファイル名、ディレクトリ名、公開向け文書は英語を基本にする
- `workspace_notes/` と実験メモでは、日本語を自由に使ってよい
- 1つのファイルは 1 つの目的に集中させる
- 識別子、コード、機械可読な見出しの中で、日本語と英語を混ぜすぎない

## 実験メモ

- 短く、まとまっていない途中メモは `workspace_notes/` や各コンペの `notes/` に置く
- 後で比較したい結果は `workspace_experiments/` や各コンペの `experiments/` に置く
- コンペごとの実験履歴は `experiment_log.md` に置く
- `experiment_log.md` を、そのコンペの実験履歴の一次情報として扱う

## 例

- `workspace_notes/2026-05-22_feature_ideas.md`
- `workspace_experiments/lgbm_vs_catboost.md`
- `docs/workflow.md`
- `competitions/titanic/notes/2026-05-22_leakage_check.md`
- `competitions/titanic/experiments/lgbm_baseline.md`
- `competitions/titanic/docs/assumptions.md`

