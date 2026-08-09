from android.commands import AndroidCommandClient
from android.events import AndroidEventClient
from android.session import AndroidSession
from android.storage import AndroidStateStore
from android.state import ConnectionState
from zelda.mobile.transport import TransportFrame


class AndroidClient:
    """Coordinates Android session, command, and event handling."""

    def __init__(self, access_token: str, state_path: str, on_event=None) -> None:
        self.session = AndroidSession(AndroidStateStore(state_path))
        self.commands = AndroidCommandClient(access_token)
        self.events = AndroidEventClient(access_token, self.session.store, on_event)
        self.access_token = access_token

    @property
    def state(self) -> ConnectionState:
        return self.session.state.state

    def connect(self, request_id: str) -> TransportFrame:
        self.session.begin_connect()
        return self.session.build_hello(request_id, self.access_token)

    def mark_connected(self) -> None:
        self.session.mark_connected()

    def command(self, request_id: str, command: str) -> TransportFrame:
        if self.state != ConnectionState.CONNECTED:
            raise RuntimeError("client is not connected")
        return self.commands.send(request_id, command)

    def handle(self, frame: TransportFrame) -> TransportFrame | None:
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

    def _handle_sync(self, frame: TransportFrame):
        payload = frame.payload or {}
        events = payload.get("events", [])
        for item in events:
            self.handle(TransportFrame("EVENT", payload={
                "sequence": item["sequence"],
                "topic": item["payload"].get("topic", item.get("topic", "")),
                "payload": item["payload"].get("payload", item.get("payload", {})),
                "created_at": item["payload"].get("created_at"),
            }))
        return None
