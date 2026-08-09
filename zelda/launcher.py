from __future__ import annotations

import platform

from zelda.onboarding import first_run_onboarding
from zelda.setup_wizard import needs_setup


def startup_message() -> str:
    host = platform.system()
    if host == "Darwin":
        return "Z.E.L.D.A. starting on macOS"
    if host == "Linux":
        return "Z.E.L.D.A. starting on Linux"
    return f"Z.E.L.D.A. starting on {host}"


def launch() -> None:
    print(startup_message())

    if needs_setup():
        first_run_onboarding()

    from zelda.cli import main
    main()


if __name__ == "__main__":
    launch()
