import random

from server.core.users.bot import Bot
from server.core.users.test_user import MockUser
from server.game_utils.cards import Card, Deck
from server.games.blackjack.game import BlackjackGame, BlackjackOptions


def make_card(card_id: int, rank: int, suit: int) -> Card:
    return Card(id=card_id, rank=rank, suit=suit)


def create_game_with_host() -> tuple[BlackjackGame, object, MockUser]:
    game = BlackjackGame()
    host_user = MockUser("Host")
    host_player = game.add_player("Host", host_user)
    game.host = "Host"
    return game, host_player, host_user


def test_blackjack_game_creation() -> None:
    game = BlackjackGame()
    assert game.get_name() == "Blackjack"
    assert game.get_name_key() == "game-name-blackjack"
    assert game.get_type() == "blackjack"
    assert game.get_category() == "category-card-games"
    assert game.get_min_players() == 1
    assert game.get_max_players() == 7


def test_blackjack_options_defaults() -> None:
    game = BlackjackGame()
    assert game.options.rules_profile == "vegas"
    assert game.options.starting_chips == 500
    assert game.options.base_bet == 10
    assert game.options.table_min_bet == 5
    assert game.options.table_max_bet == 100
    assert game.options.deck_count == 4
    assert game.options.dealer_hits_soft_17 is True
    assert game.options.dealer_peeks_blackjack is True
    assert game.options.players_cards_face_up is True
    assert game.options.allow_insurance is True
    assert game.options.allow_late_surrender is True
    assert game.options.blackjack_payout == "3_to_2"
    assert game.options.double_down_rule == "any_two"
    assert game.options.allow_double_after_split is True
    assert game.options.split_rule == "same_rank"
    assert game.options.max_split_hands == 2
    assert game.options.split_aces_one_card_only is True
    assert game.options.split_aces_count_as_blackjack is False
    assert game.options.turn_timer == "0"


def test_blackjack_prestart_validation_rejects_large_bet() -> None:
    game = BlackjackGame(options=BlackjackOptions(starting_chips=50, base_bet=100))
    host_user = MockUser("Host")
    game.add_player("Host", host_user)
    errors = game.prestart_validate()
    assert "blackjack-error-bet-too-high" in errors


def test_blackjack_prestart_validation_rejects_invalid_table_limits() -> None:
    game = BlackjackGame(
        options=BlackjackOptions(
            starting_chips=500,
            base_bet=10,
            table_min_bet=25,
            table_max_bet=20,
        )
    )
    host_user = MockUser("Host")
    game.add_player("Host", host_user)
    errors = game.prestart_validate()
    assert "blackjack-error-table-limits-invalid" in errors
    assert "blackjack-error-bet-below-min" in errors


def test_blackjack_hand_value_handles_soft_aces() -> None:
    game = BlackjackGame()
    hand = [make_card(1, 1, 1), make_card(2, 6, 2)]
    total, soft = game.hand_value(hand)
    assert total == 17
    assert soft is True

    hand.append(make_card(3, 10, 3))
    total, soft = game.hand_value(hand)
    assert total == 17
    assert soft is False


def test_blackjack_on_start_deals_and_posts_bets() -> None:
    game, host_player, _host_user = create_game_with_host()
    game.options = BlackjackOptions(starting_chips=100, base_bet=10, deck_count=1)
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)

    game.on_start()

    assert game.status == "playing"
    assert len(host_player.hand) == 2
    assert len(guest_player.hand) == 2
    assert len(game.dealer_hand) == 2
    assert host_player.bet == 10
    assert guest_player.bet == 10
    assert host_player.chips == 90
    assert guest_player.chips == 90


def test_blackjack_on_start_single_player_does_not_end_immediately() -> None:
    game, host_player, _host_user = create_game_with_host()
    game.options = BlackjackOptions(starting_chips=100, base_bet=10, deck_count=1)

    game.on_start()

    assert game.status == "playing"
    assert game.phase in {"players", "insurance", "settle"}
    assert game.hand_number == 1
    assert host_player.bet > 0
    assert len(host_player.hand) == 2
    assert len(game.dealer_hand) == 2


def test_blackjack_settle_single_player_continues_when_player_has_chips() -> None:
    game, host_player, _host_user = create_game_with_host()
    game.status = "playing"
    game.game_active = True
    game.phase = "players"
    host_player.chips = 90
    host_player.bet = 10
    host_player.hand = [make_card(1, 10, 1), make_card(2, 9, 2)]
    host_player.hand_done = True
    game.dealer_hand = [make_card(3, 10, 3), make_card(4, 7, 4)]  # dealer 17, player 19 wins

    game._settle_hand()

    assert game.status == "playing"
    assert game.next_hand_wait_ticks == 40
    assert host_player.chips == 110


def test_blackjack_hit_bust_advances_turn() -> None:
    game, host_player, _host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)

    game.status = "playing"
    game.game_active = True
    game.phase = "players"
    game.set_turn_players([host_player, guest_player], reset_index=True)
    game.deck = Deck(cards=[make_card(9, 10, 1)])
    game.dealer_hand = [make_card(10, 9, 2), make_card(11, 7, 3)]

    host_player.hand = [make_card(1, 10, 1), make_card(2, 9, 1)]
    host_player.bet = 10
    guest_player.hand = [make_card(3, 5, 1), make_card(4, 6, 1)]
    guest_player.bet = 10

    game._action_hit(host_player, "hit")

    assert host_player.busted is True
    assert host_player.hand_done is True
    assert game.current_player == guest_player


def test_blackjack_split_creates_two_hands() -> None:
    game, host_player, _host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)
    game.status = "playing"
    game.game_active = True
    game.phase = "players"
    game.set_turn_players([host_player, guest_player], reset_index=True)
    game.deck = Deck(cards=[make_card(900, 3, 1), make_card(901, 4, 2)])

    host_player.hand = [make_card(1, 8, 1), make_card(2, 8, 2)]
    host_player.bet = 10
    host_player.chips = 90

    game._action_split(host_player, "split")

    assert host_player.split_bet == 10
    assert host_player.chips == 80
    assert len(host_player.hand) == 2
    assert len(host_player.split_hand) == 2
    assert host_player.active_hand_index == 0
    assert game.current_player == host_player


def test_blackjack_double_down_increases_bet_and_ends_hand() -> None:
    game, host_player, _host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)
    game.status = "playing"
    game.game_active = True
    game.phase = "players"
    game.set_turn_players([host_player, guest_player], reset_index=True)
    game.deck = Deck(cards=[make_card(910, 10, 1)])

    host_player.hand = [make_card(1, 5, 1), make_card(2, 6, 2)]
    host_player.bet = 10
    host_player.chips = 90

    game._action_double_down(host_player, "double_down")

    assert host_player.bet == 20
    assert host_player.chips == 80
    assert len(host_player.hand) == 3
    assert host_player.hand_done is True
    assert game.current_player == guest_player


def test_blackjack_late_surrender_refunds_half_and_advances() -> None:
    game, host_player, _host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)
    game.status = "playing"
    game.game_active = True
    game.phase = "players"
    game.set_turn_players([host_player, guest_player], reset_index=True)

    host_player.hand = [make_card(1, 10, 1), make_card(2, 6, 2)]
    host_player.bet = 10
    host_player.chips = 90

    game._action_surrender(host_player, "surrender")

    assert host_player.chips == 95
    assert host_player.surrendered_main is True
    assert host_player.hand_done is True
    assert game.current_player == guest_player


def test_blackjack_insurance_wins_when_dealer_has_blackjack() -> None:
    game, host_player, _host_user = create_game_with_host()
    game.status = "playing"
    game.game_active = True
    game.phase = "insurance"
    game.set_turn_players([host_player], reset_index=True)
    game._advance_insurance_to_next_player = lambda: None  # type: ignore[method-assign]

    host_player.hand = [make_card(1, 10, 1), make_card(2, 9, 2)]
    host_player.bet = 10
    host_player.chips = 90
    host_player.insurance_decision_done = False
    game.dealer_hand = [make_card(10, 1, 3), make_card(11, 13, 4)]

    game._action_take_insurance(host_player, "take_insurance")

    assert host_player.insurance_bet == 5
    assert host_player.chips == 85
    assert host_player.insurance_decision_done is True

    host_player.hand_done = True
    game._settle_hand()
    assert host_player.chips == 100


def test_blackjack_even_money_pays_one_to_one() -> None:
    game, host_player, _host_user = create_game_with_host()
    game.status = "playing"
    game.game_active = True
    game.phase = "insurance"
    game.set_turn_players([host_player], reset_index=True)
    game._advance_insurance_to_next_player = lambda: None  # type: ignore[method-assign]

    host_player.hand = [make_card(1, 1, 1), make_card(2, 13, 2)]
    host_player.has_blackjack = True
    host_player.bet = 10
    host_player.chips = 90
    host_player.insurance_decision_done = False
    game.dealer_hand = [make_card(10, 1, 3), make_card(11, 13, 4)]

    game._action_even_money(host_player, "even_money")

    assert host_player.took_even_money is True
    assert host_player.insurance_decision_done is True

    host_player.hand_done = True
    game._settle_hand()
    assert host_player.chips == 110


def test_blackjack_should_offer_insurance_when_dealer_shows_ace() -> None:
    game, host_player, _host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)
    host_player.bet = 10
    host_player.chips = 100
    guest_player.bet = 10
    guest_player.chips = 100
    game.dealer_hand = [make_card(10, 1, 3), make_card(11, 7, 4)]

    assert game._should_offer_insurance([host_player, guest_player]) is True

    game.options.allow_insurance = False
    assert game._should_offer_insurance([host_player, guest_player]) is False


def test_blackjack_split_limit_disables_split() -> None:
    game, host_player, _host_user = create_game_with_host()
    game.options.max_split_hands = 1
    host_player.hand = [make_card(1, 8, 1), make_card(2, 8, 2)]
    host_player.bet = 10
    host_player.chips = 100
    assert game._can_split(host_player) is False


def test_blackjack_split_aces_auto_stand_when_enabled() -> None:
    game, host_player, _host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)
    game.status = "playing"
    game.game_active = True
    game.phase = "players"
    game.set_turn_players([host_player, guest_player], reset_index=True)
    game.options.split_aces_one_card_only = True
    game.deck = Deck(cards=[make_card(900, 9, 1), make_card(901, 8, 2)])

    host_player.hand = [make_card(1, 1, 1), make_card(2, 1, 2)]
    host_player.bet = 10
    host_player.chips = 90

    game._action_split(host_player, "split")

    assert host_player.hand_done is True
    assert host_player.split_hand_done is True
    assert host_player.main_from_split_aces is True
    assert host_player.split_from_split_aces is True
    assert game.current_player == guest_player


def test_blackjack_split_aces_can_count_as_blackjack() -> None:
    game, host_player, _host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)
    game.status = "playing"
    game.game_active = True
    game.phase = "players"
    game.set_turn_players([host_player, guest_player], reset_index=True)
    game.options.split_aces_one_card_only = True
    game.options.split_aces_count_as_blackjack = True
    game.deck = Deck(cards=[make_card(900, 10, 1), make_card(901, 10, 2)])

    host_player.hand = [make_card(1, 1, 1), make_card(2, 1, 2)]
    host_player.bet = 10
    host_player.chips = 90

    game._action_split(host_player, "split")

    assert host_player.has_blackjack is True
    assert host_player.split_has_blackjack is True


def test_blackjack_settle_split_hands_independently() -> None:
    game, host_player, _host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)
    game.status = "playing"
    game.game_active = True
    game.phase = "players"
    game.dealer_hand = [make_card(100, 10, 1), make_card(101, 8, 2)]  # 18

    host_player.hand = [make_card(1, 10, 3), make_card(2, 10, 4)]  # 20, win
    host_player.bet = 10
    host_player.hand_done = True
    host_player.split_hand = [make_card(3, 10, 1), make_card(4, 9, 2), make_card(5, 5, 3)]  # bust
    host_player.split_bet = 10
    host_player.split_busted = True
    host_player.split_hand_done = True
    host_player.chips = 80

    guest_player.hand = [make_card(6, 7, 1), make_card(7, 7, 2)]
    guest_player.bet = 10
    guest_player.hand_done = True
    guest_player.chips = 90

    game._settle_hand()

    assert host_player.chips == 100


def test_blackjack_rules_profile_applies_preset() -> None:
    game = BlackjackGame()
    game._handle_option_change("rules_profile", "european")

    assert game.options.rules_profile == "european"
    assert game.options.dealer_hits_soft_17 is False
    assert game.options.dealer_peeks_blackjack is False
    assert game.options.allow_insurance is True
    assert game.options.allow_late_surrender is False
    assert game.options.blackjack_payout == "3_to_2"
    assert game.options.double_down_rule == "9_to_11"
    assert game.options.allow_double_after_split is False
    assert game.options.split_rule == "same_rank"
    assert game.options.max_split_hands == 2
    assert game.options.split_aces_one_card_only is True
    assert game.options.split_aces_count_as_blackjack is False


def test_blackjack_split_rule_controls_ten_value_splits() -> None:
    game, host_player, _host_user = create_game_with_host()
    host_player.hand = [make_card(1, 10, 1), make_card(2, 13, 2)]
    host_player.bet = 10
    host_player.chips = 100

    game.options.split_rule = "same_value"
    assert game._can_split(host_player) is True

    game.options.split_rule = "same_rank"
    assert game._can_split(host_player) is False


def test_blackjack_double_down_rules_and_das() -> None:
    game, host_player, _host_user = create_game_with_host()
    host_player.bet = 10
    host_player.chips = 100

    game.options.double_down_rule = "9_to_11"
    host_player.hand = [make_card(1, 4, 1), make_card(2, 4, 2)]  # total 8
    assert game._can_double_down(host_player) is False

    host_player.hand = [make_card(3, 5, 1), make_card(4, 5, 2)]  # total 10
    assert game._can_double_down(host_player) is True

    host_player.split_hand = [make_card(5, 5, 3), make_card(6, 5, 4)]
    host_player.split_bet = 10
    host_player.active_hand_index = 1
    game.options.allow_double_after_split = False
    assert game._can_double_down(host_player) is False

    game.options.allow_double_after_split = True
    assert game._can_double_down(host_player) is True


def test_blackjack_blackjack_payout_modes() -> None:
    game = BlackjackGame()

    game.options.blackjack_payout = "3_to_2"
    assert game._blackjack_total_payout(10) == 25

    game.options.blackjack_payout = "6_to_5"
    assert game._blackjack_total_payout(10) == 22

    game.options.blackjack_payout = "1_to_1"
    assert game._blackjack_total_payout(10) == 20


def test_blackjack_dealer_no_peek_does_not_auto_settle() -> None:
    game, host_player, _host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    game.add_player("Guest", guest_user)
    game.options.dealer_peeks_blackjack = False
    game.options.allow_insurance = False

    events = {"settled": 0, "started_turn": 0}

    def fake_post_bets(players: list) -> None:
        for player in players:
            player.bet = 10

    def fake_deal_initial_cards(players: list) -> None:
        for player in players:
            player.hand = [make_card(1, 10, 1), make_card(2, 9, 2)]
            player.hand_done = False
        game.dealer_hand = [make_card(3, 1, 1), make_card(4, 13, 2)]

    game._ensure_deck = lambda min_cards=1: None  # type: ignore[method-assign]
    game._post_bets = fake_post_bets  # type: ignore[method-assign]
    game._deal_initial_cards = fake_deal_initial_cards  # type: ignore[method-assign]
    game._settle_hand = lambda: events.__setitem__("settled", events["settled"] + 1)  # type: ignore[method-assign]
    game._start_turn = lambda: events.__setitem__("started_turn", events["started_turn"] + 1)  # type: ignore[method-assign]

    game.on_start()

    assert events["settled"] == 0
    assert events["started_turn"] == 1
    assert game.phase == "players"
    assert game.current_player == host_player


def test_blackjack_read_rules_action_speaks_summary() -> None:
    game, host_player, host_user = create_game_with_host()
    game._action_read_rules(host_player, "read_rules")
    spoken = host_user.get_last_spoken() or ""
    assert "Rules:" in spoken
    assert "Table limits" in spoken


def test_blackjack_pitch_style_hides_initial_cards_from_other_players() -> None:
    game, host_player, host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)
    game.options.players_cards_face_up = False
    game.deck = Deck(
        cards=[
            make_card(1, 10, 1),  # host
            make_card(2, 9, 2),  # guest
            make_card(3, 6, 3),  # dealer up
            make_card(4, 7, 4),  # host
            make_card(5, 8, 1),  # guest
            make_card(6, 12, 2),  # dealer hole
        ]
    )

    game._deal_initial_cards([host_player, guest_player])

    host_spoken = " ".join(host_user.get_spoken_messages())
    guest_spoken = " ".join(guest_user.get_spoken_messages())
    assert "You have" in host_spoken
    assert "You have" in guest_spoken
    assert "Host has" not in guest_spoken
    assert "Guest has" not in host_spoken


def test_blackjack_pitch_style_hides_other_totals_in_table_status() -> None:
    game, host_player, host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)
    game.status = "playing"
    game.game_active = True
    game.phase = "players"
    game.options.players_cards_face_up = False

    host_player.chips = 100
    host_player.bet = 10
    host_player.hand = [make_card(11, 10, 1), make_card(12, 6, 2)]

    guest_player.chips = 100
    guest_player.bet = 10
    guest_player.hand = [make_card(13, 2, 1), make_card(14, 5, 2)]

    game._action_table_status(host_player, "table_status")

    spoken = host_user.get_last_spoken() or ""
    assert "Host: 100 chips, bet 10, total" in spoken
    assert "Guest: 100 chips, bet 10, total" not in spoken
    assert "Guest: 100 chips, bet 10" in spoken


def test_blackjack_insurance_prompt_announced_to_player() -> None:
    game, host_player, host_user = create_game_with_host()
    game.status = "playing"
    game.game_active = True
    game.phase = "insurance"
    game.dealer_hand = [make_card(1, 1, 1), make_card(2, 9, 2)]
    host_player.bet = 10
    host_player.chips = 100
    host_player.hand = [make_card(3, 10, 1), make_card(4, 7, 2)]
    host_player.insurance_decision_done = False
    game.set_turn_players([host_player], reset_index=True)

    game._start_insurance_turn()

    spoken = " ".join(host_user.get_spoken_messages())
    assert "insurance" in spoken.lower()


def test_blackjack_dealer_hits_soft_17_when_enabled() -> None:
    game = BlackjackGame()
    game.options.dealer_hits_soft_17 = True
    game.status = "playing"
    game.dealer_hand = [make_card(1, 1, 1), make_card(2, 6, 2)]
    game.deck = Deck(cards=[make_card(3, 2, 3)])
    game._settle_hand = lambda: None  # type: ignore[method-assign]

    game._play_dealer_turn()

    assert len(game.dealer_hand) == 3


def test_blackjack_dealer_stands_soft_17_when_disabled() -> None:
    game = BlackjackGame()
    game.options.dealer_hits_soft_17 = False
    game.status = "playing"
    game.dealer_hand = [make_card(1, 1, 1), make_card(2, 6, 2)]
    game.deck = Deck(cards=[make_card(3, 2, 3)])
    game._settle_hand = lambda: None  # type: ignore[method-assign]

    game._play_dealer_turn()

    assert len(game.dealer_hand) == 2


def test_blackjack_bot_game_completes() -> None:
    random.seed(12345)
    game = BlackjackGame(
        options=BlackjackOptions(
            starting_chips=40,
            base_bet=10,
            deck_count=1,
            turn_timer="0",
        )
    )
    for index in range(3):
        bot = Bot(f"Bot{index}")
        game.add_player(f"Bot{index}", bot)

    game.on_start()

    for _ in range(120000):
        if game.status == "finished":
            break
        game.on_tick()

    assert game.status == "finished"


def test_blackjack_bot_game_completes_with_save_reload_cycles() -> None:
    random.seed(67890)
    game = BlackjackGame(
        options=BlackjackOptions(
            starting_chips=60,
            base_bet=10,
            table_min_bet=5,
            table_max_bet=20,
            deck_count=1,
            turn_timer="0",
        )
    )
    bots = [Bot(f"Bot{index}") for index in range(3)]
    for bot in bots:
        game.add_player(bot.username, bot)

    game.on_start()

    for tick in range(140000):
        if game.status == "finished":
            break

        if tick > 0 and tick % 75 == 0:
            saved_users = dict(game._users)
            saved_keybinds = dict(game._keybinds)
            payload = game.to_json()
            game = BlackjackGame.from_json(payload)
            game._users = saved_users
            game._keybinds = saved_keybinds
            game.rebuild_runtime_state()
            for player in game.players:
                if game.get_user(player):
                    game.setup_player_actions(player)

        game.on_tick()

    assert game.status == "finished"


def test_blackjack_persistence_round_trip_preserves_new_state_and_reconnect() -> None:
    game, host_player, host_user = create_game_with_host()
    guest_user = MockUser("Guest")
    guest_player = game.add_player("Guest", guest_user)
    game.status = "playing"
    game.game_active = True
    game.phase = "insurance"
    game.options = BlackjackOptions(
        rules_profile="friendly",
        starting_chips=900,
        base_bet=25,
        table_min_bet=10,
        table_max_bet=200,
        deck_count=2,
        dealer_hits_soft_17=False,
        dealer_peeks_blackjack=False,
        allow_insurance=True,
        allow_late_surrender=True,
        players_cards_face_up=False,
        blackjack_payout="6_to_5",
        double_down_rule="10_to_11",
        allow_double_after_split=False,
        split_rule="same_value",
        max_split_hands=2,
        split_aces_one_card_only=True,
        split_aces_count_as_blackjack=True,
        turn_timer="30",
    )
    game.dealer_hand = [make_card(20, 1, 1), make_card(21, 13, 2)]
    game.set_turn_players([host_player, guest_player], reset_index=True)

    host_player.hand = [make_card(1, 1, 1), make_card(2, 13, 2)]
    host_player.has_blackjack = True
    host_player.bet = 25
    host_player.chips = 875
    host_player.insurance_bet = 12
    host_player.insurance_decision_done = True
    host_player.took_even_money = True
    host_player.split_hand = [make_card(3, 1, 3), make_card(4, 10, 4)]
    host_player.split_bet = 25
    host_player.split_has_blackjack = True
    host_player.main_from_split_aces = True
    host_player.split_from_split_aces = True
    host_player.surrendered_main = False
    host_player.surrendered_split = False

    payload = game.to_json()
    loaded = BlackjackGame.from_json(payload)
    loaded.rebuild_runtime_state()

    loaded_host = next(p for p in loaded.players if p.name == "Host")
    loaded_guest = next(p for p in loaded.players if p.name == "Guest")
    loaded.attach_user(loaded_host.id, host_user)
    loaded.attach_user(loaded_guest.id, guest_user)
    loaded.setup_player_actions(loaded_host)
    loaded.setup_player_actions(loaded_guest)

    assert loaded.options.table_min_bet == 10
    assert loaded.options.table_max_bet == 200
    assert loaded.options.allow_late_surrender is True
    assert loaded.options.players_cards_face_up is False
    assert loaded.options.blackjack_payout == "6_to_5"
    assert loaded.options.split_aces_count_as_blackjack is True
    assert loaded.options.double_down_rule == "10_to_11"

    assert loaded_host.insurance_bet == 12
    assert loaded_host.took_even_money is True
    assert loaded_host.main_from_split_aces is True
    assert loaded_host.split_from_split_aces is True
    assert loaded_host.split_has_blackjack is True
    assert loaded.current_player == loaded_host

    loaded._action_read_rules(loaded_host, "read_rules")
    spoken = host_user.get_last_spoken() or ""
    assert "Rules:" in spoken
