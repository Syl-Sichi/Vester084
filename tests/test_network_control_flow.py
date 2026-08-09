from zelda.auth.sessions import SessionManager
from zelda.control.ai_control import AIControlService
from zelda.control.bootstrap import register_ubuntu_readonly_capabilities
from zelda.control.capabilities import CapabilityRegistry
from zelda.control.policy import CapabilityPolicy
from zelda.mobile.gateway import MobileGateway
from zelda.mobile.transport import TransportFrame


def build_gateway():
    sessions = SessionManager()
    registry = CapabilityRegistry()
    register_ubuntu_readonly_capabilities(registry)
    control = AIControlService(registry, CapabilityPolicy.from_registry(registry))
    gateway = MobileGateway(sessions, control.handle)
    token, session = sessions.create("test-client", {"command.execute", "health.read"})
    return gateway, token, session


def test_authenticated_command_returns_capability_result():
    gateway, token, session = build_gateway()
    frame = TransportFrame("COMMAND", "req-1", {"access_token": token, "command": "show system info"})
    gateway.transport.inject(frame)
    response = gateway.transport.receive(timeout=1)
    assert response.kind == "RESPONSE"
    assert response.request_id == "req-1"
    assert response.payload["result"]["accepted"] is True
    assert response.payload["result"]["capability"] == "system.info"


def test_unauthenticated_command_is_rejected():
    gateway, _, _ = build_gateway()
    frame = TransportFrame("COMMAND", "req-2", {"access_token": "invalid", "command": "show system info"})
    gateway.transport.inject(frame)
    response = gateway.transport.receive(timeout=1)
    assert response.kind == "ERROR"
    assert response.request_id == "req-2"
    assert response.payload["error"] == "unauthorized"
