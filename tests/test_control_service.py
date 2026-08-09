from zelda.control.bootstrap import register_ubuntu_readonly_capabilities
from zelda.control.capabilities import CapabilityRegistry
from zelda.control.service import AIControlService


def test_control_service_executes_routed_read_only_intent():
    registry = CapabilityRegistry()
    register_ubuntu_readonly_capabilities(registry)
    service = AIControlService(registry)

    result = service.handle_text("show running processes")
    assert result.capability == "system.processes.read"
    assert isinstance(result.result, list)


def test_control_service_exposes_registered_capabilities():
    registry = CapabilityRegistry()
    register_ubuntu_readonly_capabilities(registry)
    service = AIControlService(registry)

    names = {item["name"] for item in service.capabilities()}
    assert names == {
        "system.info",
        "system.environment.read",
        "system.processes.read",
    }
