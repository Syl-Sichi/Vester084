"""Minimal desktop shell model for Z.E.L.D.A.

The shell is deliberately separate from execution. UI integrations should
send requests through the same controlled runtime used by the CLI.
"""
from dataclasses import dataclass, field


@dataclass
class DesktopState:
    assistant_name: str = "Z.E.L.D.A."
    status: str = "Ready"
    active_view: str = "Chat"
    messages: list[str] = field(default_factory=list)


class DesktopShell:
    VIEWS = ("Chat", "System", "Apps", "Files", "Security", "Settings")

    def __init__(self, assistant_name: str = "Z.E.L.D.A.") -> None:
        self.state = DesktopState(assistant_name=assistant_name)

    def select_view(self, view: str) -> None:
        if view not in self.VIEWS:
            raise ValueError(f"Unknown desktop view: {view}")
        self.state.active_view = view

    def add_message(self, message: str) -> None:
        self.state.messages.append(message)

    def set_status(self, status: str) -> None:
        self.state.status = status

    def snapshot(self) -> dict:
        return {
            "assistant_name": self.state.assistant_name,
            "status": self.state.status,
            "active_view": self.state.active_view,
            "messages": list(self.state.messages),
        }
