import json

import pytest

from zelda.mobile.gateway import MobileGateway
from zelda.mobile.transport import TransportFrame
from zelda.mobile.ws_gateway import WebSocketGateway


class FakeWebSocket:
    def __init__(self, messages):
        self.messages = messages
        self.sent = []

    def __aiter__(self):
        self._iterator = iter(self.messages)
        return self

    async def __anext__(self):
        try:
            return next(self._iterator)
        except StopIteration:
            raise StopAsyncIteration

    async def send(self, message):
        self.sent.append(message)


class Sessions:
    def validate(self, token, scope):
        return {"token": token, "scope": scope} if token == "valid" else None


@pytest.mark.asyncio
async def test_websocket_gateway_routes_ping():
    gateway = MobileGateway(Sessions(), lambda command: {"result": command})
    ws = FakeWebSocket([TransportFrame("PING", "p1").to_json()])
    await WebSocketGateway(gateway).handle(ws)
    response = json.loads(ws.sent[0])
    assert response["kind"] == "PONG"
    assert response["request_id"] == "p1"
