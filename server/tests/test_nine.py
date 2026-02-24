import json
import random

from server.games.nine.game import (
    NineGame,
    NinePlayer,
    RANK_NINE,
    SUIT_CLUBS,
    SUIT_DIAMONDS,
    SUIT_HEARTS,
    SUIT_SPADES,
    RANK_SIX, RANK_SEVEN, RANK_EIGHT, RANK_TEN, RANK_JACK, RANK_QUEEN, RANK_KING, RANK_ACE
)
from server.games.nine.state import NineState, SequenceState
from server.game_utils.cards import Card, Deck
from server.core.users.test_user import MockUser
from server.core.users.bot import Bot
from server.messages.localization import Localization # For checking reasons

class TestNineGameUnit:
    """Unit tests for Nine game functions."""

    def test_game_creation(self):
        """Test creating a new Nine game."""
        game = NineGame()
        assert game.get_name() == "Nine"
        assert game.get_type() == "nine"
        assert game.get_category() == "category-card-games"
        assert game.get_min_players() == 2
        assert game.get_max_players() == 6

    def test_player_creation(self):
        """Test creating a player with correct initial state."""
        game = NineGame()
        user = MockUser("Alice")
        player = game.add_player("Alice", user)

        assert player.name == "Alice"
        assert player.is_bot is False
        assert isinstance(player, NinePlayer)
        assert player.hand == []

    def test_options_defaults(self):
        """Test default game options."""
        game = NineGame()
        # With NineOptions removed, winning_score would be defined directly in NineGame or removed
        # For now, it is not an option
        # assert game.options.winning_score == 1 # Winning when 1 card left (i.e. emptied hand)
        pass


    def test_build_nine_deck(self):
        """Test the custom nine deck building."""
        game = NineGame()
        deck = game._build_nine_deck()
        assert deck.size() == 36

        # Check a specific card exists, e.g., Nine of Clubs
        nine_of_clubs_found = False
        for card in deck.cards:
            if card.rank == RANK_NINE and card.suit == SUIT_CLUBS:
                nine_of_clubs_found = True
                break
        assert nine_of_clubs_found, "Nine of Clubs not found in deck."

        # Check no invalid ranks
        invalid_rank_found = False
        for card in deck.cards:
            if card.rank not in [RANK_SIX, RANK_SEVEN, RANK_EIGHT, RANK_NINE, RANK_TEN, RANK_JACK, RANK_QUEEN, RANK_KING, RANK_ACE]:
                invalid_rank_found = True
                break
        assert not invalid_rank_found, "Invalid rank found in deck."

    def test_prestart_validate_player_counts(self):
        """Test player count validation."""
        user_a = MockUser("A")
        user_b = MockUser("B")
        user_c = MockUser("C")
        user_d = MockUser("D")
        user_e = MockUser("E")
        user_f = MockUser("F")

        # Valid: 2 players
        game_2 = NineGame()
        game_2.add_player("A", user_a)
        game_2.add_player("B", user_b)
        assert not game_2.prestart_validate()

        # Valid: 3 players
        game_3 = NineGame()
        game_3.add_player("A", user_a)
        game_3.add_player("B", user_b)
        game_3.add_player("C", user_c)
        assert not game_3.prestart_validate()

        # Valid: 4 players
        game_4 = NineGame()
        game_4.add_player("A", user_a)
        game_4.add_player("B", user_b)
        game_4.add_player("C", user_c)
        game_4.add_player("D", user_d)
        assert not game_4.prestart_validate()

        # Invalid: 5 players
        game_5 = NineGame()
        game_5.add_player("A", user_a)
        game_5.add_player("B", user_b)
        game_5.add_player("C", user_c)
        game_5.add_player("D", user_d)
        game_5.add_player("E", user_e)
        assert game_5.prestart_validate() == [Localization.get("en", "nine-error-invalid-player-count")]

        # Valid: 6 players
        game_6 = NineGame()
        game_6.add_player("A", user_a)
        game_6.add_player("B", user_b)
        game_6.add_player("C", user_c)
        game_6.add_player("D", user_d)
        game_6.add_player("E", user_e)
        game_6.add_player("F", user_f)
        assert not game_6.prestart_validate()


class TestNineGameSerialization:
    """Tests for game serialization."""

    def test_serialization(self):
        """Test that game state can be serialized and deserialized."""
        game = NineGame()
        user1 = MockUser("Alice")
        user2 = MockUser("Bob")
        game.add_player("Alice", user1)
        game.add_player("Bob", user2)

        # Start game and modify some state
        game.on_start()

        # Play some cards to change the state
        # Find Nine of Clubs and play it
        nine_of_clubs_player = None
        nine_of_clubs_slot = -1
        for i, p in enumerate(game.get_active_players()):
            for j, card in enumerate(p.hand):
                if card.rank == RANK_NINE and card.suit == SUIT_CLUBS:
                    nine_of_clubs_player = p
                    nine_of_clubs_slot = j
                    break
            if nine_of_clubs_player:
                break
        
        assert nine_of_clubs_player is not None

        # Ensure it's the nine_of_clubs_player's turn
        game.current_player = nine_of_clubs_player
        game._action_play_card(nine_of_clubs_player, f"play_card_slot_{nine_of_clubs_slot+1}")

        # The game's _end_turn logic (triggered by _action_play_card) should have advanced the current_player.
        # So, loaded_game.current_player should automatically be the next player.


        # Serialize
        json_str = game.to_json()
        data = json.loads(json_str)

        # Verify some critical state
        assert data["game_active"] is True
        assert data["nine_state"]["nine_of_clubs_played"] is True
        assert len(data["players"]) == 2
        assert data["nine_state"]["sequences"][str(SUIT_CLUBS)]["low_card"]["rank"] == RANK_NINE
        
        # Deserialize
        loaded_game = NineGame.from_json(json_str)

        # Verify loaded state matches original
        assert loaded_game.game_active is True
        assert loaded_game.nine_state.nine_of_clubs_played is True
        assert len(loaded_game.players) == 2
        assert loaded_game.nine_state.sequences[SUIT_CLUBS].low_card.rank == RANK_NINE
        assert loaded_game.nine_state.sequences[SUIT_CLUBS].low_card.suit == SUIT_CLUBS

        # Ensure the game can continue after loading
        # The exact continuation depends on the bot logic, but we can verify it doesn't crash
        # For simplicity, just check that current_player is correctly loaded and can make a move
        assert loaded_game.current_player is not None
        assert loaded_game._has_valid_move(loaded_game.current_player)

# Placeholder for Play Tests (integration tests with bots)
# Will add these after unit tests are passing and basic functionality is stable.
class TestNineGamePlayTest:
    """Integration tests for complete game play."""

    def test_two_player_game_completes(self):
        """Test that a 2-player bot game completes."""
        random.seed(42) # For reproducible bot behavior
        game = NineGame()

        bot1 = Bot("Bot1")
        bot2 = Bot("Bot2")
        game.add_player("Bot1", bot1)
        game.add_player("Bot2", bot2)

        game.on_start()

        # Run game for many ticks
        max_ticks = 10000 # Max ticks to prevent infinite loops in case of logic error
        for _ in range(max_ticks):
            if game.status == "finished":
                break
            game.on_tick()

        assert game.status == "finished"
        winner_found = False
        for p in game.players:
            if len(p.hand) == 0:
                winner_found = True
                break
        assert winner_found, "Game finished but no player emptied their hand."

        # Verify final scores are sorted by cards remaining (ascending)
        game_result = game.build_game_result()
        final_scores = game_result.custom_data["final_scores"]
        sorted_player_names = list(final_scores.keys())
        # The winner should have 0 cards, so the first element should be the lowest
        assert final_scores[sorted_player_names[0]] == 0 
        assert final_scores[sorted_player_names[0]] <= final_scores[sorted_player_names[1]]
