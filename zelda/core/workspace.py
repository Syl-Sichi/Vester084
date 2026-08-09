import os
from pathlib import Path


class WorkspacePolicy:
    """Restrict filesystem tools to explicitly configured roots."""

    def __init__(self, roots: list[str] | None = None) -> None:
        configured = roots or [os.getenv("ZELDA_WORKSPACE", str(Path.home() / "ZeldaWorkspace"))]
        self.roots = tuple(Path(root).expanduser().resolve() for root in configured)

    def allows(self, path: str) -> bool:
        candidate = Path(path).expanduser().resolve()
        return any(candidate == root or root in candidate.parents for root in self.roots)
