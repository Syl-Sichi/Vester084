import pytest

from zelda.mobile.delivery import MobileDeliveryQueue
from zelda.mobile.transport import TransportFrame


def test_delivery_queue_assigns_monotonic_sequences():
    queue = MobileDeliveryQueue(2)
    first = queue.enqueue(TransportFrame("EVENT", payload={"n": 1}))
    second = queue.enqueue(TransportFrame("EVENT", payload={"n": 2}))
    assert first.sequence == 1
    assert second.sequence == 2
    assert queue.next().sequence == 1


def test_delivery_queue_is_bounded():
    queue = MobileDeliveryQueue(1)
    queue.enqueue(TransportFrame("EVENT"))
    with pytest.raises(Exception):
        queue.enqueue(TransportFrame("EVENT"))
