"""
Tests for the Metal Pipe game.
"""

import json
import random

from server.games.metalpipe.game import MetalPipeGame, MetalPipePlayer
from server.core.users.test_user import MockUser
from server.core.users.bot import Bot


class TestMetalPipeUnit:
    """Unit tests for Metal Pipe game."""

    def test_game_creation(self):
        """Test creating a new Metal Pipe game."""
        game = MetalPipeGame()
        assert game.get_name() == "Metal Pipe"
        assert game.get_type() == "metalpipe"
        assert game.get_category() == "category-uncategorized"
        assert game.get_min_players() == 2
        assert game.get_max_players() == 8

    def test_player_creation(self):
        """Test creating a player with correct initial state."""
        game = MetalPipeGame()
        user = MockUser("Alice")
        player = game.add_player("Alice", user)

        assert player.name == "Alice"
        assert player.is_bot is False
        assert isinstance(player, MetalPipePlayer)
        assert player.alive is True

    def test_serialization(self):
        """Test that game state can be serialized and deserialized."""
        game = MetalPipeGame()
        user1 = MockUser("Alice")
        user2 = MockUser("Bob")
        game.add_player("Alice", user1)
        game.add_player("Bob", user2)

        # Serialize
        json_str = game.to_json()
        data = json.loads(json_str)

        assert data["options"]["multiple_bonks"] is False
        assert data["options"]["allow_self_bonk"] is True

        # Deserialize
        loaded = MetalPipeGame.from_json(json_str)
        assert loaded.options.multiple_bonks is False
        assert loaded.options.allow_self_bonk is True


class TestMetalPipePlayTest:
    """Integration tests for complete game play."""

    def _run_game_to_completion(self, game, max_ticks=5000):
        """Helper to run a game to completion."""
        game.on_start()
        for _ in range(max_ticks):
            if game.status == "finished":
                break
            game.on_tick()
        assert game.status == "finished"

    def test_single_bonk_completes(self):
        """Test that a single bonk game completes."""
        game = MetalPipeGame()
        bot1 = Bot("Bot1")
        bot2 = Bot("Bot2")
        game.add_player("Bot1", bot1)
        game.add_player("Bot2", bot2)
        self._run_game_to_completion(game)
        assert len(game._winner_names) >= 1

    def test_single_bonk_no_self_bonk(self):
        """Test single bonk with self-bonk disabled always has bonker win."""
        game = MetalPipeGame()
        game.options.allow_self_bonk = False
        bot1 = Bot("Bot1")
        bot2 = Bot("Bot2")
        game.add_player("Bot1", bot1)
        game.add_player("Bot2", bot2)
        self._run_game_to_completion(game)
        # With self-bonk off, bonker always wins (exactly 1 winner)
        assert len(game._winner_names) == 1

    def test_single_bonk_self_bonk_everyone_else_wins(self):
        """Test that self-bonk makes everyone else win."""
        # Force a self-bonk by seeding random
        game = MetalPipeGame()
        game.options.allow_self_bonk = True
        bot1 = Bot("Bot1")
        bot2 = Bot("Bot2")
        bot3 = Bot("Bot3")
        game.add_player("Bot1", bot1)
        game.add_player("Bot2", bot2)
        game.add_player("Bot3", bot3)

        # Run many times to verify logic (self-bonk should yield 2 winners out of 3)
        found_self_bonk = False
        for seed in range(100):
            game2 = MetalPipeGame()
            game2.options.allow_self_bonk = True
            b1 = Bot("Bot1")
            b2 = Bot("Bot2")
            b3 = Bot("Bot3")
            game2.add_player("Bot1", b1)
            game2.add_player("Bot2", b2)
            game2.add_player("Bot3", b3)

            random.seed(seed)
            self._run_game_to_completion(game2)

            if len(game2._winner_names) == 2:
                # Self-bonk occurred: 2 out of 3 players won
                found_self_bonk = True
                break

        assert found_self_bonk, "Expected at least one self-bonk in 100 seeds"

    def test_multiple_bonks_completes(self):
        """Test that multiple bonks mode completes."""
        game = MetalPipeGame()
        game.options.multiple_bonks = True
        for i in range(4):
            bot = Bot(f"Bot{i}")
            game.add_player(f"Bot{i}", bot)
        self._run_game_to_completion(game)
        assert len(game._winner_names) == 1

    def test_multiple_bonks_last_alive_wins(self):
        """Test that in multiple bonks mode, last alive player wins."""
        game = MetalPipeGame()
        game.options.multiple_bonks = True
        for i in range(4):
            bot = Bot(f"Bot{i}")
            game.add_player(f"Bot{i}", bot)
        self._run_game_to_completion(game)

        winner = game._winner_names[0]
        # The winner should be the only alive player
        for player in game.players:
            if player.name == winner:
                assert player.alive is True
            else:
                assert player.alive is False

    def test_multiple_bonks_no_self_bonk(self):
        """Test multiple bonks with self-bonk disabled."""
        game = MetalPipeGame()
        game.options.multiple_bonks = True
        game.options.allow_self_bonk = False
        for i in range(4):
            bot = Bot(f"Bot{i}")
            game.add_player(f"Bot{i}", bot)
        self._run_game_to_completion(game)
        assert len(game._winner_names) == 1

    def test_two_player_multiple_bonks(self):
        """Test 2-player multiple bonks (edge case)."""
        game = MetalPipeGame()
        game.options.multiple_bonks = True
        bot1 = Bot("Bot1")
        bot2 = Bot("Bot2")
        game.add_player("Bot1", bot1)
        game.add_player("Bot2", bot2)
        self._run_game_to_completion(game)
        assert len(game._winner_names) == 1

    def test_eight_player_game(self):
        """Test max player game completes."""
        game = MetalPipeGame()
        game.options.multiple_bonks = True
        for i in range(8):
            bot = Bot(f"Bot{i}")
            game.add_player(f"Bot{i}", bot)
        self._run_game_to_completion(game)
        assert len(game._winner_names) == 1

    def test_game_result_built(self):
        """Test that game result is built correctly."""
        game = MetalPipeGame()
        game.options.multiple_bonks = True
        for i in range(3):
            bot = Bot(f"Bot{i}")
            game.add_player(f"Bot{i}", bot)
        self._run_game_to_completion(game)

        result = game.build_game_result()
        assert result.game_type == "metalpipe"
        assert len(result.player_results) == 3
        assert "winner_names" in result.custom_data
        assert result.custom_data["multiple_bonks"] is True


class TestMetalPipePersistence:
    """Tests for game persistence."""

    def test_options_preserved(self):
        """Test that options are preserved through save/load."""
        game = MetalPipeGame()
        game.options.multiple_bonks = True
        game.options.allow_self_bonk = False

        user1 = MockUser("Alice")
        user2 = MockUser("Bob")
        game.add_player("Alice", user1)
        game.add_player("Bob", user2)

        json_str = game.to_json()
        loaded = MetalPipeGame.from_json(json_str)

        assert loaded.options.multiple_bonks is True
        assert loaded.options.allow_self_bonk is False
