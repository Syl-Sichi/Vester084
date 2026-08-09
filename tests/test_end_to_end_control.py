from zelda.control.bootstrap import register_ubuntu_readonly_capabilities
from zelda.control.capabilities import CapabilityRegistry
from zelda.control.policy import CapabilityPolicy
from zelda.control.ai_control import AIControlService


def test_natural_language_reaches_ubuntu_readonly_capability():
    registry = CapabilityRegistry()
    register_ubuntu_readonly_capabilities(registry)
    policy = CapabilityPolicy.from_registry(registry)
    service = AIControlService(registry, policy)

    result = service.handle("show system info")

    assert result["accepted"] is True
    assert result["capability"] == "system.info"
    assert result["result"]["platform"]
    assert result["result"]["machine"]


def test_unsupported_request_never_reaches_executor():
    registry = CapabilityRegistry()
    register_ubuntu_readonly_capabilities(registry)
    service = AIControlService(registry, CapabilityPolicy.from_registry(registry))

    try:
        service.handle("delete everything")
    except ValueError as exc:
        assert str(exc) == "intent_not_supported"
    else:
        raise AssertionError("unsupported intent was accepted")
