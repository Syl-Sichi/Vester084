from zelda.control.capabilities import Capability, CapabilityRegistry
from zelda.control.ubuntu_processes import UbuntuProcessCapabilities
from zelda.control.ubuntu_readonly import UbuntuReadonlyCapabilities


def register_ubuntu_readonly_capabilities(registry: CapabilityRegistry) -> None:
    """Register the safe, read only Ubuntu host capabilities."""
    registry.register(Capability(
        "system.info",
        "Read basic host platform information",
        UbuntuReadonlyCapabilities.system_info,
    ))
    registry.register(Capability(
        "system.environment.read",
        "Read explicitly requested environment variables",
        UbuntuReadonlyCapabilities.environment,
    ))
    registry.register(Capability(
        "system.processes.read",
        "Read running process IDs and names",
        UbuntuProcessCapabilities.processes_read,
    ))
