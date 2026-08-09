import platform

from zelda.platform import current_platform, is_macos


def test_detects_macos(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    assert current_platform() == "macos"
    assert is_macos() is True


def test_detects_linux(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    assert current_platform() == "linux"
    assert is_macos() is False
