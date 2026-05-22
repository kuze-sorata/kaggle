#!/usr/bin/env python3
"""Kaggle CLI を使ってコンペデータをダウンロードする。"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("competition", help="Kaggle のコンペ名")
    parser.add_argument(
        "--target",
        default=None,
        help="保存先ディレクトリ。省略時は competitions/<competition>/data",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="保存先が既にあっても続行する",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    kaggle = shutil.which("kaggle")
    if kaggle is None:
        print("kaggle CLI が見つかりません。先に Kaggle API クライアントを用意してください。", file=sys.stderr)
        return 1

    target = Path(args.target) if args.target else Path("competitions") / args.competition / "data"
    if target.exists() and not args.force:
        print(f"保存先は既に存在します: {target}", file=sys.stderr)
        print("--force を付けるか、別の保存先を指定してください。", file=sys.stderr)
        return 1

    target.mkdir(parents=True, exist_ok=True)

    command = [kaggle, "competitions", "download", "-c", args.competition, "-p", str(target)]
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        return completed.returncode

    archive = target / f"{args.competition}.zip"
    if archive.exists():
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(target)
        archive.unlink()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
