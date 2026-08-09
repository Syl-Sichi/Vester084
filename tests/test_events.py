from zelda.events.bus import Event, EventBus


def test_event_bus_dispatches_to_subscriber():
    bus = EventBus()
    received = []
    bus.subscribe("message.received", received.append)
    event = Event("message.received", {"text": "hello"})
    bus.publish(event)
    assert received == [event]
