from zelda.core.orchestrator import Orchestrator
from zelda.core.permissions import PermissionEngine
from zelda.tools.registry import ToolRegistry
from zelda.tools.system import SystemStatusTool
from zelda.tools.time import CurrentTimeTool


def build_orchestrator() -> Orchestrator:
    registry = ToolRegistry()
    registry.register(SystemStatusTool())
    registry.register(CurrentTimeTool())

    permissions = PermissionEngine()
    permissions.allow("system.status")
    permissions.allow("system.time")

    return Orchestrator(registry, permissions)


orchestrator = build_orchestrator()
