from zelda.mobile.durable_delivery import DurableMobileDelivery
from zelda.mobile.journal import MobileEventJournal
from zelda.mobile.sync import MobileSyncProtocol
from zelda.mobile.transport import TransportFrame


def test_sync_returns_events_after_client_ack(tmp_path):
    journal = MobileEventJournal(str(tmp_path / "sync.db"), max_items=10)
    delivery = DurableMobileDelivery(journal)
    first = delivery.record(TransportFrame("EVENT", payload={"n": 1}))
    second = delivery.record(TransportFrame("EVENT", payload={"n": 2}))

    sync = MobileSyncProtocol(delivery)
    result = sync.hello(first.sequence)

    assert result.acknowledged == first.sequence
    assert [item.frame.payload["n"] for item in result.replay] == [2]
    sync.ack(second.sequence)
    assert delivery.replay() == []
    journal.close()
