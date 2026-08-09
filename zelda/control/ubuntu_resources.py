from __future__ import annotations

import shutil
from pathlib import Path


class UbuntuResourceCapabilities:
    """Read only host resource inspection."""

    @staticmethod
    def memory_read(args: list[str]) -> dict[str, int]:
        meminfo = Path("/proc/meminfo")
        values: dict[str, int] = {}
        if meminfo.exists():
            for line in meminfo.read_text(encoding="utf-8").splitlines():
                key, _, value = line.partition(":")
                if key in {"MemTotal", "MemAvailable", "SwapTotal", "SwapFree"}:
                    parts = value.strip().split()
                    if parts and parts[0].isdigit():
                        values[key] = int(parts[0]) * (1024 if len(parts) > 1 and parts[1] == "kB" else 1)
        return values

    @staticmethod
    def disk_read(args: list[str]) -> dict[str, int]:
        path = Path(args[0]).expanduser() if args else Path("/")
        usage = shutil.disk_usage(path)
        return {"total": usage.total, "used": usage.used, "free": usage.free}
