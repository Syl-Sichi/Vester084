from android.protocol import AndroidHello
from android.state import AndroidConnectionState, ConnectionState
from android.storage import AndroidStateStore


class AndroidSession:
    """Coordinates persisted client state with connection and sync handshakes."""

    def __init__(self, state_store: AndroidStateStore) -> None:
        self.store = state_store
        self.state = AndroidConnectionState()
        self.state.acknowledge(self.store.load_last_acknowledged())

    def begin_connect(self) -> None:
        if self.state.state == ConnectionState.DISCONNECTED:
            self.state.transition(ConnectionState.CONNECTING)
        elif self.state.state == ConnectionState.CONNECTED:
            return
        else:
            self.state.transition(ConnectionState.RECONNECTING)

    def mark_connected(self) -> None:
        self.state.transition(ConnectionState.CONNECTED)

    def build_hello(self, request_id: str, access_token: str):
        return AndroidHello(
            request_id=request_id,
            access_token=access_token,
            last_acknowledged=self.state.last_acknowledged,
        ).frame()

    def acknowledge(self, sequence: int) -> None:
        self.state.acknowledge(sequence)
        self.store.save_last_acknowledged(self.state.last_acknowledged)

    def disconnect(self) -> None:
        if self.state.state != ConnectionState.CLOSED:
            self.state.transition(ConnectionState.RECONNECTING)
