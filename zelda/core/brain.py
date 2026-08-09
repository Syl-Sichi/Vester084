from zelda.core.models import ExecutionResult, Intent
from zelda.core.provider import ModelProvider
from zelda.core.permissions import PermissionEngine
from zelda.tools.registry import ToolRegistry


class Brain:
    """AI decision layer. It can understand commands and route only registered tools."""

    def __init__(self, provider: ModelProvider, registry: ToolRegistry, permissions: PermissionEngine) -> None:
        self.provider = provider
        self.registry = registry
        self.permissions = permissions

    def handle(self, text: str) -> ExecutionResult:
        intent: Intent = self.provider.understand(text)
        if intent.name == "conversation.unknown":
            return ExecutionResult(False, "I do not have a capability for that request yet.")

        tool = self.registry.get(intent.name)
        if tool is None:
            return ExecutionResult(False, f"No capability is registered for {intent.name}.")
        if not self.permissions.allows(tool.name, intent):
            return ExecutionResult(False, "That capability is not currently permitted.")

        return tool.execute(intent.arguments)
