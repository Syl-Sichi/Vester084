from zelda.control.bootstrap import register_ubuntu_readonly_capabilities
from zelda.control.capabilities import CapabilityRegistry


def test_ubuntu_bootstrap_is_idempotent():
    registry = CapabilityRegistry()
    register_ubuntu_readonly_capabilities(registry)
    register_ubuntu_readonly_capabilities(registry)
    assert registry.names() == (
        "app.find",
        "app.list",
        "app.status",
        "system.disk.read",
        "system.environment.read",
        "system.info",
        "system.memory.read",
        "system.network.info",
        "system.network.port.check",
        "system.processes.read",
    )
