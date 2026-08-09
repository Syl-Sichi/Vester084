from dataclasses import dataclass


@dataclass(frozen=True)
class DeliveryAck:
    sequence: int


class AckTracker:
    """Tracks the highest contiguous event sequence acknowledged by a client."""

    def __init__(self) -> None:
        self._acknowledged = 0

    @property
    def acknowledged(self) -> int:
        return self._acknowledged

    def acknowledge(self, sequence: int) -> int:
        if sequence < 0:
            raise ValueError("sequence must be non negative")
        if sequence > self._acknowledged:
            self._acknowledged = sequence
        return self._acknowledged

    def needs_replay(self, sequence: int) -> bool:
        return sequence > self._acknowledged
