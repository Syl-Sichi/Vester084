from enum import Enum


class ConnectionState(str, Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    CLOSED = "closed"


class AndroidConnectionState:
    def __init__(self) -> None:
        self._state = ConnectionState.DISCONNECTED
        self._last_acknowledged = 0

    @property
    def state(self) -> ConnectionState:
        return self._state

    @property
    def last_acknowledged(self) -> int:
        return self._last_acknowledged

    def transition(self, state: ConnectionState) -> None:
        if self._state == ConnectionState.CLOSED and state != ConnectionState.CLOSED:
            raise RuntimeError("closed connection cannot transition")
        self._state = state

    def acknowledge(self, sequence: int) -> None:
        if sequence < 0:
            raise ValueError("sequence must be non negative")
        if sequence > self._last_acknowledged:
            self._last_acknowledged = sequence
