import pytest

from zelda.control.workspace_executor import WorkspaceExecutor


def test_executor_allows_only_workspace_note_write(monkeypatch):
    calls = []

    def fake_note_write(args):
        calls.append(args)
        return {"written": True}

    monkeypatch.setattr(
        "zelda.control.workspace_executor.UbuntuWorkspaceCapabilities.note_write",
        fake_note_write,
    )

    result = WorkspaceExecutor()("workspace.note.write", ["note.txt", "hello"])
    assert result == {"written": True}
    assert calls == [["note.txt", "hello"]]


def test_executor_rejects_other_capabilities():
    with pytest.raises(PermissionError, match="write_capability_not_allowed"):
        WorkspaceExecutor()("file.delete", ["note.txt"])
