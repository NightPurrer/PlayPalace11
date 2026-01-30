"""Tests for the VirtualBotManager core behaviors."""

from types import SimpleNamespace

import pytest

import server.core.virtual_bots as vb_module
import server.games.registry as registry_module

from server.core.virtual_bots import (
    VirtualBot,
    VirtualBotManager,
    VirtualBotState,
)


class FakeTables:
    def __init__(self):
        self.tables = {}
        self.waiting_tables = []

    def get_table(self, table_id):
        return self.tables.get(table_id)

    def remove_table(self, table_id):
        self.tables.pop(table_id, None)

    def get_waiting_tables(self):
        return list(self.waiting_tables)

    def create_table(self, *args, **kwargs):
        raise AssertionError("Not expected in this test")


class FakeServer:
    def __init__(self, db=None):
        self._db = db
        self._users = {}
        self._user_states = {}
        self._tables = FakeTables()
        self.broadcasts = []
        self.table_broadcasts = []

    def _broadcast_presence_l(self, message_id, username, sound):
        self.broadcasts.append((message_id, username, sound))

    def _broadcast_table_created(self, host_name, game_name):
        self.table_broadcasts.append((host_name, game_name))


class DummyNetworkUser:
    def __init__(self):
        self.approved = True


class DummyTableForJoin:
    def __init__(self, table_id, game):
        self.table_id = table_id
        self.game = game
        self.members = []

    def add_member(self, name, user, as_spectator=False):
        self.members.append((name, as_spectator))


class DummyGameForJoin:
    def __init__(self, host):
        self.status = "waiting"
        self.players = []
        self.host = host
        self.broadcasts = []
        self.table = None

    def get_min_players(self):
        return 2

    def get_max_players(self):
        return 4

    def add_player(self, name, user):
        self.players.append(SimpleNamespace(name=name))

    def broadcast_l(self, message_id, **kwargs):
        self.broadcasts.append((message_id, kwargs))

    def broadcast_sound(self, sound):
        self.broadcasts.append(("sound", sound))

    def rebuild_all_menus(self):
        pass

    def initialize_lobby(self, host_name, user):
        self.players.append(SimpleNamespace(name=host_name))


def test_virtual_bots_load_config_and_fill_server(tmp_path, monkeypatch):
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        """
        [virtual_bots]
        names = ["BotA", "BotB", "BotC", "BotD"]
        min_idle_ticks = 10
        max_idle_ticks = 20
        min_online_ticks = 30
        max_online_ticks = 40
        min_offline_ticks = 50
        max_offline_ticks = 60
        """
    )

    server = FakeServer()
    manager = VirtualBotManager(server)
    manager.load_config(config_path)
    assert manager._config.names == ["BotA", "BotB", "BotC", "BotD"]
    assert manager._config.min_idle_ticks == 10
    assert manager._config.max_offline_ticks == 60

    monkeypatch.setattr("server.core.virtual_bots.random.shuffle", lambda seq: seq)
    monkeypatch.setattr("server.core.virtual_bots.random.randint", lambda a, b: a)

    added, online = manager.fill_server()
    assert added == 4
    assert online == 2  # half rounded down
    assert set(server._users.keys()) == {"BotA", "BotB"}
    assert all(state["menu"] == "main_menu" for state in server._user_states.values())
    assert server.broadcasts == [
        ("user-online", "BotA", "online.ogg"),
        ("user-online", "BotB", "online.ogg"),
    ]


def test_virtual_bots_save_and_load_state(monkeypatch):
    saved = []

    class FakeDB:
        def delete_all_virtual_bots(self):
            saved.clear()

        def save_virtual_bot(self, **payload):
            saved.append(payload)

        def load_all_virtual_bots(self):
            return [
                {
                    "name": "Alpha",
                    "state": "online_idle",
                    "online_ticks": 12,
                    "target_online_ticks": 25,
                    "table_id": None,
                    "game_join_tick": 3,
                },
                {
                    "name": "Ignored",
                    "state": "offline",
                    "online_ticks": 0,
                    "target_online_ticks": 0,
                    "table_id": None,
                    "game_join_tick": 0,
                },
            ]

    server = FakeServer(db=FakeDB())
    manager = VirtualBotManager(server)
    manager._config.names = ["Alpha"]
    manager._bots["Alpha"] = VirtualBot(
        name="Alpha",
        state=VirtualBotState.ONLINE_IDLE,
        online_ticks=5,
        target_online_ticks=10,
    )

    manager.save_state()
    assert saved[0]["name"] == "Alpha"
    assert saved[0]["state"] == VirtualBotState.ONLINE_IDLE.value

    manager._bots.clear()
    loaded = manager.load_state()
    assert loaded == 1
    assert "Alpha" in manager._bots
    assert "Alpha" in server._users
    assert server._user_states["Alpha"]["menu"] == "main_menu"
    assert "Ignored" not in manager._bots


def test_restore_bot_user_conflict_sets_offline(monkeypatch):
    server = FakeServer()
    server._users["Taken"] = DummyNetworkUser()  # Represents real user, not virtual
    manager = VirtualBotManager(server)
    bot = VirtualBot("Taken", state=VirtualBotState.ONLINE_IDLE)

    monkeypatch.setattr("server.core.virtual_bots.random.randint", lambda a, b: a)

    manager._restore_bot_user(bot)

    assert bot.state == VirtualBotState.OFFLINE
    assert bot.cooldown_ticks == 200  # from patched randint
    assert server._users["Taken"] is not None  # original user untouched


def test_leave_current_table_executes_leave_and_removes_member():
    class DummyGame:
        def __init__(self, name):
            self.player = SimpleNamespace(name=name)
            self.leaves = []

        def get_player_by_name(self, name):
            if name == self.player.name:
                return self.player

        def execute_action(self, player, action_id):
            self.leaves.append((player.name, action_id))

    class DummyTable:
        def __init__(self, table_id, bot_name):
            self.table_id = table_id
            self.game = DummyGame(bot_name)
            self.members_removed = []

        def remove_member(self, name):
            self.members_removed.append(name)

    server = FakeServer()
    manager = VirtualBotManager(server)
    bot = VirtualBot("Zed", state=VirtualBotState.IN_GAME, table_id="T1")
    table = DummyTable("T1", "Zed")
    server._tables.tables["T1"] = table
    server._users["Zed"] = DummyNetworkUser()

    manager._leave_current_table(bot)

    assert bot.table_id is None
    assert table.members_removed == ["Zed"]
    assert table.game.leaves == [("Zed", "leave")]


def test_take_bot_offline_removes_user_and_broadcasts(monkeypatch):
    server = FakeServer()
    manager = VirtualBotManager(server)
    bot = VirtualBot("Yin", state=VirtualBotState.ONLINE_IDLE)
    server._users["Yin"] = DummyNetworkUser()
    server._user_states["Yin"] = {"menu": "main"}

    monkeypatch.setattr("server.core.virtual_bots.random.randint", lambda a, b: a)

    manager._take_bot_offline(bot)

    assert bot.state == VirtualBotState.OFFLINE
    assert "Yin" not in server._users
    assert "Yin" not in server._user_states
    assert server.broadcasts[-1] == ("user-offline", "Yin", "offline.ogg")
    assert bot.cooldown_ticks == manager._config.min_offline_ticks


def test_process_online_idle_bot_goes_offline_when_threshold_met(monkeypatch):
    server = FakeServer()
    manager = VirtualBotManager(server)
    bot = VirtualBot("Ada", state=VirtualBotState.ONLINE_IDLE)
    manager._bots["Ada"] = bot
    server._users["Ada"] = DummyNetworkUser()
    bot.online_ticks = manager._config.min_online_ticks
    bot.target_online_ticks = 0
    bot.think_ticks = 0

    monkeypatch.setattr("server.core.virtual_bots.random.random", lambda: 0.0)
    monkeypatch.setattr("server.core.virtual_bots.random.randint", lambda a, b: a)

    manager._process_online_idle_bot(bot)

    assert bot.state == VirtualBotState.OFFLINE
    assert server.broadcasts[-1][0] == "user-offline"


def test_start_leaving_game_sets_state_and_logout_flag(monkeypatch):
    server = FakeServer()
    manager = VirtualBotManager(server)
    bot = VirtualBot("Hex", state=VirtualBotState.IN_GAME)

    monkeypatch.setattr("server.core.virtual_bots.random.randint", lambda a, b: a)
    monkeypatch.setattr("server.core.virtual_bots.random.random", lambda: 0.9)

    manager._start_leaving_game(bot)

    assert bot.state == VirtualBotState.LEAVING_GAME
    assert bot.cooldown_ticks == 0
    # Since random.random returned 0.9 and logout chance default 0.33, flag False
    assert bot.logout_after_game is False


def test_try_join_game_adds_bot_to_waiting_table(monkeypatch):
    server = FakeServer()
    manager = VirtualBotManager(server)
    bot = VirtualBot("Joiner", state=VirtualBotState.ONLINE_IDLE)
    manager._bots["Joiner"] = bot
    user = DummyNetworkUser()
    server._users["Joiner"] = user

    game = DummyGameForJoin(host="other")
    table = DummyTableForJoin("table-1", game)
    server._tables.waiting_tables = [table]

    monkeypatch.setattr("server.core.virtual_bots.random.choice", lambda seq: seq[0])

    joined = manager._try_join_game(bot)

    assert joined
    assert bot.state == VirtualBotState.IN_GAME
    assert bot.table_id == "table-1"
    assert server._user_states["Joiner"]["menu"] == "in_game"
    assert table.members == [("Joiner", False)]
    assert game.broadcasts[0][0] == "table-joined"


def test_try_create_game_builds_table(monkeypatch):
    server = FakeServer()
    manager = VirtualBotManager(server)
    bot = VirtualBot("Creator", state=VirtualBotState.ONLINE_IDLE)
    manager._bots["Creator"] = bot
    server._users["Creator"] = DummyNetworkUser()

    class DummyGameClass:
        @classmethod
        def get_type(cls):
            return "dummy"

        @classmethod
        def get_name(cls):
            return "Dummy Game"

        def __init__(self):
            self.players = []

        def initialize_lobby(self, host_name, user):
            self.players.append(SimpleNamespace(name=host_name))

        def get_min_players(self):
            return 2

        def get_max_players(self):
            return 4

    dummy_table = SimpleNamespace(
        table_id="new-table",
        game=None,
    )

    def fake_create_table(game_type, host_name, user):
        assert game_type == "dummy"
        return dummy_table

    monkeypatch.setattr(
        registry_module.GameRegistry,
        "get_all",
        classmethod(lambda cls: [DummyGameClass]),
    )
    monkeypatch.setattr("server.core.virtual_bots.random.choice", lambda seq: seq[0])
    monkeypatch.setattr(server._tables, "create_table", fake_create_table)

    created = manager._try_create_game(bot)

    assert created
    assert bot.state == VirtualBotState.IN_GAME
    assert bot.table_id == "new-table"
    assert dummy_table.game is not None
    assert server._user_states["Creator"]["menu"] == "in_game"
    assert server.table_broadcasts[-1] == ("Creator", "Dummy Game")


def test_clear_bots_removes_tables_and_calls_db(monkeypatch):
    tables_removed = []

    class TableWithGame:
        def __init__(self):
            self.game = SimpleNamespace(broadcast_l=lambda *args, **kwargs: None)

        def remove_member(self, name):
            tables_removed.append(name)

    class DBTracker:
        def __init__(self):
            self.cleared = 0

        def delete_all_virtual_bots(self):
            self.cleared += 1

    server = FakeServer(db=DBTracker())
    manager = VirtualBotManager(server)
    bot = VirtualBot("Cleaner", state=VirtualBotState.IN_GAME, table_id="table-clean")
    manager._bots["Cleaner"] = bot
    server._users["Cleaner"] = DummyNetworkUser()
    server._tables.tables["table-clean"] = SimpleNamespace(
        game=SimpleNamespace(broadcast_l=lambda *args, **kwargs: None),
    )

    bots_cleared, tables_killed = manager.clear_bots()

    assert bots_cleared == 1
    assert tables_killed == 1
    assert "Cleaner" not in manager._bots
    assert server._db.cleared == 1


def test_load_config_with_max_tables_per_game(tmp_path):
    """Test that max_tables_per_game config is loaded correctly."""
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        """
        [virtual_bots]
        names = ["BotA"]
        max_tables_per_game = 2
        """
    )

    server = FakeServer()
    manager = VirtualBotManager(server)
    manager.load_config(config_path)

    assert manager._config.max_tables_per_game == 2


def test_count_bot_owned_tables():
    """Test counting tables owned by virtual bots."""

    class FakeTablesWithAll(FakeTables):
        def __init__(self, tables_list):
            super().__init__()
            self._all_tables = tables_list

        def get_all_tables(self):
            return self._all_tables

    # Create mock tables with games
    table1 = SimpleNamespace(
        game=SimpleNamespace(get_type=lambda: "scopa", host="BotA")
    )
    table2 = SimpleNamespace(
        game=SimpleNamespace(get_type=lambda: "scopa", host="BotB")
    )
    table3 = SimpleNamespace(
        game=SimpleNamespace(get_type=lambda: "ninetynine", host="BotA")
    )
    table4 = SimpleNamespace(
        game=SimpleNamespace(get_type=lambda: "scopa", host="HumanPlayer")
    )

    server = FakeServer()
    server._tables = FakeTablesWithAll([table1, table2, table3, table4])

    manager = VirtualBotManager(server)
    manager._bots["BotA"] = VirtualBot("BotA")
    manager._bots["BotB"] = VirtualBot("BotB")
    # HumanPlayer is not a bot

    assert manager._count_bot_owned_tables("scopa") == 2  # BotA and BotB
    assert manager._count_bot_owned_tables("ninetynine") == 1  # Only BotA
    assert manager._count_bot_owned_tables("othergame") == 0


def test_can_create_game_type_with_limits():
    """Test that _can_create_game_type respects limits."""

    class FakeTablesWithAll(FakeTables):
        def __init__(self, tables_list):
            super().__init__()
            self._all_tables = tables_list

        def get_all_tables(self):
            return self._all_tables

    # Create 2 scopa tables owned by bots
    table1 = SimpleNamespace(
        game=SimpleNamespace(get_type=lambda: "scopa", host="BotA")
    )
    table2 = SimpleNamespace(
        game=SimpleNamespace(get_type=lambda: "scopa", host="BotB")
    )

    server = FakeServer()
    server._tables = FakeTablesWithAll([table1, table2])

    manager = VirtualBotManager(server)
    manager._bots["BotA"] = VirtualBot("BotA")
    manager._bots["BotB"] = VirtualBot("BotB")

    # Set limit of 2 per game type
    manager._config.max_tables_per_game = 2

    # Should not be able to create more scopa tables (at limit)
    assert manager._can_create_game_type("scopa") is False

    # Should be able to create ninetynine (0 tables exist)
    assert manager._can_create_game_type("ninetynine") is True

    # Increase limit to 3
    manager._config.max_tables_per_game = 3
    assert manager._can_create_game_type("scopa") is True

    # 0 means unlimited
    manager._config.max_tables_per_game = 0
    assert manager._can_create_game_type("scopa") is True


def test_try_create_game_respects_limits_and_falls_back_to_join(monkeypatch):
    """Test that _try_create_game picks alternative game or joins when limited."""

    class FakeTablesWithAll(FakeTables):
        def __init__(self):
            super().__init__()
            self._all_tables = []

        def get_all_tables(self):
            return self._all_tables

        def create_table(self, game_type, host_name, user):
            return SimpleNamespace(table_id="new-table", game=None)

    # Create 2 scopa tables owned by bots (at limit)
    table1 = SimpleNamespace(
        game=SimpleNamespace(get_type=lambda: "scopa", host="BotA")
    )
    table2 = SimpleNamespace(
        game=SimpleNamespace(get_type=lambda: "scopa", host="BotB")
    )

    server = FakeServer()
    server._tables = FakeTablesWithAll()
    server._tables._all_tables = [table1, table2]

    manager = VirtualBotManager(server)
    manager._bots["BotA"] = VirtualBot("BotA")
    manager._bots["BotB"] = VirtualBot("BotB")
    manager._config.max_tables_per_game = 2  # Limit of 2 per game type

    # Create a bot that wants to create a game
    bot = VirtualBot("Creator", state=VirtualBotState.ONLINE_IDLE)
    manager._bots["Creator"] = bot
    server._users["Creator"] = DummyNetworkUser()

    # Mock registry to only return scopa (which is at limit)
    class ScopaGameClass:
        @classmethod
        def get_type(cls):
            return "scopa"

        @classmethod
        def get_name(cls):
            return "Scopa"

    monkeypatch.setattr(
        registry_module.GameRegistry,
        "get_all",
        classmethod(lambda cls: [ScopaGameClass]),
    )

    # No waiting tables to join either
    server._tables.waiting_tables = []

    # Should fail since scopa is at limit and no other games available
    created = manager._try_create_game(bot)
    assert created is False
    assert bot.state == VirtualBotState.ONLINE_IDLE  # State unchanged

    # Now add a waiting table - should fall back to joining
    game = DummyGameForJoin(host="other")
    table = DummyTableForJoin("table-1", game)
    server._tables.waiting_tables = [table]

    monkeypatch.setattr("server.core.virtual_bots.random.choice", lambda seq: seq[0])

    created = manager._try_create_game(bot)
    assert created is True
    assert bot.state == VirtualBotState.IN_GAME
    assert bot.table_id == "table-1"  # Joined existing table


def test_try_create_game_picks_available_game_type(monkeypatch):
    """Test that _try_create_game picks a game type that isn't at its limit."""

    class FakeTablesWithAll(FakeTables):
        def __init__(self):
            super().__init__()
            self._all_tables = []
            self.created_game_types = []

        def get_all_tables(self):
            return self._all_tables

        def create_table(self, game_type, host_name, user):
            self.created_game_types.append(game_type)
            return SimpleNamespace(table_id="new-table", game=None)

    # Create 2 scopa tables (at limit)
    table1 = SimpleNamespace(
        game=SimpleNamespace(get_type=lambda: "scopa", host="BotA")
    )
    table2 = SimpleNamespace(
        game=SimpleNamespace(get_type=lambda: "scopa", host="BotB")
    )

    server = FakeServer()
    server._tables = FakeTablesWithAll()
    server._tables._all_tables = [table1, table2]

    manager = VirtualBotManager(server)
    manager._bots["BotA"] = VirtualBot("BotA")
    manager._bots["BotB"] = VirtualBot("BotB")
    manager._config.max_tables_per_game = 2  # Limit of 2 per game type

    bot = VirtualBot("Creator", state=VirtualBotState.ONLINE_IDLE)
    manager._bots["Creator"] = bot
    server._users["Creator"] = DummyNetworkUser()

    # Mock registry with scopa (at limit) and ninetynine (available)
    class ScopaGameClass:
        @classmethod
        def get_type(cls):
            return "scopa"

        @classmethod
        def get_name(cls):
            return "Scopa"

    class NinetyNineGameClass:
        @classmethod
        def get_type(cls):
            return "ninetynine"

        @classmethod
        def get_name(cls):
            return "Ninety Nine"

        def __init__(self):
            self.players = []

        def initialize_lobby(self, host_name, user):
            self.players.append(SimpleNamespace(name=host_name))

    monkeypatch.setattr(
        registry_module.GameRegistry,
        "get_all",
        classmethod(lambda cls: [ScopaGameClass, NinetyNineGameClass]),
    )
    # Force random.choice to pick the first available (ninetynine since scopa is filtered)
    monkeypatch.setattr("server.core.virtual_bots.random.choice", lambda seq: seq[0])

    created = manager._try_create_game(bot)

    assert created is True
    assert server._tables.created_game_types == ["ninetynine"]
    assert bot.state == VirtualBotState.IN_GAME
