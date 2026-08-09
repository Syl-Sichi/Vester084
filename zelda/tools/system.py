import platform
import shutil
from typing import Any

from zelda.core.models import ExecutionResult
from zelda.tools.base import Tool


class SystemStatusTool(Tool):
    name = "system.status"
    description = "Read safe, non mutating Ubuntu host status."

    def execute(self, arguments: dict[str, Any]) -> ExecutionResult:
        disk = shutil.disk_usage("/")
        data = {
            "platform": platform.platform(),
            "kernel": platform.release(),
            "machine": platform.machine(),
            "disk_total_bytes": disk.total,
            "disk_free_bytes": disk.free,
        }
        return ExecutionResult(True, "System status collected.", data)
