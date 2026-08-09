import sqlite3
from pathlib import Path


class MobileStateStore:
    """Small SQLite store for mobile delivery state that survives daemon restarts."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        self._db = sqlite3.connect(self.path, check_same_thread=False)
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS mobile_state (client_id TEXT PRIMARY KEY, acknowledged_sequence INTEGER NOT NULL DEFAULT 0)"
        )
        self._db.commit()

    def acknowledged(self, client_id: str) -> int:
        row = self._db.execute(
            "SELECT acknowledged_sequence FROM mobile_state WHERE client_id = ?", (client_id,)
        ).fetchone()
        return int(row[0]) if row else 0

    def acknowledge(self, client_id: str, sequence: int) -> int:
        if sequence < 0:
            raise ValueError("sequence must be non negative")
        current = self.acknowledged(client_id)
        value = max(current, sequence)
        self._db.execute(
            "INSERT INTO mobile_state(client_id, acknowledged_sequence) VALUES(?, ?) "
            "ON CONFLICT(client_id) DO UPDATE SET acknowledged_sequence = excluded.acknowledged_sequence",
            (client_id, value),
        )
        self._db.commit()
        return value

    def close(self) -> None:
        self._db.close()
