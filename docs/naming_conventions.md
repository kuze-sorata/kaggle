# 命名規約

## 基本ルール

- ディレクトリ名、ファイル名、コードの識別子、公開向け文書は英語を基本にする
- 日本語は、メモや内部向けの説明など、意図して使う場所だけに使う
- 名前は短すぎず、用途が分かるものにする
- Python のモジュール名やユーティリティファイルは lower_snake_case にする

## 推奨パターン

- コンペフォルダ: `competitions/<competition_name>/`
- 実験一覧: `experiments/index.md`
- 実験詳細: `experiments/exp001.md`
- 追加の実験: `experiments/exp002.md` のように増やす
- 実験アーカイブ: `experiments/archive/`
- ワークスペースメモ: `workspace_notes/YYYY-MM-DD_short_topic.md`
- ワークスペースの実験まとめ: `workspace_experiments/<topic>.md`
- コンペの実験詳細: `competitions/<competition_name>/experiments/expXXX.md`
- 共有ヘルパー: `shared/<area>/<name>.py`

## 避けたいもの

- コード識別子の中で日本語と英語を混ぜること
- `temp.py`、`new.py`、`final_final.py` のような曖昧な名前
- 長すぎて目的が分かりにくい名前

## コミットメッセージの形

- 件名は日本語で書く
- 本文は箇条書きで書く
- 例:
  - 件名: `実験テンプレートを日本語化`
  - 本文:
    - `templates/tabular_baseline/experiments/` の文言を日本語化
    - `competitions/titanic/experiments/` の既存ファイルを日本語化
    - `create_competition.py` の生成テンプレートを日本語化
