import platform

from zelda.launcher import startup_message


def test_launcher_identifies_macos(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    assert startup_message() == "Z.E.L.D.A. starting on macOS"


def test_launcher_identifies_linux(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    assert startup_message() == "Z.E.L.D.A. starting on Linux"
