import pytest

from android.state import AndroidConnectionState, ConnectionState


def test_android_connection_state_and_ack():
    state = AndroidConnectionState()
    assert state.state == ConnectionState.DISCONNECTED
    state.transition(ConnectionState.CONNECTING)
    state.transition(ConnectionState.CONNECTED)
    state.acknowledge(12)
    state.acknowledge(8)
    assert state.last_acknowledged == 12


def test_closed_android_connection_cannot_restart():
    state = AndroidConnectionState()
    state.transition(ConnectionState.CLOSED)
    with pytest.raises(RuntimeError):
        state.transition(ConnectionState.CONNECTING)
