from __future__ import annotations

from zelda.control.ai_control import AIControlService
from zelda.control.workspace_executor import WorkspaceExecutor
from zelda.control.write_control import WriteController


def configure_write_controller(service: AIControlService) -> AIControlService:
    """Attach the constrained workspace writer to an existing control service."""
    service.write_controller = WriteController(WorkspaceExecutor())
    return service
