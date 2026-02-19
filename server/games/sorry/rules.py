"""Rules profile models for Sorry editions."""

from dataclasses import dataclass
from typing import Protocol


class SorryRulesProfile(Protocol):
    """Protocol implemented by each Sorry ruleset profile."""

    profile_id: str
    display_name: str

    def card_faces(self) -> tuple[str, ...]:
        """Return supported card faces for this profile."""
        ...


@dataclass(frozen=True)
class Classic00390Rules:
    """Classic Sorry rules profile based on Hasbro 00390."""

    profile_id: str = "classic_00390"
    display_name: str = "Classic 00390"
    _faces: tuple[str, ...] = (
        "1",
        "2",
        "3",
        "4",
        "5",
        "7",
        "8",
        "10",
        "11",
        "12",
        "sorry",
    )

    def card_faces(self) -> tuple[str, ...]:
        return self._faces
