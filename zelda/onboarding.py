from __future__ import annotations

import json
from pathlib import Path

from zelda.platform import current_platform
from zelda.setup_wizard import run_setup


CONFIG_FILE = Path.home() / ".zelda" / "config.json"


def first_run_onboarding() -> dict[str, str]:
    print("Welcome to Z.E.L.D.A.")
    print("Preparing your first run environment...")

    config = run_setup()
    config["assistant_name"] = "Z.E.L.D.A."
    config["ai_provider"] = "rules"
    config["capabilities"] = [
        "system.status",
        "system.time",
        "workspace.note.write",
    ]
    config["platform"] = current_platform()

    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")

    print("Setup complete.")
    return config
