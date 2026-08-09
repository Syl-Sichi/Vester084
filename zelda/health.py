from datetime import datetime, timezone
from time import monotonic

_started_at = monotonic()
_ready = False
_active_connections = 0
_events_processed = 0
_commands_processed = 0


def set_ready(ready: bool) -> None:
    global _ready
    _ready = ready


def set_active_connections(count: int) -> None:
    global _active_connections
    _active_connections = max(0, count)


def record_event() -> None:
    global _events_processed
    _events_processed += 1


def record_command() -> None:
    global _commands_processed
    _commands_processed += 1


def snapshot() -> dict[str, object]:
    return {
        "service": "zelda",
        "status": "ok",
        "ready": _ready,
        "uptime_seconds": max(0.0, monotonic() - _started_at),
        "active_connections": _active_connections,
        "events_processed": _events_processed,
        "commands_processed": _commands_processed,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
