from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    platform: str
    conversation_id: str
    sender_id: str
    text: str
    message_id: str | None = None


class MessagingAdapter(ABC):
    """Platform adapter contract. Credentials stay inside each adapter."""

    platform: str

    @abstractmethod
    def send(self, conversation_id: str, text: str) -> Message:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
