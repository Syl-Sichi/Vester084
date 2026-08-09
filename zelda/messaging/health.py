from dataclasses import dataclass
from datetime import datetime, timezone

from zelda.messaging.lifecycle import AdapterState


@dataclass(frozen=True)
class AdapterHealth:
    platform: str
    state: AdapterState
    checked_at: str
    detail: str = ""


def health(platform: str, state: AdapterState, detail: str = "") -> AdapterHealth:
    return AdapterHealth(
        platform=platform,
        state=state,
        checked_at=datetime.now(timezone.utc).isoformat(),
        detail=detail,
    )
