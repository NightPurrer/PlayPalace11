# Sorry Profiles Implementation Plan (2026-02-19)

## Inputs

- Design doc: `docs/plans/2026-02-19-sorry-profiles-design.md`
- Existing implementation: `server/games/sorry/`
- Existing classic tests:
  - `server/tests/test_sorry.py`
  - `server/tests/test_sorry_moves.py`
  - `server/tests/test_sorry_turns.py`
  - `server/tests/test_sorry_bot.py`
  - `server/tests/test_sorry_play.py`

## Scope for This Plan

- Add profile-selectable Sorry rules for:
  - `classic_00390` (existing, preserved)
  - `a5065_core` (new)
- Add `rules_profile` table option for new games.
- Keep existing/saved games on classic by default unless explicitly configured otherwise.
- Track `a5065_fire_ice` as blocked follow-up (no implementation in this plan).

## Success Criteria

- New Sorry tables can select classic or A5065 core profile.
- Classic behavior remains unchanged and existing Sorry tests continue to pass.
- A5065 core behavior is implemented with profile-specific tests.
- Save/load preserves selected rules profile.
- Full server test suite passes.

## Milestone 1: Rules Interface Refactor (Parity Lock)

### Work

- Expand `SorryRulesProfile` in `server/games/sorry/rules.py`:
  - metadata (`profile_id`, `display_name`, `pawns_per_player`)
  - card and policy hooks used by move generation and turn flow
- Keep `Classic00390Rules` explicitly returning current classic behavior.
- Update call sites to consume profile policy methods without altering behavior.

### Exit Criteria

- No functional behavior changes for classic.
- Existing classic Sorry tests pass unchanged.

## Milestone 2: Option + Serialization Wiring

### Work

- Add `rules_profile` option to `SorryOptions` in `server/games/sorry/game.py`.
- Add localized labels/change messages for rules profile option.
- Ensure `rules_profile_id` resolution is deterministic:
  - options value -> active profile
  - unknown/missing value -> `classic_00390` fallback
- Preserve profile id in save/load payloads.

### Exit Criteria

- New tables can choose profile in options.
- Legacy payloads missing profile still load as classic.

## Milestone 3: Profile-Aware State and Pawn Count

### Work

- Remove fixed pawn-count assumptions from `server/games/sorry/state.py` and related code paths.
- Build player pawn lists from active profile pawn count.
- Ensure `pawns_in_start` and win checks derive from actual pawn list length.

### Exit Criteria

- Classic uses 4 pawns; A5065 core uses 3 pawns.
- Win detection and counters work for both profiles.

## Milestone 4: A5065 Core Move Semantics

### Work

- Update `server/games/sorry/moves.py` and `server/games/sorry/game.py` to respect profile policies:
  - leave-start eligibility differences
  - card-2 extra-turn differences
  - `SORRY!` fallback forward-4 branch for A5065 core
  - slide semantics controlled by profile policy
- Add any required move type/model additions for new branching while preserving deterministic action IDs.

### Exit Criteria

- Legal moves and applied moves match A5065 core semantics.
- Classic legal move/apply behavior remains unchanged.

## Milestone 5: Bot Policy Compatibility

### Work

- Verify bot scoring/selection logic in `server/games/sorry/bot.py` remains profile-safe.
- Adjust heuristic assumptions tied to pawn count or classic-only move types.

### Exit Criteria

- Bot-only games complete for both profiles.
- Bots do not attempt illegal moves in either profile.

## Milestone 6: Localization

### Work

- Add/adjust localization keys in `server/locales/en/sorry.ftl` for:
  - rules profile option labels and change messages
  - any new A5065-specific move/turn announcement text
- Run locale sync workflow so all locale files stay complete.

### Exit Criteria

- Locale completeness checks pass.
- No new user-facing hardcoded strings.

## Milestone 7: Test Expansion

### Work

- Add focused unit tests for A5065 core rules profile behavior.
- Add move-generation/apply tests for profile deltas:
  - start-card eligibility
  - no extra turn on `2`
  - `SORRY!` forward-4 fallback branch
  - slide behavior differences
- Add integration/play/persistence tests for A5065 core.
- Add compatibility tests for legacy payload and unknown profile fallback.

### Exit Criteria

- Sorry-specific tests pass for both profiles.
- Regression checks for registry/category/locale completeness pass.

## Milestone 8: Stabilization and Docs

### Work

- Update `server/games/sorry/README.md` with profile selection and behavior matrix summary.
- Confirm action/keybind/menu behavior remains consistent under both profiles.
- Capture Fire/Ice as explicit blocked follow-up with required source artifact.

### Exit Criteria

- Ready-to-ship classic + A5065 core profiles.
- Fire/Ice backlog item documented as blocked by official rules text.

## Verification Commands

From repo root:

```bash
cd server && uv run pytest -q tests/test_sorry.py tests/test_sorry_moves.py tests/test_sorry_turns.py tests/test_sorry_bot.py tests/test_sorry_play.py
cd server && uv run pytest -q -k "sorry or game_registered or locale_completeness"
cd server && uv run pytest -q
```

## Deferred Follow-up

- Implement `a5065_fire_ice` as a separate profile once official rule text is available and approved.
- Revisit previously discussed custom/house-rule variants after A5065 core parity ships.
