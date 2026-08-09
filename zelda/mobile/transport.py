import json
import queue
import threading
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class TransportFrame:
    kind: str
    request_id: str | None = None
    payload: dict | None = None

    def encode(self) -> bytes:
        return (json.dumps({"kind": self.kind, "request_id": self.request_id, "payload": self.payload or {}}, separators=(",", ":")) + "\n").encode("utf-8")

    @classmethod
    def decode(cls, data: bytes) -> "TransportFrame":
        value = json.loads(data.decode("utf-8"))
        if not isinstance(value, dict) or not isinstance(value.get("kind"), str):
            raise ValueError("invalid transport frame")
        payload = value.get("payload", {})
        if not isinstance(payload, dict):
            raise ValueError("invalid frame payload")
        return cls(value["kind"], value.get("request_id"), payload)


class LocalTransport:
    """In process transport abstraction for mobile protocol testing."""

    def __init__(self) -> None:
        self._incoming: queue.Queue[TransportFrame] = queue.Queue()
        self._outgoing: queue.Queue[TransportFrame] = queue.Queue()
        self._handlers: list[Callable[[TransportFrame], None]] = []
        self._closed = threading.Event()

    def on_frame(self, handler: Callable[[TransportFrame], None]) -> None:
        self._handlers.append(handler)

    def send(self, frame: TransportFrame) -> None:
        if self._closed.is_set():
            raise RuntimeError("transport is closed")
        self._outgoing.put(frame)

    def inject(self, frame: TransportFrame) -> None:
        if self._closed.is_set():
            return
        self._incoming.put(frame)
        for handler in tuple(self._handlers):
            handler(frame)

    def receive(self, timeout: float | None = None) -> TransportFrame:
        return self._outgoing.get(timeout=timeout)

    def close(self) -> None:
        self._closed.set()
