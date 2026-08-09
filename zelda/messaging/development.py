from uuid import uuid4

from zelda.messaging.base import Message, MessagingAdapter
from zelda.messaging.lifecycle import AdapterLifecycle


class DevelopmentMessagingAdapter(MessagingAdapter):
    """Local adapter used to test the messaging pipeline without external accounts."""

    platform = "development"

    def __init__(self) -> None:
        self.lifecycle = AdapterLifecycle()
        self.lifecycle.authenticated()
        self.lifecycle.connected()
        self.sent: list[Message] = []

    def send(self, conversation_id: str, text: str) -> Message:
        message = Message("development", conversation_id, "zelda", text, uuid4().hex)
        self.sent.append(message)
        return message

    def close(self) -> None:
        self.lifecycle.close()
