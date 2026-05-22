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
        "## 実験管理\n\n"
        "- 実験一覧は `experiments/index.md`\n"
        "- 実験の詳細は `experiments/expXXX.md`\n"
        "- 実装は `src/` に置く\n"
        "- やることは `TODO.md` に残す\n",
        encoding="utf-8",
    )


def initialize_todo(target: Path) -> None:
    todo = target / "TODO.md"
    todo.write_text(
        "# TODO\n\n"
        "- [ ] 初回ベースラインを実行する\n"
        "- [ ] CV と LB の差分を確認する\n"
        "- [ ] 改善仮説を 1 つ以上追加する\n",
        encoding="utf-8",
    )


def initialize_experiments(target: Path) -> None:
    experiments = target / "experiments"
    experiments.mkdir(parents=True, exist_ok=True)

    (experiments / "index.md").write_text(
        "# Experiments\n\n"
        "| Exp    | Date       | Topic    | CV Score | LB Score | Status           | Notes            |\n"
        "| ------ | ---------- | -------- | -------- | -------- | ---------------- | ---------------- |\n"
        "| exp001 | YYYY-MM-DD | Baseline | TBD      | TBD      | Done/In Progress | Initial baseline |\n",
        encoding="utf-8",
    )

    (experiments / "exp001.md").write_text(
        "# exp001 - Baseline\n\n"
        "## Date\n\n"
        "YYYY-MM-DD\n\n"
        "## Competition\n\n"
        "## Objective\n\n"
        "Create the first reproducible baseline.\n\n"
        "## Hypothesis\n\n"
        "A simple baseline model will reveal the basic data structure and validation behavior.\n\n"
        "## Why\n\n"
        "Before adding complex features or models, we need a reliable benchmark.\n\n"
        "## Changes\n\n"
        "* Created baseline preprocessing\n"
        "* Built initial model\n"
        "* Generated first submission\n\n"
        "## Validation Design\n\n"
        "Describe the CV strategy and why it is appropriate.\n\n"
        "## CV Score\n\n"
        "TBD\n\n"
        "## LB Score\n\n"
        "TBD\n\n"
        "## Findings\n\n"
        "*\n\n"
        "## Problems / Risks\n\n"
        "* Possible leakage:\n"
        "* Distribution shift:\n"
        "* Validation mismatch:\n\n"
        "## Next Actions\n\n"
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
