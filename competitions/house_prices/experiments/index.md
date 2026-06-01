# 実験一覧

## exp001

- Date: 2026-05-26
- Phase: EDA
- Change: Codex-generated broad data inspection before baseline
- Result: CV N/A / LB N/A
- Status: Done
- Notes: データ全体の概観、欠損、目的変数の歪み、相関、train/test shift、外れ値候補を確認した。

## exp002

- Date: 2026-05-29
- Phase: EDA
- Change: user-written exploratory analysis for deeper data understanding
- Result: CV N/A / LB N/A
- Status: Done
- Notes: `MSSubClass`, `MSZoning`, `LotFrontage`, `LotArea`, `Street` などを手作業で確認し、土地面積、欠損、品質、築年数、カテゴリ特徴量の扱いを後続仮説として整理した。次は baseline と CV を作る。

## exp003

- Date: TBD
- Phase: Baseline
- Change: 最小限の前処理とモデルで baseline / CV を作成する
- Result: TBD
- Status: Planned
- Notes: `exp002` の仮説検証に入る前に、比較基準となる再現可能な baseline を作る。
