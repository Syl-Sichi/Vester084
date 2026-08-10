from __future__ import annotations

import platform

from zelda.control.capabilities import Capability, CapabilityRegistry
from zelda.control.macos_display import MacOSDisplayCapabilities


def register_macos_display_capabilities(registry: CapabilityRegistry) -> None:
    """Register explicit macOS display capabilities."""
    if platform.system() != "Darwin":
        return

    capabilities = (
        Capability("display.list", "Request display information from the native macOS app", MacOSDisplayCapabilities.list_displays),
        Capability("window.move", "Request moving the Z.E.L.D.A. window to a display", MacOSDisplayCapabilities.move_zelda),
    )
    for capability in capabilities:
        if registry.get(capability.name) is None:
            registry.register(capability)
