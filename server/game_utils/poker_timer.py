from __future__ import annotations

from dataclasses import dataclass

from mashumaro.mixins.json import DataClassJSONMixin


@dataclass
class PokerTurnTimer(DataClassJSONMixin):
    """Per-turn countdown timer (ticks at 20/s).

    Attributes:
        ticks_remaining: Remaining ticks in the countdown.
    """
    ticks_remaining: int = 0

    def start(self, seconds: int) -> None:
        """Start the timer for a number of seconds."""
        self.ticks_remaining = max(0, seconds) * 20

    def clear(self) -> None:
        """Clear the timer to zero."""
        self.ticks_remaining = 0

    def tick(self) -> bool:
        """Advance the timer by one tick; return True if it expired."""
        if self.ticks_remaining <= 0:
            return False
        self.ticks_remaining -= 1
        return self.ticks_remaining == 0

    def seconds_remaining(self) -> int:
        """Return remaining whole seconds."""
        if self.ticks_remaining <= 0:
            return 0
        return (self.ticks_remaining + 19) // 20
