from zelda.control.bootstrap import register_ubuntu_readonly_capabilities
from zelda.control.capabilities import CapabilityRegistry


def test_bootstrap_registers_expected_ubuntu_readonly_capabilities():
    registry = CapabilityRegistry()
    register_ubuntu_readonly_capabilities(registry)
    assert registry.names() == (
        "system.environment.read",
        "system.info",
        "system.processes.read",
    )
