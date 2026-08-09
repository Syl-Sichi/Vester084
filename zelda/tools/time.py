from datetime import datetime, timezone
from typing import Any

from zelda.core.models import ExecutionResult
from zelda.tools.base import Tool


class CurrentTimeTool(Tool):
    name = "system.time"
    description = "Return the current UTC time."

    def execute(self, arguments: dict[str, Any]) -> ExecutionResult:
        now = datetime.now(timezone.utc)
        return ExecutionResult(True, now.isoformat(), {"utc": now.isoformat()})
