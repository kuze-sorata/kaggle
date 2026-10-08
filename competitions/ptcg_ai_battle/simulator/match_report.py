"""Turn an observation capture into a human-readable Markdown report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SELECT_TYPES = {
    0: "メイン行動",
    1: "カード選択",
    2: "付属カード選択",
    3: "カード/付属カード選択",
    4: "エネルギー選択",
    5: "特性選択",
    6: "攻撃選択",
    7: "進化選択",
    8: "数値選択",
    9: "YES/NO",
    10: "特殊状態選択",
}

CONTEXTS = {
    0: "メイン行動",
    1: "バトル場のポケモン選択",
    2: "ベンチのポケモン選択",
    3: "入れ替え",
    4: "バトル場へ移動",
    5: "ベンチへ移動",
    6: "場に出す",
    7: "手札へ戻す",
    8: "捨てるカード選択",
    9: "山札へ戻す",
    15: "ダメージ対象",
    18: "進化元",
    19: "進化先",
    21: "付ける対象のポケモン",
    22: "付けるカード",
    41: "先攻/後攻",
    42: "引き直し",
    43: "効果を使うか",
    44: "効果を使うか",
}

OPTION_TYPES = {
    0: "数値",
    1: "YES",
    2: "NO",
    3: "カード",
    7: "使う",
    8: "付ける",
    9: "進化",
    10: "特性",
    11: "捨てる",
    12: "逃げる",
    13: "攻撃",
    14: "終了",
}


def option_label(option: dict[str, Any]) -> str:
    """Describe an option without inventing card names unavailable in the API."""

    option_type = option.get("type")
    label = OPTION_TYPES.get(option_type, f"type={option_type}")
    details: list[str] = []
    for key in ("index", "number", "attackId", "cardId", "playerIndex", "inPlayIndex"):
        if key in option:
            details.append(f"{key}={option[key]}")
    return f"{label} ({', '.join(details)})" if details else label


def player_snapshot(player: dict[str, Any]) -> str:
    active = player.get("active") or []
    if active and active[0]:
        pokemon = active[0]
        active_text = f"ID{pokemon.get('id')} HP{pokemon.get('hp')}/{pokemon.get('maxHp')}"
        energy_count = len(pokemon.get("energyCards") or [])
        if energy_count:
            active_text += f" energy={energy_count}"
    else:
        active_text = "なし"
    return (
        f"active={active_text}; bench={len(player.get('bench') or [])}; "
        f"hand={player.get('handCount')}; deck={player.get('deckCount')}; "
        f"prize={len(player.get('prize') or [])}"
    )


def decision_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for player_index, player in enumerate(payload.get("players", [])):
        observations = player.get("observations", [])
        actions = player.get("actions", [])
        for observation, action in zip(observations, actions):
            current = observation.get("current") or {}
            select = observation.get("select")
            if select is None:
                choice = "デッキ登録（60枚）"
            else:
                options = select.get("option") or []
                selected = [
                    option_label(options[index])
                    for index in action
                    if isinstance(index, int) and 0 <= index < len(options)
                ]
                choice = ", ".join(selected) if selected else "選択なし"
                select_type = SELECT_TYPES.get(
                    select.get("type"), f"type={select.get('type')}"
                )
                context = CONTEXTS.get(
                    select.get("context"), f"context={select.get('context')}"
                )
                choice = f"{select_type} / {context} / {choice}"
            players = current.get("players") or []
            snapshot = " | ".join(
                f"P{index}: {player_snapshot(state)}"
                for index, state in enumerate(players)
            )
            rows.append(
                {
                    "step": observation.get("step", ""),
                    "player": player_index,
                    "turn": current.get("turn", ""),
                    "choice": choice,
                    "snapshot": snapshot,
                }
            )
    return sorted(rows, key=lambda row: (row["step"], row["player"]))


def render_report(payload: dict[str, Any]) -> str:
    match = payload.get("match", {})
    rows = decision_rows(payload)
    lines = [
        "# PTCG AI Battle match report",
        "",
        "## 結果",
        "",
        f"- Outcome: `{match.get('outcome')}`",
        f"- Status: `{match.get('statuses')}`",
        f"- Rewards: `{match.get('rewards')}`",
        f"- BO result: `{match.get('result')}`",
        f"- Environment steps: `{match.get('steps')}`",
        f"- Recorded decisions: `{len(rows)}`",
        "",
        "## 判断の流れ",
        "",
        "カード名は現時点のローカルSDK観測に含まれないため、カードIDで表示しています。",
        "各行は、その時点でAIに見えていた盤面と、AIが選んだ選択肢です。",
        "",
        "| Step | Player | Turn | Choice | Board snapshot |",
        "|---:|---:|---:|---|---|",
    ]
    for row in rows:
        snapshot = str(row["snapshot"]).replace("|", "\\|")
        choice = str(row["choice"]).replace("|", "\\|")
        lines.append(
            f"| {row['step']} | P{row['player']} | {row['turn']} | {choice} | {snapshot} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = json.loads(args.observations.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(payload), encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
