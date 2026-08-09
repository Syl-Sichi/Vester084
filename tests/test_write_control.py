import pytest

from zelda.control.write_control import WriteController, WriteRequest
from zelda.control.write_policy import WriteAuthorization


def test_write_requires_authorization():
    controller = WriteController(lambda capability, args: {"ok": True})
    with pytest.raises(PermissionError, match="write_confirmation_required"):
        controller.execute(WriteRequest("workspace.note.write", ["note.txt", "hello"]))


def test_write_rejects_wrong_capability():
    controller = WriteController(lambda capability, args: {"ok": True})
    authorization = WriteAuthorization("file.create", confirmed=True)
    with pytest.raises(PermissionError, match="write_confirmation_required"):
        controller.execute(
            WriteRequest("workspace.note.write", ["note.txt", "hello"]),
            authorization,
        )


def test_write_executes_after_explicit_confirmation():
    calls = []

    def executor(capability, args):
        calls.append((capability, args))
        return {"written": True}

    controller = WriteController(executor)
    request = WriteRequest("workspace.note.write", ["note.txt", "hello"])
    authorization = WriteAuthorization("workspace.note.write", confirmed=True)

    result = controller.execute(request, authorization)

    assert result["accepted"] is True
    assert result["capability"] == "workspace.note.write"
    assert calls == [("workspace.note.write", ["note.txt", "hello"])]
