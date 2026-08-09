import pytest

from zelda.control.ubuntu_workspace import UbuntuWorkspaceCapabilities
from zelda.control.workspace_executor import execute_workspace_write


def test_workspace_executor_dispatches(monkeypatch):
    calls = []

    def fake_write(args):
        calls.append(args)
        return {"written": "true"}

    monkeypatch.setattr(UbuntuWorkspaceCapabilities, "note_write", staticmethod(fake_write))
    assert execute_workspace_write("workspace.note.write", ["note.txt", "hello"]) == {"written": "true"}
    assert calls == [["note.txt", "hello"]]


def test_workspace_executor_rejects_other_capability():
    with pytest.raises(PermissionError, match="write_capability_not_allowed"):
        execute_workspace_write("file.delete", ["note.txt"])
