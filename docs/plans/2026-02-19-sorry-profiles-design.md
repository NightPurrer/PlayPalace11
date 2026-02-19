# Sorry Profiles Design (2026-02-19)

## Status

Approved design for implementation planning.

## Objective

Extend `Sorry` from a single classic profile to a profile-selectable game that supports:

- Existing `classic_00390` behavior without regressions.
- New official `a5065_core` profile with full parity target.
- Future `a5065_fire_ice` support as a planned follow-up profile.

## Decisions Captured

- Use profile-driven architecture (single shared engine; profile policy hooks).
- Add table-level `rules_profile` selection option for new games.
- Existing/saved games remain on classic unless explicitly created with another profile.
- Target full parity for `a5065_core`.
- Keep "other discussed rules" out of this implementation scope and track as follow-up.
- Treat Fire/Ice as planned but blocked until official rule text is available.

## Scope

### In scope

- Implement selectable `rules_profile` for `Sorry`.
- Implement `a5065_core` profile.
- Preserve `classic_00390` behavior.
- Add tests for profile selection, profile-specific move semantics, bot play, and persistence.
- Add required localization for profile labels and new move messages.

### Out of scope

- Implementing Fire/Ice mechanics.
- Bundling additional house rules from earlier brainstorming discussions.
- Client protocol changes.

## Profile Strategy

Use one shared game engine with profile-level behavior controls.

### Profile IDs

- `classic_00390` (default; existing)
- `a5065_core` (new; implemented in this phase)
- `a5065_fire_ice` (reserved; planned, not implemented)

### Selection behavior

- New tables: host selects profile in game options.
- Existing saves: preserve stored profile.
- Missing profile in legacy payload: default to `classic_00390`.

## Architecture Changes

### Rules interface expansion

Expand `SorryRulesProfile` to include explicit behavior policy, not only `card_faces()`.
Expected additions include:

- profile metadata (`profile_id`, `display_name`)
- profile pawn count (`pawns_per_player`)
- start-card eligibility policy
- card-2 extra-turn policy
- `SORRY!` fallback policy
- slide behavior policy
- optional deck composition policy if profile decks differ

### Engine ownership

- `game.py`: keep orchestration, actions, turn control, persistence wiring.
- `moves.py`: keep legal-move generation/application, but remove hardcoded classic assumptions by calling profile policy methods.
- `rules.py`: define `Classic00390Rules` and `A5065CoreRules`.

### Data model and serialization

- Replace fixed pawn-count assumptions with profile-driven pawn creation at game start.
- Persist selected profile id.
- Legacy payload compatibility:
  - missing profile -> classic
  - unknown profile -> safe fallback to classic

## Semantics Matrix

### Pawn count

- `classic_00390`: 4 pawns/player
- `a5065_core`: 3 pawns/player

### Leave-start eligibility

- `classic_00390`: cards `1` and `2` only
- `a5065_core`: any card with forward value (subject to legal destination checks)

### Card `2` turn behavior

- `classic_00390`: grants extra turn
- `a5065_core`: no extra turn

### `SORRY!` behavior

- `classic_00390`: replace opponent from start
- `a5065_core`: same primary behavior, with profile-gated fallback branch to move forward 4 when no valid replacement target exists

### Slides

- Keep classic slide semantics for `classic_00390`.
- Implement `a5065_core` slide semantics through profile policy hooks.

### Unchanged unless profile policy says otherwise

- split 7 model
- 10 forward/back branch
- 11 forward/swap model
- exact-home requirement
- deterministic legal move sorting
- discard reshuffle behavior

## UI and Option Behavior

- Add `rules_profile` option in `SorryOptions`.
- Keep current action IDs and keybind pattern (`draw_card`, `move_slot_<n>`).
- Keep default profile as classic.
- Do not expose `a5065_fire_ice` in user-facing options yet.

## Error Handling and Safety

- Unknown profile id: use classic fallback rather than crash.
- Profile/card mismatch: produce no legal moves for unsupported branch, preserving deterministic flow.
- Preserve current invalid move protection in `apply_move`, adding checks for any new move type.

## Localization

Add/update locale keys for:

- rules-profile option labels
- profile change confirmation strings
- any new profile-specific move labels/announcements

Run locale completeness propagation after keys are introduced.

## Test Strategy

### Unit tests

- Profile method behavior tests (`classic_00390`, `a5065_core`).
- Profile-specific legal move generation:
  - start eligibility differences
  - card-2 extra-turn differences
  - `SORRY!` fallback behavior
  - slide policy differences

### Integration and play tests

- A5065 core turn flow
- bot-vs-bot completion under A5065 core
- save/load cycle preserving selected profile and behavior

### Compatibility tests

- legacy payload missing profile -> classic
- unknown profile id -> safe fallback
- option exposure/registry behavior for selectable profiles

## Rollout Milestones

1. Refactor rules interface and lock classic parity.
2. Add profile selection option and serialization support.
3. Implement A5065 core behavior deltas.
4. Add localization and profile-specific tests.
5. Document and track `a5065_fire_ice` as blocked follow-up.

## Exit Criteria

- Full server test suite passes.
- Existing classic tests remain green.
- New A5065 core tests pass for rules, flow, bots, and persistence.
- No client protocol changes are required.

## Follow-up Backlog

- Implement `a5065_fire_ice` once official rules text is available.
- Resume "other discussed rules" after A5065 core parity is shipped.
