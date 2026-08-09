from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Intent:
    """Normalized intent produced by the AI layer."""

    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    requires_confirmation: bool = False


@dataclass(frozen=True)
class ExecutionResult:
    """Safe, serializable result returned by a tool."""

    success: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)
