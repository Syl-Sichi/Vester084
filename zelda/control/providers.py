from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ProviderIntent:
    capability: str
    args: list[str]


class AIProvider(Protocol):
    def interpret(self, text: str) -> ProviderIntent: ...


class RulesProvider:
    """Deterministic provider used as the safe baseline."""

    _routes = {
        "show running processes": "system.processes.read",
        "list running processes": "system.processes.read",
        "what processes are running": "system.processes.read",
        "system info": "system.info",
        "show system info": "system.info",
        "what system am i running": "system.info",
    }

    def interpret(self, text: str) -> ProviderIntent:
        normalized = " ".join(text.strip().lower().split())
        capability = self._routes.get(normalized)
        if capability is None:
            raise ValueError("intent_not_supported")
        return ProviderIntent(capability, [])


def build_provider(name: str) -> AIProvider:
    if name == "rules":
        return RulesProvider()
    if name == "ollama":
        from zelda.control.ollama_provider import OllamaProvider

        return OllamaProvider()
    raise ValueError(f"ai_provider_not_implemented:{name}")
