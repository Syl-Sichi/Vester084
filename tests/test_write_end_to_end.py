from pathlib import Path

from zelda.control.ai_control import AIControlService
from zelda.control.capabilities import CapabilityRegistry
from zelda.control.confirmation import ConfirmationManager
from zelda.control.policy import CapabilityPolicy
from zelda.control.workspace_executor import WorkspaceExecutor
from zelda.control.write_control import WriteController
from zelda.control.write_policy import WriteAuthorization


def test_workspace_write_end_to_end(tmp_path, monkeypatch):
    monkeypatch.setattr("zelda.control.ubuntu_workspace.Path.home", lambda: tmp_path)

    registry = CapabilityRegistry()
    policy = CapabilityPolicy({"workspace.note.write"})
    controller = WriteController(WorkspaceExecutor())
    service = AIControlService(
        registry,
        policy,
        write_controller=controller,
        confirmation_manager=ConfirmationManager(),
    )

    pending = service.request_write("workspace.note.write", ["hello.txt", "Hello Z.E.L.D.A."])
    assert pending["confirmation_required"] is True

    result = service.confirm_write(pending["confirmation_token"])
    assert result["accepted"] is True
    assert (tmp_path / ".zelda" / "workspace" / "hello.txt").read_text(encoding="utf-8") == "Hello Z.E.L.D.A."
