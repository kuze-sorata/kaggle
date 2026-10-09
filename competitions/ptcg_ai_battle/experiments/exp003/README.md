# exp003 artifacts

`experiments/exp003.md` is the canonical experiment record.

- `agent/`: energy-first heuristic and its local baseline helpers
- `decks/`: fixed deck copied from exp002
- `outputs/`: tournament summaries in JSON and CSV form
- `run_evaluation.py`: evaluation against random and exp002

The configured energy card ID is experiment-specific because the deck is fixed.
Reusable CABT execution and tournament aggregation remain in `simulator/`.
