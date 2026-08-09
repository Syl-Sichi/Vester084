from android.client import AndroidClient
from android.state import ConnectionState
from zelda.mobile.transport import TransportFrame


def test_android_client_connects_and_sends_command(tmp_path):
    client = AndroidClient("token", str(tmp_path / "state.json"))
    hello = client.connect("hello-1")
    assert hello.kind == "HELLO"
    assert hello.payload["last_acknowledged"] == 0

    client.mark_connected()
    assert client.state == ConnectionState.CONNECTED
    command = client.command("cmd-1", "status")
    assert command.kind == "COMMAND"
    assert command.payload["command"] == "status"


def test_android_client_handles_event(tmp_path):
    received = []
    client = AndroidClient("token", str(tmp_path / "state.json"), received.append)
    client.connect("hello-1")
    client.mark_connected()
    ack = client.handle(TransportFrame("EVENT", payload={
        "sequence": 1,
        "topic": "task.completed",
        "payload": {"task_id": "abc"},
    }))
    assert received[0].payload["task_id"] == "abc"
    assert ack.kind == "ACK"
    assert ack.payload["sequence"] == 1
