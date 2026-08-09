from zelda.auth.sessions import SessionManager
from zelda.mobile.durable_delivery import DurableMobileDelivery
from zelda.mobile.gateway import MobileGateway
from zelda.mobile.journal import MobileEventJournal
from zelda.mobile.transport import TransportFrame


def test_gateway_handles_hello_and_ack(tmp_path):
    sessions = SessionManager()
    token, _ = sessions.create("android", {"health.read", "command.execute"})
    journal = MobileEventJournal(str(tmp_path / "gateway.db"), max_items=10)
    delivery = DurableMobileDelivery(journal)
    event = delivery.record(TransportFrame("EVENT", payload={"n": 1}))
    gateway = MobileGateway(sessions, lambda command: {"ok": True}, delivery)

    gateway.transport.inject(TransportFrame("HELLO", "hello-1", {
        "access_token": token,
        "last_acknowledged": 0,
    }))
    sync = gateway.transport.receive()
    assert sync.kind == "SYNC"
    assert sync.payload["events"][0]["sequence"] == event.sequence

    gateway.transport.inject(TransportFrame("ACK", "ack-1", {
        "access_token": token,
        "sequence": event.sequence,
    }))
    ack = gateway.transport.receive()
    assert ack.payload["acknowledged"] == event.sequence
    assert delivery.replay() == []
    journal.close()
