import pytest

from zelda.daemon_server import DaemonConfig
from zelda.network_runtime import NetworkRuntime


class FakeServer:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True

    async def wait_closed(self):
        return None


@pytest.mark.asyncio
async def test_network_runtime_assembles_gateway_and_server():
    calls = []
    server = FakeServer()

    async def serve(handler, host, port):
        calls.append((handler, host, port))
        return server

    runtime = NetworkRuntime(lambda command: {"command": command}, DaemonConfig("127.0.0.1", 9001))
    await runtime.start(serve)
    assert runtime.server.running is True
    assert calls[0][1:] == ("127.0.0.1", 9001)
    assert calls[0][0] == runtime.websocket_gateway.handle

    await runtime.stop()
    assert server.closed is True
    assert runtime.server.running is False
