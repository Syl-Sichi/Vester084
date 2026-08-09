from __future__ import annotations

import os
from typing import Any


class UbuntuProcessCapabilities:
    """Read only process inspection using /proc on Linux."""

    @staticmethod
    def processes_read(args: list[str]) -> list[dict[str, Any]]:
        processes: list[dict[str, Any]] = []
        proc = "/proc"
        try:
            entries = os.listdir(proc)
        except OSError:
            return processes

        for entry in entries:
            if not entry.isdigit():
                continue
            pid = int(entry)
            try:
                with open(os.path.join(proc, entry, "comm"), "r", encoding="utf-8") as handle:
                    name = handle.read().strip()
                processes.append({"pid": pid, "name": name})
            except (OSError, UnicodeDecodeError):
                continue

        return sorted(processes, key=lambda item: item["pid"])
