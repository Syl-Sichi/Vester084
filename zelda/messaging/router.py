from zelda.events.bus import Event, EventBus
from zelda.messaging.base import Message
from zelda.messaging.registry import MessagingRegistry


class MessagingRouter:
    """Routes normalized messages to the event bus and selected platform adapter."""

    def __init__(self, registry: MessagingRegistry, event_bus: EventBus) -> None:
        self.registry = registry
        self.event_bus = event_bus

    def receive(self, message: Message) -> None:
        self.event_bus.publish(Event("message.received", {"message": message}))

    def send(self, platform: str, conversation_id: str, text: str) -> Message:
        adapter = self.registry.get(platform)
        if adapter is None:
            raise KeyError(f"No messaging adapter registered for {platform}")
        message = adapter.send(conversation_id, text)
        self.event_bus.publish(Event("message.sent", {"message": message}))
        return message
