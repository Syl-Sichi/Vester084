import pytest

from zelda.control.confirmation import ConfirmationManager
from zelda.control.write_control import WriteController, WriteRequest


def test_confirmation_creates_pending_request():
    manager = ConfirmationManager()
    pending = manager.request_confirmation(WriteRequest("workspace.note.write", ["note.txt", "hello"]))
    assert pending.token
    assert pending.request.capability == "workspace.note.write"


def test_confirmation_executes_once():
    manager = ConfirmationManager()
    calls = []
    controller = WriteController(lambda capability, args: calls.append((capability, args)) or {"written": True})
    pending = manager.request_confirmation(WriteRequest("workspace.note.write", ["note.txt", "hello"]))

    result = manager.confirm(pending.token, controller)
    assert result["accepted"] is True
    assert calls == [("workspace.note.write", ["note.txt", "hello"])]

    with pytest.raises(ValueError, match="confirmation_not_found"):
        manager.confirm(pending.token, controller)


def test_cancel_removes_pending_request():
    manager = ConfirmationManager()
    pending = manager.request_confirmation(WriteRequest("workspace.note.write", ["note.txt", "hello"]))
    manager.cancel(pending.token)
    with pytest.raises(ValueError, match="confirmation_not_found"):
        manager.confirm(pending.token, WriteController(lambda *_: {"written": True}))
