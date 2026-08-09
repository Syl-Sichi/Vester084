from zelda.auth.sessions import SessionManager
from zelda.mobile.transport import LocalTransport, TransportFrame


class MobileGateway:
    """Bridge mobile transport frames to authenticated Z.E.L.D.A. operations."""

    def __init__(self, sessions: SessionManager, command_handler) -> None:
        self.sessions = sessions
        self.command_handler = command_handler
        self.transport = LocalTransport()
        self.transport.on_frame(self._handle)

    def _handle(self, frame: TransportFrame) -> None:
        if frame.kind == "PING":
            self.transport.send(TransportFrame("PONG", frame.request_id))
            return
        if frame.kind != "COMMAND":
            self.transport.send(TransportFrame("ERROR", frame.request_id, {"error": "unsupported_frame"}))
            return

        payload = frame.payload or {}
        token = payload.get("access_token")
        if not isinstance(token, str):
            self.transport.send(TransportFrame("ERROR", frame.request_id, {"error": "unauthorized"}))
            return
        if self.sessions.validate(token, "command.execute") is None:
            self.transport.send(TransportFrame("ERROR", frame.request_id, {"error": "unauthorized"}))
            return

        command = payload.get("command")
        if not isinstance(command, str) or not command.strip():
            self.transport.send(TransportFrame("ERROR", frame.request_id, {"error": "command_required"}))
            return

        result = self.command_handler(command.strip())
        self.transport.send(TransportFrame("RESPONSE", frame.request_id, {"result": result}))
