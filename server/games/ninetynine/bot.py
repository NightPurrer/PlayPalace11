"""
Bot AI for Ninety Nine game.

Direct port of the v10 Lua bot (bot_ai.lua) to Python.
"""

from typing import TYPE_CHECKING

from ...game_utils.cards import (
    Card,
    RS_RANK_PLUS_10,
    RS_RANK_MINUS_10,
    RS_RANK_PASS,
    RS_RANK_REVERSE,
    RS_RANK_SKIP,
    RS_RANK_NINETY_NINE,
)

if TYPE_CHECKING:
    from .game import NinetyNineGame, NinetyNinePlayer

# Game constants
MAX_COUNT = 99
TWO_DIVIDE_THRESHOLD = 49


def bot_think(game: "NinetyNineGame", player: "NinetyNinePlayer") -> str | None:
    """
    Bot AI decision making.

    Args:
        game: The Ninety Nine game instance.
        player: The bot player making a decision.

    Returns:
        Action ID to execute, or None if no action available.
    """
    if game.current_player != player:
        return None

    return _bot_choose_card(game, player)


def _bot_choose_card(game: "NinetyNineGame", player: "NinetyNinePlayer") -> str | None:
    """Bot chooses which card to play."""
    if not player.hand:
        return None

    best_slot = 0
    best_score = -99999
    best_rank = 0

    # Evaluate each card
    for i, card in enumerate(player.hand):
        score = _bot_evaluate_card(game, player, card)

        # Choose card with best score, or highest rank if tied
        if score > best_score or (score == best_score and card.rank > best_rank):
            best_score = score
            best_slot = i
            best_rank = card.rank

    return f"card_slot_{best_slot + 1}"


def _bot_evaluate_card(
    game: "NinetyNineGame", player: "NinetyNinePlayer", card: Card
) -> int:
    """Evaluate a card's value for playing."""
    current_count = game.count
    rank = card.rank
    is_rs_games = not game.is_quentin_c

    # RS Games variant
    if is_rs_games:
        return _bot_eval_rs_card(game, player, current_count, rank)

    # Quentin C variant
    else:
        return _bot_eval_quentin_card(game, player, current_count, rank, card)

    return 0


def _bot_eval_rs_card(
    game: "NinetyNineGame",
    player: "NinetyNinePlayer",
    current_count: int,
    rank: int,
) -> int:
    if rank == 1:
        return _bot_evaluate_count(game, player, current_count + 1, rank)
    if rank == 2:
        return _bot_evaluate_count(game, player, current_count + 2, rank)
    if 3 <= rank <= 9:
        return _bot_evaluate_count(game, player, current_count + rank, rank)
    if rank == RS_RANK_PLUS_10:
        return _bot_evaluate_count(game, player, current_count + 10, rank)
    if rank == RS_RANK_MINUS_10:
        return _bot_evaluate_count(game, player, current_count - 10, rank)
    if rank in (RS_RANK_PASS, RS_RANK_REVERSE, RS_RANK_SKIP):
        return _bot_evaluate_count(game, player, current_count, rank)
    if rank == RS_RANK_NINETY_NINE:
        return _bot_evaluate_count(game, player, 99, rank)
    return 0


def _bot_eval_quentin_card(
    game: "NinetyNineGame",
    player: "NinetyNinePlayer",
    current_count: int,
    rank: int,
    card: Card,
) -> int:
    if rank == 1:
        score_plus_11 = _bot_evaluate_count(game, player, current_count + 11, rank)
        score_plus_1 = _bot_evaluate_count(game, player, current_count + 1, rank)
        return max(score_plus_11, score_plus_1)
    if rank == 10 and current_count < 90:
        score_plus = _bot_evaluate_count(game, player, current_count + 10, rank)
        score_minus = _bot_evaluate_count(game, player, current_count - 10, rank)
        return max(score_plus, score_minus)
    if rank == 2:
        new_count = _calculate_two_effect(current_count)
        return _bot_evaluate_count(game, player, new_count, rank)
    if rank == 9:
        return _bot_evaluate_count(game, player, current_count, rank)
    if rank == 11 and len(game.alive_players) == 2:
        return _bot_eval_two_player_jack(game, player, current_count, card)
    value = _get_card_value(rank)
    return _bot_evaluate_count(game, player, current_count + value, rank)


def _bot_eval_two_player_jack(
    game: "NinetyNineGame",
    player: "NinetyNinePlayer",
    current_count: int,
    card: Card,
) -> int:
    jack_count = sum(1 for c in player.hand if c.rank == 11)
    if jack_count < 1:
        return _bot_evaluate_count(game, player, current_count + 10, 11)
    new_count = current_count + 10
    if new_count > 99:
        return -99999
    if current_count < 33 < new_count:
        return -8000
    if current_count < 66 < new_count:
        return -8000
    remaining_hand = [c for c in player.hand if c is not card]
    return _evaluate_jack_chain(game, current_count + 10, remaining_hand)


def _bot_evaluate_count(
    game: "NinetyNineGame", player: "NinetyNinePlayer", new_count: int, rank: int
) -> int:
    """Evaluate a potential new count."""
    current_count = game.count
    is_rs_games = not game.is_quentin_c

    # Priority 1: NEVER go over 99 (instant loss!)
    if new_count > 99:
        return -99999

    alive_count = len(game.alive_players)
    is_two_player = alive_count == 2
    milestone_score = _score_quentin_milestone_transition(
        current_count, new_count, is_rs_games
    )
    if milestone_score is not None:
        return milestone_score

    is_skip_card = (rank == 11 and not is_rs_games) or (
        rank == RS_RANK_SKIP and is_rs_games
    )

    two_player_score = _score_two_player_setup(
        is_rs_games, is_two_player, is_skip_card, current_count, new_count
    )
    if two_player_score is not None:
        return two_player_score

    setup_zone_score = _score_setup_zones(is_rs_games, new_count)
    if setup_zone_score is not None:
        return setup_zone_score

    if not is_rs_games:
        trap_score = _score_quentin_trap_avoidance(player, new_count)
        if trap_score is not None:
            return trap_score

    score = 0
    score += _score_special_card_usage(is_rs_games, current_count, rank)
    score += _score_count_ranges(is_rs_games, current_count, new_count)

    return score


def _score_quentin_milestone_transition(
    current_count: int, new_count: int, is_rs_games: bool
) -> int | None:
    """Handle Quentin C milestone rewards and pass-through penalties."""
    if is_rs_games:
        return None
    if new_count in (33, 66, 99) and new_count > current_count:
        return 10000
    if current_count < 33 < new_count:
        return -8000
    if current_count < 66 < new_count:
        return -8000
    return None


def _score_two_player_setup(
    is_rs_games: bool,
    is_two_player: bool,
    is_skip_card: bool,
    current_count: int,
    new_count: int,
) -> int | None:
    """Score two-player trap setups and skip usage."""
    if not is_two_player:
        return None

    if not is_rs_games:
        if is_skip_card:
            is_danger_zone = (
                (28 <= new_count <= 32)
                or (61 <= new_count <= 65)
                or (88 <= new_count <= 98)
                or new_count in (23, 56, 89)
            )
            if is_danger_zone:
                return -5000

        if new_count in (31, 97):
            return 7000
        if new_count == 64:
            return 3000
        return None

    if is_skip_card and 88 <= new_count <= 98:
        return -5000
    if new_count == 97:
        return 7000
    return None


def _score_setup_zones(is_rs_games: bool, new_count: int) -> int | None:
    """Reward setup-zone positioning for Quentin C regardless of player count."""
    if is_rs_games:
        return None
    if (29 <= new_count <= 32) or (62 <= new_count <= 65) or (95 <= new_count <= 98):
        return 5000
    return None


def _score_quentin_trap_avoidance(
    player: "NinetyNinePlayer", new_count: int
) -> int | None:
    """Avoid trap setups if holding multiple +10 cards."""
    if new_count not in (23, 56, 89):
        return None
    plus_ten_count = sum(1 for c in player.hand if c.rank in (10, 11, 12, 13))
    if plus_ten_count >= 2:
        return -3000
    return None


def _score_special_card_usage(
    is_rs_games: bool, current_count: int, rank: int
) -> int:
    """Score special card usage relative to danger zones."""
    score = 0
    if is_rs_games:
        in_danger_zone = current_count >= 85
        if not in_danger_zone:
            if rank == RS_RANK_PASS:
                score -= 400
            elif rank == RS_RANK_SKIP:
                score -= 400
            elif rank == RS_RANK_MINUS_10:
                score -= 300
            elif rank == RS_RANK_REVERSE:
                score -= 200
            elif rank == RS_RANK_NINETY_NINE:
                score -= 250
        else:
            if rank in (RS_RANK_PASS, RS_RANK_SKIP):
                score += 150
            elif rank == RS_RANK_MINUS_10:
                score += 200
        return score

    in_danger_zone = (
        (28 <= current_count <= 32)
        or (61 <= current_count <= 65)
        or current_count >= 88
    )
    if not in_danger_zone:
        if rank == 1:
            score -= 350
        elif rank == 9:
            score -= 300
        elif rank == 10:
            score -= 200
        elif rank == 2:
            score -= 150
    else:
        if rank == 1:
            score += 100
        elif rank == 9:
            score += 50
        elif rank == 10:
            score += 0
    return score


def _score_count_ranges(
    is_rs_games: bool, current_count: int, new_count: int
) -> int:
    """Score counts based on safety ranges."""
    score = 0
    if is_rs_games:
        if 70 <= new_count <= 96:
            score += (new_count - 70) * -8
        if 20 <= new_count <= 60:
            score += 150
        if 0 <= new_count <= 30:
            score += 50
        return score

    if 70 <= new_count <= 94:
        score += (new_count - 70) * -5
    if 40 <= new_count <= 60:
        score += 100
    return score


def _calculate_two_effect(current_count: int) -> int:
    """Calculate the new count after playing a 2 (Quentin C)."""
    if current_count % 2 == 0 and current_count > TWO_DIVIDE_THRESHOLD:
        return current_count // 2
    else:
        return current_count * 2


def _get_card_value(rank: int) -> int:
    """Get simple card value for Quentin C."""
    if 3 <= rank <= 8:
        return rank
    elif rank == 9:
        return 0
    elif rank in (11, 12, 13):  # J, Q, K
        return 10
    return 0


# =============================================================================
# Jack Chain Evaluation (2-player only)
# =============================================================================

def _evaluate_jack_chain(
    game: "NinetyNineGame", count_after_jack: int, remaining_hand: list["Card"]
) -> int:
    """
    Evaluate the best outcome achievable after playing a Jack in 2-player.

    In 2-player, Jacks skip the opponent, so the bot plays again immediately.
    This allows chaining multiple Jacks and planning the final position.

    Args:
        game: The game instance
        count_after_jack: Count after playing the Jack (+10)
        remaining_hand: Cards remaining in hand after playing the Jack

    Returns:
        Best score achievable through the chain
    """
    if count_after_jack > 99:
        return -99999  # Busted

    # Check if we hit a milestone with this Jack
    if count_after_jack == 99:
        return 15000  # Hit 99, round ends, huge bonus

    if count_after_jack in (33, 66):
        # We hit a milestone! And we get to play again (Jack skips opponent).
        # Find best continuation from remaining hand
        if remaining_hand:
            continuation_score = _find_best_chain_continuation(
                game, count_after_jack, remaining_hand
            )
            # Milestone bonus + continuation (continuation could be negative if bad)
            return 12000 + max(0, continuation_score // 10)
        else:
            return 12000  # Just the milestone

    # Check for milestone pass-through (bad!)
    # We need the original count to check this, but we only have count_after_jack
    # The caller should have already checked this, so we just evaluate the position

    if not remaining_hand:
        # No more cards, evaluate opponent's position
        return _score_opponent_position(count_after_jack)

    # Find best play from remaining hand
    return _find_best_chain_continuation(game, count_after_jack, remaining_hand)


def _find_best_chain_continuation(
    game: "NinetyNineGame", current_count: int, hand: list["Card"]
) -> int:
    """
    Find the best score achievable from current position with given hand.

    Args:
        game: The game instance
        current_count: Current count
        hand: Cards available to play

    Returns:
        Best score achievable
    """
    best_score = -99999

    for i, card in enumerate(hand):
        remaining = hand[:i] + hand[i + 1 :]

        if card.rank == 11:  # Another Jack
            new_count = current_count + 10
            if new_count <= 99:
                # Check for milestone pass-through
                if current_count < 33 < new_count:
                    score = -8000  # Would pass through 33
                elif current_count < 66 < new_count:
                    score = -8000  # Would pass through 66
                else:
                    score = _evaluate_jack_chain(game, new_count, remaining)
                best_score = max(best_score, score)
        else:
            # Non-Jack - evaluate all possible final positions
            for final_count in _get_card_final_counts(card, current_count):
                if final_count > 99:
                    continue
                # Check for milestone pass-through
                if current_count < 33 < final_count:
                    score = -8000
                elif current_count < 66 < final_count:
                    score = -8000
                elif final_count in (33, 66, 99):
                    score = 10000  # Milestone hit!
                else:
                    score = _score_opponent_position(final_count)
                best_score = max(best_score, score)

    return best_score


def _get_card_final_counts(card: "Card", current_count: int) -> list[int]:
    """
    Get possible final counts for playing a card.

    For cards with choices (Ace, 10), returns both options.
    """
    rank = card.rank
    if rank == 1:  # Ace: +1 or +11
        return [current_count + 1, current_count + 11]
    elif rank == 10:  # Ten: +10 or -10
        return [current_count + 10, current_count - 10]
    elif rank == 2:  # Two: multiply/divide
        return [_calculate_two_effect(current_count)]
    elif rank == 9:  # Nine: pass
        return [current_count]
    elif rank in (12, 13):  # Q, K: +10
        return [current_count + 10]
    elif 3 <= rank <= 8:  # Number cards
        return [current_count + rank]
    return [current_count]


def _score_opponent_position(count: int) -> int:
    """
    Score a position based on how bad it is for the opponent.

    Higher score = worse for opponent = better for us.
    """
    if count > 99:
        return -99999  # We busted (shouldn't happen)

    # Perfect traps - opponent is almost guaranteed to lose tokens
    # 31: Almost every card passes through 33 (only escape: 9, Ace+1, or 10-10)
    # 97: Almost every card goes over 99 (only escape: 9, Ace+1, or 10-10)
    if count in (31, 97):
        return 9000

    # Weaker trap (opponent can escape with 2 to divide)
    if count == 64:
        return 6000

    # Setup zones - opponent is in danger of passing through milestones
    if 29 <= count <= 30:  # Will likely pass through 33
        return 7000
    if count == 32:  # Very dangerous, only 9/Ace+1 avoids passing 33
        return 7500
    if 62 <= count <= 63:  # Will likely pass through 66
        return 7000
    if count == 65:  # Very dangerous
        return 7500
    if 95 <= count <= 96:  # Will likely go over 99
        return 7000
    if count == 98:  # Very dangerous
        return 7500

    # Bad positions for US to leave (opponent can hit milestones easily)
    if count in (23, 56, 89):
        return -3000  # Opponent can hit 33, 66, 99 with +10

    if count in (22, 55, 88):
        return -2000  # Opponent can hit milestones with +11

    # Neutral-ish positions
    if 40 <= count <= 60:
        return 100  # Safe middle range, slight bonus

    # High counts are generally worse for opponent
    if 70 <= count <= 94:
        return (count - 70) * 50  # More dangerous as count increases

    return 0


# Export for use in game.py (bot choice selection)
evaluate_count = _bot_evaluate_count
