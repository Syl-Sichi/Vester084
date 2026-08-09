from zelda.core.intent import IntentParser
from zelda.core.models import ExecutionResult


class Orchestrator:
    """Coordinates understanding and execution without granting arbitrary code access."""

    def __init__(self, tool_registry, permission_engine) -> None:
        self.tool_registry = tool_registry
        self.permission_engine = permission_engine
        self.parser = IntentParser()

    def handle(self, text: str) -> ExecutionResult:
        intent = self.parser.parse(text)

        if intent.name == "conversation.unknown":
            return ExecutionResult(False, "I do not know how to perform that action yet.")

        tool = self.tool_registry.get(intent.name)
        if tool is None:
            return ExecutionResult(False, f"No tool is registered for {intent.name}.")

        if not self.permission_engine.allows(tool.name, intent):
            return ExecutionResult(False, "Permission is required before I can perform that action.")

        return tool.execute(intent.arguments)
