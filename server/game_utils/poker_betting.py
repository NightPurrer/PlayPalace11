from __future__ import annotations

from dataclasses import dataclass, field

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class PokerBettingRound(DataClassJSONMixin):
    """Track betting state for a single poker betting round.

    Attributes:
        order: Player IDs in betting order.
        max_raises: Maximum raises allowed (None for unlimited).
        current_bet: Current amount to call.
        last_raise_size: Size of the last raise.
        raises_count: Number of raises so far.
        bets: Per-player bet amounts for this round.
        acted_since_raise: Players who have acted since the last raise.
    """
    order: list[str]
    max_raises: int | None = None
    current_bet: int = 0
    last_raise_size: int = 0
    raises_count: int = 0
    bets: dict[str, int] = field(default_factory=dict)
    acted_since_raise: set[str] = field(default_factory=set)

    def reset(
        self,
        current_bet: int = 0,
        last_raise_size: int = 0,
        initial_bets: dict[str, int] | None = None,
    ) -> None:
        """Reset round state with optional initial bet values."""
        self.current_bet = current_bet
        self.last_raise_size = last_raise_size
        self.raises_count = 0
        self.bets = {pid: 0 for pid in self.order}
        if initial_bets:
            for pid, amount in initial_bets.items():
                if pid in self.bets:
                    self.bets[pid] = amount
        self.acted_since_raise = set()

    def amount_to_call(self, player_id: str) -> int:
        """Return the amount needed for a player to call."""
        return max(0, self.current_bet - self.bets.get(player_id, 0))

    def can_raise(self) -> bool:
        """Return True if the raise cap has not been reached."""
        if self.max_raises is None:
            return True
        return self.raises_count < self.max_raises

    def record_bet(self, player_id: str, amount: int, is_raise: bool) -> None:
        """Record a bet or raise and update round state."""
        self.bets[player_id] = self.bets.get(player_id, 0) + amount
        if is_raise:
            self.raises_count += 1
            raise_size = self.bets[player_id] - self.current_bet
            self.last_raise_size = max(self.last_raise_size, raise_size)
            self.current_bet = self.bets[player_id]
            self.acted_since_raise = {player_id}
        else:
            self.acted_since_raise.add(player_id)

    def is_complete(self, active_ids: set[str], all_in_ids: set[str]) -> bool:
        """Return True if all active players have matched the bet and acted."""
        for pid in active_ids:
            if pid in all_in_ids:
                continue
            if self.bets.get(pid, 0) != self.current_bet:
                return False
        # Everyone who can act has acted since the last raise
        for pid in active_ids:
            if pid in all_in_ids:
                continue
            if pid not in self.acted_since_raise:
                return False
        return True

    def next_player(self, current_id: str | None, active_ids: set[str]) -> str | None:
        """Return the next active player id in betting order."""
        if not self.order:
            return None
        start_index = 0
        if current_id and current_id in self.order:
            start_index = (self.order.index(current_id) + 1) % len(self.order)
        for i in range(len(self.order)):
            idx = (start_index + i) % len(self.order)
            pid = self.order[idx]
            if pid in active_ids:
                return pid
        return None
