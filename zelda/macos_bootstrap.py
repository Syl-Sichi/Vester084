"""Fresh macOS installation bootstrap for Z.E.L.D.A.

This module prepares the local runtime and installs the per-user LaunchAgent.
It is intentionally explicit and does not require administrator privileges.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from zelda.macos_service import install_launch_agent

ZELDA_HOME = Path.home() / ".zelda"
WORKSPACE = ZELDA_HOME / "workspace"
LOGS = ZELDA_HOME / "logs"


def prepare_directories() -> None:
    for directory in (ZELDA_HOME, WORKSPACE, LOGS):
        directory.mkdir(parents=True, exist_ok=True)


def write_runtime_metadata() -> Path:
    metadata = ZELDA_HOME / "runtime.json"
    metadata.write_text(
        '{\n'
        '  "platform": "macOS",\n'
        f'  "python": "{sys.executable}",\n'
        f'  "workspace": "{WORKSPACE}"\n'
        '}\n',
        encoding="utf-8",
    )
    return metadata


def install_service() -> Path:
    return install_launch_agent(
        python_executable=sys.executable,
        working_directory=os.getcwd(),
    )


def bootstrap() -> Path:
    if sys.platform != "darwin":
        raise RuntimeError("Z.E.L.D.A. macOS bootstrap requires macOS")
    prepare_directories()
    write_runtime_metadata()
    return install_service()


if __name__ == "__main__":
    print(bootstrap())
