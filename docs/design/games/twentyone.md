# 21 (Survival Rules)

## Status

Implemented in `server/games/twentyone.py`.

## Overview

- Type: card game
- Players: 2
- Mode: head-to-head HP battle
- Base target: `21` (can be changed by target modifiers)
- Damage: loser of a round takes damage equal to their current bet

## Round Flow

1. Both players receive 2 number cards.
2. First dealt card is hidden (private), second dealt card is face-up (public).
3. Turn actions:
- `hit`: draw a number card
- `play_modifier`: play one modifier from hand
- `stand`: mark as standing
4. Turn does not pass on `hit` or `play_modifier`.
5. Turn passes only when the current player chooses `stand`.
6. Round resolves only after both players stand consecutively.
- Any non-stand card action between stands resets pending stands.
7. Round winner is decided by closest to target with bust rules.

## Visibility Rules

- Hidden:
- Each player's first dealt card (hole card)
- All modifier cards in hand
- Public:
- Each player's second dealt card
- Number cards drawn after the initial deal
- Active table effects
- Private readouts are available for hand/modifier details.

## Deck Rules

- There is no discard pile.
- If a modifier removes a face-up card from a hand, that card is placed on top of the deck.
- This applies to both opponent and self removals where relevant.

## Bets And Damage

- Bet starts from `base_bet` and is modified by active table effects.
- `Stake Raise` effects increase incoming damage to the opponent.
- `Guard` effects reduce incoming damage to the player.
- At round settle, the loser takes damage equal to their computed current bet.

## Modifier Summary

### Bet/Defense Effects

- `Stake Raise 1`: Opponent damage +1; gain 1 random modifier.
- `Stake Raise 2`: Opponent damage +2; gain 1 random modifier.
- `Stake Raise 2+`: Opponent damage +2; return opponent last face-up card to top of deck; gain 1 random modifier.
- `Guard`: Reduce incoming damage by 1 while active.
- `Guard+`: Reduce incoming damage by 2 while active.
- `Precision Draw+`: Precision draw and increase opponent damage by 5 while active.

### Exact Draw Effects

- `Exact 2`, `Exact 3`, `Exact 4`, `Exact 5`, `Exact 6`, `Exact 7`: draw that exact number if available.

### Card/Effect Control

- `Scrap Card`: Return opponent last face-up card to top of deck.
- `Recycle Card`: Return opponent last face-up card to top of deck.
- `Swap Draw`: Both players remove their own last face-up card, both draw one, removed cards go to top of deck.
- `Break Effect`: Destroy opponent newest table effect.
- `Break All`: Destroy all opponent table effects.
- `Lockdown`: Clear opponent table effects and prevent opponent playing modifiers while active.

### Modifier Economy

- `Redraft`: Discard 2 random modifiers; gain 3 random modifiers.
- `Redraft+`: Discard 1 random modifier; gain 4 random modifiers.
- `Salvage`: Whenever any modifier is played, gain 1 random modifier while active.
- `Prime Draw`: Precision draw and gain 2 random modifiers.

### Target Control

- `Target 17`: Set round target to 17.
- `Target 24`: Set round target to 24.
- `Target 27`: Set round target to 27.

### Opponent Assistance

- `Aid Rival`: Opponent draws their best available card for the current target.

## Keybinds

- `1`: Hit
- `2`: Stand
- `3`: Play modifier
- `4`: Check 21 status
- `M`: Modifier guide
- `O`: Read opponent face-up cards
- `R`: Read current hand
- `B`: Read current bets
- `E`: Read active modifier effects

Note:
- Global/common table keybinds from base systems still apply.

## Test Coverage

Covered by `server/tests/test_twentyone.py`, including:

- Hidden/public card visibility rules
- Turn and stand-resolution behavior
- Modifier visibility and playability
- Keybind mappings and readout actions
- Top-of-deck return behavior for removed face-up cards
- Bot play with save/reload round-trip
