from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True)
class Capability:
    name: str
    description: str
    executor: Callable[[list[str]], Any]


class CapabilityRegistry:
    """Explicit allowlist of actions the control service may execute."""

    def __init__(self) -> None:
        self._capabilities: dict[str, Capability] = {}

    def register(self, capability: Capability) -> None:
        if not capability.name or "." not in capability.name:
            raise ValueError("capability name must use a namespace")
        if capability.name in self._capabilities:
            raise ValueError("capability already registered")
        self._capabilities[capability.name] = capability

    def get(self, name: str) -> Capability | None:
        return self._capabilities.get(name)

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._capabilities))

    def execute(self, name: str, args: list[str]) -> Any:
        capability = self.get(name)
        if capability is None:
            raise PermissionError(f"capability_not_allowed:{name}")
        return capability.executor(args)
