from dataclasses import dataclass

from zelda.control.capabilities import CapabilityRegistry


@dataclass(frozen=True)
class CapabilityPolicy:
    allowed: frozenset[str]

    @classmethod
    def from_registry(cls, registry: CapabilityRegistry) -> "CapabilityPolicy":
        return cls(frozenset(registry.names()))

    def permits(self, capability: str) -> bool:
        return capability in self.allowed

    def require(self, capability: str) -> None:
        if not self.permits(capability):
            raise PermissionError(f"capability_not_allowed:{capability}")

    def snapshot(self) -> tuple[str, ...]:
        return tuple(sorted(self.allowed))
