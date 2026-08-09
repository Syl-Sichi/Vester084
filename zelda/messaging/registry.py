from zelda.messaging.base import MessagingAdapter


class MessagingRegistry:
    """Allowlist of messaging integrations available to Z.E.L.D.A."""

    def __init__(self) -> None:
        self._adapters: dict[str, MessagingAdapter] = {}

    def register(self, adapter: MessagingAdapter) -> None:
        if adapter.platform in self._adapters:
            raise ValueError(f"Messaging adapter already registered: {adapter.platform}")
        self._adapters[adapter.platform] = adapter

    def get(self, platform: str) -> MessagingAdapter | None:
        return self._adapters.get(platform)

    def platforms(self) -> tuple[str, ...]:
        return tuple(sorted(self._adapters))
