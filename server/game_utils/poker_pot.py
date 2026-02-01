from __future__ import annotations

from dataclasses import dataclass, field

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class PokerPot(DataClassJSONMixin):
    """Represent a single main/side pot.

    Attributes:
        amount: Total chips in this pot.
        eligible_player_ids: Players eligible to win this pot.
    """
    amount: int
    eligible_player_ids: set[str] = field(default_factory=set)


@dataclass
class PokerPotManager(DataClassJSONMixin):
    """Track contributions and compute main/side pots.

    Attributes:
        contributions: Player id -> chips contributed.
        folded: Player ids that have folded.
    """

    contributions: dict[str, int] = field(default_factory=dict)
    folded: set[str] = field(default_factory=set)

    def reset(self) -> None:
        """Clear all contributions and folded state."""
        self.contributions.clear()
        self.folded.clear()

    def add_contribution(self, player_id: str, amount: int) -> None:
        """Add chips to a player's contribution if amount is positive."""
        if amount <= 0:
            return
        self.contributions[player_id] = self.contributions.get(player_id, 0) + amount

    def mark_folded(self, player_id: str) -> None:
        """Mark a player as folded for pot eligibility."""
        self.folded.add(player_id)

    def total_pot(self) -> int:
        """Return the total chips across all contributions."""
        return sum(self.contributions.values())

    def get_pots(self) -> list[PokerPot]:
        """Compute main/side pots from contributions."""
        amounts = [amt for amt in self.contributions.values() if amt > 0]
        if not amounts:
            return []

        levels = sorted(set(amounts))
        pots: list[PokerPot] = []
        prev = 0
        for level in levels:
            contributors = [pid for pid, amt in self.contributions.items() if amt >= level]
            pot_amount = (level - prev) * len(contributors)
            if pot_amount <= 0:
                prev = level
                continue
            eligible = {pid for pid in contributors if pid not in self.folded}
            pots.append(PokerPot(amount=pot_amount, eligible_player_ids=eligible))
            prev = level
        return pots
