from __future__ import annotations

import json
from pathlib import Path

from zelda.platform import current_platform


CONFIG_DIR = Path.home() / ".zelda"
CONFIG_FILE = CONFIG_DIR / "config.json"


def run_setup() -> dict[str, str]:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    config = {
        "platform": current_platform(),
        "workspace": str(CONFIG_DIR / "workspace"),
        "setup_complete": "true",
    }

    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")
    (CONFIG_DIR / "workspace").mkdir(exist_ok=True)

    return config


def needs_setup() -> bool:
    return not CONFIG_FILE.exists()


if __name__ == "__main__":
    print(run_setup())
