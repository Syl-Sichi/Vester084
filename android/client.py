from android.commands import AndroidCommandClient
from android.events import AndroidEventClient
from android.session import AndroidSession
from android.storage import AndroidStateStore
from android.state import ConnectionState
from android.transport import FrameTransport
from zelda.mobile.transport import TransportFrame


class AndroidClient:
    """Coordinates Android session, commands, events, and frame transport."""

    def __init__(self, access_token: str, state_path: str, transport: FrameTransport, on_event=None) -> None:
        self.session = AndroidSession(AndroidStateStore(state_path))
        self.commands = AndroidCommandClient(access_token)
        self.events = AndroidEventClient(access_token, self.session.store, on_event)
        self.access_token = access_token
        self.transport = transport

    @property
    def state(self) -> ConnectionState:
        return self.session.state.state

    def connect(self, request_id: str) -> None:
        self.transport.connect()
        self.session.begin_connect()
        self.transport.send(self.session.build_hello(request_id, self.access_token))

    def mark_connected(self) -> None:
        self.session.mark_connected()

    def command(self, request_id: str, command: str) -> None:
        if self.state != ConnectionState.CONNECTED:
            raise RuntimeError("client is not connected")
        self.transport.send(self.commands.send(request_id, command))

    def poll_once(self) -> TransportFrame | object | None:
        frame = self.transport.receive()
        if frame is None:
            return None
        result = self.handle(frame)
        if isinstance(result, TransportFrame):
            self.transport.send(result)
        return result

    def handle(self, frame: TransportFrame) -> TransportFrame | object | None:
        if frame.kind == "EVENT":
            ack = self.events.handle(frame)
            if ack is not None:
                self.session.acknowledge(self.events.last_acknowledged)
            return ack
        if frame.kind == "RESPONSE":
            return self.commands.resolve(frame)
        if frame.kind == "SYNC":
            return self._handle_sync(frame)
        if frame.kind == "PONG":
            return None
        if frame.kind == "ERROR":
            raise RuntimeError((frame.payload or {}).get("error", "unknown_error"))
        raise ValueError(f"unsupported frame: {frame.kind}")

    def _handle_sync(self, frame: TransportFrame) -> None:
        payload = frame.payload or {}
        events = payload.get("events", [])
        if not isinstance(events, list):
            raise ValueError("invalid sync events")
        for item in events:
            if not isinstance(item, dict):
                raise ValueError("invalid sync event")
            event_payload = item.get("payload", {})
            if not isinstance(event_payload, dict):
                raise ValueError("invalid sync event payload")
            self.handle(TransportFrame("EVENT", payload={
                "sequence": item["sequence"],
                "topic": event_payload.get("topic", item.get("topic", "")),
                "payload": event_payload.get("payload", item.get("payload", {})),
                "created_at": event_payload.get("created_at"),
            }))
