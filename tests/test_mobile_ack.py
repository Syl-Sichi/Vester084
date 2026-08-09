import pytest

from zelda.mobile.ack import AckTracker


def test_ack_tracker_keeps_highest_ack():
    tracker = AckTracker()
    assert tracker.acknowledge(3) == 3
    assert tracker.acknowledge(2) == 3
    assert tracker.needs_replay(4) is True
    assert tracker.needs_replay(3) is False


def test_ack_tracker_rejects_negative_sequence():
    with pytest.raises(ValueError):
        AckTracker().acknowledge(-1)
