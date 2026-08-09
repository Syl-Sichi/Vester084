from dataclasses import dataclass


@dataclass(frozen=True)
class DaemonConfig:
    host: str = "127.0.0.1"
    port: int = 8765

    @classmethod
    def from_env(cls, environ=None):
        import os
        env = os.environ if environ is None else environ
        host = env.get("ZELDA_HOST", cls.host)
        raw_port = env.get("ZELDA_PORT", str(cls.port))
        try:
            port = int(raw_port)
        except ValueError as exc:
            raise ValueError("ZELDA_PORT must be an integer") from exc
        if not 1 <= port <= 65535:
            raise ValueError("ZELDA_PORT must be between 1 and 65535")
        return cls(host, port)


class DaemonServer:
    """Lifecycle boundary for the networked Z.E.L.D.A. service."""

    def __init__(self, config: DaemonConfig, websocket_gateway) -> None:
        self.config = config
        self.websocket_gateway = websocket_gateway
        self.running = False
        self._server = None

    async def start(self, serve):
        self.running = True
        self._server = await serve(
            self.websocket_gateway.handle,
            self.config.host,
            self.config.port,
        )
        return self._server

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
            wait_closed = getattr(self._server, "wait_closed", None)
            if wait_closed is not None:
                await wait_closed()
            self._server = None
        self.running = False
