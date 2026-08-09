from zelda.auth.sessions import SessionManager
from zelda.mobile.gateway import MobileGateway
from zelda.mobile.transport import TransportFrame


def test_gateway_requires_scope_and_returns_response():
    sessions = SessionManager()
    token, _ = sessions.create("android", {"command.execute"})
    calls = []
    gateway = MobileGateway(sessions, lambda command: calls.append(command) or {"ok": True})

    gateway.transport.inject(TransportFrame("COMMAND", "r1", {"access_token": token, "command": "ping"}))
    response = gateway.transport.receive()

    assert response.kind == "RESPONSE"
    assert response.request_id == "r1"
    assert calls == ["ping"]


def test_gateway_rejects_missing_token():
    gateway = MobileGateway(SessionManager(), lambda command: {"ok": True})
    gateway.transport.inject(TransportFrame("COMMAND", "r2", {"command": "ping"}))
    assert gateway.transport.receive().payload == {"error": "unauthorized"}
