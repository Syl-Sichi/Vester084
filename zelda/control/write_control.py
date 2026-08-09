from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from zelda.control.write_policy import WriteAuthorization


@dataclass(frozen=True)
class WriteRequest:
    capability: str
    args: list[str]


class WriteController:
    """Small authorization gate for state changing capabilities."""

    def __init__(self, executor) -> None:
        self.executor = executor

    def execute(self, request: WriteRequest, authorization: WriteAuthorization | None = None) -> dict[str, Any]:
        if authorization is None:
            raise PermissionError("write_confirmation_required")
        authorization.require_confirmation(request.capability)
        result = self.executor(request.capability, request.args)
        return {
            "accepted": True,
            "capability": request.capability,
            "result": result,
        }
