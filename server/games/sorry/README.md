# Sorry Developer Notes

This package implements the `sorry` board game using the Classic `00390` rules
profile as the current baseline.

## Module map

- `game.py`: game integration (turn flow, actions, menus, keybinds, bot ticks).
- `state.py`: serializable game/player/pawn state plus deck/track helpers.
- `rules.py`: rules-profile interface and classic ruleset declaration.
- `moves.py`: legal move generation and move application.
- `bot.py`: deterministic move chooser over legal move candidates.

## Core invariants

- Each player has exactly 4 pawns with mutually exclusive zones:
  `start`, `track`, `home_path`, `home`.
- A player's own pawns cannot share a track position or home-path step.
- Entry to `home` requires exact count (no overshoot).
- Turn flow is phase-based:
  `draw -> choose_move (if needed) -> end/advance`.
- Card `2` grants another turn after resolving the move.

## Action and keybind behavior

- Turn actions are `draw_card` and generated `move_slot_<n>` entries.
- `move_slot` actions are generated up to `max_move_slots` (currently `64`) so
  high-branching states (notably card `11` swap combinations in 4-player games)
  are not truncated.
- Keybinds:
  - `d` and `space` -> `draw_card`
  - `1` through `9` -> `move_slot_1` through `move_slot_9`

## Extension points

- Add new editions by implementing `SorryRulesProfile` and routing game options
  to select the profile.
- Keep `moves.py` deterministic for a given state/card/profile.
- Add tests for new card semantics, persistence, and bot behavior before adding
  profile toggles to the UI.
