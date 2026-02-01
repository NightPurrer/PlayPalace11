"""Shared betting helpers for poker games."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class PotLimitCaps:
    """Pot-limit caps for a bet.

    Attributes:
        total_cap: Maximum total bet size allowed for the action.
    """

    total_cap: int


def compute_pot_limit_caps(
    pot_total: int,
    to_call: int,
    raise_mode: str,
) -> Optional[PotLimitCaps]:
    """Return total bet caps for pot-limit/double-pot modes.

    Args:
        pot_total: Current total pot size.
        to_call: Amount required to call.
        raise_mode: "no_limit", "pot_limit", or "double_pot".

    Returns:
        PotLimitCaps if limits apply, otherwise None.
    """
    if raise_mode == "no_limit":
        return None
    total_cap = pot_total + to_call * 2
    if raise_mode == "double_pot":
        total_cap = pot_total * 2 + to_call * 2
    return PotLimitCaps(total_cap=total_cap)


def clamp_total_to_cap(total: int, caps: Optional[PotLimitCaps]) -> int:
    """Clamp a total bet to a pot-limit cap when present."""
    if not caps:
        return total
    return min(total, caps.total_cap)
