import pytest

from zelda.control.bootstrap import register_ubuntu_readonly_capabilities
from zelda.control.capabilities import CapabilityRegistry
from zelda.control.intent_router import IntentRouter
from zelda.control.policy import CapabilityPolicy


def make_router():
    registry = CapabilityRegistry()
    register_ubuntu_readonly_capabilities(registry)
    return IntentRouter(registry, CapabilityPolicy.from_registry(registry))


def test_router_maps_process_request():
    intent = make_router().route("  show   running processes ")
    assert intent.capability == "system.processes.read"
    assert intent.args == []


def test_router_rejects_unknown_intent():
    with pytest.raises(ValueError, match="intent_not_supported"):
        make_router().route("delete everything")
