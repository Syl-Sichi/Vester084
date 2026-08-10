"""macOS user service integration for the local Z.E.L.D.A. bridge."""
from __future__ import annotations

import os
import plistlib
import subprocess
from pathlib import Path

LABEL = "com.zelda.control.service"
PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"


def build_launch_agent(python_executable: str, working_directory: str) -> dict:
    return {
        "Label": LABEL,
        "ProgramArguments": [python_executable, "-m", "zelda.http_bridge"],
        "WorkingDirectory": working_directory,
        "RunAtLoad": True,
        "KeepAlive": True,
        "StandardOutPath": str(Path.home() / ".zelda" / "logs" / "service.out.log"),
        "StandardErrorPath": str(Path.home() / ".zelda" / "logs" / "service.err.log"),
    }


def install_launch_agent(
    python_executable: str | None = None,
    working_directory: str | None = None,
) -> Path:
    python_executable = python_executable or os.sys.executable
    working_directory = working_directory or str(Path.cwd())

    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    log_dir = Path.home() / ".zelda" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    with PLIST_PATH.open("wb") as handle:
        plistlib.dump(build_launch_agent(python_executable, working_directory), handle)

    subprocess.run(["launchctl", "load", str(PLIST_PATH)], check=False)
    return PLIST_PATH


def remove_launch_agent() -> None:
    subprocess.run(["launchctl", "unload", str(PLIST_PATH)], check=False)
    PLIST_PATH.unlink(missing_ok=True)
