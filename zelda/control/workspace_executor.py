from __future__ import annotations

from zelda.control.ubuntu_workspace import UbuntuWorkspaceCapabilities


WRITE_CAPABILITY = "workspace.note.write"


def execute_workspace_write(capability: str, args: list[str]) -> dict[str, str]:
    if capability != WRITE_CAPABILITY:
        raise PermissionError(f"write_capability_not_allowed:{capability}")
    return UbuntuWorkspaceCapabilities.note_write(args)
