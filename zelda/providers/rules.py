from zelda.core.intent import IntentParser
from zelda.core.models import Intent
from zelda.core.provider import ModelProvider


class RuleBasedProvider(ModelProvider):
    """Bootstrap provider that works without an external model or API key."""

    def __init__(self) -> None:
        self.parser = IntentParser()

    def understand(self, text: str) -> Intent:
        return self.parser.parse(text)
