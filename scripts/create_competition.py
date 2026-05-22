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
