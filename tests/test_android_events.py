import pytest

from android.events import AndroidEventClient
from android.storage import AndroidStateStore
from zelda.mobile.transport import TransportFrame


def test_event_client_accepts_event_and_persists_ack(tmp_path):
    store = AndroidStateStore(str(tmp_path / "state.json"))
    received = []
    client = AndroidEventClient("token", store, received.append)
    frame = TransportFrame("EVENT", payload={
        "sequence": 5,
        "topic": "task.completed",
        "payload": {"task_id": "1"},
        "created_at": "2026-08-09T14:00:00Z",
    })
    ack = client.handle(frame)
    assert received[0].sequence == 5
    assert received[0].topic == "task.completed"
    assert ack.kind == "ACK"
    assert ack.payload["sequence"] == 5
    assert store.load_last_acknowledged() == 5


def test_event_client_ignores_duplicate_event(tmp_path):
    store = AndroidStateStore(str(tmp_path / "state.json"))
    client = AndroidEventClient("token", store)
    frame = TransportFrame("EVENT", payload={"sequence": 2, "topic": "notification.received", "payload": {}})
    assert client.handle(frame) is not None
    assert client.handle(frame) is None


def test_event_client_rejects_invalid_event(tmp_path):
    client = AndroidEventClient("token", AndroidStateStore(str(tmp_path / "state.json")))
    with pytest.raises(ValueError):
        client.handle(TransportFrame("EVENT", payload={"sequence": 0, "topic": "x", "payload": {}}))
