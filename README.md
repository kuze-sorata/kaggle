# Kaggle ワークスペース

このリポジトリは、Kaggle の研究・実験を効率よく回すための作業場です。

## ディレクトリ構成

```text
kaggle/
├── templates/
│   ├── tabular_baseline/
│   ├── time_series/
│   ├── binary_classification/
│   ├── multiclass_classification/
│   └── regression/
├── competitions/
├── shared/
│   ├── cv/
│   ├── features/
│   ├── metrics/
│   ├── preprocessing/
│   ├── visualization/
│   ├── utils/
│   └── configs/
├── workspace_experiments/
├── workspace_notes/
├── docs/
├── scripts/
└── README.md
```

## 運用方針

- Python はリポジトリルートの共通 `.venv` を使う
- 新しいコンペは `templates/tabular_baseline` を起点に始める
- コンペ固有の作業は `competitions/<competition_name>/` にまとめる
- 再利用できるコードは `shared/` に置いて重複を減らす
- Notebook は探索用に使い、安定した処理は `src/` に移す
- 実験の一覧は `experiments/index.md` に、詳細は `experiments/expXXX.md` に残す
- ワークスペース全体のメモは `workspace_notes/`、横断比較は `workspace_experiments/`、安定したルールは `docs/` に置く
- コンペごとの実験は `competitions/<competition_name>/experiments/` 配下で管理する
- `data/` は Git 管理しない
- 大きな生データ、モデル成果物、Notebook のキャッシュはコミットしない

## 共通 Python 環境

```powershell
cd C:\Users\21td031\dev\kaggle
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Kaggle CLI の認証情報をこのワークスペース内で扱う場合は、`.kaggle/` を使います。このディレクトリは Git 管理外です。

```powershell
$env:KAGGLE_CONFIG_DIR = "$PWD\.kaggle"
```

## 言語方針

- ディレクトリ名、ファイル名、コード、関数名、クラス名、公開向けの説明は英語を基本にする
- `workspace_notes/` と各コンペのメモ系ファイルでは、日本語を自由に使ってよい
- 1つのファイルの中では、目的に応じて言語を極力揃える

## 実験ログの書き方

- `experiments/index.md` は全実験の一覧として使う
- `experiments/expXXX.md` は各実験の詳細ログとして使う
- 1つの実験を 1 ファイルで管理する
- 日付、コンペ名、目的、仮説、理由、変更内容、CV スコア、LB スコア、結果、次のアクションを残す
- 成功した実験だけでなく、失敗した実験も記録する
- 短く、事実ベースで、再現しやすく書く

## Kaggle の運用ルール

- コンペのルールとデータ利用条件を守る
- 特徴量設計、検証、ターゲット処理でリークを防ぐ
- 可能な限り乱数シードを固定する
- 提出前にローカルで確認する
- 提出ファイル名とモデル成果物はコンペごとに整理する

## Git の方針

- コード、設定、実験ログはコミットする
- `data/`、`models/`、大きなバイナリファイルは追跡しない
- 1つのコミットは 1 つの目的に絞る
- 大きすぎるコミットより、読みやすい履歴を優先する
- `shared/` は再利用前提の共通資産として扱う

## コンペの進め方

1. ベーステンプレートから新しいコンペ用フォルダを作る
2. データをローカルに置く
3. `src/` で特徴量と学習処理を実装する
4. すべての重要な変更を `experiments/index.md` と `experiments/expXXX.md` に残す
5. 必要な成果物だけを残す

### データの置き方

```bash
python scripts/download_competition_data.py titanic
```

Kaggle CLI と API 認証が整っている場合、`competitions/titanic/data/` にデータを置けます。

### 新しいコンペを作る

```bash
python scripts/create_competition.py <competition_name>
```
