import json
import sqlite3
import threading
from dataclasses import dataclass

from zelda.mobile.transport import TransportFrame


@dataclass(frozen=True)
class JournalEvent:
    sequence: int
    frame: TransportFrame


class MobileEventJournal:
    """Durable bounded event journal for mobile reconnect recovery."""

    def __init__(self, path: str, max_items: int = 1000) -> None:
        if max_items < 1:
            raise ValueError("max_items must be positive")
        self.max_items = max_items
        self._lock = threading.Lock()
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS mobile_events ("
            "sequence INTEGER PRIMARY KEY AUTOINCREMENT, "
            "frame_json TEXT NOT NULL"
            ")"
        )
        self._db.commit()

    def append(self, frame: TransportFrame) -> JournalEvent:
        encoded = json.dumps({
            "kind": frame.kind,
            "request_id": frame.request_id,
            "payload": frame.payload or {},
        }, separators=(",", ":"))
        with self._lock:
            cursor = self._db.execute("INSERT INTO mobile_events(frame_json) VALUES (?)", (encoded,))
            self._db.execute(
                "DELETE FROM mobile_events WHERE sequence <= "
                "(SELECT COALESCE(MAX(sequence), 0) - ? FROM mobile_events)",
                (self.max_items,)
            )
            self._db.commit()
            sequence = int(cursor.lastrowid)
        return JournalEvent(sequence, frame)

    def after(self, sequence: int) -> list[JournalEvent]:
        with self._lock:
            rows = self._db.execute(
                "SELECT sequence, frame_json FROM mobile_events WHERE sequence > ? ORDER BY sequence",
                (sequence,),
            ).fetchall()
        result = []
        for event_sequence, raw in rows:
            value = json.loads(raw)
            result.append(JournalEvent(
                int(event_sequence),
                TransportFrame(value["kind"], value.get("request_id"), value.get("payload", {})),
            ))
        return result

    def close(self) -> None:
        with self._lock:
            self._db.close()
