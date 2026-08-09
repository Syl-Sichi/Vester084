from zelda.control.bootstrap import register_ubuntu_readonly_capabilities
from zelda.control.capabilities import CapabilityRegistry


def test_ubuntu_bootstrap_is_idempotent():
    registry = CapabilityRegistry()
    register_ubuntu_readonly_capabilities(registry)
    register_ubuntu_readonly_capabilities(registry)
    assert registry.names() == (
        "system.environment.read",
        "system.info",
        "system.processes.read",
    )
