from dataclasses import dataclass
from typing import Any

from zelda.messaging.base import Message


@dataclass(frozen=True)
class WebhookEvent:
    platform: str
    event_type: str
    payload: dict[str, Any]


class WebhookNormalizer:
    """Converts platform webhook payloads into the internal event shape.

    Platform specific parsers should subclass this component rather than leaking
    provider payloads into the Z.E.L.D.A. core.
    """

    platform = "unknown"

    def normalize(self, payload: dict[str, Any]) -> WebhookEvent:
        return WebhookEvent(self.platform, "unknown", payload)

    @staticmethod
    def message_event(platform: str, conversation_id: str, sender_id: str, text: str, message_id: str | None = None) -> WebhookEvent:
        message = Message(platform, conversation_id, sender_id, text, message_id)
        return WebhookEvent(platform, "message.received", {"message": message})
