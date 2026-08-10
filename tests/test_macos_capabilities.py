import platform

from zelda.control.bootstrap import register_macos_display_capabilities
from zelda.control.capabilities import CapabilityRegistry


def test_macos_capabilities_register_on_registry(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    registry = CapabilityRegistry()
    register_macos_display_capabilities(registry)

    assert registry.get("display.list") is not None
    assert registry.get("window.move") is not None
