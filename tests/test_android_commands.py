import pytest

from android.commands import AndroidCommandClient
from zelda.mobile.transport import TransportFrame


def test_command_client_correlates_response():
    client = AndroidCommandClient("token")
    frame = client.send("req-1", "status")
    assert frame.kind == "COMMAND"
    assert client.pending_count == 1

    result = client.resolve(TransportFrame("RESPONSE", "req-1", {"result": {"ok": True}}))
    assert result == {"ok": True}
    assert client.pending_count == 0


def test_command_client_rejects_duplicate_request_id():
    client = AndroidCommandClient("token")
    client.send("req-1", "status")
    with pytest.raises(ValueError):
        client.send("req-1", "again")


def test_command_client_surfaces_error_response():
    client = AndroidCommandClient("token")
    client.send("req-2", "status")
    with pytest.raises(RuntimeError, match="denied"):
        client.resolve(TransportFrame("RESPONSE", "req-2", {"error": "denied"}))
