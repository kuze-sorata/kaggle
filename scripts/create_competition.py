#!/usr/bin/env python3
"""ベーステンプレートから新しいコンペ用ワークスペースを作成する。"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
COMPETITIONS = ROOT / "competitions"


def slugify(name: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "_", name.strip())
    return slug.strip("._-")


def initialize_readme(target: Path, competition_name: str, template_name: str) -> None:
    readme = target / "README.md"
    readme.write_text(
        f"# {competition_name}\n\n"
        f"テンプレート: `{template_name}`\n\n"
        "## 使い始める前の確認\n\n"
        "- repo ルートの `AGENTS.md` と `AGENTS/` の親子運用ルールを読む\n"
        "- `STATUS.md` を最初に確認し、baseline と experiment id を共有台帳として扱う\n"
        "- Python 作業は必ずこのディレクトリの `.venv` を使う\n\n"
        "## 初期セットアップ\n\n"
        "```bash\n"
        f"cd competitions/{competition_name}\n"
        "python3 -m venv .venv\n"
        "source .venv/bin/activate\n"
        "pip install -r requirements.txt\n"
        "```\n\n"
        "## 実験管理\n\n"
        "- 実験一覧は `experiments/index.md`\n"
        "- 実験の詳細は `experiments/expXXX.md`\n"
        "- 並列実験の共有台帳は `STATUS.md`\n"
        "- 実装は `src/` に置く\n"
        "- やることは `TODO.md` に残す\n",
        encoding="utf-8",
    )


def initialize_todo(target: Path) -> None:
    todo = target / "TODO.md"
    todo.write_text(
        "# TODO\n\n"
        "- [ ] 問題理解を整理する\n"
        "- [ ] 初回ベースラインを実行する\n"
        "- [ ] CV 設計を固定する\n"
        "- [ ] EDA から改善仮説を作る\n"
        "- [ ] 仮説を 1 件ずつ追加して比較する\n"
        "- [ ] モデル比較を 1 回以上行う\n"
        "- [ ] 提出と LB 記録を紐づける\n"
        "- [ ] 必要なら CV と LB のズレを点検する\n"
        "- [ ] 正式 baseline を決めて締めの記録を残す\n",
        encoding="utf-8",
    )


def initialize_status(target: Path) -> None:
    status = target / "STATUS.md"
    status.write_text(
        f"# {target.name} Parallel Run Status\n\n"
        "## Purpose\n\n"
        "このファイルは、複数の Codex やサブエージェントで並列に仮説検証するときの共有ハブとして使う。\n"
        "会話ではなく、このファイルを最新の作業前提として扱う。\n\n"
        "## Current Baseline\n\n"
        "- Baseline experiment: `exp001`\n"
        "- Baseline feature set: `TBD`\n"
        "- Baseline CV: `TBD`\n"
        "- Baseline LB: `TBD`\n"
        "- Baseline status: `bootstrap stage`\n\n"
        "## Experiment ID Reservation\n\n"
        "- Next available experiment id: `exp002`\n"
        "- Reservation rule:\n"
        "  - 親エージェントが実験を始める前に、この欄で番号を予約する\n"
        "  - 1 つの実験番号を複数の Codex で共有しない\n"
        "  - notebook, submission, experiment log は同じ実験番号でそろえる\n"
        "  - 子エージェントは自分で experiment id を採番しない\n\n"
        "## Parent Workflow\n\n"
        "1. 親が `Current Baseline` と `Next available experiment id` を確認する\n"
        "2. 親が `Active Assignments` に owner、仮説、write scope、status を記入する\n"
        "3. 親が `Next available experiment id` を次の未使用番号へ進める\n"
        "4. 子は `Active Assignments` の割り当てを確認してから着手する\n"
        "5. 子は notebook、submission、experiment log を更新し、結果を親へ返す\n"
        "6. 親が `STATUS.md`、`experiments/index.md`、必要なら `src/` を更新する\n\n"
        "## Active Assignments\n\n"
        "- None\n\n"
        "### Assignment Template\n\n"
        "- Owner: `Codex-A`\n"
        "  - Reserved experiment: `exp002`\n"
        "  - Hypothesis: `add feature X on top of exp001`\n"
        "  - Write scope: `notebooks/exp002_feature_x.ipynb`, `experiments/exp002.md`, `submissions/exp002_feature_x.csv`\n"
        "  - Status: `reserved`\n\n"
        "### Status Labels\n\n"
        "- `reserved`: 親が予約し、まだ子が実行を始めていない\n"
        "- `running`: 子が実験中\n"
        "- `done`: 子が notebook と experiment log を更新し、親への返却待ちまたは返却済み\n"
        "- `closed`: 親が結果を回収し、台帳反映まで完了した\n\n"
        "## Decision Rules\n\n"
        "- 各 Codex は、原則として notebook と experiment log までを担当する\n"
        "- `src/` の正式更新は親担当だけが行う\n"
        "- 新しい仮説は、現在の baseline に対して 1 変更だけ加えて比較する\n"
        "- 採用判断は CV を主とし、LB は補助として扱う\n"
        "- 実験完了後は `experiments/index.md` を更新してから次に進む\n\n"
        "## Handoff Format\n\n"
        "- Result summary:\n"
        "  - Experiment: `expXXX`\n"
        "  - Hypothesis: `...`\n"
        "  - CV mean/std: `...`\n"
        "  - LB: `...` or `TBD`\n"
        "  - Decision: `adopt` / `hold` / `reject`\n"
        "  - Notes: `...`\n\n"
        "## Current Notes\n\n"
        "- `exp001` の baseline が固まるまでは bootstrap stage として扱う\n",
        encoding="utf-8",
    )


def initialize_experiments(target: Path) -> None:
    experiments = target / "experiments"
    experiments.mkdir(parents=True, exist_ok=True)

    (experiments / "index.md").write_text(
        "# 実験一覧\n\n"
        "| Exp    | 日付       | トピック   | CV Score | LB Score | ステータス          | メモ             |\n"
        "| ------ | ---------- | ---------- | -------- | -------- | ------------------- | ---------------- |\n"
        "| exp001 | YYYY-MM-DD | ベースライン | TBD      | TBD      | 完了 / 進行中       | 初回ベースライン |\n",
        encoding="utf-8",
    )

    (experiments / "exp001.md").write_text(
        "# exp001 - ベースライン\n\n"
        "## 日付\n\n"
        "YYYY-MM-DD\n\n"
        "## コンペ名\n\n"
        "## 目的\n\n"
        "最初の再現可能なベースラインを作る。\n\n"
        "## 仮説\n\n"
        "シンプルなベースラインモデルを作ることで、データの基本構造と検証時の挙動が見える。\n\n"
        "## 理由\n\n"
        "複雑な特徴量やモデルを入れる前に、信頼できる基準点が必要。\n\n"
        "## 変更内容\n\n"
        "* ベースライン前処理を作成した\n"
        "* 初期モデルを構築した\n"
        "* 最初の提出ファイルを生成した\n\n"
        "## 検証設計\n\n"
        "CV の戦略と、その戦略が妥当な理由を書く。\n\n"
        "## CV スコア\n\n"
        "TBD\n\n"
        "## LB スコア\n\n"
        "TBD\n\n"
        "## 気づき\n\n"
        "*\n\n"
        "## 問題点 / リスク\n\n"
        "* リークの可能性:\n"
        "* 分布ずれ:\n"
        "* 検証との不一致:\n\n"
        "## 次のアクション\n\n"
        "*\n",
        encoding="utf-8",
    )

    (experiments / "archive").mkdir(parents=True, exist_ok=True)
    archive_keep = experiments / "archive" / ".gitkeep"
    if not archive_keep.exists():
        archive_keep.write_text("", encoding="utf-8")


def create_competition(name: str, template_name: str) -> Path:
    template_dir = TEMPLATES / template_name
    if not template_dir.exists():
        raise FileNotFoundError(f"テンプレートが見つかりません: {template_dir}")

    competition_name = slugify(name)
    if not competition_name:
        raise ValueError("コンペ名には、少なくとも1文字の有効な文字を含めてください。")

    target = COMPETITIONS / competition_name
    if target.exists():
        raise FileExistsError(f"コンペ用ディレクトリは既に存在します: {target}")

    shutil.copytree(template_dir, target)
    initialize_readme(target, competition_name, template_name)
    initialize_todo(target)
    initialize_status(target)
    initialize_experiments(target)
    return target


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="作成するコンペ用ディレクトリ名")
    parser.add_argument(
        "--template",
        default="tabular_baseline",
        help="templates/ 配下のテンプレート名。既定値: tabular_baseline",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    COMPETITIONS.mkdir(parents=True, exist_ok=True)
    target = create_competition(args.name, args.template)
    print(f"コンペ用ワークスペースを作成しました: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
