from dataclasses import dataclass
from typing import Any

from zelda.control.capabilities import CapabilityRegistry
from zelda.control.discovery import CapabilityDiscovery
from zelda.control.intent_router import IntentRouter
from zelda.control.policy import CapabilityPolicy


@dataclass(frozen=True)
class ControlResult:
    capability: str
    result: Any


class AIControlService:
    """Controlled natural-language entry point for registered capabilities."""

    def __init__(self, registry: CapabilityRegistry, policy: CapabilityPolicy | None = None) -> None:
        self.registry = registry
        self.policy = policy or CapabilityPolicy.from_registry(registry)
        self.discovery = CapabilityDiscovery(registry)
        self.router = IntentRouter(registry, self.policy)

    def capabilities(self) -> list[dict[str, str]]:
        return self.discovery.snapshot()

    def handle_text(self, text: str) -> ControlResult:
        intent = self.router.route(text)
        self.policy.require(intent.capability)
        result = self.registry.execute(intent.capability, intent.args)
        return ControlResult(intent.capability, result)
