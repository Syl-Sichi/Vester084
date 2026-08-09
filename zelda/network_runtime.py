import logging

from zelda.auth.sessions import SessionManager
from zelda.mobile.gateway import MobileGateway
from zelda.mobile.ws_gateway import WebSocketGateway
from zelda.daemon_server import DaemonConfig, DaemonServer

logger = logging.getLogger(__name__)


class NetworkRuntime:
    """Assemble the authenticated mobile gateway and network server."""

    def __init__(self, command_handler, config: DaemonConfig | None = None) -> None:
        self.config = config or DaemonConfig.from_env()
        self.sessions = SessionManager()
        self.gateway = MobileGateway(self.sessions, command_handler)
        self.websocket_gateway = WebSocketGateway(self.gateway)
        self.server = DaemonServer(self.config, self.websocket_gateway)

    async def start(self, serve):
        logger.info("Starting Z.E.L.D.A. network runtime on %s:%s", self.config.host, self.config.port)
        return await self.server.start(serve)

    async def stop(self) -> None:
        await self.server.stop()
        logger.info("Z.E.L.D.A. network runtime stopped")
