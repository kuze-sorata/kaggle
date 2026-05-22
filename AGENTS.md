# `/home/sora/dev/kaggle` 用の AGENTS.md

## 環境

- 開発と実行は既定で WSL を使う
- Python 作業では、必ずプロジェクトローカルの仮想環境を使う
- 標準的な Python セットアップ:
  - `python -m venv .venv`
  - Unix では `source .venv/bin/activate`
  - Windows では `.venv\Scripts\activate`
  - `pip install -r requirements.txt`
- 依存関係は `requirements.txt` や `pyproject.toml` など、プロジェクト設定で管理する

## 方針

- コード、ファイル名、ディレクトリ名、公開向けドキュメントは英語を基本にする
- `workspace_notes/` と実験メモでは、日本語を使ってよい
- `experiments/` 配下の本文は日本語を基本にする
- 実験履歴は `experiments/index.md` と `experiments/expXXX.md` で管理する
- 実験ログは短く、事実ベースで、再現しやすく書く
- 各コンペで共通化できる処理は `shared/` に寄せる
- `notes` / `experiments` / `docs` の使い分けは `docs/CONVENTIONS.md` を参照する
- コンペ固有の実験は `competitions/<competition_name>/experiments/` の中に置く

## 制約

- `sudo` は使わない
- Python パッケージをグローバルにインストールしない
- `pip install` を実行する前に、`.venv` を作成して有効化する

## Git と GitHub

- Git 操作は WSL から行う
- GitHub は SSH 認証を前提にする
- OS をまたいで Git 環境を混ぜない
