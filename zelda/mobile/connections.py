class ConnectionRegistry:
    """Tracks active WebSocket clients and enforces the connection cap."""

    def __init__(self, max_connections: int = 100) -> None:
        if max_connections <= 0:
            raise ValueError("max_connections must be positive")
        self.max_connections = max_connections
        self._active: set[str] = set()

    @property
    def active_count(self) -> int:
        return len(self._active)

    def acquire(self, client_id: str) -> None:
        if client_id in self._active:
            return
        if len(self._active) >= self.max_connections:
            raise RuntimeError("connection_limit_reached")
        self._active.add(client_id)

    def release(self, client_id: str) -> None:
        self._active.discard(client_id)
