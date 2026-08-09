from zelda.messaging.base import Message, MessagingAdapter


class MockMessagingAdapter(MessagingAdapter):
    """Development adapter used to test routing without contacting a real platform."""

    platform = "mock"

    def send(self, conversation_id: str, text: str) -> Message:
        return Message(
            platform=self.platform,
            conversation_id=conversation_id,
            sender_id="zelda",
            text=text,
            message_id=None,
        )

    def close(self) -> None:
        return None
