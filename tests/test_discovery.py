from zelda.control.capabilities import Capability, CapabilityRegistry
from zelda.control.discovery import CapabilityDiscovery


def test_discovery_reports_registered_capabilities():
    registry = CapabilityRegistry()
    registry.register(Capability("system.info", "Read system information", lambda args: None))
    registry.register(Capability("file.read", "Read a file", lambda args: None))

    snapshot = CapabilityDiscovery(registry).snapshot()
    assert snapshot == [
        {"name": "file.read", "description": "Read a file"},
        {"name": "system.info", "description": "Read system information"},
    ]
