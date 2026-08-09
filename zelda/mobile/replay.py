from dataclasses import dataclass
from collections import deque

from zelda.mobile.transport import TransportFrame


@dataclass(frozen=True)
class BufferedEvent:
    sequence: int
    frame: TransportFrame


class ReplayBuffer:
    """Bounded recent event buffer for reconnect replay."""

    def __init__(self, max_items: int = 256) -> None:
        if max_items < 1:
            raise ValueError("max_items must be positive")
        self._events: deque[BufferedEvent] = deque(maxlen=max_items)
        self._sequence = 0

    def add(self, frame: TransportFrame) -> BufferedEvent:
        self._sequence += 1
        event = BufferedEvent(self._sequence, frame)
        self._events.append(event)
        return event

    @property
    def latest_sequence(self) -> int:
        return self._sequence

    def after(self, sequence: int) -> list[BufferedEvent]:
        return [event for event in self._events if event.sequence > sequence]

    def oldest_sequence(self) -> int | None:
        return self._events[0].sequence if self._events else None
