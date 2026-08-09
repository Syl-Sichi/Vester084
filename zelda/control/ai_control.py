from typing import Any

from zelda.control.capabilities import CapabilityRegistry
from zelda.control.intent_router import IntentRouter
from zelda.control.policy import CapabilityPolicy


class AIControlService:
    """Controlled natural language to capability execution boundary."""

    def __init__(self, registry: CapabilityRegistry, policy: CapabilityPolicy) -> None:
        self.registry = registry
        self.policy = policy
        self.router = IntentRouter(registry, policy)

    def handle(self, text: str) -> dict[str, Any]:
        intent = self.router.route(text)
        self.policy.require(intent.capability)
        result = self.registry.execute(intent.capability, intent.args)
        return {
            "accepted": True,
            "capability": intent.capability,
            "result": result,
        }
