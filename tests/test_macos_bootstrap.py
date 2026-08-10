import sys
from pathlib import Path

from zelda import macos_bootstrap


def test_prepare_directories_creates_runtime_tree(tmp_path, monkeypatch):
    home = tmp_path / "home"
    monkeypatch.setattr(macos_bootstrap, "ZELDA_HOME", home / ".zelda")
    monkeypatch.setattr(macos_bootstrap, "WORKSPACE", home / ".zelda" / "workspace")
    monkeypatch.setattr(macos_bootstrap, "LOGS", home / ".zelda" / "logs")

    macos_bootstrap.prepare_directories()

    assert macos_bootstrap.ZELDA_HOME.is_dir()
    assert macos_bootstrap.WORKSPACE.is_dir()
    assert macos_bootstrap.LOGS.is_dir()


def test_bootstrap_rejects_non_macos(monkeypatch):
    monkeypatch.setattr(macos_bootstrap.sys, "platform", "linux")

    try:
        macos_bootstrap.bootstrap()
    except RuntimeError as exc:
        assert "requires macOS" in str(exc)
    else:
        raise AssertionError("bootstrap should reject non macOS platforms")
