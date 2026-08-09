import logging

from zelda.auth.sessions import SessionManager
from zelda.daemon_server import DaemonConfig, DaemonServer
from zelda.health_runtime import HealthRuntime
from zelda.mobile.gateway import MobileGateway
from zelda.mobile.ws_gateway import WebSocketGateway

logger = logging.getLogger(__name__)


class NetworkRuntime:
    """Assemble the mobile control plane and local health plane."""

    def __init__(self, command_handler, config: DaemonConfig | None = None, health_host: str = "127.0.0.1", health_port: int = 8766) -> None:
        self.config = config or DaemonConfig.from_env()
        self.sessions = SessionManager()
        self.gateway = MobileGateway(self.sessions, command_handler)
        self.websocket_gateway = WebSocketGateway(self.gateway)
        self.server = DaemonServer(self.config, self.websocket_gateway)
        self.health = HealthRuntime(health_host, health_port)

    async def start(self, serve):
        logger.info("Starting Z.E.L.D.A. network runtime on %s:%s", self.config.host, self.config.port)
        self.health.start()
        try:
            return await self.server.start(serve)
        except Exception:
            self.health.stop()
            raise

    async def stop(self) -> None:
        await self.server.stop()
        self.health.stop()
        logger.info("Z.E.L.D.A. network runtime stopped")
