from __future__ import annotations

import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".zelda"
CONFIG_FILE = CONFIG_DIR / "setup.json"


def run_setup() -> dict[str, object]:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    config = {
        "initialized": True,
        "workspace": str(CONFIG_DIR / "workspace"),
        "platform_setup": True,
    }

    (CONFIG_DIR / "workspace").mkdir(exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return config


def is_initialized() -> bool:
    return CONFIG_FILE.exists()
