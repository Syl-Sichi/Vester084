from zelda.mobile.persistence import MobileStateStore


def test_mobile_ack_state_survives_reopen(tmp_path):
    path = tmp_path / "mobile.db"
    store = MobileStateStore(path)
    assert store.acknowledged("android") == 0
    assert store.acknowledge("android", 12) == 12
    store.close()

    reopened = MobileStateStore(path)
    assert reopened.acknowledged("android") == 12
    assert reopened.acknowledge("android", 7) == 12
    reopened.close()
