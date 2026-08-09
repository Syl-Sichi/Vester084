from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Message:
    platform: str
    conversation_id: str
    sender: str
    text: str
    message_id: str | None = None


class MessagingAdapter(Protocol):
    """Platform specific messaging boundary. Credentials stay inside each adapter."""

    platform: str

    def send_text(self, conversation_id: str, text: str) -> Message:
        ...

    def list_conversations(self) -> list[dict[str, str]]:
        ...
