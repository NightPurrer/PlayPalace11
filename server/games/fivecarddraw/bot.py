"""
Bot AI for Five Card Draw.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ...game_utils.poker_evaluator import best_hand

if TYPE_CHECKING:
    from .game import FiveCardDrawGame, FiveCardDrawPlayer


def bot_think(game: "FiveCardDrawGame", player: "FiveCardDrawPlayer") -> str | None:
    if game.current_player != player:
        return None
    if game.phase == "draw":
        _choose_discards(game, player)
        return "draw_cards"
    if not game.betting:
        return None
    return _decide_bet(game, player)


def _choose_discards(game: "FiveCardDrawGame", player: "FiveCardDrawPlayer") -> None:
    category = _evaluate_hand_category(player.hand)
    ranks = [card.rank for card in player.hand]
    counts = _count_ranks(ranks)
    keep_ranks = _select_keep_ranks(category, ranks, counts)
    discard_indices = [
        i for i, card in enumerate(player.hand) if card.rank not in keep_ranks
    ]
    discard_indices = _limit_discards(player.hand, discard_indices)
    player.to_discard = set(discard_indices)


def _decide_bet(game: "FiveCardDrawGame", player: "FiveCardDrawPlayer") -> str | None:
    to_call = game.betting.amount_to_call(player.id)
    category = _evaluate_hand_category(player.hand)
    min_raise = max(game.betting.last_raise_size, 1)
    can_raise = game.betting.can_raise() and (to_call + min_raise) <= player.chips
    if to_call == 0:
        if can_raise and category >= 1:
            return "raise"
        return "call"
    if to_call >= player.chips:
        return "call"
    if category >= 2 and to_call <= max(1, player.chips // 6):
        return "call"
    if category >= 1 and to_call <= max(1, player.chips // 12):
        return "call"
    if to_call <= max(1, player.chips // 25):
        return "call"
    return "fold"


def _evaluate_hand_category(hand: list) -> int:
    if len(hand) < 5:
        return 0
    score, _ = best_hand(hand)
    return score[0]


def _count_ranks(ranks: list[int]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for rank in ranks:
        counts[rank] = counts.get(rank, 0) + 1
    return counts


def _select_keep_ranks(
    category: int, ranks: list[int], counts: dict[int, int]
) -> set[int]:
    if category >= 4:  # straight or better
        return set(ranks)
    if category in (1, 2):  # one pair or two pair
        return {rank for rank, count in counts.items() if count == 2}
    if category == 3:  # three of a kind
        return {rank for rank, count in counts.items() if count == 3}
    return set()


def _limit_discards(hand: list, discard_indices: list[int]) -> list[int]:
    max_discards = 4 if any(card.rank == 1 for card in hand) else 3
    if len(discard_indices) > max_discards:
        return discard_indices[:max_discards]
    return discard_indices
