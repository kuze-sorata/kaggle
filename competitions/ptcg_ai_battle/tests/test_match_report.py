from simulator.match_report import render_report


def test_match_report_contains_result_and_choice() -> None:
    payload = {
        "match": {"outcome": "agent0_win", "statuses": ["DONE", "DONE"]},
        "players": [
            {
                "observations": [
                    {"step": 1, "current": None, "select": None},
                    {
                        "step": 2,
                        "current": {
                            "turn": 1,
                            "players": [
                                {"active": [], "bench": [], "handCount": 7, "deckCount": 53, "prize": []},
                            ],
                        },
                        "select": {
                            "type": 9,
                            "context": 41,
                            "option": [{"type": 1}, {"type": 2}],
                        },
                    },
                ],
                "actions": [[1, 2], [0]],
            }
        ],
    }
    report = render_report(payload)
    assert "agent0_win" in report
    assert "デッキ登録" in report
    assert "YES/NO" in report
