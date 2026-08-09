from typing import Any

from zelda.control.capabilities import CapabilityRegistry
from zelda.control.intent_router import Intent, IntentRouter
from zelda.control.policy import CapabilityPolicy
from zelda.control.providers import AIProvider, build_provider


class AIControlService:
    """Controlled natural language to capability execution boundary."""

    def __init__(self, registry: CapabilityRegistry, policy: CapabilityPolicy, provider: AIProvider | None = None) -> None:
        self.registry = registry
        self.policy = policy
        self.provider = provider or build_provider("rules")
        self.router = IntentRouter(registry, policy)

    def handle(self, text: str) -> dict[str, Any]:
        proposed = self.provider.interpret(text)
        intent = Intent(proposed.capability, proposed.args)
        self.policy.require(intent.capability)
        if self.registry.get(intent.capability) is None:
            raise PermissionError(f"capability_not_allowed:{intent.capability}")
        result = self.registry.execute(intent.capability, intent.args)
        return {
            "accepted": True,
            "capability": intent.capability,
            "result": result,
        }
