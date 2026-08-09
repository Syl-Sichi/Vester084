from dataclasses import dataclass
from typing import Any

from android.protocol import AndroidCommand
from zelda.mobile.transport import TransportFrame


@dataclass(frozen=True)
class PendingCommand:
    request_id: str
    command: str


class AndroidCommandClient:
    """Builds commands and correlates asynchronous responses by request ID."""

    def __init__(self, access_token: str) -> None:
        self.access_token = access_token
        self._pending: dict[str, PendingCommand] = {}

    def send(self, request_id: str, command: str) -> TransportFrame:
        if not request_id or not command.strip():
            raise ValueError("request_id and command are required")
        if request_id in self._pending:
            raise ValueError("request_id already pending")
        pending = PendingCommand(request_id, command.strip())
        self._pending[request_id] = pending
        return AndroidCommand(request_id, pending.command).frame(self.access_token)

    def resolve(self, frame: TransportFrame) -> Any:
        if frame.kind != "RESPONSE":
            raise ValueError("expected RESPONSE frame")
        pending = self._pending.pop(frame.request_id, None)
        if pending is None:
            raise KeyError("unknown request_id")
        payload = frame.payload or {}
        if "result" in payload:
            return payload["result"]
        if "error" in payload:
            raise RuntimeError(payload["error"])
        return payload

    @property
    def pending_count(self) -> int:
        return len(self._pending)
