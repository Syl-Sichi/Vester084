from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ControlResult:
    accepted: bool
    action: str
    response: str
    metadata: dict[str, Any]


class AIControlService:
    """Deterministic control layer that normalizes commands before execution.

    The executor is injected so an LLM, local model, or OS adapter can be
    added later without allowing model output to directly execute actions.
    """

    def __init__(self, executor: Callable[[str, dict[str, Any]], Any] | None = None) -> None:
        self.executor = executor

    def process(self, command: str) -> ControlResult:
        normalized = " ".join(command.strip().split())
        if not normalized:
            return ControlResult(False, "noop", "empty command", {})

        action, arguments = self._parse(normalized)
        if self.executor is None:
            return ControlResult(True, action, "command accepted", {"arguments": arguments})

        result = self.executor(action, arguments)
        return ControlResult(True, action, "command executed", {"arguments": arguments, "result": result})

    def _parse(self, command: str) -> tuple[str, dict[str, Any]]:
        parts = command.split(" ", 1)
        action = parts[0].lower()
        argument = parts[1] if len(parts) == 2 else ""
        return action, {"text": argument}
