from android.storage import AndroidStateStore


def test_android_ack_state_survives_restart(tmp_path):
    path = str(tmp_path / "android-state.json")
    store = AndroidStateStore(path)
    assert store.load_last_acknowledged() == 0
    store.save_last_acknowledged(42)

    restarted = AndroidStateStore(path)
    assert restarted.load_last_acknowledged() == 42


def test_android_state_write_is_atomic(tmp_path):
    path = str(tmp_path / "nested" / "state.json")
    store = AndroidStateStore(path)
    store.save_last_acknowledged(7)
    assert store.load_last_acknowledged() == 7
