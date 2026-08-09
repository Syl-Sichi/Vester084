from dataclasses import dataclass


@dataclass(frozen=True)
class ConfirmationRequest:
    action: str
    reason: str


class ConfirmationGate:
    """Explicit approval gate for sensitive capabilities."""

    def __init__(self) -> None:
        self._approved: set[str] = set()

    def request(self, action: str, reason: str) -> ConfirmationRequest:
        return ConfirmationRequest(action, reason)

    def approve(self, action: str) -> None:
        self._approved.add(action)

    def consume(self, action: str) -> bool:
        if action not in self._approved:
            return False
        self._approved.remove(action)
        return True
