from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from zelda.control.write_control import WriteController, WriteRequest
from zelda.control.write_policy import WriteAuthorization


@dataclass(frozen=True)
class PendingConfirmation:
    token: str
    request: WriteRequest


class ConfirmationManager:
    """Creates one time confirmation tokens for pending write requests."""

    def __init__(self) -> None:
        self._pending: dict[str, PendingConfirmation] = {}

    def request_confirmation(self, request: WriteRequest) -> PendingConfirmation:
        token = uuid4().hex
        pending = PendingConfirmation(token, request)
        self._pending[token] = pending
        return pending

    def confirm(self, token: str, controller: WriteController) -> dict[str, object]:
        pending = self._pending.pop(token, None)
        if pending is None:
            raise ValueError("confirmation_not_found")
        authorization = WriteAuthorization(pending.request.capability, confirmed=True)
        return controller.execute(pending.request, authorization)

    def cancel(self, token: str) -> None:
        self._pending.pop(token, None)
