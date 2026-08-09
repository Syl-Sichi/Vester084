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
