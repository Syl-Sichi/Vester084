import pytest

from zelda.daemon_server import DaemonConfig, DaemonServer


def test_daemon_config_from_env():
    config = DaemonConfig.from_env({"ZELDA_HOST": "0.0.0.0", "ZELDA_PORT": "9000"})
    assert config.host == "0.0.0.0"
    assert config.port == 9000


def test_daemon_config_rejects_invalid_port():
    with pytest.raises(ValueError):
        DaemonConfig.from_env({"ZELDA_PORT": "nope"})
    with pytest.raises(ValueError):
        DaemonConfig.from_env({"ZELDA_PORT": "70000"})


@pytest.mark.asyncio
async def test_daemon_server_lifecycle():
    class FakeServer:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

        async def wait_closed(self):
            return None

    server = FakeServer()

    async def serve(handler, host, port):
        assert host == "127.0.0.1"
        assert port == 8765
        assert callable(handler)
        return server

    gateway = type("Gateway", (), {"handle": lambda self, websocket: None})()
    daemon = DaemonServer(DaemonConfig(), gateway)
    await daemon.start(serve)
    assert daemon.running is True
    await daemon.stop()
    assert daemon.running is False
    assert server.closed is True
