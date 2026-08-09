import json
from pathlib import Path


class AndroidStateStore:
    """Small file backed store for client delivery state."""

    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def load_last_acknowledged(self) -> int:
        if not self.path.exists():
            return 0
        data = json.loads(self.path.read_text(encoding="utf-8"))
        value = data.get("last_acknowledged", 0)
        if not isinstance(value, int) or value < 0:
            raise ValueError("invalid persisted acknowledgement")
        return value

    def save_last_acknowledged(self, sequence: int) -> None:
        if sequence < 0:
            raise ValueError("sequence must be non negative")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix(self.path.suffix + ".tmp")
        temp.write_text(json.dumps({"last_acknowledged": sequence}), encoding="utf-8")
        temp.replace(self.path)
