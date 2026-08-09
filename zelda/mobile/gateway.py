from zelda.auth.sessions import SessionManager
from zelda.mobile.durable_delivery import DurableMobileDelivery
from zelda.mobile.sync import MobileSyncProtocol
from zelda.mobile.transport import LocalTransport, TransportFrame


class MobileGateway:
    """Bridge mobile transport frames to authenticated Z.E.L.D.A. operations."""

    def __init__(self, sessions: SessionManager, command_handler, delivery: DurableMobileDelivery | None = None) -> None:
        self.sessions = sessions
        self.command_handler = command_handler
        self.transport = LocalTransport()
        self.delivery = delivery
        self.sync = MobileSyncProtocol(delivery) if delivery else None
        self.transport.on_frame(self._handle)

    def _handle(self, frame: TransportFrame) -> None:
        if frame.kind == "PING":
            self.transport.send(TransportFrame("PONG", frame.request_id))
            return
        if frame.kind == "HELLO":
            self._hello(frame)
            return
        if frame.kind == "ACK":
            self._ack(frame)
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

        try:
            result = self.command_handler(command.strip())
            self.transport.send(TransportFrame("RESPONSE", frame.request_id, {"result": result}))
        except Exception as exc:
            self.transport.send(TransportFrame("ERROR", frame.request_id, {"error": "command_failed", "detail": str(exc)}))

    def _hello(self, frame: TransportFrame) -> None:
        if self.sync is None:
            self.transport.send(TransportFrame("ERROR", frame.request_id, {"error": "sync_unavailable"}))
            return
        payload = frame.payload or {}
        token = payload.get("access_token")
        if not isinstance(token, str) or self.sessions.validate(token, "health.read") is None:
            self.transport.send(TransportFrame("ERROR", frame.request_id, {"error": "unauthorized"}))
            return
        last_ack = payload.get("last_acknowledged", 0)
        if not isinstance(last_ack, int) or last_ack < 0:
            self.transport.send(TransportFrame("ERROR", frame.request_id, {"error": "invalid_ack"}))
            return
        result = self.sync.hello(last_ack)
        self.transport.send(TransportFrame("SYNC", frame.request_id, {
            "acknowledged": result.acknowledged,
            "events": [
                {"sequence": item.sequence, "kind": item.frame.kind, "request_id": item.frame.request_id, "payload": item.frame.payload or {}}
                for item in result.replay
            ],
        }))

    def _ack(self, frame: TransportFrame) -> None:
        if self.sync is None:
            self.transport.send(TransportFrame("ERROR", frame.request_id, {"error": "sync_unavailable"}))
            return
        payload = frame.payload or {}
        token = payload.get("access_token")
        if not isinstance(token, str) or self.sessions.validate(token, "health.read") is None:
            self.transport.send(TransportFrame("ERROR", frame.request_id, {"error": "unauthorized"}))
            return
        sequence = payload.get("sequence")
        if not isinstance(sequence, int) or sequence < 0:
            self.transport.send(TransportFrame("ERROR", frame.request_id, {"error": "invalid_sequence"}))
            return
        acknowledged = self.sync.ack(sequence)
        self.transport.send(TransportFrame("RESPONSE", frame.request_id, {"acknowledged": acknowledged}))
