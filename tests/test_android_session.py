from android.session import AndroidSession
from android.state import ConnectionState
from android.storage import AndroidStateStore


def test_session_restores_ack_and_builds_hello(tmp_path):
    path = str(tmp_path / "state.json")
    AndroidStateStore(path).save_last_acknowledged(41)
    session = AndroidSession(AndroidStateStore(path))

    assert session.state.last_acknowledged == 41
    session.begin_connect()
    session.mark_connected()
    frame = session.build_hello("hello-1", "token")
    assert session.state.state == ConnectionState.CONNECTED
    assert frame.kind == "HELLO"
    assert frame.payload["last_acknowledged"] == 41


def test_session_persists_new_ack(tmp_path):
    path = str(tmp_path / "state.json")
    session = AndroidSession(AndroidStateStore(path))
    session.acknowledge(9)
    assert AndroidStateStore(path).load_last_acknowledged() == 9
