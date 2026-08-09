from __future__ import annotations

from zelda.setup_wizard import run_setup


def first_run_onboarding() -> dict[str, str]:
    print("Welcome to Z.E.L.D.A.")
    print("Preparing your first run environment...")

    config = run_setup()

    print(f"Platform detected: {config['platform']}")
    print("Workspace created.")
    print("Z.E.L.D.A. is ready.")

    return config
