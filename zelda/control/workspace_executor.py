from __future__ import annotations

from zelda.control.ubuntu_workspace import UbuntuWorkspaceCapabilities


class WorkspaceExecutor:
    """Allow only explicitly approved workspace write capabilities."""

    _allowed = {"workspace.note.write"}

    def __call__(self, capability: str, args: list[str]) -> dict[str, object]:
        if capability not in self._allowed:
            raise PermissionError("write_capability_not_allowed")
        if capability == "workspace.note.write":
            return UbuntuWorkspaceCapabilities.note_write(args)
        raise PermissionError("write_capability_not_allowed")
