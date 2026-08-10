import logging
import platform
import signal
import threading
from typing import Any

from zelda.config import ZeldaConfig
from zelda.control.ai_control import AIControlService
from zelda.control.bootstrap import register_macos_display_capabilities, register_ubuntu_readonly_capabilities
from zelda.control.capabilities import CapabilityRegistry
from zelda.control.policy import CapabilityPolicy
from zelda.control.providers import build_provider
from zelda.events.bus import Event, EventBus


class ZeldaService:
    """Long running host service with controlled AI command dispatch."""

    def __init__(self, event_bus: EventBus | None = None, config: ZeldaConfig | None = None) -> None:
        self.event_bus = event_bus or EventBus()
        self.stop_event = threading.Event()
        self.logger = logging.getLogger("zelda.service")
        self.config = config or ZeldaConfig.from_env()

        self.capabilities = CapabilityRegistry()
        register_ubuntu_readonly_capabilities(self.capabilities)
        if platform.system() == "Darwin":
            register_macos_display_capabilities(self.capabilities)
        self.policy = CapabilityPolicy.from_registry(self.capabilities)
        self.ai_control = AIControlService(
            self.capabilities,
            self.policy,
            provider=build_provider(
                self.config.ai_provider,
                ollama_url=self.config.ollama_url,
                ollama_model=self.config.ollama_model,
            ),
        )

    def request_stop(self, *_args) -> None:
        self.logger.info("Shutdown requested")
        self.stop_event.set()

    def handle_command(self, command: str) -> dict[str, Any]:
        try:
            result = self.ai_control.handle(command)
            self.event_bus.publish(Event("command.executed", result))
            self.logger.info("Command executed through capability %s", result["capability"])
            return result
        except (ValueError, PermissionError) as exc:
            error = {"accepted": False, "error": str(exc), "command": command}
            self.event_bus.publish(Event("command.rejected", error))
            self.logger.warning("Command rejected: %s", exc)
            return error

    def run(self) -> None:
        signal.signal(signal.SIGINT, self.request_stop)
        signal.signal(signal.SIGTERM, self.request_stop)
        self.logger.info("Z.E.L.D.A. service started")
        self.event_bus.publish(Event("service.started"))
        try:
            while not self.stop_event.wait(1.0):
                pass
        finally:
            self.event_bus.publish(Event("service.stopped"))
            self.logger.info("Z.E.L.D.A. service stopped")
