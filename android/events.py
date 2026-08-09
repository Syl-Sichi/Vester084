from dataclasses import dataclass
from typing import Any, Callable

from android.protocol import AndroidAck
from android.storage import AndroidStateStore
from zelda.mobile.transport import TransportFrame


@dataclass(frozen=True)
class AndroidEvent:
    sequence: int
    topic: str
    payload: dict[str, Any]
    created_at: str | None = None


class AndroidEventClient:
    """Validates incoming EVENT frames and acknowledges accepted events."""

    def __init__(self, access_token: str, state_store: AndroidStateStore, on_event: Callable[[AndroidEvent], None] | None = None) -> None:
        self.access_token = access_token
        self.state_store = state_store
        self.on_event = on_event
        self._last_acknowledged = state_store.load_last_acknowledged()

    @property
    def last_acknowledged(self) -> int:
        return self._last_acknowledged

    def handle(self, frame: TransportFrame, request_id: str | None = None) -> TransportFrame | None:
        if frame.kind != "EVENT":
            raise ValueError("expected EVENT frame")
        payload = frame.payload or {}
        sequence = payload.get("sequence")
        topic = payload.get("topic")
        event_payload = payload.get("payload", {})
        if not isinstance(sequence, int) or sequence <= 0:
            raise ValueError("invalid event sequence")
        if not isinstance(topic, str) or not topic:
            raise ValueError("invalid event topic")
        if not isinstance(event_payload, dict):
            raise ValueError("invalid event payload")
        if sequence <= self._last_acknowledged:
            return None

        event = AndroidEvent(sequence, topic, event_payload, payload.get("created_at"))
        if self.on_event is not None:
            self.on_event(event)
        self._last_acknowledged = sequence
        self.state_store.save_last_acknowledged(sequence)
        return AndroidAck(request_id or f"ack-{sequence}", self.access_token, sequence).frame()
