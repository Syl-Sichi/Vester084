from dataclasses import dataclass


@dataclass(frozen=True)
class ConnectionPolicy:
    max_connections: int = 100
    max_frame_bytes: int = 64 * 1024
    require_hello: bool = True

    def validate_frame_size(self, raw_message: str) -> None:
        if len(raw_message.encode("utf-8")) > self.max_frame_bytes:
            raise ValueError("frame_too_large")

    def validate_connection_count(self, active_connections: int) -> None:
        if active_connections >= self.max_connections:
            raise RuntimeError("connection_limit_reached")
