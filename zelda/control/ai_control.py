from typing import Any

from zelda.control.capabilities import CapabilityRegistry
from zelda.control.confirmation import ConfirmationManager
from zelda.control.intent_router import Intent
from zelda.control.policy import CapabilityPolicy
from zelda.control.providers import AIProvider, build_provider
from zelda.control.write_control import WriteRequest, WriteController


class AIControlService:
    """Controlled natural language to capability execution boundary."""

    def __init__(self, registry: CapabilityRegistry, policy: CapabilityPolicy, provider: AIProvider | None = None, *, provider_name: str = "rules", ollama_url: str = "http://127.0.0.1:11434", ollama_model: str = "gemma3", write_controller: WriteController | None = None, confirmation_manager: ConfirmationManager | None = None) -> None:
        self.registry = registry
        self.policy = policy
        self.provider = provider or build_provider(provider_name, ollama_url=ollama_url, ollama_model=ollama_model)
        self.write_controller = write_controller
        self.confirmation_manager = confirmation_manager or ConfirmationManager()

    def handle(self, text: str) -> dict[str, Any]:
        proposed = self.provider.interpret(text)
        intent = Intent(proposed.capability, proposed.args)
        self.policy.require(intent.capability)
        if self.registry.get(intent.capability) is None:
            raise PermissionError(f"capability_not_allowed:{intent.capability}")
        result = self.registry.execute(intent.capability, intent.args)
        return {"accepted": True, "capability": intent.capability, "result": result}

    def request_write(self, capability: str, args: list[str]) -> dict[str, Any]:
        self.policy.require(capability)
        request = WriteRequest(capability, args)
        pending = self.confirmation_manager.request_confirmation(request)
        return {
            "accepted": False,
            "confirmation_required": True,
            "confirmation_token": pending.token,
            "capability": capability,
            "args": args,
        }

    def confirm_write(self, token: str) -> dict[str, Any]:
        if self.write_controller is None:
            raise RuntimeError("write_controller_not_configured")
        return self.confirmation_manager.confirm(token, self.write_controller)

    def cancel_write(self, token: str) -> None:
        self.confirmation_manager.cancel(token)
