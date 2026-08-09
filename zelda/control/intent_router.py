from dataclasses import dataclass

from zelda.control.capabilities import CapabilityRegistry
from zelda.control.policy import CapabilityPolicy


@dataclass(frozen=True)
class Intent:
    capability: str
    args: list[str]


class IntentRouter:
    """Maps a small explicit set of natural language intents to capabilities."""

    def __init__(self, registry: CapabilityRegistry, policy: CapabilityPolicy) -> None:
        self.registry = registry
        self.policy = policy

    def route(self, text: str) -> Intent:
        normalized = " ".join(text.strip().lower().split())
        if normalized in {"show running processes", "list running processes", "what processes are running"}:
            capability = "system.processes.read"
        elif normalized in {"system info", "show system info", "what system am i running"}:
            capability = "system.info"
        else:
            raise ValueError("intent_not_supported")

        self.policy.require(capability)
        if self.registry.get(capability) is None:
            raise PermissionError(f"capability_not_allowed:{capability}")
        return Intent(capability, [])
