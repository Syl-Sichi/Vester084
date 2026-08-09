import json
import uuid

from zelda.health import record_command, record_event, set_active_connections
from zelda.mobile.connections import ConnectionRegistry
from zelda.mobile.gateway import MobileGateway
from zelda.mobile.rate_limit import RateLimiter
from zelda.mobile.security import ConnectionPolicy
from zelda.mobile.transport import TransportFrame


class WebSocketGateway:
    """Authenticated WebSocket adapter with connection, rate and health telemetry."""

    def __init__(self, gateway: MobileGateway, policy: ConnectionPolicy | None = None, rate_limiter: RateLimiter | None = None, connections: ConnectionRegistry | None = None) -> None:
        self.gateway = gateway
        self.policy = policy or ConnectionPolicy()
        self.rate_limiter = rate_limiter or RateLimiter()
        self.connections = connections or ConnectionRegistry(self.policy.max_connections)

    async def handle(self, websocket) -> None:
        client_id = uuid.uuid4().hex
        try:
            self.connections.acquire(client_id)
            set_active_connections(self.connections.active_count)
        except RuntimeError as exc:
            await self._error(websocket, str(exc))
            return

        authenticated = False
        try:
            async for message in websocket:
                if not isinstance(message, str):
                    await self._error(websocket, "text_frames_only")
                    continue
                try:
                    self.policy.validate_frame_size(message)
                    if not self.rate_limiter.allow(client_id):
                        await self._error(websocket, "rate_limit_exceeded")
                        continue
                    frame = TransportFrame.from_json(message)
                    if self.policy.require_hello and not authenticated and frame.kind != "HELLO":
                        await self._error(websocket, "hello_required")
                        continue

                    self.gateway.transport.inject(frame)
                    response = self.gateway.transport.receive()
                    if response is not None:
                        await websocket.send(response.to_json())
                        if frame.kind == "HELLO" and response.kind == "SYNC":
                            authenticated = True
                        elif frame.kind == "COMMAND":
                            record_command()
                        elif frame.kind == "EVENT":
                            record_event()
                except (ValueError, TypeError, KeyError, RuntimeError) as exc:
                    await self._error(websocket, str(exc))
        finally:
            self.rate_limiter.remove(client_id)
            self.connections.release(client_id)
            set_active_connections(self.connections.active_count)

    async def _error(self, websocket, error: str) -> None:
        await websocket.send(json.dumps({"kind": "ERROR", "payload": {"error": error}}))
