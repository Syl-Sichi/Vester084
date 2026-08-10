"""One-command macOS installation orchestration for Z.E.L.D.A."""
from __future__ import annotations

import platform
import time
import urllib.error
import urllib.request

from zelda.macos_bootstrap import bootstrap

HEALTH_URL = "http://127.0.0.1:8765/health"


def verify_service(timeout: float = 5.0, interval: float = 0.25) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(HEALTH_URL, timeout=1) as response:
                return response.status == 200
        except (OSError, urllib.error.URLError):
            time.sleep(interval)
    return False


def install() -> dict[str, object]:
    if platform.system() != "Darwin":
        raise RuntimeError("Z.E.L.D.A. macOS installer requires macOS")

    plist = bootstrap()
    healthy = verify_service()
    return {
        "status": "ready" if healthy else "service_start_pending",
        "launch_agent": str(plist),
        "health_url": HEALTH_URL,
    }


if __name__ == "__main__":
    result = install()
    print(f"Z.E.L.D.A.: {result['status']}")
    print(f"LaunchAgent: {result['launch_agent']}")
