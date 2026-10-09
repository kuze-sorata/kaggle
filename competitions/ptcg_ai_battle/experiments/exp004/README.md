# exp004 artifacts

`experiments/exp004.md` is the canonical experiment record.

- `agent/`: count-random selection agent and its local deck helpers
- `decks/`: fixed deck shared with the previous experiments
- `outputs/`: tournament summaries in JSON and CSV form
- `run_evaluation.py`: four-condition comparison with the current random baseline

The current max-count random behavior remains in the shared `agent/` package.
