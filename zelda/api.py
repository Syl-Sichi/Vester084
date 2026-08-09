from typing import Any

from zelda.app import brain


def handle_command(command: str) -> dict[str, Any]:
    """Programmatic API boundary for future HTTP, voice, and messaging adapters."""
    result = brain.handle(command)
    return {
        "success": result.success,
        "message": result.message,
        "data": result.data,
    }
