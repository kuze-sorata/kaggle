# Observation schema (exp001)

This document records the fields observed by the local random agent during
`exp001`. It describes the data actually passed to the agent; it does not
claim that every possible card-effect field has been catalogued.

## Top-level fields

- `select`: the current selection request, or `null` when the engine asks for
  the initial 60-card deck.
- `current`: the current board state. It is `null` during initial deck input.
- `logs`: events since the previous selection.
- `step`: the environment step number.
- `remainingOverageTime`: remaining agent overage time.
- `search_begin_input`: engine-provided search input; it was preserved as
  received and is not used by the baseline.

## Selection

When `select` is present, the baseline reads:

- `option`: the available choices. The action is a list of indices into this
  array.
- `minCount`: minimum number of choices.
- `maxCount`: maximum number of choices.
- `type`: selection category.
- `context`: detailed reason for the selection.

The agent must return a list of option indices. It must return the deck list
instead when `select` is `null` at the beginning of a battle.

## Visibility rule

The observation is recorded exactly as received by each agent. The opponent's
hand is represented by public information such as `handCount`; the local
baseline does not access hidden state through the simulator internals.
