from dataclasses import dataclass
from enum import Enum
from typing import Any


class MessageType(str, Enum):
    AUTHENTICATE = "authenticate"
    COMMAND = "command"
    EVENT = "event"
    RESPONSE = "response"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"


@dataclass(frozen=True)
class Envelope:
    type: MessageType
    request_id: str | None = None
    payload: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type.value,
            "request_id": self.request_id,
            "payload": self.payload or {},
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Envelope":
        return cls(
            type=MessageType(value["type"]),
            request_id=value.get("request_id"),
            payload=value.get("payload") or {},
        )
