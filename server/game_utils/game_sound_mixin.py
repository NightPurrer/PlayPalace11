"""Mixin providing sound scheduling, event scheduling, and playback for games."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..games.base import Player
    from server.core.users.base import User


class GameSoundMixin:
    """Schedule and play sounds and game events for games.

    Expected Game attributes:
        scheduled_sounds: list of [tick, sound, vol, pan, pitch].
        sound_scheduler_tick: int.
        event_queue: list of (tick, event_type, data).
        is_animating: bool.
        current_music: str.
        current_ambience: str.
        players: list[Player].
        get_user(player) -> User | None.
    """

    # ==========================================================================
    # Sound Scheduling
    # ==========================================================================

    TICKS_PER_SECOND = 20  # 50ms per tick

    def schedule_sound(
        self,
        sound: str,
        delay_ticks: int = 0,
        volume: int = 100,
        pan: int = 0,
        pitch: int = 100,
    ) -> None:
        """Schedule a sound to play after a delay.

        Args:
            sound: Sound file name to play.
            delay_ticks: Number of ticks to wait before playing (0 = next tick).
            volume: Volume (0-100).
            pan: Pan (-100 to 100, 0 = center).
            pitch: Pitch (100 = normal).
        """
        target_tick = self.sound_scheduler_tick + delay_ticks
        self.scheduled_sounds.append([target_tick, sound, volume, pan, pitch])

    def schedule_sound_sequence(
        self,
        sounds: list[tuple[str, int]],
        start_delay: int = 0,
    ) -> None:
        """Schedule a sequence of sounds with delays between them.

        Args:
            sounds: List of (sound_name, delay_after) tuples.
            start_delay: Initial delay before first sound.
        """
        current_tick = start_delay
        for sound, delay_after in sounds:
            self.schedule_sound(sound, delay_ticks=current_tick)
            current_tick += delay_after

    def clear_scheduled_sounds(self) -> None:
        """Clear all scheduled sounds."""
        self.scheduled_sounds.clear()

    def process_scheduled_sounds(self) -> None:
        """Process scheduled sounds. Called automatically in on_tick()."""
        current_tick = self.sound_scheduler_tick

        # Find and play sounds scheduled for this tick
        remaining = []
        for scheduled in self.scheduled_sounds:
            tick, sound, volume, pan, pitch = scheduled
            if tick <= current_tick:
                self.play_sound(sound, volume, pan, pitch)
            else:
                remaining.append(scheduled)

        self.scheduled_sounds = remaining
        self.sound_scheduler_tick += 1

    # ==========================================================================
    # Event Scheduling
    # ==========================================================================

    def schedule_event(
        self, event_type: str, data: dict, delay_ticks: int = 0
    ) -> None:
        """Schedule a game event to fire after a delay.

        Args:
            event_type: Event identifier (game-specific).
            data: Event payload dict.
            delay_ticks: Ticks to wait before firing (0 = next tick).
        """
        target_tick = self.sound_scheduler_tick + delay_ticks
        self.event_queue.append((target_tick, event_type, data))

    def process_scheduled_events(self) -> None:
        """Process scheduled events. Call in on_tick() after process_scheduled_sounds().

        Events whose tick has arrived are dispatched to on_game_event().
        Uses queue-swap so events added during handling are preserved.
        """
        if not self.event_queue:
            return

        to_process = self.event_queue
        self.event_queue = []
        remaining = []
        current_tick = self.sound_scheduler_tick

        for tick, event_type, data in to_process:
            if tick <= current_tick:
                self.on_game_event(event_type, data)
            else:
                remaining.append((tick, event_type, data))

        self.event_queue = remaining + self.event_queue

    def on_game_event(self, event_type: str, data: dict) -> None:
        """Handle a scheduled game event. Override in subclasses.

        Args:
            event_type: The event identifier.
            data: The event payload dict.
        """
        pass

    # ==========================================================================
    # Sound Playback
    # ==========================================================================

    def broadcast_sound(
        self, name: str, volume: int = 100, pan: int = 0, pitch: int = 100
    ) -> None:
        """Play a sound for all players."""
        for player in self.players:
            user = self.get_user(player)
            if user:
                user.play_sound(name, volume, pan, pitch)

    def play_sound(
        self, name: str, volume: int = 100, pan: int = 0, pitch: int = 100
    ) -> None:
        """Alias for broadcast_sound."""
        self.broadcast_sound(name, volume, pan, pitch)

    def play_music(self, name: str, looping: bool = True) -> None:
        """Play music for all players and store as current."""
        self.current_music = name
        for player in self.players:
            user = self.get_user(player)
            if user:
                user.play_music(name, looping)

    def play_ambience(self, loop: str, intro: str = "", outro: str = "") -> None:
        """Play ambient sound for all players."""
        self.current_ambience = loop
        for player in self.players:
            user = self.get_user(player)
            if user:
                user.play_ambience(loop, intro, outro)

    def stop_ambience(self) -> None:
        """Stop ambient sound for all players."""
        self.current_ambience = ""
        for player in self.players:
            user = self.get_user(player)
            if user:
                user.stop_ambience()
