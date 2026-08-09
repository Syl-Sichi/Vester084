from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import time


class ConnectionState(str, Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    CLOSED = "closed"


@dataclass
class ConnectionConfig:
    heartbeat_seconds: float = 30.0
    reconnect_initial_seconds: float = 1.0
    reconnect_max_seconds: float = 30.0


class MobileConnection:
    """Transport independent connection state machine for the Android client."""

    def __init__(self, config: ConnectionConfig | None = None) -> None:
        self.config = config or ConnectionConfig()
        self.state = ConnectionState.DISCONNECTED
        self.last_activity = 0.0
        self.reconnect_attempt = 0

    def begin(self) -> None:
        if self.state == ConnectionState.CLOSED:
            raise RuntimeError("Connection is closed")
        self.state = ConnectionState.CONNECTING

    def connected(self) -> None:
        self.state = ConnectionState.CONNECTED
        self.reconnect_attempt = 0
        self.touch()

    def failed(self) -> float:
        if self.state == ConnectionState.CLOSED:
            return 0.0
        self.state = ConnectionState.RECONNECTING
        self.reconnect_attempt += 1
        delay = self.config.reconnect_initial_seconds * (2 ** (self.reconnect_attempt - 1))
        return min(delay, self.config.reconnect_max_seconds)

    def touch(self) -> None:
        self.last_activity = time.monotonic()

    def heartbeat_due(self) -> bool:
        return self.state == ConnectionState.CONNECTED and (time.monotonic() - self.last_activity) >= self.config.heartbeat_seconds

    def close(self) -> None:
        self.state = ConnectionState.CLOSED
