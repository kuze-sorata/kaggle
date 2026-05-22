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

- 新しいコンペは `templates/tabular_baseline` を起点に始める
- コンペ固有の作業は `competitions/<competition_name>/` にまとめる
- 再利用できるコードは `shared/` に置いて重複を減らす
- Notebook は探索用に使い、安定した処理は `src/` に移す
- ログ、仮説、評価結果は `experiment_log.md` に残す
- ワークスペース全体のメモは `workspace_notes/`、横断比較は `workspace_experiments/`、安定したルールは `docs/` に置く
- コンペごとのメモ、実験、資料は `competitions/<competition_name>/` 配下に置く
- 大きな生データ、モデル成果物、Notebook のキャッシュはコミットしない

## 言語方針

- ディレクトリ名、ファイル名、コード、関数名、クラス名、公開向けの説明は英語を基本にする
- `workspace_notes/` と各コンペのメモ系ファイルでは、日本語を自由に使ってよい
- 1つのファイルの中では、目的に応じて言語を極力揃える

## 実験ログの書き方

- 1つの実験を 1 セクションで書く。例: `## exp001`
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
4. すべての重要な変更を `experiment_log.md` に残す
5. 必要な成果物だけを残す

### 新しいコンペを作る

```bash
python scripts/create_competition.py <competition_name>
```

