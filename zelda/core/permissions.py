from zelda.core.models import Intent


class PermissionEngine:
    """Default deny policy for capabilities not explicitly approved."""

    def __init__(self, allowed_tools: set[str] | None = None) -> None:
        self.allowed_tools = allowed_tools or set()

    def allow(self, tool_name: str) -> None:
        self.allowed_tools.add(tool_name)

    def revoke(self, tool_name: str) -> None:
        self.allowed_tools.discard(tool_name)

    def allows(self, tool_name: str, intent: Intent) -> bool:
        return tool_name in self.allowed_tools and not intent.requires_confirmation
