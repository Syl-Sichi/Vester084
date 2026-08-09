from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Event:
    topic: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EventBus:
    """Small in process event bus for decoupling adapters from the AI core."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[Event], None]]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Callable[[Event], None]) -> None:
        if handler not in self._subscribers[topic]:
            self._subscribers[topic].append(handler)

    def publish(self, event: Event) -> None:
        for handler in tuple(self._subscribers.get(event.topic, ())):
            handler(event)

    def topics(self) -> tuple[str, ...]:
        return tuple(sorted(self._subscribers))
