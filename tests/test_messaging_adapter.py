from zelda.messaging.development import DevelopmentMessagingAdapter
from zelda.messaging.lifecycle import AdapterState


def test_development_adapter_lifecycle_and_send():
    adapter = DevelopmentMessagingAdapter()
    assert adapter.lifecycle.state == AdapterState.CONNECTED
    message = adapter.send("conversation-1", "hello")
    assert message.platform == "development"
    assert message.text == "hello"
    adapter.close()
    assert adapter.lifecycle.state == AdapterState.CLOSED
