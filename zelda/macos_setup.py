"""User facing macOS setup command for Z.E.L.D.A."""
from __future__ import annotations

import platform

from zelda.macos_install import install


def setup() -> dict[str, object]:
    """Run the complete first installation flow on macOS."""
    if platform.system() != "Darwin":
        raise RuntimeError("Z.E.L.D.A. setup requires macOS")
    return install()


def main() -> int:
    print("Z.E.L.D.A. macOS setup")
    print("Preparing your local installation...")
    try:
        result = setup()
    except Exception as exc:
        print(f"Setup failed: {exc}")
        return 1
    print(f"Status: {result['status']}")
    print(f"LaunchAgent: {result['launch_agent']}")
    print("Z.E.L.D.A. setup complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
