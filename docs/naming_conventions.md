# 命名規約

## 基本ルール

- ディレクトリ名、ファイル名、コードの識別子、公開向け文書は英語を基本にする
- 日本語は、メモや内部向けの説明など、意図して使う場所だけに使う
- 名前は短すぎず、用途が分かるものにする
- Python のモジュール名やユーティリティファイルは lower_snake_case にする

## 推奨パターン

- コンペフォルダ: `competitions/<competition_name>/`
- 実験ログ: `experiment_log.md`
- ワークスペースメモ: `workspace_notes/YYYY-MM-DD_short_topic.md`
- コンペメモ: `competitions/<competition_name>/notes/YYYY-MM-DD_short_topic.md`
- ワークスペースの実験まとめ: `workspace_experiments/<topic>.md`
- コンペの実験まとめ: `competitions/<competition_name>/experiments/<topic>.md`
- 共有ヘルパー: `shared/<area>/<name>.py`

## 避けたいもの

- コード識別子の中で日本語と英語を混ぜること
- `temp.py`、`new.py`、`final_final.py` のような曖昧な名前
- 長すぎて目的が分かりにくい名前

