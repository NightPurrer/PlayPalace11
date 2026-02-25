# Sorry Classic Implementation Plan (2026-02-19)

## Inputs

- Design doc: `docs/plans/2026-02-19-sorry-classic-design.md`
- Baseline rules: Classic Hasbro `00390`

## Success Criteria

- New game appears in game registry and can be created/played.
- Human gameplay supports complete classic flow and victory.
- Basic bots can complete full games.
- `auto_apply_single_move` and `faster_setup_one_pawn_out` options work.
- Unit + play/persistence tests pass in server suite.

## Milestone 1: Scaffold and Registration

### Work

- Create:
  - `server/games/sorry/__init__.py`
  - `server/games/sorry/game.py`
  - `server/games/sorry/state.py`
  - `server/games/sorry/rules.py`
  - `server/games/sorry/moves.py`
  - `server/games/sorry/bot.py`
- Register `sorry` in game registry.
- Add minimal game metadata (`get_name`, `get_type`, players min/max, options schema).

### Exit criteria

- Server starts and can instantiate Sorry table.
- No import cycles and no startup errors.

## Milestone 2: State and Board Model

### Work

- Implement serializable dataclasses for:
  - deck/discard
  - per-player pawn state
  - turn phase and current card
  - options and game outcome fields
- Encode board coordinate model used by legal-move engine:
  - start zones
  - track spaces
  - safety/home paths
  - home slots
- Implement deck build/shuffle/reshuffle helpers.

### Exit criteria

- State can serialize/deserialize cleanly.
- Board position helpers cover all location types without ambiguity.

## Milestone 3: Rules Profile + Legal Move Engine

### Work

- Define `SorryRulesProfile` interface and `Classic00390Rules`.
- Implement legal move generation for all classic cards:
  - `1,2,3,4,5,7,8,10,11,12,SORRY!`
- Implement split-7 computation and validation.
- Implement exact-home entry checks.
- Implement swap and `SORRY!` targeting constraints.
- Implement slide detection and resulting captures.

### Exit criteria

- Given a game snapshot + drawn card, legal move list is deterministic and valid.
- Edge-case unit tests pass for card semantics.

## Milestone 4: Turn Flow and Actions

### Work

- Implement turn phases:
  - draw
  - choose/apply move
  - resolve side effects
  - end/advance turn
- Add action handlers and menu wiring:
  - `Draw card`
  - generated legal-move actions
  - read-only status actions
- Implement option handling:
  - `auto_apply_single_move`
  - `faster_setup_one_pawn_out`
- Add `2`-card extra-turn behavior.

### Exit criteria

- Human players can complete a full game with correct turn control.
- No dead-end states in turn progression.

## Milestone 5: Bot Policy

### Work

- Implement basic deterministic bot strategy:
  1. winning move
  2. capture move
  3. leave start
  4. safer progress
  5. max-progress fallback
- Ensure bot operates only from legal move list.

### Exit criteria

- Bot-only games complete consistently.
- Bot never attempts illegal actions.

## Milestone 6: Localization and User Messaging

### Work

- Add `server/locales/en/sorry.ftl`.
- Add gameplay strings:
  - turn prompts
  - draw announcements
  - move/capture/slide/swap results
  - invalid move feedback
  - victory/summary lines
- Run locale sync workflow to propagate new game file to all locales.

### Exit criteria

- Locale completeness checks pass.
- No hard-coded user-facing strings remain in game logic.

## Milestone 7: Test Suite

### Work

- Add focused unit tests:
  - per-card movement semantics
  - split-7
  - 10 forward/backward
  - 11 swap
  - `SORRY!`
  - slide/capture
  - exact-home
  - reshuffle behavior
- Add integration/play tests:
  - bot-vs-bot completion
  - save/load persistence during progression
- Add option toggle tests.

### Exit criteria

- `cd server && uv run pytest` passes for new and existing tests.

## Milestone 8: Stabilization and Documentation

### Work

- Verify CLI/manual play with mixed human/bot tables.
- Add concise game-specific developer notes where needed.
- Ensure consistent keybind and action-menu behavior with existing games.

### Exit criteria

- Sorry is shippable as a normal registered game.
- No regressions found in adjacent game infrastructure tests.

## Recommended Execution Order

1. Milestones 1-2
2. Milestone 3
3. Milestone 4
4. Milestone 7 (early subset for fast feedback)
5. Milestone 5
6. Milestones 6-8
7. Final full server test run

## Verification Commands

From repo root:

```bash
cd server && uv sync
cd server && uv run pytest -q
cd server && uv run pytest -q -k "sorry"
```

If using nix shell helpers:

```bash
./scripts/nix_server_pytest.sh
```
