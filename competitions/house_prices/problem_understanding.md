# House Prices 問題設定の整理

## 概要

- コンペ名: House Prices - Advanced Regression Techniques
- タスク種別: 回帰
- 目的: Ames, Iowa の住宅について、各物件の最終売却価格 `SalePrice` を予測する
- データの特徴:
  - 79 個の説明変数がある
  - 住宅の面積、品質、築年、立地、設備など幅広い属性を含む

## 目的変数

- 目的変数: `SalePrice`
- 値の意味:
  - 各住宅の最終売却価格
  - 連続値であり、分類ではない

## 評価指標

- 指標: `RMSLE`
- 意味:
  - 予測価格と実価格の対数差を使う回帰指標
  - 高価格帯の絶対誤差だけで押し切るより、比率のズレも強く見る
  - 小さいほど良い

## 提出形式

- 必須列:
  - `Id`
  - `SalePrice`
- 期待される形:
  - `test.csv` の各住宅に対して 1 行ずつ予測を書く

例:

```csv
Id,SalePrice
1461,169000.0
1462,187724.0
1463,183000.0
```

## データ構造

### `train.csv`

- 学習用データ
- `SalePrice` を含む
- ベースライン構築とローカル CV に使う

### `test.csv`

- 推論用データ
- `SalePrice` を含まない
- 提出ファイル生成に使う

### `sample_submission.csv`

- 提出形式の確認に使う
- 列名と行数を合わせる基準になる

### `data_description.txt`

- 各列の意味、カテゴリ値、補足説明を確認する一次資料
- EDA 前に一度読んでおく価値が高い

## 特徴量辞書

このセクションは `data_description.txt` をもとに、日本語で意味を整理したものです。カテゴリ列は主な取りうる値も併記します。`NA` は「欠損」ではなく、「その設備自体が存在しない」意味で使われる列があります。

### 基本情報と敷地

- `Id`: 各物件の識別子
- `MSSubClass`: 建物タイプを表すコード
  - `20`: 1946年以降の平屋
  - `30`: 1945年以前の平屋
  - `40`: 仕上げ済み屋根裏付き平屋
  - `45`: 1.5階建て、上階未仕上げ
  - `50`: 1.5階建て、上階仕上げ済み
  - `60`: 1946年以降の2階建て
  - `70`: 1945年以前の2階建て
  - `75`: 2.5階建て
  - `80`: スプリットレベル / 多層階
  - `85`: スプリットフォイヤー
  - `90`: 二世帯住宅 / デュプレックス
  - `120`: 平屋の PUD
  - `150`: 1.5階建ての PUD
  - `160`: 2階建ての PUD
  - `180`: 多層階の PUD
  - `190`: 2世帯向け転用住宅
- `MSZoning`: 用途地域
  - `A`: 農業地域
  - `C` / `C (all)`: 商業系
  - `FV`: 浮動村住宅地区
  - `I`: 工業地域
  - `RH`: 高密度住宅地域
  - `RL`: 低密度住宅地域
  - `RP`: 低密度公園住宅地域
  - `RM`: 中密度住宅地域
- `LotFrontage`: 道路に接している敷地間口の長さ
- `LotArea`: 敷地面積
- `Street`: 接道の種類
  - `Grvl`: 砂利道
  - `Pave`: 舗装道路
- `Alley`: 路地接道の種類
  - `Grvl`: 砂利
  - `Pave`: 舗装
  - `NA`: 路地接道なし
- `LotShape`: 敷地形状
  - `Reg`: 整形
  - `IR1`: やや不整形
  - `IR2`: 中程度の不整形
  - `IR3`: 強い不整形
- `LandContour`: 地盤の高低 / 平坦さ
  - `Lvl`: ほぼ平坦
  - `Bnk`: 道路から急に高くなっている
  - `HLS`: 横方向の傾斜が大きい丘陵地
  - `Low`: 低地 / くぼ地
- `Utilities`: 利用可能な公共インフラ
  - `AllPub`: 電気・ガス・水道・下水すべてあり
  - `NoSewr`: 下水なし
  - `NoSeWa`: 下水・水道の一部なし
  - `ELO`: 電気のみ
- `LotConfig`: 敷地の接道配置
  - `Inside`: 中間地
  - `Corner`: 角地
  - `CulDSac`: 袋小路
  - `FR2`: 二方向接道
  - `FR3`: 三方向接道
- `LandSlope`: 傾斜の強さ
  - `Gtl`: 緩やか
  - `Mod`: 中程度
  - `Sev`: 急傾斜

### 立地と建物タイプ

- `Neighborhood`: Ames 市内の地区
  - `Blmngtn`: Bloomington Heights
  - `Blueste`: Bluestem
  - `BrDale`: Briardale
  - `BrkSide`: Brookside
  - `ClearCr`: Clear Creek
  - `CollgCr`: College Creek
  - `Crawfor`: Crawford
  - `Edwards`: Edwards
  - `Gilbert`: Gilbert
  - `IDOTRR`: Iowa DOT / 線路周辺
  - `MeadowV`: Meadow Village
  - `Mitchel`: Mitchell
  - `NAmes`: North Ames
  - `NoRidge`: Northridge
  - `NPkVill`: Northpark Villa
  - `NridgHt`: Northridge Heights
  - `NWAmes`: Northwest Ames
  - `OldTown`: Old Town
  - `SWISU`: Iowa State University 南西側
  - `Sawyer`: Sawyer
  - `SawyerW`: Sawyer West
  - `Somerst`: Somerset
  - `StoneBr`: Stone Brook
  - `Timber`: Timberland
  - `Veenker`: Veenker
- `Condition1`: 主な周辺条件との近接
  - `Artery`: 幹線道路沿い
  - `Feedr`: 補助道路沿い
  - `Norm`: 特に問題なし
  - `RRNn`: 南北鉄道から 200 フィート以内
  - `RRAn`: 南北鉄道に隣接
  - `PosN`: 公園や緑地など良い外部要因に近い
  - `PosA`: 良い外部要因に隣接
  - `RRNe`: 東西鉄道から 200 フィート以内
  - `RRAe`: 東西鉄道に隣接
- `Condition2`: 副次的な周辺条件との近接
  - `Artery`: 幹線道路沿い
  - `Feedr`: 補助道路沿い
  - `Norm`: 特に問題なし
  - `RRNn`: 南北鉄道から 200 フィート以内
  - `RRAn`: 南北鉄道に隣接
  - `PosN`: 良い外部要因に近い
  - `PosA`: 良い外部要因に隣接
  - `RRNe`: 東西鉄道から 200 フィート以内
  - `RRAe`: 東西鉄道に隣接
- `BldgType`: 建物種別
  - `1Fam`: 独立した一戸建て
  - `2FmCon` / `2fmCon`: 元は一戸建ての二世帯向け転用住宅
  - `Duplx`: 二戸一住宅
  - `TwnhsE`: 端部のタウンハウス
  - `TwnhsI` / `Twnhs`: 中間のタウンハウス
- `HouseStyle`: 建物の階構成 / スタイル
  - `1Story`: 平屋
  - `1.5Fin`: 1.5階建て、2階部分仕上げ済み
  - `1.5Unf`: 1.5階建て、2階部分未仕上げ
  - `2Story`: 2階建て
  - `2.5Fin`: 2.5階建て、上階仕上げ済み
  - `2.5Unf`: 2.5階建て、上階未仕上げ
  - `SFoyer`: スプリットフォイヤー
  - `SLvl`: スプリットレベル

### 総合品質・築年・外装

- `OverallQual`: 建材と仕上げの総合品質
  - `10`: 非常に優秀
  - `9`: 優秀
  - `8`: とても良い
  - `7`: 良い
  - `6`: 平均より上
  - `5`: 平均
  - `4`: 平均より下
  - `3`: やや悪い
  - `2`: 悪い
  - `1`: 非常に悪い
- `OverallCond`: 建物全体の状態評価
  - `10`: 非常に優秀
  - `9`: 優秀
  - `8`: とても良い
  - `7`: 良い
  - `6`: 平均より上
  - `5`: 平均
  - `4`: 平均より下
  - `3`: やや悪い
  - `2`: 悪い
  - `1`: 非常に悪い
- `YearBuilt`: 建築年
- `YearRemodAdd`: 増改築年。改築がなければ建築年と同じ
- `RoofStyle`: 屋根形状
  - `Flat`: 陸屋根
  - `Gable`: 切妻
  - `Gambrel`: 腰折れ屋根
  - `Hip`: 寄棟
  - `Mansard`: マンサード
  - `Shed`: 片流れ
- `RoofMatl`: 屋根材
  - `ClyTile`: 粘土瓦 / タイル
  - `CompShg`: 一般的な複合シングル
  - `Membran`: 膜材
  - `Metal`: 金属
  - `Roll`: ロール材
  - `Tar&Grv`: タールと砂利
  - `WdShake`: 木製シェイク
  - `WdShngl`: 木製シングル
- `Exterior1st`: 主たる外装材
  - `AsbShng`: アスベスト系シングル
  - `AsphShn`: アスファルトシングル
  - `BrkComm`: 一般レンガ
  - `BrkFace`: 化粧レンガ
  - `CBlock`: コンクリートブロック
  - `CemntBd`: セメントボード
  - `HdBoard`: ハードボード
  - `ImStucc`: 擬似スタッコ
  - `MetalSd`: 金属サイディング
  - `Other`: その他
  - `Plywood`: 合板
  - `PreCast`: プレキャスト
  - `Stone`: 石材
  - `Stucco`: スタッコ
  - `VinylSd`: ビニールサイディング
  - `Wd Sdng`: 木製サイディング
  - `WdShing`: 木製シングル
- `Exterior2nd`: 副次的な外装材
  - `AsbShng`: アスベスト系シングル
  - `AsphShn`: アスファルトシングル
  - `BrkComm` / `Brk Cmn`: 一般レンガ
  - `BrkFace`: 化粧レンガ
  - `CBlock`: コンクリートブロック
  - `CemntBd` / `CmentBd`: セメントボード
  - `HdBoard`: ハードボード
  - `ImStucc`: 擬似スタッコ
  - `MetalSd`: 金属サイディング
  - `Other`: その他
  - `Plywood`: 合板
  - `PreCast`: プレキャスト
  - `Stone`: 石材
  - `Stucco`: スタッコ
  - `VinylSd`: ビニールサイディング
  - `Wd Sdng`: 木製サイディング
  - `WdShing` / `Wd Shng`: 木製シングル
- `MasVnrType`: 化粧石材 / レンガ張りの種類
  - `BrkCmn`: 一般レンガ
  - `BrkFace`: 化粧レンガ
  - `CBlock`: コンクリートブロック
  - `None`: なし
  - `Stone`: 石材
- `MasVnrArea`: 化粧石材部分の面積
- `ExterQual`: 外装材の品質
  - `Ex`: 優秀
  - `Gd`: 良い
  - `TA`: 標準 / 平均
  - `Fa`: やや悪い
  - `Po`: 悪い
- `ExterCond`: 外装材の現在状態
  - `Ex`: 優秀
  - `Gd`: 良い
  - `TA`: 標準 / 平均
  - `Fa`: やや悪い
  - `Po`: 悪い
- `Foundation`: 基礎形式
  - `BrkTil`: レンガとタイル
  - `CBlock`: コンクリートブロック
  - `PConc`: 打設コンクリート
  - `Slab`: ベタ基礎 / スラブ
  - `Stone`: 石造
  - `Wood`: 木造基礎

### 地下室

- `BsmtQual`: 地下室の高さ品質
  - `Ex`: 非常に高い
  - `Gd`: 良い
  - `TA`: 標準
  - `Fa`: やや低い
  - `Po`: 低い
  - `NA`: 地下室なし
- `BsmtCond`: 地下室全体の状態
  - `Ex`: 優秀
  - `Gd`: 良い
  - `TA`: 標準
  - `Fa`: 湿気やひびが少しある
  - `Po`: 深刻なひび・沈下・湿気あり
  - `NA`: 地下室なし
- `BsmtExposure`: 地下室の採光 / 露出具合
  - `Gd`: 良い露出
  - `Av`: 平均的
  - `Mn`: 最小限
  - `No`: 露出なし
  - `NA`: 地下室なし
- `BsmtFinType1`: 主たる地下室仕上げ区画の種類
  - `GLQ`: 良質な居住空間
  - `ALQ`: 平均的な居住空間
  - `BLQ`: 平均以下の居住空間
  - `Rec`: レクリエーションルーム
  - `LwQ`: 低品質
  - `Unf`: 未仕上げ
  - `NA`: 地下室なし
- `BsmtFinSF1`: 主たる地下室仕上げ面積
- `BsmtFinType2`: 副次的な地下室仕上げ区画の種類
  - `GLQ`: 良質な居住空間
  - `ALQ`: 平均的な居住空間
  - `BLQ`: 平均以下の居住空間
  - `Rec`: レクリエーションルーム
  - `LwQ`: 低品質
  - `Unf`: 未仕上げ
  - `NA`: 地下室なし
- `BsmtFinSF2`: 副次的な地下室仕上げ面積
- `BsmtUnfSF`: 地下室の未仕上げ面積
- `TotalBsmtSF`: 地下室の総面積

### 暖房・電気・居住空間

- `Heating`: 暖房方式
  - `Floor`: 床暖房 / 床置き暖房
  - `GasA`: ガス強制送風暖房
  - `GasW`: ガス温水 / 蒸気暖房
  - `Grav`: 重力式暖房
  - `OthW`: ガス以外の温水 / 蒸気暖房
  - `Wall`: 壁付け暖房
- `HeatingQC`: 暖房の品質と状態
  - `Ex`: 優秀
  - `Gd`: 良い
  - `TA`: 標準 / 平均
  - `Fa`: やや悪い
  - `Po`: 悪い
- `CentralAir`: セントラル空調の有無
  - `Y`: あり
  - `N`: なし
- `Electrical`: 電気設備
  - `SBrkr`: 標準的なブレーカー方式
  - `FuseA`: 60A 超のヒューズ方式
  - `FuseF`: 60A のヒューズ方式
  - `FuseP`: 古い低品質ヒューズ方式
  - `Mix`: 混在
- `1stFlrSF`: 1階面積
- `2ndFlrSF`: 2階面積
- `LowQualFinSF`: 低品質な仕上げ面積
- `GrLivArea`: 地上部分の居住面積
- `BsmtFullBath`: 地下室のフルバス数
- `BsmtHalfBath`: 地下室のハーフバス数
- `FullBath`: 地上部分のフルバス数
- `HalfBath`: 地上部分のハーフバス数
- `BedroomAbvGr`: 地上部分の寝室数
- `KitchenAbvGr`: 地上部分のキッチン数
- `KitchenQual`: キッチン品質
  - `Ex`: 優秀
  - `Gd`: 良い
  - `TA`: 標準 / 平均
  - `Fa`: やや悪い
  - `Po`: 悪い
- `TotRmsAbvGrd`: 地上部分の総部屋数。浴室は含まない
- `Functional`: 住宅機能性の評価
  - `Typ`: 標準的
  - `Min1`: 軽微な減点 1
  - `Min2`: 軽微な減点 2
  - `Mod`: 中程度の問題
  - `Maj1`: 大きな問題 1
  - `Maj2`: 大きな問題 2
  - `Sev`: 深刻な損傷
  - `Sal`: ほぼ解体前提

### 暖炉・ガレージ・外構

- `Fireplaces`: 暖炉の数
- `FireplaceQu`: 暖炉品質
  - `Ex`: 非常に高品質な組積造暖炉
  - `Gd`: 良質な暖炉
  - `TA`: 標準的な暖炉
  - `Fa`: 地下室などにある簡易暖炉
  - `Po`: 低品質なストーブ型
  - `NA`: 暖炉なし
- `GarageType`: ガレージ位置 / 種類
  - `2Types`: 複数タイプあり
  - `Attchd`: 建物に接続
  - `Basment`: 地下ガレージ
  - `BuiltIn`: 建物一体型
  - `CarPort`: カーポート
  - `Detchd`: 離れガレージ
  - `NA`: ガレージなし
- `GarageYrBlt`: ガレージ建築年
- `GarageFinish`: ガレージ内部仕上げ
  - `Fin`: 仕上げ済み
  - `RFn`: ラフ仕上げ
  - `Unf`: 未仕上げ
  - `NA`: ガレージなし
- `GarageCars`: 収容可能台数
- `GarageArea`: ガレージ面積
- `GarageQual`: ガレージ品質
  - `Ex`: 優秀
  - `Gd`: 良い
  - `TA`: 標準 / 平均
  - `Fa`: やや悪い
  - `Po`: 悪い
  - `NA`: ガレージなし
- `GarageCond`: ガレージ状態
  - `Ex`: 優秀
  - `Gd`: 良い
  - `TA`: 標準 / 平均
  - `Fa`: やや悪い
  - `Po`: 悪い
  - `NA`: ガレージなし
- `PavedDrive`: 私道 / 駐車スペースの舗装状況
  - `Y`: 全面舗装
  - `P`: 一部舗装
  - `N`: 未舗装 / 砂利
- `WoodDeckSF`: 木製デッキ面積
- `OpenPorchSF`: 開放ポーチ面積
- `EnclosedPorch`: 屋内化されたポーチ面積
- `3SsnPorch`: 3 シーズン用ポーチ面積
- `ScreenPorch`: 網戸付きポーチ面積
- `PoolArea`: プール面積
- `PoolQC`: プール品質
  - `Ex`: 優秀
  - `Gd`: 良い
  - `TA`: 標準 / 平均
  - `Fa`: やや悪い
  - `NA`: プールなし
- `Fence`: フェンス品質
  - `GdPrv`: 良いプライバシーフェンス
  - `MnPrv`: 最低限のプライバシー確保
  - `GdWo`: 良質な木製フェンス
  - `MnWw`: 最低限の木 / ワイヤーフェンス
  - `NA`: フェンスなし
- `MiscFeature`: その他設備
  - `Elev`: エレベーター
  - `Gar2`: 第2ガレージ
  - `Othr`: その他
  - `Shed`: 物置
  - `TenC`: テニスコート
  - `NA`: 該当なし
- `MiscVal`: その他設備の評価額

### 売却情報

- `MoSold`: 売却月
- `YrSold`: 売却年
- `SaleType`: 売却形態
  - `WD`: 通常の保証証書売買
  - `CWD`: 現金での保証証書売買
  - `VWD`: VA ローンでの保証証書売買
  - `New`: 新築後すぐの販売
  - `COD`: 裁判所 / 遺産整理経由
  - `Con`: 通常条件の分割契約
  - `ConLw`: 頭金少なめ・低金利契約
  - `ConLI`: 低金利契約
  - `ConLD`: 頭金少なめ契約
  - `Oth`: その他
- `SaleCondition`: 売却時の状態
  - `Normal`: 通常売却
  - `Abnorml`: 差し押さえ / ショートセールなど特殊売却
  - `AdjLand`: 隣接地購入を伴う
  - `Alloca`: 複数区画への割当売却
  - `Family`: 親族間売買
  - `Partial`: 完成前評価段階での売却
- `SalePrice`: 最終売却価格。予測対象

## 先に確認したい主な列の種類

- 識別子:
  - `Id`
- 価格や広さに強く関係しそうな数値列:
  - `OverallQual`
  - `GrLivArea`
  - `TotalBsmtSF`
  - `1stFlrSF`
  - `GarageArea`
  - `YearBuilt`
  - `YearRemodAdd`
- 立地やカテゴリ列:
  - `Neighborhood`
  - `MSZoning`
  - `HouseStyle`
  - `Exterior1st`
  - `KitchenQual`
- 欠損や意味解釈が重要そうな列:
  - `LotFrontage`
  - `Alley`
  - `FireplaceQu`
  - `GarageType`
  - `GarageYrBlt`
  - `PoolQC`
  - `Fence`
  - `MiscFeature`

## 初期のモデリング上の含意

- `Id` は基本的に識別子なので、そのまま特徴量に使う必要は薄い
- 評価指標が `RMSLE` なので、`SalePrice` に `log1p` をかけて学習し、予測時に戻す構成は自然
- 数値列とカテゴリ列が混在しているため、前処理パイプラインを最初に安定させる価値が高い
- 欠損は「未知」ではなく「設備なし」を意味する列が含まれる可能性があり、機械的な一律補完は危険
- 外れ値の影響が大きい可能性があるので、`GrLivArea` や面積系・価格系の分布確認は早めにやりたい

## 注意点とリスク

- 指標ずれ:
  - 学習中に `RMSE` や `MAE` だけを見ると、本番評価とズレる
  - ローカル CV でも `RMSLE` 相当で比較したい
- 前処理リーク:
  - 欠損補完、標準化、エンコードを train/test 全体でまとめて fit しない
- 外れ値依存:
  - 少数の極端な物件が CV を不安定にする可能性がある
- 高次元化:
  - One-Hot を広くかけると列数が増えやすい
  - 小規模データなので、複雑化の割に安定改善しない可能性がある

## 当面の作業前提

- 最初は再現可能な `exp001` ベースラインを優先する
- まずは `KFold` を仮置きの CV として始める
- 変更は 1 実験につき 1 仮説に絞る
- 改善候補は、欠損処理、対数変換、カテゴリ処理、面積系の集約特徴から順に見る

## 最初のベースライン案

- 目的変数:
  - `log1p(SalePrice)`
- 前処理:
  - 数値列は単純補完
  - カテゴリ列は最頻値補完 + One-Hot Encoding
- モデル候補:
  - LightGBM
  - XGBoost
  - 比較用に Ridge か ElasticNet を 1 本置くのもあり
- 評価:
  - `KFold` で fold ごとの score、mean、std を確認する

## 次に確認したいこと

- `train.csv` と `test.csv` の shape
- `SalePrice` の歪み具合
- 欠損率の高い列が何か
- train/test で分布差が強い列があるか
- 最初の CV と Public LB がどれくらい整合するか
