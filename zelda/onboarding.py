from __future__ import annotations

import json
from pathlib import Path

from zelda.capabilities import DEFAULT_CAPABILITIES
from zelda.platform import current_platform
from zelda.setup_wizard import run_setup


CONFIG_FILE = Path.home() / ".zelda" / "config.json"


def _ask(prompt: str, default: str) -> str:
    try:
        value = input(f"{prompt} [{default}]: ").strip()
        return value or default
    except EOFError:
        return default


def first_run_onboarding() -> dict:
    print("Welcome to Z.E.L.D.A.")
    print("Preparing your first run environment...")

    config = run_setup()

    assistant_name = _ask("Assistant name", "Z.E.L.D.A.")
    ai_provider = _ask("AI provider (rules/ollama/cloud)", "rules")

    print("\nCapabilities:")
    for item in DEFAULT_CAPABILITIES:
        state = "enabled" if item["enabled"] else "disabled"
        print(f"  [{state}] {item['name']}")

    config["assistant_name"] = assistant_name
    config["ai_provider"] = ai_provider
    config["capabilities"] = [
        item["id"] for item in DEFAULT_CAPABILITIES if item["enabled"]
    ]
    config["capability_preferences"] = DEFAULT_CAPABILITIES
    config["confirmation_required"] = True
    config["platform"] = current_platform()

    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")

    print("Setup complete.")
    return config
