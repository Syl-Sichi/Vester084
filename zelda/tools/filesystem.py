from pathlib import Path
from typing import Any

from zelda.core.models import ExecutionResult
from zelda.tools.base import Tool


class FilesystemListTool(Tool):
    name = "filesystem.list"
    description = "List entries in a permitted directory without modifying files."

    def execute(self, arguments: dict[str, Any]) -> ExecutionResult:
        raw_path = str(arguments.get("path", "."))
        path = Path(raw_path).expanduser().resolve()
        if not path.exists():
            return ExecutionResult(False, "Directory does not exist.")
        if not path.is_dir():
            return ExecutionResult(False, "Path is not a directory.")

        entries = [
            {"name": item.name, "type": "directory" if item.is_dir() else "file"}
            for item in sorted(path.iterdir(), key=lambda p: p.name.lower())
        ]
        return ExecutionResult(True, f"Found {len(entries)} entries.", {"path": str(path), "entries": entries})


class FilesystemReadTool(Tool):
    name = "filesystem.read"
    description = "Read a UTF 8 text file within the permitted workspace."

    def execute(self, arguments: dict[str, Any]) -> ExecutionResult:
        raw_path = str(arguments.get("path", ""))
        if not raw_path:
            return ExecutionResult(False, "A file path is required.")
        path = Path(raw_path).expanduser().resolve()
        if not path.exists() or not path.is_file():
            return ExecutionResult(False, "File does not exist.")
        if path.stat().st_size > 1_000_000:
            return ExecutionResult(False, "File is larger than the safe read limit.")
        try:
            content = path.read_text(encoding="utf 8")
        except UnicodeDecodeError:
            return ExecutionResult(False, "File is not valid UTF 8 text.")
        return ExecutionResult(True, "File read successfully.", {"path": str(path), "content": content})
