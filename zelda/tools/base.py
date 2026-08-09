from abc import ABC, abstractmethod
from typing import Any

from zelda.core.models import ExecutionResult


class Tool(ABC):
    """A narrowly scoped capability exposed to the AI core."""

    name: str
    description: str
    dangerous: bool = False

    @abstractmethod
    def execute(self, arguments: dict[str, Any]) -> ExecutionResult:
        raise NotImplementedError
