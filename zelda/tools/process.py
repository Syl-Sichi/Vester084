from typing import Any

from zelda.core.models import ExecutionResult
from zelda.tools.base import Tool


class ProcessSnapshotTool(Tool):
    name = "process.snapshot"
    description = "Return a read only snapshot of running processes without exposing command execution."

    def execute(self, arguments: dict[str, Any]) -> ExecutionResult:
        try:
            import psutil
        except ImportError:
            return ExecutionResult(False, "Process support requires the psutil dependency.")

        limit = min(max(int(arguments.get("limit", 20)), 1), 100)
        processes = []
        for proc in psutil.process_iter(["pid", "name", "status"]):
            try:
                info = proc.info
                processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
            if len(processes) >= limit:
                break
        return ExecutionResult(True, "Process snapshot collected.", {"processes": processes})
