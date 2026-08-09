import json
import sqlite3
from pathlib import Path
from typing import Any


class MemoryStore:
    """Small local SQLite memory store. No network access and no secrets by default."""

    def __init__(self, path: str | Path = "~/.zelda/memory.db") -> None:
        self.path = Path(path).expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS memories (key TEXT PRIMARY KEY, value TEXT NOT NULL)")

    def set(self, key: str, value: Any) -> None:
        encoded = json.dumps(value, ensure_ascii=False)
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO memories(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, encoded))

    def get(self, key: str) -> Any | None:
        with sqlite3.connect(self.path) as db:
            row = db.execute("SELECT value FROM memories WHERE key=?", (key,)).fetchone()
        return None if row is None else json.loads(row[0])

    def delete(self, key: str) -> bool:
        with sqlite3.connect(self.path) as db:
            cursor = db.execute("DELETE FROM memories WHERE key=?", (key,))
            return cursor.rowcount > 0
