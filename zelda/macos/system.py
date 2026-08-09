from __future__ import annotations

import platform
import subprocess


class MacOSSystemCapabilities:
    """Read only macOS host inspection."""

    @staticmethod
    def system_info(args: list[str]) -> dict[str, str]:
        return {
            "platform": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        }

    @staticmethod
    def app_list(args: list[str]) -> list[str]:
        result = subprocess.run(
            ["/usr/bin/find", "/Applications", "-maxdepth", "1", "-type", "d", "-name", "*.app"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return []
        return sorted(
            [line.rsplit("/", 1)[-1][:-4] for line in result.stdout.splitlines() if line.endswith(".app")],
            key=str.casefold,
        )
