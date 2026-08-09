import pytest

from zelda.control.capabilities import Capability, CapabilityRegistry


def test_registry_requires_namespaced_capabilities():
    registry = CapabilityRegistry()
    with pytest.raises(ValueError):
        registry.register(Capability("open", "invalid", lambda args: None))


def test_registry_executes_only_registered_capabilities():
    registry = CapabilityRegistry()
    registry.register(Capability("app.open", "Open an application", lambda args: {"args": args}))
    assert registry.execute("app.open", ["messages"]) == {"args": ["messages"]}
    with pytest.raises(PermissionError, match="capability_not_allowed"):
        registry.execute("system.shell", ["anything"])
