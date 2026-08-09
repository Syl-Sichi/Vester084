import json

from zelda.mobile.gateway import MobileGateway
from zelda.mobile.security import ConnectionPolicy
from zelda.mobile.transport import TransportFrame


class WebSocketGateway:
    """Authenticated WebSocket adapter for the mobile protocol."""

    def __init__(self, gateway: MobileGateway, policy: ConnectionPolicy | None = None) -> None:
        self.gateway = gateway
        self.policy = policy or ConnectionPolicy()

    async def handle(self, websocket) -> None:
        authenticated = False
        async for message in websocket:
            if not isinstance(message, str):
                await self._error(websocket, "text_frames_only")
                continue
            try:
                self.policy.validate_frame_size(message)
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
            except (ValueError, TypeError, KeyError, RuntimeError) as exc:
                await self._error(websocket, str(exc))

    async def _error(self, websocket, error: str) -> None:
        await websocket.send(json.dumps({"kind": "ERROR", "payload": {"error": error}}))
