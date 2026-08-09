from dataclasses import dataclass

from zelda.control.capabilities import CapabilityRegistry


@dataclass(frozen=True)
class CapabilityDescriptor:
    name: str
    description: str


class CapabilityDiscovery:
    """Expose the currently registered capabilities without granting new access."""

    def __init__(self, registry: CapabilityRegistry) -> None:
        self.registry = registry

    def discover(self) -> tuple[CapabilityDescriptor, ...]:
        descriptors = []
        for name in self.registry.names():
            capability = self.registry.get(name)
            if capability is not None:
                descriptors.append(CapabilityDescriptor(name, capability.description))
        return tuple(descriptors)

    def snapshot(self) -> list[dict[str, str]]:
        return [{"name": item.name, "description": item.description} for item in self.discover()]
