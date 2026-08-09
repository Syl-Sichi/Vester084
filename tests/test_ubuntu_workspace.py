from pathlib import Path

import pytest

from zelda.control.ubuntu_workspace import UbuntuWorkspaceCapabilities
from zelda.control.write_policy import WriteAuthorization


def test_note_write_stays_inside_private_workspace(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    result = UbuntuWorkspaceCapabilities.note_write(["notes/hello.txt", "hello Z.E.L.D.A."])
    target = tmp_path / ".zelda" / "workspace" / "notes" / "hello.txt"

    assert target.read_text(encoding="utf-8") == "hello Z.E.L.D.A."
    assert result == {"path": str(target.resolve()), "written": "true"}


def test_note_write_rejects_path_escape(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    with pytest.raises(PermissionError, match="workspace_path_not_allowed"):
        UbuntuWorkspaceCapabilities.note_write(["../outside.txt", "blocked"])


def test_write_authorization_requires_explicit_confirmation():
    with pytest.raises(PermissionError, match="write_confirmation_required"):
        WriteAuthorization("workspace.note.write").require_confirmation("workspace.note.write")

    WriteAuthorization("workspace.note.write", confirmed=True).require_confirmation("workspace.note.write")
