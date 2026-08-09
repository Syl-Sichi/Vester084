from typing import Any

from zelda.control.capabilities import CapabilityRegistry
from zelda.control.intent_router import Intent
from zelda.control.policy import CapabilityPolicy
from zelda.control.providers import AIProvider, build_provider


class AIControlService:
    """Controlled natural language to capability execution boundary."""

    def __init__(self, registry: CapabilityRegistry, policy: CapabilityPolicy, provider: AIProvider | None = None, *, provider_name: str = "rules", ollama_url: str = "http://127.0.0.1:11434", ollama_model: str = "gemma3") -> None:
        self.registry = registry
        self.policy = policy
        self.provider = provider or build_provider(provider_name, ollama_url=ollama_url, ollama_model=ollama_model)

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
