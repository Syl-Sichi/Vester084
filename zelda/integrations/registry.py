from zelda.integrations.messaging import MessagingAdapter


class IntegrationRegistry:
    """Keeps platform adapters isolated from the core AI and from each other."""

    def __init__(self) -> None:
        self._messaging: dict[str, MessagingAdapter] = {}

    def register_messaging(self, adapter: MessagingAdapter) -> None:
        if adapter.platform in self._messaging:
            raise ValueError(f"Messaging adapter already registered: {adapter.platform}")
        self._messaging[adapter.platform] = adapter

    def messaging(self, platform: str) -> MessagingAdapter | None:
        return self._messaging.get(platform)

    def platforms(self) -> tuple[str, ...]:
        return tuple(sorted(self._messaging))
