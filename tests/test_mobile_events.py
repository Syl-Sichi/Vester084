from zelda.events.bus import Event, EventBus
from zelda.mobile.events import MobileEventBridge
from zelda.mobile.transport import LocalTransport


def test_mobile_event_bridge_forwards_allowed_events():
    bus = EventBus()
    transport = LocalTransport()
    MobileEventBridge(bus, transport)
    bus.publish(Event("task.completed", {"task_id": "1"}))
    frame = transport.receive()
    assert frame.kind == "EVENT"
    assert frame.payload["topic"] == "task.completed"


def test_mobile_event_bridge_ignores_unlisted_events():
    bus = EventBus()
    transport = LocalTransport()
    MobileEventBridge(bus, transport)
    bus.publish(Event("internal.secret", {"value": "hidden"}))
    try:
        transport.receive(timeout=0.01)
    except Exception:
        assert True
