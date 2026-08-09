from zelda.mobile.connection import ConnectionConfig, ConnectionState, MobileConnection


def test_mobile_connection_reconnects_with_backoff():
    connection = MobileConnection(ConnectionConfig(reconnect_initial_seconds=1, reconnect_max_seconds=4))
    connection.begin()
    assert connection.state == ConnectionState.CONNECTING
    connection.connected()
    assert connection.state == ConnectionState.CONNECTED
    assert connection.failed() == 1
    assert connection.failed() == 2
    assert connection.failed() == 4


def test_closed_connection_cannot_restart():
    connection = MobileConnection()
    connection.close()
    try:
        connection.begin()
    except RuntimeError:
        pass
    else:
        raise AssertionError("closed connection should not restart")
