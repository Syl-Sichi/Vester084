"""Display discovery abstraction for Z.E.L.D.A.

The core remains platform neutral. The macOS implementation can later map
these records to NSScreen and window placement without changing the planner.
"""
from __future__ import annotations

import platform
from dataclasses import dataclass


@dataclass(frozen=True)
class DisplayInfo:
    identifier: str
    name: str
    primary: bool = False


def list_displays() -> list[DisplayInfo]:
    """Return a conservative display list for the current platform."""
    if platform.system() == "Darwin":
        # Native SwiftUI/AppKit code will provide the authoritative NSScreen
        # records. The Python core intentionally avoids pretending to know
        # display geometry until that bridge is connected.
        return [DisplayInfo(identifier="macos", name="Mac display", primary=True)]
    return []


def display_summary() -> dict[str, object]:
    displays = list_displays()
    return {
        "platform": platform.system(),
        "count": len(displays),
        "displays": [
            {
                "identifier": display.identifier,
                "name": display.name,
                "primary": display.primary,
            }
            for display in displays
        ],
    }
