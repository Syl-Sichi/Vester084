from zelda.mobile.replay import ReplayBuffer
from zelda.mobile.transport import TransportFrame


def test_replay_buffer_returns_events_after_sequence():
    buffer = ReplayBuffer(3)
    buffer.add(TransportFrame("EVENT", payload={"n": 1}))
    buffer.add(TransportFrame("EVENT", payload={"n": 2}))
    buffer.add(TransportFrame("EVENT", payload={"n": 3}))
    assert [item.sequence for item in buffer.after(1)] == [2, 3]
    assert buffer.latest_sequence == 3


def test_replay_buffer_is_bounded():
    buffer = ReplayBuffer(2)
    buffer.add(TransportFrame("EVENT", payload={"n": 1}))
    buffer.add(TransportFrame("EVENT", payload={"n": 2}))
    buffer.add(TransportFrame("EVENT", payload={"n": 3}))
    assert buffer.oldest_sequence() == 2
    assert [item.sequence for item in buffer.after(0)] == [2, 3]
