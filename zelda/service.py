import logging
import signal
import threading
from typing import Any

from zelda.events.bus import Event, EventBus


class ZeldaService:
    """Long running host service with graceful shutdown and command dispatch."""

    def __init__(self, event_bus: EventBus | None = None) -> None:
        self.event_bus = event_bus or EventBus()
        self.stop_event = threading.Event()
        self.logger = logging.getLogger("zelda.service")

    def request_stop(self, *_args) -> None:
        self.logger.info("Shutdown requested")
        self.stop_event.set()

    def handle_command(self, command: str) -> dict[str, Any]:
        self.event_bus.publish(Event("command.received", {"command": command}))
        self.logger.info("Command received: %s", command)
        return {"accepted": True, "command": command}

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
