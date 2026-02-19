"""Tests for the Sorry game scaffold."""

import random

from server.core.users.test_user import MockUser
from server.games.registry import GameRegistry
from server.games.sorry.game import SorryGame, SorryOptions, SorryPlayer
from server.games.sorry.state import (
    TRACK_LENGTH,
    build_initial_game_state,
    clockwise_distance,
    discard_current_card,
    draw_next_card,
    get_home_entry_track_for_seat,
    get_start_track_for_seat,
    get_track_occupancy,
)


def test_game_creation() -> None:
    """Sorry game metadata should be wired correctly."""
    game = SorryGame()
    assert game.get_name() == "Sorry!"
    assert game.get_type() == "sorry"
    assert game.get_category() == "category-board-games"
    assert game.get_min_players() == 2
    assert game.get_max_players() == 4
    assert game.rules_profile_id == "classic_00390"


def test_game_registered() -> None:
    """Sorry game should be available via game registry."""
    registered = GameRegistry.get("sorry")
    assert registered is SorryGame


def test_player_creation_defaults() -> None:
    """Players should use Sorry-specific state fields."""
    game = SorryGame()
    user = MockUser("Alice")
    player = game.add_player("Alice", user)

    assert isinstance(player, SorryPlayer)
    assert player.name == "Alice"
    assert player.pawns_in_start == 4
    assert player.pawns_in_home == 0


def test_on_start_initializes_state_with_faster_setup() -> None:
    """Fast setup should place one pawn out for each player."""
    game = SorryGame(
        options=SorryOptions(
            auto_apply_single_move=False,
            faster_setup_one_pawn_out=True,
        )
    )
    user1 = MockUser("Alice")
    user2 = MockUser("Bob")
    p1 = game.add_player("Alice", user1)
    p2 = game.add_player("Bob", user2)

    game.on_start()

    assert game.status == "playing"
    assert game.game_active is True
    assert p1.pawns_in_start == 3
    assert p2.pawns_in_start == 3

    s1 = game.game_state.player_states[p1.id]
    s2 = game.game_state.player_states[p2.id]
    assert game.game_state.player_order == [p1.id, p2.id]
    assert s1.pawns[0].zone == "track"
    assert s2.pawns[0].zone == "track"
    assert s1.pawns[0].track_position == s1.start_track
    assert s2.pawns[0].track_position == s2.start_track


def test_serialization_round_trip_preserves_options() -> None:
    """Scaffold options and state should serialize cleanly."""
    game = SorryGame(
        options=SorryOptions(
            auto_apply_single_move=True,
            faster_setup_one_pawn_out=False,
        )
    )
    user1 = MockUser("Alice")
    user2 = MockUser("Bob")
    game.add_player("Alice", user1)
    game.add_player("Bob", user2)
    game.on_start()

    payload = game.to_json()
    loaded = SorryGame.from_json(payload)

    assert loaded.options.auto_apply_single_move is True
    assert loaded.options.faster_setup_one_pawn_out is False
    assert loaded.game_state.turn_phase == "draw"


def test_state_builder_assigns_seat_tracks() -> None:
    """Each player should get stable seat-based start/home mapping."""
    state = build_initial_game_state(
        ["p1", "p2", "p3", "p4"],
        shuffle_deck=False,
    )

    assert state.player_states["p1"].start_track == get_start_track_for_seat(0)
    assert state.player_states["p2"].start_track == get_start_track_for_seat(1)
    assert state.player_states["p3"].start_track == get_start_track_for_seat(2)
    assert state.player_states["p4"].start_track == get_start_track_for_seat(3)
    assert state.player_states["p1"].home_entry_track == get_home_entry_track_for_seat(0)
    assert state.player_states["p4"].home_entry_track == get_home_entry_track_for_seat(3)


def test_clockwise_distance_wraps_track_length() -> None:
    """Distance helper should wrap around track boundaries."""
    assert clockwise_distance(TRACK_LENGTH - 1, 0) == 1
    assert clockwise_distance(5, 8) == 3


def test_draw_and_discard_cycle() -> None:
    """Draw/discard helpers should reshuffle discard when draw pile is empty."""
    rng = random.Random(7)
    state = build_initial_game_state(["p1", "p2"], shuffle_deck=False)
    state.draw_pile = ["1"]
    state.discard_pile = ["2", "3", "4"]

    first = draw_next_card(state, rng=rng)
    assert first == "1"
    discard_current_card(state)
    assert state.current_card is None
    assert "1" in state.discard_pile
    state.draw_pile = []

    second = draw_next_card(state, rng=rng)
    assert second is not None
    assert second in {"1", "2", "3", "4"}


def test_track_occupancy_maps_positions() -> None:
    """Track occupancy helper should include all track-zone pawns."""
    state = build_initial_game_state(
        ["p1", "p2"],
        faster_setup_one_pawn_out=True,
        shuffle_deck=False,
    )
    p1 = state.player_states["p1"]
    p2 = state.player_states["p2"]
    p2.pawns[1].zone = "track"
    p2.pawns[1].track_position = p1.start_track

    occupancy = get_track_occupancy(state)
    occupants = occupancy[p1.start_track]
    assert ("p1", 1) in occupants
    assert ("p2", 2) in occupants
