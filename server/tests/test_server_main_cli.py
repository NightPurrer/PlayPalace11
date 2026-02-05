import importlib
import os
import sys

import pytest


@pytest.fixture
def main_module():
    """Import server.main and restore cwd after the test."""
    original_cwd = os.getcwd()
    main_mod = importlib.import_module("server.main")
    try:
        yield main_mod
    finally:
        os.chdir(original_cwd)


def _set_argv(monkeypatch, args: list[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["main.py", *args])


def test_main_passes_preload_flag(monkeypatch, main_module):
    captured = {}

    async def fake_run_server(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(main_module, "run_server", fake_run_server)
    _set_argv(monkeypatch, ["--preload-locales"])
    main_module.main()

    assert captured["preload_locales"] is True


def test_main_default_preload_false(monkeypatch, main_module):
    captured = {}

    async def fake_run_server(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(main_module, "run_server", fake_run_server)
    _set_argv(monkeypatch, [])
    main_module.main()

    assert captured["preload_locales"] is False
