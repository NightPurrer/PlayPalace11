"""Turn-flow tests for Sorry draw and move phases."""

from server.core.ui.keybinds import KeybindState
from server.core.users.test_user import MockUser
from server.game_utils.actions import Visibility
from server.games.sorry.game import SorryGame, SorryOptions


def _build_game(
    *,
    auto_apply_single_move: bool = False,
    rules_profile: str = "classic_00390",
) -> tuple[SorryGame, MockUser, MockUser]:
    game = SorryGame(
        options=SorryOptions(
            rules_profile=rules_profile,
            auto_apply_single_move=auto_apply_single_move,
            faster_setup_one_pawn_out=False,
        )
    )
    user1 = MockUser("Alice")
    user2 = MockUser("Bob")
    game.add_player("Alice", user1)
    game.add_player("Bob", user2)
    game.on_start()
    return game, user1, user2


def _set_track(pawn, position: int) -> None:
    pawn.zone = "track"
    pawn.track_position = position
    pawn.home_steps = 0


def test_draw_card_enters_choose_phase_when_multiple_moves() -> None:
    game, _, _ = _build_game(auto_apply_single_move=False)
    player = game.current_player
    assert player is not None

    game.game_state.draw_pile = ["1"]
    game.execute_action(player, "draw_card")

    assert game.game_state.current_card == "1"
    assert game.game_state.turn_phase == "choose_move"
    assert game.current_player == player
    assert len(game._get_current_legal_moves(player)) >= 2


def test_choose_move_applies_and_advances_turn() -> None:
    game, _, _ = _build_game(auto_apply_single_move=False)
    player = game.current_player
    assert player is not None
    first_player_id = player.id

    game.game_state.draw_pile = ["1"]
    game.execute_action(player, "draw_card")
    game.execute_action(player, "move_slot_1")

    player_state = game.game_state.player_states[first_player_id]
    assert player_state.pawns[0].zone == "track"
    assert game.current_player is not None
    assert game.current_player.id != first_player_id
    assert game.game_state.current_card is None
    assert game.game_state.turn_phase == "draw"


def test_auto_apply_single_move_applies_immediately() -> None:
    game, _, _ = _build_game(auto_apply_single_move=True)
    player = game.current_player
    assert player is not None
    player_state = game.game_state.player_states[player.id]

    player_state.pawns[0].zone = "track"
    player_state.pawns[0].track_position = 0
    game.game_state.draw_pile = ["3"]

    game.execute_action(player, "draw_card")

    assert player_state.pawns[0].track_position == 3
    assert game.current_player is not None
    assert game.current_player.id != player.id
    assert game.game_state.turn_phase == "draw"
    assert game.game_state.current_card is None


def test_no_legal_moves_discards_and_advances_turn() -> None:
    game, _, _ = _build_game(auto_apply_single_move=False)
    player = game.current_player
    assert player is not None
    player_state = game.game_state.player_states[player.id]

    # With no pawns in start, Sorry card has no legal moves.
    for idx, pawn in enumerate(player_state.pawns):
        pawn.zone = "track"
        pawn.track_position = idx

    game.game_state.draw_pile = ["sorry"]
    game.execute_action(player, "draw_card")

    assert game.current_player is not None
    assert game.current_player.id != player.id
    assert game.game_state.current_card is None
    assert game.game_state.turn_phase == "draw"


def test_card_two_grants_extra_turn() -> None:
    game, _, _ = _build_game(auto_apply_single_move=True)
    player = game.current_player
    assert player is not None
    player_state = game.game_state.player_states[player.id]

    player_state.pawns[0].zone = "track"
    player_state.pawns[0].track_position = 0
    game.game_state.draw_pile = ["2"]

    game.execute_action(player, "draw_card")

    assert player_state.pawns[0].track_position == 2
    assert game.current_player == player
    assert game.game_state.current_card is None
    assert game.game_state.turn_phase == "draw"
    assert game.game_state.turn_number == 2


def test_a5065_card_two_does_not_grant_extra_turn() -> None:
    game, _, _ = _build_game(auto_apply_single_move=True, rules_profile="a5065_core")
    player = game.current_player
    assert player is not None
    player_state = game.game_state.player_states[player.id]

    player_state.pawns[0].zone = "track"
    player_state.pawns[0].track_position = 0
    game.game_state.draw_pile = ["2"]

    game.execute_action(player, "draw_card")

    assert player_state.pawns[0].track_position == 2
    assert game.current_player is not None
    assert game.current_player.id != player.id
    assert game.game_state.current_card is None
    assert game.game_state.turn_phase == "draw"
    assert game.game_state.turn_number == 2


def test_high_branching_move_slots_remain_accessible() -> None:
    game = SorryGame(
        options=SorryOptions(
            auto_apply_single_move=False,
            faster_setup_one_pawn_out=False,
        )
    )
    for name in ("P1", "P2", "P3", "P4"):
        game.add_player(name, MockUser(name))
    game.on_start()

    current = game.current_player
    assert current is not None

    own_state = game.game_state.player_states[current.id]
    for pawn, position in zip(own_state.pawns, (0, 5, 10, 15), strict=False):
        _set_track(pawn, position)

    opponent_layout = (
        (20, 21, 22, 23),
        (30, 31, 32, 33),
        (40, 41, 42, 43),
    )
    for opponent, positions in zip(game.players[1:], opponent_layout, strict=False):
        opponent_state = game.game_state.player_states[opponent.id]
        for pawn, position in zip(opponent_state.pawns, positions, strict=False):
            _set_track(pawn, position)

    game.game_state.turn_phase = "choose_move"
    game.game_state.current_card = "11"
    legal = game._get_current_legal_moves(current)

    assert len(legal) == 52
    assert len(legal) > 24
    assert game.max_move_slots >= len(legal)
    assert game._is_move_slot_hidden(current, "move_slot_52") == Visibility.VISIBLE
    assert game._is_move_slot_enabled(current, "move_slot_52") is None
    assert game._is_move_slot_hidden(current, "move_slot_53") == Visibility.HIDDEN
    assert game._is_move_slot_enabled(current, "move_slot_53") == "action-not-available"


def test_setup_keybinds_registers_draw_and_number_slots() -> None:
    game = SorryGame()
    game.setup_keybinds()

    d_bindings = game._keybinds.get("d", [])
    assert any(
        binding.actions == ["draw_card"] and binding.state == KeybindState.ACTIVE
        for binding in d_bindings
    )
    space_bindings = game._keybinds.get("space", [])
    assert any(
        binding.actions == ["draw_card"] and binding.state == KeybindState.ACTIVE
        for binding in space_bindings
    )
    one_bindings = game._keybinds.get("1", [])
    assert any(
        binding.actions == ["move_slot_1"] and binding.state == KeybindState.ACTIVE
        for binding in one_bindings
    )
    nine_bindings = game._keybinds.get("9", [])
    assert any(
        binding.actions == ["move_slot_9"] and binding.state == KeybindState.ACTIVE
        for binding in nine_bindings
    )
