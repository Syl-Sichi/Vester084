from collections import deque
from typing import Protocol

from zelda.mobile.transport import TransportFrame


class FrameTransport(Protocol):
    def connect(self) -> None: ...
    def send(self, frame: TransportFrame) -> None: ...
    def receive(self, timeout: float | None = None) -> TransportFrame: ...
    def close(self) -> None: ...


class InMemoryAndroidTransport:
    """Test transport implementing the same boundary a real socket transport will use."""

    def __init__(self) -> None:
        self.connected = False
        self.sent: deque[TransportFrame] = deque()
        self.incoming: deque[TransportFrame] = deque()

    def connect(self) -> None:
        self.connected = True

    def send(self, frame: TransportFrame) -> None:
        if not self.connected:
            raise RuntimeError("transport is not connected")
        self.sent.append(frame)

    def receive(self, timeout: float | None = None) -> TransportFrame:
        if not self.connected:
            raise RuntimeError("transport is not connected")
        if not self.incoming:
            raise TimeoutError("no frame available")
        return self.incoming.popleft()

    def close(self) -> None:
        self.connected = False

    def inject(self, frame: TransportFrame) -> None:
        if self.connected:
            self.incoming.append(frame)
