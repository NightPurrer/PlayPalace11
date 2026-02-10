"""
Bot AI logic for Tradeoff game.

Handles bot decision making for trading and taking phases.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import TradeoffGame, TradeoffPlayer


def bot_think_trading(game: "TradeoffGame", player: "TradeoffPlayer") -> str | None:
    """
    Bot AI for trading phase.

    Strategy: Keep dice that contribute to sets, trade the rest.
    Simple heuristic: keep duplicates, trade unique values.

    Note: All dice start marked for trading by default, so bot must
    toggle OFF the ones it wants to keep.
    """
    if player.trades_confirmed:
        return None

    counts = _count_dice(player.rolled_dice)
    _merge_counts(counts, player.hand)

    desired_keeps = _select_keep_indices(player.rolled_dice, counts, min_keeps=2)

    toggle_action = _next_trade_toggle(player.trading_indices, desired_keeps)
    if toggle_action:
        return toggle_action

    # Confirm trades
    return "confirm_trades"


def bot_think_taking(game: "TradeoffGame", player: "TradeoffPlayer") -> str | None:
    """
    Bot AI for taking phase.

    Strategy: Take dice that match what we already have.
    """
    if game.taking_index >= len(game.taking_order):
        return None
    if game.taking_order[game.taking_index] != player.id:
        return None
    if player.dice_taken_count >= player.dice_traded_count:
        return None

    counts = _count_dice(player.hand)
    pool_counts = _count_dice(game.pool)
    best_value = _select_best_pool_value(counts, pool_counts)
    return f"take_{best_value}" if best_value is not None else None


def _count_dice(values: list[int]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return counts


def _merge_counts(counts: dict[int, int], values: list[int]) -> None:
    for value in values:
        counts[value] = counts.get(value, 0) + 1


def _select_keep_indices(
    rolled_dice: list[int], counts: dict[int, int], min_keeps: int
) -> list[int]:
    desired_keeps = [
        i for i, value in enumerate(rolled_dice) if counts.get(value, 0) > 1
    ]
    if len(desired_keeps) >= min_keeps:
        return desired_keeps

    sorted_dice = sorted(
        enumerate(rolled_dice),
        key=lambda x: counts.get(x[1], 0),
        reverse=True,
    )
    for i, _ in sorted_dice:
        if i not in desired_keeps:
            desired_keeps.append(i)
            if len(desired_keeps) >= min_keeps:
                break
    return desired_keeps


def _next_trade_toggle(trading_indices: set[int], desired_keeps: list[int]) -> str | None:
    for index in desired_keeps:
        if index in trading_indices:
            return f"toggle_trade_{index}"
    return None


def _select_best_pool_value(
    counts: dict[int, int], pool_counts: dict[int, int]
) -> int | None:
    best_value = None
    best_score = -1
    for value, count in pool_counts.items():
        if count <= 0:
            continue
        score = counts.get(value, 0)
        if score > best_score:
            best_score = score
            best_value = value
    return best_value
