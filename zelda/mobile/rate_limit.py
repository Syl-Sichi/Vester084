import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, max_events: int = 30, window_seconds: float = 10.0) -> None:
        if max_events <= 0 or window_seconds <= 0:
            raise ValueError("invalid rate limit configuration")
        self.max_events = max_events
        self.window_seconds = window_seconds
        self._events: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, client_id: str, now: float | None = None) -> bool:
        current = time.monotonic() if now is None else now
        events = self._events[client_id]
        cutoff = current - self.window_seconds
        while events and events[0] <= cutoff:
            events.popleft()
        if len(events) >= self.max_events:
            return False
        events.append(current)
        return True

    def remove(self, client_id: str) -> None:
        self._events.pop(client_id, None)
