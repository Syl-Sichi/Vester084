from zelda.mobile.durable_delivery import DurableMobileDelivery
from zelda.mobile.journal import MobileEventJournal
from zelda.mobile.transport import TransportFrame


def test_pending_events_follow_ack_position(tmp_path):
    journal = MobileEventJournal(str(tmp_path / "events.db"), max_items=10)
    delivery = DurableMobileDelivery(journal)
    first = delivery.record(TransportFrame("EVENT", payload={"n": 1}))
    second = delivery.record(TransportFrame("EVENT", payload={"n": 2}))

    assert [frame.payload["n"] for frame in delivery.replay()] == [1, 2]
    delivery.acknowledge(first.sequence)
    assert [frame.payload["n"] for frame in delivery.replay()] == [2]
    delivery.acknowledge(second.sequence)
    assert delivery.replay() == []
    journal.close()
