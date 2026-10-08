# PTCG AI Battle Challenge Playground

The competition workspace for the Kaggle Pokémon Trading Card Game AI Battle Challenge Playground.

## Directory layout

- `agent/`: Submission agent code. The entry point will be `main.py`.
- `decks/`: Deck lists, card ID references, and deck-selection experiments.
- `simulator/`: Local simulator setup, adapters, and evaluation harnesses.
- `experiments/`: Competition-specific experiment records.
- `notebooks/`: Exploratory analysis and replay inspection notebooks.
- `STATUS.md`: Shared project status and experiment reservations.
- `TODO.md`: Current work queue.

## Competition references

- [Kaggle competition](https://www.kaggle.com/competitions/the-pokemon-company-ptcg-ai-battle-challenge-playground)
- [CABT API documentation](https://matsuoinstitute.github.io/cabt/)

## Initial development policy

Start with a deterministic, legal-action baseline and a local self-play harness. Add search or learning only after the baseline can complete games reliably and produce reproducible evaluation results.
