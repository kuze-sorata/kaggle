# 実験一覧

## exp001

- Date: 2026-05-22
- Phase: Baseline
- Change: true baseline
- Result: CV 0.79687 / LB 0.76555
- Status: Submitted

## exp002

- Date: 2026-05-22
- Phase: EDA
- Change: feature inspection
- Result: CV N/A / LB N/A
- Status: Done

## exp003

- Date: 2026-05-22
- Phase: Feature
- Change: add `Title`
- Result: CV 0.82828 / LB 0.76555
- Status: Submitted

## exp004

- Date: 2026-05-22
- Phase: Feature
- Change: add `HasCabin`
- Result: CV 0.80247 / LB 0.76555
- Status: Submitted

## exp005

- Date: 2026-05-22
- Phase: Feature
- Change: add `Title` + `HasCabin`
- Result: CV 0.82826 / LB Not Submitted
- Status: Done

## exp006

- Date: 2026-05-22
- Phase: Feature
- Change: add `Title` + `FamilyGroup`
- Result: CV 0.82939 / LB 0.77272
- Status: Submitted

## exp007

- Date: 2026-05-22
- Phase: Feature
- Change: add `SexPclass` on top of `Title` + `FamilyGroup`
- Result: CV 0.83614 / LB 0.77511
- Status: Submitted

## exp008

- Date: 2026-05-22
- Phase: Feature
- Change: add `FareBand` on top of `Title` + `FamilyGroup`
- Result: CV 0.82827 / LB Not Submitted
- Status: Done

## exp009

- Date: 2026-05-22
- Phase: Feature
- Change: add `FareBand` on top of `Title` + `FamilyGroup` + `SexPclass`
- Result: CV 0.83275 / LB Not Submitted
- Status: Done

## exp010

- Date: 2026-05-25
- Phase: Feature
- Change: add `AgeBand` on top of `Title` + `FamilyGroup` + `SexPclass`
- Result: CV 0.83053 / LB Not Submitted
- Status: Done

## exp011

- Date: 2026-05-25
- Phase: Feature
- Change: add `TicketGroupSize` on top of `Title` + `FamilyGroup` + `SexPclass`
- Result: CV 0.83501 / LB Not Submitted
- Status: Done

## exp012

- Date: 2026-05-25
- Phase: Model
- Change: replace `LogisticRegression` with `RandomForest` on top of `Title` + `FamilyGroup` + `SexPclass`
- Result: CV 0.80808 / LB Not Submitted
- Status: Done

## exp013

- Date: 2026-05-25
- Phase: Model
- Change: replace `LogisticRegression` with `CatBoost` on top of `Title` + `FamilyGroup` + `SexPclass`
- Result: CV 0.83839 / LB 0.75598
- Status: Done

## exp014

- Date: 2026-05-25
- Phase: Validation
- Change: review CV stability for `exp007` vs `exp013` across multiple seeds and holdout splits
- Result: `exp013` gain was unstable; holdout mean delta was negative
- Status: Done
