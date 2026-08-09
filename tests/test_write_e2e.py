from pathlib import Path

from zelda.control.ai_control import AIControlService
from zelda.control.confirmation import ConfirmationManager
from zelda.control.capabilities import CapabilityRegistry
from zelda.control.policy import CapabilityPolicy
from zelda.control.providers import RulesProvider
from zelda.control.ubuntu_workspace import UbuntuWorkspaceCapabilities
from zelda.control.write_control import WriteController
from zelda.control.workspace_executor import WorkspaceExecutor


def test_write_confirmation_to_workspace(monkeypatch, tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    def fake_note_write(args):
        if len(args) < 2:
            raise ValueError("note_arguments_required")
        target = workspace / args[0]
        target.write_text(args[1], encoding="utf-8")
        return {"path": str(target), "bytes": target.stat().st_size}

    monkeypatch.setattr(UbuntuWorkspaceCapabilities, "note_write", staticmethod(fake_note_write))

    registry = CapabilityRegistry()
    policy = CapabilityPolicy.from_registry(registry)
    controller = WriteController(WorkspaceExecutor())
    service = AIControlService(
        registry,
        policy,
        provider=RulesProvider(),
        write_controller=controller,
        confirmation_manager=ConfirmationManager(),
    )

    pending = service.request_write("workspace.note.write", ["hello.txt", "Hello Z.E.L.D.A."])
    assert pending["confirmation_required"] is True
    assert not (workspace / "hello.txt").exists()

    result = service.confirm_write(pending["confirmation_token"])
    assert result["accepted"] is True
    assert (workspace / "hello.txt").read_text(encoding="utf-8") == "Hello Z.E.L.D.A."
