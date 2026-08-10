import pytest

from zelda import macos_install


def test_install_rejects_non_macos(monkeypatch):
    monkeypatch.setattr(macos_install.platform, "system", lambda: "Linux")
    with pytest.raises(RuntimeError, match="requires macOS"):
        macos_install.install()


def test_verify_service_returns_false_when_unavailable(monkeypatch):
    def unavailable(*args, **kwargs):
        raise OSError("offline")

    monkeypatch.setattr(macos_install.urllib.request, "urlopen", unavailable)
    monkeypatch.setattr(macos_install.time, "sleep", lambda _: None)
    assert macos_install.verify_service(timeout=0.01, interval=0) is False
