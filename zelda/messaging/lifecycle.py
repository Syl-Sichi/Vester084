from enum import Enum


class AdapterState(str, Enum):
    CREATED = "created"
    AUTHENTICATED = "authenticated"
    CONNECTED = "connected"
    CLOSED = "closed"
    ERROR = "error"


class AdapterLifecycle:
    def __init__(self) -> None:
        self.state = AdapterState.CREATED

    def authenticated(self) -> None:
        self.state = AdapterState.AUTHENTICATED

    def connected(self) -> None:
        self.state = AdapterState.CONNECTED

    def close(self) -> None:
        self.state = AdapterState.CLOSED

    def error(self) -> None:
        self.state = AdapterState.ERROR
