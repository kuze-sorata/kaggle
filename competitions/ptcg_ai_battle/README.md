# PTCG AI Battle Challenge Playground

The competition workspace for the Kaggle Pokémon Trading Card Game AI Battle Challenge Playground.

## Directory layout

- `agent/`: Current submission candidate. The entry point is `main.py`.
- `decks/`: Shared deck files; experiment-specific decks live with the experiment.
- `simulator/`: Reusable local simulator setup, adapters, and evaluation harnesses.
- `experiments/`: Experiment records and per-experiment snapshots/artifacts.
- `notebooks/`: Exploratory analysis and replay inspection notebooks.
- `STATUS.md`: Shared project status and experiment reservations.
- `TODO.md`: Current work queue.

## Competition references

- [Kaggle competition](https://www.kaggle.com/competitions/the-pokemon-company-ptcg-ai-battle-challenge-playground)
- [CABT API documentation](https://matsuoinstitute.github.io/cabt/)

## Initial development policy

Start with a legal-action baseline and a local self-play harness. Add search or learning only after the baseline can complete games reliably and produce repeatable aggregate comparisons.

## Local baseline

The first milestone uses the official `kaggle-environments` CABT environment
with a fixed 60-card deck and a random agent. The environment and development
dependencies are managed by `uv`.

```powershell
uv sync --extra dev
uv run pytest -q
uv run python -m simulator.run_match --deck experiments\exp001\decks\exp001_deck.csv --seed 0 --render experiments\exp001\outputs\exp001_match.html
uv run python -m simulator.inspect_observation --deck experiments\exp001\decks\exp001_deck.csv --output experiments\exp001\outputs\exp001_observations.json
uv run python -m simulator.match_report --observations experiments\exp001\outputs\exp001_observations.json --output experiments\exp001\outputs\exp001_report.md
uv run python -m simulator.run_tournament --deck experiments\exp001\decks\exp001_deck.csv --games 100 --output experiments\exp001\outputs\exp001_random_vs_random.json
```

The submission entry point is `agent/main.py`. It is currently a safe random
baseline; strategy experiments will be added only after the simulator and
evaluation harness are stable.

For human review, open `experiments/exp001/outputs/exp001_match.html` for the
visual CABT replay and `experiments/exp001/outputs/exp001_report.md` for the
decision-by-decision text report.
