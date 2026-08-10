"""Controlled macOS display capability requests.

The Python service exposes only intent level display operations. The native
Swift app remains responsible for manipulating its own window.
"""
from __future__ import annotations

from typing import Any


class MacOSDisplayCapabilities:
    @staticmethod
    def list_displays() -> dict[str, Any]:
        return {"action": "display.list", "native_required": True}

    @staticmethod
    def move_zelda(target: str) -> dict[str, Any]:
        return {
            "action": "window.move",
            "target": target,
            "native_required": True,
            "confirmation_required": True,
        }
