from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    risk: str
    handler: Callable[[dict[str, Any]], dict[str, Any]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def describe(self) -> list[dict[str, str]]:
        return [
            {"name": t.name, "description": t.description, "risk": t.risk}
            for t in sorted(self._tools.values(), key=lambda item: item.name)
        ]


class PermissionEngine:
    """Conservative first phase permission policy.

    Read-only tools can execute automatically. Tools marked as sensitive must
    explicitly receive an approval flag from a trusted interface.
    """

    def allowed(self, tool: Tool, approved: bool = False) -> bool:
        if tool.risk == "read":
            return True
        return approved


class IntentRouter:
    """Small deterministic router used until an AI model is connected."""

    def route(self, command: str) -> str | None:
        normalized = command.strip().lower()
        if normalized in {"system status", "status", "computer status", "system info"}:
            return "system.status"
        if normalized in {"time", "what time is it", "current time"}:
            return "system.time"
        return None


class ControlCore:
    def __init__(self, registry: ToolRegistry, audit: Callable[[dict[str, Any]], None]) -> None:
        self.registry = registry
        self.permissions = PermissionEngine()
        self.router = IntentRouter()
        self.audit = audit

    def handle(self, command: str, approved: bool = False) -> dict[str, Any]:
        tool_name = self.router.route(command)
        if tool_name is None:
            result = {
                "ok": False,
                "error": "I do not have a registered capability for that command yet.",
                "command": command,
            }
            self.audit({"command": command, "tool": None, "result": result})
            return result

        tool = self.registry.get(tool_name)
        if tool is None:
            result = {"ok": False, "error": "Routed tool is not registered.", "tool": tool_name}
            self.audit({"command": command, "tool": tool_name, "result": result})
            return result

        if not self.permissions.allowed(tool, approved):
            result = {"ok": False, "error": "Permission required.", "tool": tool_name}
            self.audit({"command": command, "tool": tool_name, "result": result})
            return result

        result = tool.handler({"command": command})
        self.audit({"command": command, "tool": tool_name, "result": result})
        return {"ok": True, "tool": tool_name, "result": result}
