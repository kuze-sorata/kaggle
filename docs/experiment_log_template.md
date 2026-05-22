# Experiment Log Template

このテンプレートは、各コンペの `experiments/` に共通で使うための基準です。

## `experiments/index.md`

```md
# 実験一覧

| Exp    | Date       | Phase    | Topic        | CV Score | LB Score | Status | Notes |
| ------ | ---------- | -------- | ------------ | -------- | -------- | ------ | ----- |
| exp001 | 2026-05-22 | Baseline | first submit | TBD      | TBD      | WIP    | 初回提出 |
```

## `experiments/expXXX.md`

```md
# expXXX - short title

## Date

YYYY-MM-DD

## Competition

<competition_name>

## Phase

Problem Understanding / Baseline / CV / EDA / Feature Engineering / Model Comparison / Submission / Experiment Logging

## Objective

今回の実験で達成したいことを 1-2 文で書く。

## Hypothesis

何が効くと考えたかを書く。

## Reason

なぜその仮説を持ったかを書く。

## Changes

- 実装・設定・データ処理の変更点

## Validation Plan

- 分割方法
- 評価指標
- 比較条件

## Result

- CV:
- LB:

## Observations

- 事実ベースの気づき

## Risks

- リーク、分布ずれ、評価の不安定さなど

## Next Actions

- 次に試すこと
```

## 運用ルール

- `Phase` は標準フローのどこに属するかを明示する
- `Changes` は事実だけを書く
- `Observations` と `Next Actions` を分ける
- 数値が未確定なら `TBD` と書く
