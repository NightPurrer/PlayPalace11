import asyncio
from pathlib import Path

import pytest

import server.core.server as core_server


class _DummyDB:
    def __init__(self, path: str) -> None:
        self.path = path

    def connect(self) -> None:
        return None

    def get_user_count(self) -> int:
        return 1

    def get_server_owner(self) -> str:
        return "owner"

    def close(self) -> None:
        return None


@pytest.mark.asyncio
async def test_run_server_uses_bind_ip_from_config(tmp_path, monkeypatch):
    config_path = tmp_path / "config.toml"
    config_path.write_text('[server]\nbind_ip = "0.0.0.0"\n', encoding="utf-8")

    (tmp_path / "config.example.toml").write_text("", encoding="utf-8")
    (tmp_path / "playpalace.db").write_text("", encoding="utf-8")

    captured = {}

    class DummyServer:
        def __init__(self, *args, **kwargs):
            captured["host"] = kwargs.get("host")

        async def start(self) -> None:
            return None

        async def stop(self) -> None:
            return None

    async def fake_sleep(_):
        raise KeyboardInterrupt

    monkeypatch.setattr(core_server, "_MODULE_DIR", Path(tmp_path))
    monkeypatch.setattr(core_server, "Database", _DummyDB)
    monkeypatch.setattr(core_server, "Server", DummyServer)
    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    await core_server.run_server(host=None)

    assert captured["host"] == "0.0.0.0"


@pytest.mark.asyncio
async def test_run_server_defaults_bind_ip_to_localhost(tmp_path, monkeypatch):
    config_path = tmp_path / "config.toml"
    config_path.write_text("[server]\n", encoding="utf-8")

    (tmp_path / "config.example.toml").write_text("", encoding="utf-8")
    (tmp_path / "playpalace.db").write_text("", encoding="utf-8")

    captured = {}

    class DummyServer:
        def __init__(self, *args, **kwargs):
            captured["host"] = kwargs.get("host")

        async def start(self) -> None:
            return None

        async def stop(self) -> None:
            return None

    async def fake_sleep(_):
        raise KeyboardInterrupt

    monkeypatch.setattr(core_server, "_MODULE_DIR", Path(tmp_path))
    monkeypatch.setattr(core_server, "Database", _DummyDB)
    monkeypatch.setattr(core_server, "Server", DummyServer)
    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    await core_server.run_server(host=None)

    assert captured["host"] == "127.0.0.1"


@pytest.mark.asyncio
async def test_run_server_host_param_overrides_config(tmp_path, monkeypatch):
    config_path = tmp_path / "config.toml"
    config_path.write_text('[server]\nbind_ip = "127.0.0.1"\n', encoding="utf-8")

    (tmp_path / "config.example.toml").write_text("", encoding="utf-8")
    (tmp_path / "playpalace.db").write_text("", encoding="utf-8")

    captured = {}

    class DummyServer:
        def __init__(self, *args, **kwargs):
            captured["host"] = kwargs.get("host")

        async def start(self) -> None:
            return None

        async def stop(self) -> None:
            return None

    async def fake_sleep(_):
        raise KeyboardInterrupt

    monkeypatch.setattr(core_server, "_MODULE_DIR", Path(tmp_path))
    monkeypatch.setattr(core_server, "Database", _DummyDB)
    monkeypatch.setattr(core_server, "Server", DummyServer)
    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    await core_server.run_server(host="0.0.0.0")

    assert captured["host"] == "0.0.0.0"
