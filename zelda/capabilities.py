from __future__ import annotations


DEFAULT_CAPABILITIES = [
    {
        "id": "system.status",
        "name": "System information",
        "enabled": True,
    },
    {
        "id": "system.apps",
        "name": "Application discovery",
        "enabled": True,
    },
    {
        "id": "workspace.note.write",
        "name": "Workspace files",
        "enabled": True,
    },
    {
        "id": "system.processes",
        "name": "Process management",
        "enabled": False,
    },
    {
        "id": "network.tools",
        "name": "Network tools",
        "enabled": False,
    },
    {
        "id": "voice.assistant",
        "name": "Voice assistant",
        "enabled": False,
    },
]


def enabled_capabilities() -> list[str]:
    return [item["id"] for item in DEFAULT_CAPABILITIES if item["enabled"]]
