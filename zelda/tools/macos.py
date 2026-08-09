from __future__ import annotations

from typing import Any

from zelda.core.models import ExecutionResult
from zelda.macos.system import MacOSSystemCapabilities
from zelda.tools.base import Tool


class MacOSSystemStatusTool(Tool):
    name = "macos.system.status"
    description = "Read safe, non mutating macOS host status."

    def execute(self, arguments: dict[str, Any]) -> ExecutionResult:
        return ExecutionResult(True, "macOS system status collected.", MacOSSystemCapabilities.system_info([]))


class MacOSApplicationsTool(Tool):
    name = "macos.applications.list"
    description = "List applications installed in /Applications on macOS."

    def execute(self, arguments: dict[str, Any]) -> ExecutionResult:
        return ExecutionResult(True, "macOS applications collected.", {"applications": MacOSSystemCapabilities.app_list([])})
