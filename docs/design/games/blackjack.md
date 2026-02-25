# Blackjack (Design and Rules)

## Status

Implemented in `server/games/blackjack/`.

## Overview

- Type: card game
- Players: 1 to 7
- Mode: individual chips, multi-hand elimination against an always-present dealer
- Flow:
- Multiplayer: repeated hands until one player has chips remaining
- Solo: repeated hands until the player reaches 0 chips

Solo table note:
- With exactly 1 player, hands continue until the player reaches 0 chips (no immediate win state).

## Hand Flow

1. Start hand, reset player/dealer hand state.
2. Post bets (clamped by table limits and available chips).
3. Deal 2 cards to each player and dealer (dealer upcard visible).
4. If dealer upcard is Ace and insurance is enabled, run insurance phase.
5. Player action phase:
- `hit`, `stand`, `double_down`, `split`, `surrender` (when eligible)
6. Dealer phase:
- Dealer reveals hole card and draws/stands per soft-17 rule.
7. Settlement:
- Insurance/even money, blackjack payouts, wins/losses/pushes, bust/surrender handling.
8. Start the next hand while continuation conditions are met:
- Multiplayer: at least 2 players still have chips.
- Solo: the player still has chips.

## Options

### Core Economy

- `starting_chips` (default `500`)
- `base_bet` (default `10`)
- `table_min_bet` (default `5`)
- `table_max_bet` (default `100`)
- `deck_count` (default `4`)

Validation:
- `base_bet <= starting_chips`
- `table_min_bet <= table_max_bet`
- `table_min_bet <= base_bet <= table_max_bet`

### Dealer/Flow

- `dealer_hits_soft_17` (default `true`)
- `dealer_peeks_blackjack` (default `true`)
- `players_cards_face_up` (default `true`)
- `allow_insurance` (default `true`)
- `allow_late_surrender` (default `true`)
- `turn_timer` (menu, default `0` = unlimited)

Card visibility:
- `players_cards_face_up = true`: standard shoe-style visibility (all player cards/totals are public).
- `players_cards_face_up = false`: pitch-style visibility (each player can only hear their own cards/totals; others are hidden in readouts).

### Payout/Player Rules

- `blackjack_payout`:
- `3_to_2` (default)
- `6_to_5`
- `1_to_1`
- `double_down_rule`:
- `any_two` (default)
- `9_to_11`
- `10_to_11`
- `allow_double_after_split` (DAS, default `true`)
- `split_rule`:
- `same_rank` (default)
- `same_value`
- `max_split_hands` (default `2`, currently supports `1` or `2`)
- `split_aces_one_card_only` (default `true`)
- `split_aces_count_as_blackjack` (default `false`)

## Rules Profiles

Changing `rules_profile` applies a preset to related options.
`players_cards_face_up` is independent and is not changed by profile selection.

### Vegas (default)

- `dealer_hits_soft_17 = true`
- `dealer_peeks_blackjack = true`
- `allow_insurance = true`
- `allow_late_surrender = true`
- `blackjack_payout = 3_to_2`
- `double_down_rule = any_two`
- `allow_double_after_split = true`
- `split_rule = same_rank`
- `max_split_hands = 2`
- `split_aces_one_card_only = true`
- `split_aces_count_as_blackjack = false`

### European

- `dealer_hits_soft_17 = false`
- `dealer_peeks_blackjack = false`
- `allow_insurance = true`
- `allow_late_surrender = false`
- `blackjack_payout = 3_to_2`
- `double_down_rule = 9_to_11`
- `allow_double_after_split = false`
- `split_rule = same_rank`
- `max_split_hands = 2`
- `split_aces_one_card_only = true`
- `split_aces_count_as_blackjack = false`

### Friendly

- `dealer_hits_soft_17 = false`
- `dealer_peeks_blackjack = true`
- `allow_insurance = true`
- `allow_late_surrender = true`
- `blackjack_payout = 3_to_2`
- `double_down_rule = any_two`
- `allow_double_after_split = true`
- `split_rule = same_value`
- `max_split_hands = 2`
- `split_aces_one_card_only = false`
- `split_aces_count_as_blackjack = true`

## Player Actions

### Hit / Stand

- Standard blackjack behavior.
- If `split_aces_one_card_only` locked a split-ace hand, hit is disallowed for that hand.

### Double Down

Requires:
- Current hand has exactly 2 cards.
- Player has chips >= current hand bet.
- Total fits `double_down_rule`.
- If on split hand, `allow_double_after_split` must be enabled.
- If split-ace one-card lock is active on current hand, double is disallowed.

### Split

Requires:
- Main hand only (not already on split hand).
- Exactly 2 cards.
- Not already split.
- `max_split_hands > 1`.
- Player has chips >= current bet.
- Card matching per `split_rule`.

Split aces:
- If `split_aces_one_card_only = true`, both split hands auto-stand after one draw each.
- If `split_aces_count_as_blackjack = true`, two-card 21 from split-ace hands is treated as blackjack.

### Late Surrender

Requires:
- `allow_late_surrender = true`
- Main (unsplit) hand only
- Exactly 2 cards
- Not blackjack
- Hand not already completed

Effect:
- Immediately refunds half the hand bet and marks hand complete.

## Insurance and Even Money

Insurance phase is offered when:
- Dealer upcard is Ace
- `allow_insurance = true`
- At least one player is eligible for insurance/even money

Insurance:
- Available to non-blackjack main hands.
- Insurance bet is half the main bet.
- If dealer has blackjack: insurance pays 2:1 profit (3:1 returned including stake).
- Otherwise insurance is lost.

Even money:
- Available to players with natural blackjack during insurance phase.
- Locks 1:1 profit on the main bet regardless of dealer outcome.

## Settlement Rules

- Surrendered hands: no further settlement (loss already applied by half-bet surrender).
- Blackjack payout uses `blackjack_payout` mode.
- Normal win pays 1:1.
- Push returns original bet.
- Loss loses original bet.
- Insurance and even-money outcomes are handled before/within hand resolution.
- End condition:
- Multiplayer ends when only 1 player has chips left.
- Solo ends when the player reaches 0 chips.

## Blackjack-Specific Keybinds

- `Space`: Hit
- `X`: Stand
- `D`: Double down
- `P`: Split
- `S`: Surrender
- `I`: Take insurance
- `N`: Decline insurance
- `M`: Even money
- `R`: Read hand
- `C`: Read dealer
- `E`: Table status
- `Shift+R`: Read rules
- `Shift+T`: Check turn timer

Note:
- Global/common keybinds inherited from base game systems also apply.

## Readout and UX

- `read_rules` action announces active profile and all major toggles/limits.
- `table_status` includes the same rules summary plus current player/dealer status lines.
- In pitch-style visibility, `table_status` hides other players' hand totals and only reports public chip/bet info.
- Insurance phase gives explicit prompts for insurance or even money decisions.

## Test Coverage

Covered by `server/tests/test_blackjack.py`:

- Unit behavior for split/double/surrender/insurance/even-money.
- Rule-profile and rule-toggle behavior.
- Visibility mode behavior (`players_cards_face_up` true/false).
- Dealer behavior (soft 17 and peek/no-peek).
- Solo flow behavior (does not auto-win immediately, continues between hands while chips remain).
- Save/reload cycles during bot play.
- Persistence/reconnect round-trip for blackjack-specific state.
