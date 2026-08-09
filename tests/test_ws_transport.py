import pytest

from zelda.mobile.transport import TransportFrame
from zelda.mobile.ws_transport import WebSocketTransport


class FakeWebSocket:
    def __init__(self):
        self.sent = []
        self.incoming = []
        self.closed = False

    async def send(self, data):
        self.sent.append(data)

    async def recv(self):
        return self.incoming.pop(0)

    async def close(self):
        self.closed = True


@pytest.mark.asyncio
async def test_websocket_transport_round_trip_frame():
    socket = FakeWebSocket()
    transport = WebSocketTransport(socket)
    outgoing = TransportFrame("PING", "r1", {"x": 1})
    await transport.send(outgoing)
    assert TransportFrame.decode(socket.sent[0]) == outgoing

    socket.incoming.append(TransportFrame("PONG", "r1", {}).encode())
    incoming = await transport.receive()
    assert incoming.kind == "PONG"
    assert incoming.request_id == "r1"

    await transport.close()
    assert socket.closed
    assert transport.connected is False
