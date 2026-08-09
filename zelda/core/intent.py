from dataclasses import dataclass

from zelda.core.models import Intent


@dataclass(frozen=True)
class IntentRule:
    name: str
    keywords: tuple[str, ...]
    requires_confirmation: bool = False


class IntentParser:
    """Deterministic fallback parser used when no model provider is configured."""

    def __init__(self) -> None:
        self.rules = (
            IntentRule("system.status", ("system status", "computer status", "check my computer", "system")),
            IntentRule("system.time", ("what time", "current time", "time")),
        )

    def parse(self, text: str) -> Intent:
        normalized = " ".join(text.lower().strip().split())
        for rule in self.rules:
            if any(keyword in normalized for keyword in rule.keywords):
                return Intent(rule.name, {}, rule.requires_confirmation)
        return Intent("conversation.unknown", {"text": text})
