import asyncio
import json

from zelda.auth.sessions import SessionManager
from zelda.control.ai_control import AIControlService
from zelda.control.bootstrap import register_ubuntu_readonly_capabilities
from zelda.control.capabilities import CapabilityRegistry
from zelda.control.policy import CapabilityPolicy
from zelda.mobile.gateway import MobileGateway
from zelda.mobile.ws_gateway import WebSocketGateway


class FakeWebSocket:
    def __init__(self, messages):
        self.messages = iter(messages)
        self.sent = []

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.messages)
        except StopIteration:
            raise StopAsyncIteration

    async def send(self, message):
        self.sent.append(json.loads(message))


def build_gateway():
    sessions = SessionManager()
    registry = CapabilityRegistry()
    register_ubuntu_readonly_capabilities(registry)
    control = AIControlService(registry, CapabilityPolicy.from_registry(registry))
    gateway = MobileGateway(sessions, control.handle)
    token, _ = sessions.create("ws-client", {"command.execute", "health.read"})
    return WebSocketGateway(gateway), token


def test_websocket_requires_hello_before_command():
    gateway, token = build_gateway()
    command = json.dumps({"kind": "COMMAND", "request_id": "1", "payload": {"access_token": token, "command": "show system info"}})
    ws = FakeWebSocket([command])
    asyncio.run(gateway.handle(ws))
    assert ws.sent[0]["kind"] == "ERROR"
    assert ws.sent[0]["payload"]["error"] == "hello_required"


def test_websocket_reaches_control_service_after_hello():
    gateway, token = build_gateway()
    hello = json.dumps({"kind": "HELLO", "request_id": "h", "payload": {"access_token": token, "last_acknowledged": 0}})
    command = json.dumps({"kind": "COMMAND", "request_id": "c", "payload": {"access_token": token, "command": "show system info"}})
    ws = FakeWebSocket([hello, command])
    asyncio.run(gateway.handle(ws))
    assert ws.sent[0]["kind"] == "SYNC"
    assert ws.sent[1]["kind"] == "RESPONSE"
    assert ws.sent[1]["payload"]["result"]["capability"] == "system.info"
