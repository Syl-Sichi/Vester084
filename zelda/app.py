from zelda.config import use_ollama
from zelda.core.brain import Brain
from zelda.core.permissions import PermissionEngine
from zelda.core.orchestrator import Orchestrator
from zelda.providers.ollama import OllamaProvider
from zelda.providers.rules import RuleBasedProvider
from zelda.tools.macos import MacOSApplicationsTool, MacOSSystemStatusTool
from zelda.tools.registry import ToolRegistry
from zelda.tools.system import SystemStatusTool
from zelda.tools.time import CurrentTimeTool


def build_components() -> tuple[Brain, Orchestrator]:
    registry = ToolRegistry()
    registry.register(SystemStatusTool())
    registry.register(CurrentTimeTool())
    registry.register(MacOSSystemStatusTool())
    registry.register(MacOSApplicationsTool())

    permissions = PermissionEngine()
    permissions.allow("system.status")
    permissions.allow("system.time")
    permissions.allow("macos.system.status")
    permissions.allow("macos.applications.list")

    provider = OllamaProvider() if use_ollama() else RuleBasedProvider()
    brain = Brain(provider, registry, permissions)
    orchestrator = Orchestrator(registry, permissions)
    return brain, orchestrator


brain, orchestrator = build_components()
