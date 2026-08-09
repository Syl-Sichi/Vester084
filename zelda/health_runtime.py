from zelda.health import set_ready
from zelda.health_server import HealthServer


class HealthRuntime:
    """Owns the local health/readiness server lifecycle."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8766) -> None:
        self.server = HealthServer(host, port)

    def start(self) -> None:
        self.server.start()
        set_ready(True)

    def stop(self) -> None:
        set_ready(False)
        self.server.stop()
