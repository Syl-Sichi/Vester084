from __future__ import annotations

from pathlib import Path


class MacOSWorkspaceCapabilities:
    """Constrained workspace writes for macOS."""

    @staticmethod
    def note_write(args: list[str]) -> dict[str, str]:
        if len(args) < 2:
            raise ValueError("note_write_requires_name_and_content")
        name, content = args[0], args[1]
        root = Path.home() / ".zelda" / "workspace"
        root.mkdir(parents=True, exist_ok=True)
        target = (root / name).resolve()
        if root.resolve() not in target.parents:
            raise ValueError("workspace_path_escape")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {"path": str(target), "bytes": str(len(content.encode("utf-8")))}
