from zelda.control.capabilities import Capability, CapabilityRegistry
from zelda.control.ubuntu_processes import UbuntuProcessCapabilities
from zelda.control.ubuntu_readonly import UbuntuReadonlyCapabilities


def register_ubuntu_readonly_capabilities(registry: CapabilityRegistry) -> None:
    """Register the safe, read only Ubuntu host capabilities."""
    capabilities = (
        Capability(
            "system.info",
            "Read basic host platform information",
            UbuntuReadonlyCapabilities.system_info,
        ),
        Capability(
            "system.environment.read",
            "Read explicitly requested environment variables",
            UbuntuReadonlyCapabilities.environment,
        ),
        Capability(
            "system.processes.read",
            "Read running process IDs and names",
            UbuntuProcessCapabilities.processes_read,
        ),
    )
    for capability in capabilities:
        if registry.get(capability.name) is None:
            registry.register(capability)
