"""Shared helpers for poker seat ordering."""

from __future__ import annotations


def order_after_button(active_ids: list[str], button_id: str | None) -> list[str]:
    """Return seat order starting left of the button.

    Args:
        active_ids: Active player ids in seat order.
        button_id: Current dealer/button player id.

    Returns:
        Ordered list starting left of the button, or active_ids if no button.
    """
    if not active_ids:
        return []
    if button_id and button_id in active_ids:
        start_index = (active_ids.index(button_id) + 1) % len(active_ids)
        return active_ids[start_index:] + active_ids[:start_index]
    return active_ids
