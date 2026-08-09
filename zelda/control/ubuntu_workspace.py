from __future__ import annotations

from pathlib import Path


class UbuntuWorkspaceCapabilities:
    """Controlled writes inside Z.E.L.D.A.'s private workspace only."""

    @staticmethod
    def note_write(args: list[str]) -> dict[str, str]:
        if len(args) < 2:
            raise ValueError("note_path_and_content_required")

        relative_path = Path(args[0])
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise PermissionError("workspace_path_not_allowed")

        content = args[1]
        workspace = (Path.home() / ".zelda" / "workspace").resolve()
        target = (workspace / relative_path).resolve()

        if workspace not in target.parents:
            raise PermissionError("workspace_path_not_allowed")

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {"path": str(target), "written": "true"}
