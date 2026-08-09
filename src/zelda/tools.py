from __future__ import annotations

from datetime import datetime, timezone
import platform

from .core import Tool, ToolRegistry


def system_status(_: dict) -> dict:
    return {
        "platform": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    }


def current_time(_: dict) -> dict:
    now = datetime.now(timezone.utc)
    return {"utc": now.isoformat()}


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        Tool(
            name="system.status",
            description="Read basic operating system status.",
            risk="read",
            handler=system_status,
        )
    )
    registry.register(
        Tool(
            name="system.time",
            description="Read the current UTC time.",
            risk="read",
            handler=current_time,
        )
    )
    return registry
