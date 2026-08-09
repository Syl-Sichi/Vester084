from __future__ import annotations

import subprocess


class MacOSProcessCapabilities:
    """Read only discovery of running macOS processes."""

    @staticmethod
    def processes_read(args: list[str]) -> list[dict[str, object]]:
        result = subprocess.run(
            ["/bin/ps", "-axo", "pid=,comm="],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return []
        processes: list[dict[str, object]] = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                continue
            try:
                pid = int(parts[0])
            except ValueError:
                continue
            processes.append({"pid": pid, "name": parts[1]})
        return processes
