# exp001 EDA Summary

## Overview

- Train shape: 1460 rows x 81 columns
- Test shape: 1459 rows x 80 columns
- Numeric columns: 38
- Categorical columns: 43
- SalePrice skew: 1.8829
- log1p(SalePrice) skew: 0.1213

## High missing columns

```
     column  train_missing_pct  test_missing_pct
     PoolQC              99.52             99.79
MiscFeature              96.30             96.50
      Alley              93.77             92.67
      Fence              80.75             80.12
 MasVnrType              59.73             61.27
FireplaceQu              47.26             50.03
```

## Top numeric correlations with SalePrice

```
     feature  correlation
 OverallQual     0.790982
   GrLivArea     0.708624
  GarageCars     0.640409
  GarageArea     0.623431
 TotalBsmtSF     0.613581
    1stFlrSF     0.605852
    FullBath     0.560664
TotRmsAbvGrd     0.533723
```

## Strong train/test numeric shifts

```
     feature  ks_stat  train_mean  test_mean
          Id   1.0000    730.5000  2190.0000
    2ndFlrSF   0.0471    346.9925   325.9678
   GrLivArea   0.0464   1515.4637  1486.0459
TotRmsAbvGrd   0.0449      6.5178     6.3852
 TotalBsmtSF   0.0413   1057.4295  1046.1180
      MoSold   0.0378      6.3219     6.1042
YearRemodAdd   0.0372   1984.8658  1983.6628
     LotArea   0.0372  10516.8281  9819.1611
```

## Strong train/test categorical shifts

```
     feature  tv_distance top_train_level top_test_level
Neighborhood       0.0723           NAmes          NAmes
 FireplaceQu       0.0374     __MISSING__    __MISSING__
 Exterior2nd       0.0319         VinylSd        VinylSd
BsmtFinType1       0.0318             Unf            GLQ
    MSZoning       0.0289              RL             RL
    BsmtQual       0.0282              TA             TA
  PavedDrive       0.0261               Y              Y
  HouseStyle       0.0251          1Story         1Story
```

## Outlier summary

```
                                  feature  outlier_count  outlier_pct
                                SalePrice             61         4.18
                                GrLivArea             31         2.12
                                  LotArea             69         4.73
                              TotalBsmtSF             61         4.18
                               GarageArea             21         1.44
GrLivArea_gt_4000_and_SalePrice_lt_300000              2         0.14
```

## Initial implications

- `SalePrice` is strongly right-skewed, and `log1p` largely stabilizes the target distribution.
- Several columns have structural missingness (`PoolQC`, `MiscFeature`, `Alley`, `Fence`, `FireplaceQu`), so missingness itself may be informative.
- `OverallQual`, `GrLivArea`, `GarageCars`, `GarageArea`, `TotalBsmtSF`, and `1stFlrSF` are strong starting points for the first baseline.
- Some features show train/test distribution gaps, so aggressive hand-tuned thresholds should be treated carefully.
- A small number of very large houses look like outlier candidates and should be tracked explicitly before model comparison.
