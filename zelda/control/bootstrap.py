from zelda.control.capabilities import Capability, CapabilityRegistry
from zelda.control.macos_display import MacOSDisplayCapabilities
from zelda.control.ubuntu_apps import UbuntuApplicationCapabilities
from zelda.control.ubuntu_network import UbuntuNetworkCapabilities
from zelda.control.ubuntu_processes import UbuntuProcessCapabilities
from zelda.control.ubuntu_readonly import UbuntuReadonlyCapabilities
from zelda.control.ubuntu_resources import UbuntuResourceCapabilities


def register_ubuntu_readonly_capabilities(registry: CapabilityRegistry) -> None:
    """Register the safe, read only Ubuntu host capabilities."""
    capabilities = (
        Capability("system.info", "Read basic host platform information", UbuntuReadonlyCapabilities.system_info),
        Capability("system.environment.read", "Read explicitly requested environment variables", UbuntuReadonlyCapabilities.environment),
        Capability("system.processes.read", "Read running process IDs and names", UbuntuProcessCapabilities.processes_read),
        Capability("system.memory.read", "Read host memory and swap statistics", UbuntuResourceCapabilities.memory_read),
        Capability("system.disk.read", "Read disk usage for a requested path", UbuntuResourceCapabilities.disk_read),
        Capability("system.network.info", "Read local hostname and addresses", UbuntuNetworkCapabilities.network_info),
        Capability("system.network.port.check", "Check whether a local TCP port is open", UbuntuNetworkCapabilities.port_check),
        Capability("app.list", "List installed desktop applications", UbuntuApplicationCapabilities.app_list),
        Capability("app.find", "Find installed desktop applications by name", UbuntuApplicationCapabilities.app_find),
        Capability("app.status", "Check whether a matching application process is running", UbuntuApplicationCapabilities.app_status),
    )
    for capability in capabilities:
        if registry.get(capability.name) is None:
            registry.register(capability)


def register_macos_display_capabilities(registry: CapabilityRegistry) -> None:
    """Register macOS display intents behind the common capability boundary."""
    capabilities = (
        Capability("display.list", "Request native macOS display information", MacOSDisplayCapabilities.list_displays),
        Capability("window.move", "Request moving the Z.E.L.D.A. window to a display", lambda args: MacOSDisplayCapabilities.move_zelda(args[0] if args else "primary")),
    )
    for capability in capabilities:
        if registry.get(capability.name) is None:
            registry.register(capability)
