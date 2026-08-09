from __future__ import annotations

import platform


def current_platform() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "linux":
        return "linux"
    if system == "windows":
        return "windows"
    return "unknown"


def is_macos() -> bool:
    return current_platform() == "macos"
