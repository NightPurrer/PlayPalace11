"""Tests for Hangin' with Friends."""

import json
import random
from pathlib import Path

from server.games.hangin_with_friends.game import (
    BOT_DIFFICULTY_CHOICES,
    WHEEL_OUTCOMES,
    HanginWithFriendsGame,
    HanginWithFriendsOptions,
)
from server.users.bot import Bot
from server.users.test_user import MockUser


class TestHanginWithFriendsUnit:
    """Unit tests for Hangin' with Friends core logic."""

    def test_game_creation(self):
        game = HanginWithFriendsGame()
        assert game.get_name() == "Hangin' with Friends"
        assert game.get_type() == "hangin_with_friends"
        assert game.get_category() == "category-word-games"
        assert game.get_min_players() == 2
        assert game.get_max_players() == 2

    def test_player_creation(self):
        game = HanginWithFriendsGame()
        user = MockUser("Alice")
        player = game.add_player("Alice", user)
        assert player.balloons_remaining == 5
        assert player.score == 0

    def test_options_defaults_include_no_limits(self):
        game = HanginWithFriendsGame()
        assert game.options.max_rounds == 0
        assert game.options.max_score == 0
        assert game.options.spectators_see_all_actions is True

    def test_serialization(self):
        game = HanginWithFriendsGame()
        user1 = MockUser("Alice")
        user2 = MockUser("Bob")
        p1 = game.add_player("Alice", user1)
        p2 = game.add_player("Bob", user2)
        game.on_start()

        game.phase = "guessing"
        game.setter_id = p1.id
        game.guesser_id = p2.id
        game.tile_rack = list("planetzebraxy")
        game.secret_word = "planet"
        game.masked_word = "pl_ne_"
        game.guessed_letters = ["p", "l", "n", "e"]
        game.wrong_guesses = 2
        game.max_wrong_guesses = 8
        p1.balloons_remaining = 4
        p2.balloons_remaining = 3

        data = json.loads(game.to_json())
        assert data["secret_word"] == "planet"
        assert data["masked_word"] == "pl_ne_"
        assert data["wrong_guesses"] == 2
        assert data["players"][0]["balloons_remaining"] == 4

        loaded = HanginWithFriendsGame.from_json(game.to_json())
        assert loaded.secret_word == "planet"
        assert loaded.masked_word == "pl_ne_"
        assert loaded.wrong_guesses == 2
        assert loaded.players[0].balloons_remaining == 4

    def test_bot_difficulty_word_buckets(self):
        game = HanginWithFriendsGame()
        candidates = ["eat", "dog", "queen", "jazz"]

        game.options.default_bot_difficulty = "easy"
        assert game._select_bot_word_by_difficulty(candidates) == "eat"

        game.options.default_bot_difficulty = "medium"
        assert game._select_bot_word_by_difficulty(candidates) == "dog"

        game.options.default_bot_difficulty = "hard"
        assert game._select_bot_word_by_difficulty(candidates) == "queen"

        game.options.default_bot_difficulty = "extreme"
        assert game._select_bot_word_by_difficulty(candidates) == "jazz"

    def test_invalid_bot_difficulty_defaults_to_medium(self):
        game = HanginWithFriendsGame()
        candidates = ["eat", "dog", "queen", "jazz"]
        game.options.default_bot_difficulty = "unknown"
        assert game._select_bot_word_by_difficulty(candidates) == "dog"

    def test_per_bot_difficulty_override(self):
        game = HanginWithFriendsGame()
        host = MockUser("Host")
        bot = Bot("Bot1")
        host_player = game.add_player("Host", host)
        bot_player = game.add_player("Bot1", bot)
        game.host = "Host"
        game.status = "waiting"
        game.options.default_bot_difficulty = "easy"

        options = game._per_bot_difficulty_options(host_player)
        target = f"{bot_player.name}|extreme"
        assert target in options

        game.execute_action(host_player, "set_bot_difficulty", target)
        assert game.bot_difficulties[bot_player.id] == "extreme"
        assert game._effective_bot_difficulty(bot_player) == "extreme"


class TestHanginWithFriendsActions:
    """Action tests for round flow."""

    def setup_method(self):
        random.seed(123)
        self.game = HanginWithFriendsGame(
            options=HanginWithFriendsOptions(starting_balloons=3)
        )
        self.user1 = MockUser("Alice")
        self.user2 = MockUser("Bob")
        self.p1 = self.game.add_player("Alice", self.user1)
        self.p2 = self.game.add_player("Bob", self.user2)
        self.game.on_start()

    def _force_round(self, setter, guesser, word: str):
        self.game.phase = "choose_word"
        self.game.setter_id = setter.id
        self.game.guesser_id = guesser.id
        self.game.current_player = setter
        self.game.tile_rack = list(word + "zzzzzzzzzzzz")[:12]

    def test_choose_word_and_guess_letter(self):
        self._force_round(self.p1, self.p2, "planet")
        self.game.execute_action(self.p1, "choose_word", "planet")
        assert self.game.phase == "guessing"
        assert self.game.current_player == self.p2
        assert self.game.masked_word == "______"

        self.game.execute_action(self.p2, "guess_letter_p")
        assert self.game.masked_word[0] == "p"
        assert "p" in self.game.guessed_letters

    def test_solved_word_makes_setter_lose_balloon(self):
        self._force_round(self.p1, self.p2, "cat")
        self.game.execute_action(self.p1, "choose_word", "cat")
        before = self.p1.balloons_remaining

        self.game.execute_action(self.p2, "guess_letter_c")
        self.game.execute_action(self.p2, "guess_letter_a")
        self.game.execute_action(self.p2, "guess_letter_t")

        assert self.p1.balloons_remaining == before - 1

    def test_failed_round_makes_guesser_lose_balloon(self):
        self._force_round(self.p1, self.p2, "cat")
        self.game.execute_action(self.p1, "choose_word", "cat")
        self.game.max_wrong_guesses = 1
        before = self.p2.balloons_remaining

        self.game.execute_action(self.p2, "guess_letter_z")
        assert self.p2.balloons_remaining == before - 1

    def test_invalid_word_rejected(self):
        self._force_round(self.p1, self.p2, "cat")
        self.game.execute_action(self.p1, "choose_word", "toolongword")
        assert self.game.phase == "choose_word"
        self.game.execute_action(self.p1, "choose_word", "123")
        assert self.game.phase == "choose_word"

    def test_max_score_limit_ends_game(self):
        self.game.options.max_score = 1
        self._force_round(self.p1, self.p2, "cat")
        self.game.execute_action(self.p1, "choose_word", "cat")
        self.game.execute_action(self.p2, "guess_letter_c")
        self.game.execute_action(self.p2, "guess_letter_a")
        self.game.execute_action(self.p2, "guess_letter_t")
        assert not self.game.game_active
        assert self.game.status == "finished"

    def test_max_rounds_limit_ends_game(self):
        self.game.options.max_rounds = 1
        self._force_round(self.p1, self.p2, "cat")
        self.game.execute_action(self.p1, "choose_word", "cat")
        self.game.max_wrong_guesses = 1
        self.game.execute_action(self.p2, "guess_letter_z")
        assert not self.game.game_active
        assert self.game.status == "finished"

    def test_zero_limits_do_not_apply(self):
        self.game.options.max_rounds = 0
        self.game.options.max_score = 0
        self.game.round = 999
        self.p1.score = 999
        self.p1.balloons_remaining = 2
        self.p2.balloons_remaining = 2
        assert self.game._check_match_end() is False


class TestHanginSpectatorVisibility:
    """Spectator private-state visibility tests."""

    def _setup_game(self, spectators_see_all_actions: bool):
        game = HanginWithFriendsGame()
        u1 = MockUser("Alice")
        u2 = MockUser("Bob")
        us = MockUser("Spec")
        p1 = game.add_player("Alice", u1)
        p2 = game.add_player("Bob", u2)
        game.add_spectator("Spec", us)
        game.options.spectators_see_all_actions = spectators_see_all_actions
        game.on_start()
        game.phase = "choose_word"
        game.setter_id = p1.id
        game.guesser_id = p2.id
        game.current_player = p1
        game.tile_rack = list("planetzzzzzz")
        us.clear_messages()
        return game, p1, p2, us

    def test_spectator_gets_private_state_when_enabled(self):
        game, p1, p2, spectator = self._setup_game(True)
        game.execute_action(p1, "choose_word", "planet")
        game.execute_action(p2, "guess_letter_p")
        spoken = spectator.get_spoken_messages()
        assert any(msg.startswith("Secret word chosen by Alice: PLANET") for msg in spoken)
        assert any(msg.startswith("Alice board:") for msg in spoken)
        assert any(msg.startswith("Bob board:") for msg in spoken)

    def test_spectator_private_state_hidden_when_disabled(self):
        game, p1, p2, spectator = self._setup_game(False)
        game.execute_action(p1, "choose_word", "planet")
        game.execute_action(p2, "guess_letter_p")
        spoken = spectator.get_spoken_messages()
        assert not any(msg.startswith("Secret word chosen by Alice: PLANET") for msg in spoken)
        assert not any(msg.startswith("Alice board:") for msg in spoken)
        assert not any(msg.startswith("Bob board:") for msg in spoken)


class TestHanginWithFriendsPlay:
    """Play test with bots and persistence reload."""

    def test_two_bot_game_completes(self):
        random.seed(999)
        game = HanginWithFriendsGame(
            options=HanginWithFriendsOptions(starting_balloons=2)
        )
        bot1 = Bot("Bot1")
        bot2 = Bot("Bot2")
        game.add_player("Bot1", bot1)
        game.add_player("Bot2", bot2)
        game.on_start()

        for tick in range(2500):
            if not game.game_active:
                break

            if tick > 0 and tick % 50 == 0:
                payload = game.to_json()
                game = HanginWithFriendsGame.from_json(payload)
                game.attach_user("Bot1", bot1)
                game.attach_user("Bot2", bot2)
                game.rebuild_runtime_state()
                for player in game.players:
                    user = game.get_user(player)
                    if user:
                        game.setup_player_actions(player)

            game.on_tick()

        assert not game.game_active, "Game should complete with two bots"


class TestHanginCoverageEdges:
    """Target uncovered branches in hangin_with_friends game logic."""

    def setup_method(self):
        self.game = HanginWithFriendsGame()
        self.u1 = MockUser("Host")
        self.u2 = MockUser("BotX")
        self.p1 = self.game.add_player("Host", self.u1)
        self.p2 = self.game.add_player("BotX", Bot("BotX"))
        self.game.host = "Host"
        self.game.status = "waiting"

    def _start_two_player_round(self):
        self.game.on_start()
        self.game.phase = "choose_word"
        self.game.setter_id = self.game.players[0].id
        self.game.guesser_id = self.game.players[1].id
        self.game.current_player = self.game.players[0]
        self.game.tile_rack = list("planetzzzzzz")
        return self.game.players[0], self.game.players[1]

    def test_prestart_validate_errors(self):
        self.game.options.min_word_length = 8
        self.game.options.max_word_length = 3
        self.game.options.rack_size = 2
        errors = self.game.prestart_validate()
        assert "hwf-error-min-length-greater-than-max" in errors
        assert "hwf-error-rack-smaller-than-max-length" in errors

    def test_lava_scheduler_and_tick(self):
        self.game.sound_scheduler_tick = 10
        self.game._schedule_next_lava_ambience(initial=True)
        assert self.game.lava_next_tick > 10
        self.game.lava_next_tick = self.game.sound_scheduler_tick
        self.game._maybe_play_lava_ambience()
        assert any("bg_lava5.ogg" in s for s in self.u1.get_sounds_played())
        self.game.lava_next_tick = self.game.sound_scheduler_tick + 100
        self.u1.clear_messages()
        self.game._maybe_play_lava_ambience()
        assert not any("bg_lava5.ogg" in s for s in self.u1.get_sounds_played())

    def test_setup_keybinds_and_start_round_match_end_guard(self, monkeypatch):
        game = HanginWithFriendsGame()
        game.setup_keybinds()
        assert "w" in game._keybinds
        assert "c" in game._keybinds
        assert "1" in game._keybinds
        assert "2" in game._keybinds
        assert "3" in game._keybinds

        game.add_player("A", MockUser("A"))
        game.add_player("B", MockUser("B"))
        game.round = 5
        monkeypatch.setattr(game, "_check_match_end", lambda: True)
        game._start_round()
        assert game.round == 5

    def test_start_round_short_player_list(self):
        solo = HanginWithFriendsGame()
        u = MockUser("Solo")
        p = solo.add_player("Solo", u)
        solo.set_turn_players([p])
        solo.round = 0
        solo._start_round()
        assert solo.round == 1
        assert solo.phase == "lobby"

    def test_action_choose_word_invalid_paths(self):
        setter, _ = self._start_two_player_round()
        self.game.options.dictionary_mode = "strict"
        self.game._dictionary_loaded = True
        self.game._dictionary_words = ("planet",)
        self.game.execute_action(setter, "choose_word", "123")
        self.game.execute_action(setter, "choose_word", "thisislonger")
        self.game.execute_action(setter, "choose_word", "apple")  # not rack-valid
        self.game.execute_action(setter, "choose_word", "plank")  # strict miss
        assert self.game.phase == "choose_word"
        assert any("sfx_submitwordinvalid6.ogg" in s for s in self.u1.get_sounds_played())

    def test_action_choose_word_strict_dictionary_branch(self):
        setter, _ = self._start_two_player_round()
        self.game.options.dictionary_mode = "strict"
        self.game._dictionary_loaded = True
        self.game._dictionary_words = ("planet",)
        self.game.tile_rack = list("plankzzzzzzz")
        self.game.execute_action(setter, "choose_word", "plank")
        assert self.game.phase == "choose_word"
        assert any("strict mode" in m for m in self.u1.get_spoken_messages())

    def test_action_choose_word_with_missing_guesser(self):
        setter, _ = self._start_two_player_round()
        self.game.guesser_id = "missing"
        self.game.execute_action(setter, "choose_word", "planet")
        assert self.game.phase == "choose_word"

    def test_action_guess_word_invalid_and_no_fullword(self):
        game = HanginWithFriendsGame()
        u1 = MockUser("S1")
        u2 = MockUser("S2")
        p1 = game.add_player("S1", u1)
        p2 = game.add_player("S2", u2)
        game.on_start()
        game.phase = "choose_word"
        game.setter_id = p1.id
        game.guesser_id = p2.id
        game.current_player = p1
        game.tile_rack = list("planetzzzzzz")
        game.execute_action(p1, "choose_word", "planet")
        game.options.allow_full_word_guess = False
        game.execute_action(p2, "guess_word", "planet")
        game.options.allow_full_word_guess = True
        game.execute_action(p2, "guess_word", "12")
        spoken = game.get_user(p2).get_spoken_messages()
        assert any("Word guess must contain letters only." in m for m in spoken)

    def test_action_guess_word_disabled_and_wrong_guess_paths(self):
        setter, guesser = self._start_two_player_round()
        self.game.execute_action(setter, "choose_word", "planet")
        self.game.options.allow_full_word_guess = False
        wrong_before = self.game.wrong_guesses
        self.game._action_guess_word(guesser, "planet", "guess_word")
        assert self.game.wrong_guesses == wrong_before

        self.game.options.allow_full_word_guess = True
        self.game.max_wrong_guesses = 5
        self.game._action_guess_word(guesser, "plank", "guess_word")
        assert self.game.phase == "guessing"
        assert self.game.wrong_guesses == wrong_before + 1

    def test_lifeline_actions_and_guards(self):
        setter, guesser = self._start_two_player_round()
        self.game.execute_action(setter, "choose_word", "planet")
        guesser = self.game.get_player_by_id(self.game.guesser_id)
        assert guesser is not None
        # guard branches with no resources
        assert self.game._is_lifeline_remove_enabled(guesser) == "action-not-available"
        # reveal
        guesser.lifeline_reveal = 1
        self.game.execute_action(guesser, "lifeline_reveal")
        assert guesser.lifeline_reveal == 0
        # remove strike
        self.game.wrong_guesses = 1
        guesser.lifeline_remove = 1
        self.game.execute_action(guesser, "lifeline_remove")
        assert self.game.wrong_guesses == 0
        # retry
        guesser.lifeline_retry = 1
        self.game.execute_action(guesser, "lifeline_retry")
        assert guesser.retry_shield_active
        # wrong guess consumed by shield
        self.game._apply_wrong_guess(guesser)
        assert not guesser.retry_shield_active

    def test_lifeline_early_return_paths(self):
        setter, guesser = self._start_two_player_round()
        self.game.execute_action(setter, "choose_word", "planet")
        guesser = self.game.get_player_by_id(self.game.guesser_id)
        assert guesser is not None

        guesser.lifeline_reveal = 0
        self.game._action_lifeline_reveal(guesser, "lifeline_reveal")
        guesser.lifeline_reveal = 1
        self.game.masked_word = self.game.secret_word
        self.game._action_lifeline_reveal(guesser, "lifeline_reveal")

        guesser.lifeline_remove = 0
        self.game.wrong_guesses = 1
        self.game._action_lifeline_remove(guesser, "lifeline_remove")
        guesser.lifeline_remove = 1
        self.game.wrong_guesses = 0
        self.game._action_lifeline_remove(guesser, "lifeline_remove")

        guesser.lifeline_retry = 0
        guesser.retry_shield_active = False
        self.game._action_lifeline_retry(guesser, "lifeline_retry")
        guesser.lifeline_retry = 1
        guesser.retry_shield_active = True
        self.game._action_lifeline_retry(guesser, "lifeline_retry")

    def test_retry_guard_branch_when_shield_active(self):
        setter, _ = self._start_two_player_round()
        self.game.execute_action(setter, "choose_word", "planet")
        guesser = self.game.get_player_by_id(self.game.guesser_id)
        assert guesser is not None
        guesser.lifeline_retry = 1
        guesser.retry_shield_active = True
        assert self.game._is_lifeline_retry_enabled(guesser) == "action-not-available"
        guesser.lifeline_remove = 1
        self.game.wrong_guesses = 0
        assert self.game._is_lifeline_remove_enabled(guesser) == "action-not-available"

    def test_set_bot_difficulty_invalid_paths(self):
        # malformed value branch
        self.game._action_set_bot_difficulty(self.p1, "bad", "set_bot_difficulty")
        # missing bot branch
        self.game._action_set_bot_difficulty(self.p1, "NoBot|hard", "set_bot_difficulty")
        assert self.game.bot_difficulties == {}

    def test_set_bot_difficulty_enabled_no_bots_branch(self):
        game = HanginWithFriendsGame()
        host_user = MockUser("HostOnly")
        host_player = game.add_player("HostOnly", host_user)
        game.host = "HostOnly"
        game.status = "waiting"
        assert game._is_set_bot_difficulty_enabled(host_player) == "action-no-bots"

    def test_spin_wheel_all_outcomes(self, monkeypatch):
        setter, guesser = self._start_two_player_round()
        self.game.secret_word = "planet"
        self.game.max_wrong_guesses = 5

        class FixedRandom:
            def __init__(self, *_args, **_kwargs):
                pass

            def choice(self, _items):
                return self.value

        for outcome in WHEEL_OUTCOMES:
            fixed = FixedRandom()
            fixed.value = outcome
            monkeypatch.setattr("server.games.hangin_with_friends.game.random.Random", lambda *_a, **_k: fixed)
            before = (guesser.coins, guesser.lifeline_reveal, guesser.lifeline_remove, guesser.lifeline_retry)
            self.game._spin_wheel(guesser)
            assert self.game.wheel_result == outcome
            after = (guesser.coins, guesser.lifeline_reveal, guesser.lifeline_remove, guesser.lifeline_retry)
            if outcome == "nothing":
                assert after == before

    def test_bot_paths_and_utilities(self, monkeypatch, tmp_path):
        setter, guesser = self._start_two_player_round()
        self.game.secret_word = "planet"
        self.game.masked_word = "______"
        self.game.max_wrong_guesses = 3
        self.game.phase = "guessing"
        self.game.guesser_id = guesser.id
        # bot_think branches
        guesser.lifeline_remove = 1
        self.game.wrong_guesses = self.game.max_wrong_guesses - 1
        assert self.game.bot_think(guesser) == "lifeline_remove"
        guesser.lifeline_remove = 0
        guesser.lifeline_retry = 1
        self.game.wrong_guesses = self.game.max_wrong_guesses - 2
        assert self.game.bot_think(guesser) == "lifeline_retry"
        guesser.lifeline_retry = 0
        guesser.lifeline_reveal = 1
        assert self.game.bot_think(guesser) == "lifeline_reveal"

        # guess_word fallback
        self.game.masked_word = "____"
        self.game.secret_word = ""
        assert self.game._get_candidate_words() == []
        assert self.game._bot_guess_word_input(guesser) == "aaaa"

        # choose_word fallback with no candidates
        self.game.tile_rack = list("zzzzzzzzzzzz")
        self.game.options.min_word_length = 3
        assert len(self.game._bot_choose_word_input(guesser)) == 3

        # buckets with empty ranked list
        assert self.game._build_score_buckets([]) == [[], [], [], []]

        # normalize/effective difficulty fallback
        self.game.options.default_bot_difficulty = "weird"
        non_bot = self.game.players[0]
        assert self.game._effective_bot_difficulty(non_bot) == "medium"

        # sync stale bot overrides cleanup
        self.game.bot_difficulties["stale"] = "hard"
        self.game._sync_bot_difficulty_overrides()
        assert "stale" not in self.game.bot_difficulties

        # dictionary load early return
        self.game._dictionary_loaded = True
        old_words = self.game._dictionary_words
        self.game._load_dictionary()
        assert self.game._dictionary_words == old_words

        # read_words filters and keeps alpha/length only
        words_file = tmp_path / "words.txt"
        words_file.write_text("ab\nabc\nabcd1\nplanet\nzzzzzzzzzzzzzz\n", encoding="utf-8")
        self.game.options.min_word_length = 3
        self.game.options.max_word_length = 8
        loaded = self.game._read_words(Path(words_file))
        assert "abc" in loaded
        assert "planet" in loaded
        assert "ab" not in loaded

        # bot_think early return branch
        self.game.phase = "choose_word"
        self.game.setter_id = setter.id
        assert self.game.bot_think(guesser) is None

        # sparse bucket rebalance branch
        buckets = self.game._build_score_buckets(["solo"])
        assert all(bucket for bucket in buckets)

    def test_guess_resolution_missing_and_repeated_paths(self):
        setter, guesser = self._start_two_player_round()
        self.game.execute_action(setter, "choose_word", "planet")
        self.game.guesser_id = "missing"
        self.game._resolve_letter_guess("p")

        self.game.guesser_id = guesser.id
        self.game._resolve_letter_guess("p")
        first_state = (self.game.masked_word, list(self.game.guessed_letters))
        self.game._resolve_letter_guess("p")
        assert (self.game.masked_word, self.game.guessed_letters) == first_state

    def test_guess_word_wrong_guess_resolve_round_branch(self, monkeypatch):
        setter, guesser = self._start_two_player_round()
        self.game.execute_action(setter, "choose_word", "planet")
        self.game.max_wrong_guesses = 1
        self.game.wrong_guesses = 0
        called = {"value": None}

        def fake_resolve_round(*, guesser_solved: bool):
            called["value"] = guesser_solved

        monkeypatch.setattr(self.game, "_resolve_round", fake_resolve_round)
        self.game._action_guess_word(guesser, "plank", "guess_word")
        assert called["value"] is False

    def test_resolve_round_missing_players_and_level_up(self):
        self.game.on_start()
        self.game.setter_id = "missing"
        self.game.guesser_id = "missing"
        self.game._resolve_round(guesser_solved=True)

        player = self.game.players[0]
        player.level = 1
        player.score = 0
        self.game._award_score(player, 5)
        assert player.level >= 2

    def test_check_match_end_no_active_players(self):
        game = HanginWithFriendsGame()
        spectator = game.add_spectator("Spec", MockUser("Spec"))
        assert spectator.is_spectator
        assert game._check_match_end() is False

    def test_spectator_board_broadcast_skips_spectator_participants(self, monkeypatch):
        game = HanginWithFriendsGame()
        active = game.add_player("P1", MockUser("P1"))
        spectator_participant = game.add_spectator("SpecP", MockUser("SpecP"))
        spectator_listener = game.add_spectator("SpecL", MockUser("SpecL"))
        assert spectator_participant.is_spectator
        assert spectator_listener.is_spectator
        game.options.spectators_see_all_actions = True

        monkeypatch.setattr(game, "get_active_players", lambda: [active, spectator_participant])
        game._broadcast_spectator_player_boards()
        spoken = game.get_user(spectator_listener).get_spoken_messages()
        assert any(msg.startswith("P1 board:") for msg in spoken)
        assert not any(msg.startswith("SpecP board:") for msg in spoken)

    def test_add_remove_bot_actions_sync_difficulty_overrides(self):
        game = HanginWithFriendsGame()
        host_user = MockUser("Host")
        host_player = game.add_player("Host", host_user)
        game.host = "Host"
        game.status = "waiting"
        game._action_add_bot(host_player, "", "add_bot")
        bot_ids = [p.id for p in game.players if p.is_bot]
        assert bot_ids
        for bot_id in bot_ids:
            assert bot_id in game.bot_difficulties
        game._action_remove_bot(host_player, "remove_bot")
        remaining_bot_ids = {p.id for p in game.players if p.is_bot}
        assert all(bot_id in remaining_bot_ids for bot_id in game.bot_difficulties)

    def test_score_bucket_right_fill_branch(self, monkeypatch):
        game = HanginWithFriendsGame()

        def fake_ceil(value: float) -> int:
            if value <= 0.5:
                return 0
            return 1

        monkeypatch.setattr("server.games.hangin_with_friends.game.math.ceil", fake_ceil)
        buckets = game._build_score_buckets(["solo"])
        assert all(bucket for bucket in buckets)

    def test_finish_with_winner_and_format_screen(self):
        game = HanginWithFriendsGame()
        a = game.add_player("A", MockUser("A"))
        b = game.add_player("B", MockUser("B"))
        a.score = 5
        b.score = 2
        lines = game.format_end_screen(
            game.build_game_result(),
            "en",
        )
        assert any("Winner:" in line for line in lines)

        # winner sound / loser sound path
        game._finish_with_winner(a, "done")
        sounds_a = game.get_user(a).get_sounds_played()
        sounds_b = game.get_user(b).get_sounds_played()
        assert any("sfx_gamewon1.ogg" in s for s in sounds_a)
        assert any("sfx_gamelost1.ogg" in s for s in sounds_b)
