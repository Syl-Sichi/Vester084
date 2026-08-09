import os
import shutil
from typing import Any

from zelda.core.models import ExecutionResult
from zelda.tools.base import Tool


class ApplicationDiscoveryTool(Tool):
    name = "application.discover"
    description = "Check whether named executable applications are available on the host."

    def execute(self, arguments: dict[str, Any]) -> ExecutionResult:
        names = arguments.get("names", [])
        if isinstance(names, str):
            names = [names]
        if not isinstance(names, list):
            return ExecutionResult(False, "names must be a list or string.")

        results = []
        for name in names[:50]:
            if not isinstance(name, str) or not name.strip():
                continue
            executable = shutil.which(name.strip())
            results.append({"name": name.strip(), "available": executable is not None, "path": executable})

        return ExecutionResult(True, "Application discovery completed.", {"results": results, "user": os.getenv("USER")})


class ApplicationLaunchTool(Tool):
    name = "application.launch"
    description = "Prepare a launch request for an explicitly permitted executable."
    dangerous = True

    def __init__(self, allowed: set[str] | None = None) -> None:
        self.allowed = allowed or set()

    def execute(self, arguments: dict[str, Any]) -> ExecutionResult:
        name = str(arguments.get("name", "")).strip()
        if not name:
            return ExecutionResult(False, "An application name is required.")
        if name not in self.allowed:
            return ExecutionResult(False, "That application is not explicitly permitted.")
        executable = shutil.which(name)
        if executable is None:
            return ExecutionResult(False, "Application is not installed or not on PATH.")
        return ExecutionResult(False, "Application launch is awaiting an approved process runner.", {"path": executable})
