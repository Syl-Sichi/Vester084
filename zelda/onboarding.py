from __future__ import annotations

import json
from pathlib import Path

from zelda.platform import current_platform
from zelda.setup_wizard import run_setup


CONFIG_FILE = Path.home() / ".zelda" / "config.json"


def _ask(prompt: str, default: str) -> str:
    try:
        value = input(f"{prompt} [{default}]: ").strip()
    except EOFError:
        value = ""
    return value or default


def first_run_onboarding() -> dict[str, str]:
    print("Welcome to Z.E.L.D.A.")
    print("Preparing your first run environment...\n")

    assistant_name = _ask("Assistant name", "Z.E.L.D.A.")
    provider = _ask("AI provider (rules/ollama/cloud)", "rules")

    config = run_setup()
    config["assistant_name"] = assistant_name
    config["ai_provider"] = provider
    config["capabilities"] = [
        "system.status",
        "system.time",
        "workspace.note.write",
    ]
    config["platform"] = current_platform()
    config["confirmation_required"] = True

    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")

    print(f"{assistant_name} is ready.")
    return config
