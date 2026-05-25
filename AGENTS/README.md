# Agent Roles

このディレクトリは、並列実験で使う親エージェントと子エージェントの役割を分けて置くための補助文書です。  
全体ルールはルートの `AGENTS.md` を優先し、ここでは親子運用の実務だけを補足します。

## Files

- `parent.md`
  - 親エージェントの責務
  - baseline 管理、実験番号予約、子への割り当て、結果統合、正式コード反映
- `child.md`
  - 子エージェントの責務
  - 個別仮説の notebook 実装、実行、実験ログ更新

## How To Use

- 親を使うときは、最初に `AGENTS.md` と `AGENTS/parent.md` を読む
- 子を使うときは、最初に `AGENTS.md` と `AGENTS/child.md` を読む
- コンペごとの現在地は `competitions/<competition_name>/STATUS.md` を見る
- 親が `STATUS.md` で experiment id を予約し、子へ割り当ててから実験を始める
- 子は `STATUS.md` に自分の割り当てがない状態では新規実験を開始しない
