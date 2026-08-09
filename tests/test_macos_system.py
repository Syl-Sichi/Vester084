import platform

from zelda.macos.system import MacOSSystemCapabilities


def test_system_info_is_read_only(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(platform, "release", lambda: "24.0.0")
    monkeypatch.setattr(platform, "version", lambda: "test-version")
    monkeypatch.setattr(platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(platform, "python_version", lambda: "3.12.0")

    assert MacOSSystemCapabilities.system_info([]) == {
        "platform": "Darwin",
        "release": "24.0.0",
        "version": "test-version",
        "machine": "x86_64",
        "python": "3.12.0",
    }
