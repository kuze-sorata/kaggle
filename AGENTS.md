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

## 並列運用

- 複数の Codex やサブエージェントで同じコンペを並列に進める場合は、会話履歴ではなく共有ファイルを最新の前提として扱う
- 同一コンペの並列実験は、原則として親エージェント 1 つと子エージェント複数の構成で進める
- 親子運用の補助文書は `AGENTS/` 配下を参照する
- `competitions/<competition_name>/STATUS.md` がある場合は、作業開始前に必ず確認し、現在の baseline、予約済み実験番号、担当範囲をそこで共有する
- 実験番号の予約、配布、解放は親エージェントだけが行う
- 子エージェントは、親から割り当てられた `expXXX` だけを使う
- 実験番号は開始前に予約し、同じ `expXXX` を複数の Codex で共有しない
- notebook、submission、experiment log は同じ実験番号でそろえる
- 子エージェントは作業開始時に `STATUS.md` の自分の割り当てを確認し、完了時に結果を親へ返す
- 実験完了後の `STATUS.md` 更新と baseline の昇格判断は親エージェントが担当する
- 並列実行中は、原則として各 Codex は notebook と実験ログの更新までを担当する
- `src/features.py`、`src/train.py`、`src/predict.py` などの正式コード更新は、担当を 1 つに決めて衝突を避ける

## 制約

- `sudo` は使わない
- Python パッケージをグローバルにインストールしない
- `pip install` を実行する前に、`.venv` を作成して有効化する

## Git と GitHub

- Git 操作は WSL から行う
- GitHub は SSH 認証を前提にする
- OS をまたいで Git 環境を混ぜない
- コミットメッセージは日本語を基本にする
- コミットメッセージは件名だけで終えず、本文で何をしたかを箇条書きで残す
