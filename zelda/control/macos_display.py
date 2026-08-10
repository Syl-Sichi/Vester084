"""Controlled macOS display capability contracts."""
from __future__ import annotations

from typing import Any


class MacOSDisplayCapabilities:
    @staticmethod
    def list_displays(_args: list[str]) -> dict[str, Any]:
        return {"action": "display.list", "native_required": True}

    @staticmethod
    def move_zelda(args: list[str]) -> dict[str, Any]:
        target = args[0] if args else "primary"
        return {
            "action": "window.move",
            "target": target,
            "native_required": True,
            "confirmation_required": True,
        }
