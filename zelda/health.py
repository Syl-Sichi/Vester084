from datetime import datetime, timezone


def snapshot() -> dict[str, str]:
    return {
        "service": "zelda",
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
