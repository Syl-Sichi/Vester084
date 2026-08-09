from abc import ABC, abstractmethod

from zelda.core.models import Intent


class ModelProvider(ABC):
    """Interface for replaceable local or remote AI model providers."""

    @abstractmethod
    def understand(self, text: str) -> Intent:
        raise NotImplementedError
