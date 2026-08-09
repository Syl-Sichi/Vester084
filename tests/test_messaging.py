from zelda.events.bus import EventBus
from zelda.messaging.base import Message
from zelda.messaging.mock import MockMessagingAdapter
from zelda.messaging.registry import MessagingRegistry
from zelda.messaging.router import MessagingRouter


def test_message_is_normalized_into_event():
    bus = EventBus()
    registry = MessagingRegistry()
    registry.register(MockMessagingAdapter())
    router = MessagingRouter(registry, bus)
    received = []
    bus.subscribe("message.received", received.append)

    message = Message("mock", "conversation-1", "user-1", "hello")
    router.receive(message)

    assert received[0].payload["message"] == message


def test_mock_send_routes_through_registry():
    bus = EventBus()
    registry = MessagingRegistry()
    registry.register(MockMessagingAdapter())
    router = MessagingRouter(registry, bus)

    message = router.send("mock", "conversation-1", "hello")
    assert message.platform == "mock"
    assert message.text == "hello"
