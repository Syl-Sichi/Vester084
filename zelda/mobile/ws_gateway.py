import json

from zelda.mobile.gateway import MobileGateway
from zelda.mobile.transport import TransportFrame


class WebSocketGateway:
    """Adapter that exposes MobileGateway over a text WebSocket connection."""

    def __init__(self, gateway: MobileGateway) -> None:
        self.gateway = gateway

    async def handle(self, websocket) -> None:
        async for message in websocket:
            if not isinstance(message, str):
                await websocket.send(json.dumps({"kind": "ERROR", "payload": {"error": "text_frames_only"}}))
                continue
            try:
                frame = TransportFrame.from_json(message)
                self.gateway.transport.inject(frame)
                response = self.gateway.transport.receive()
                if response is not None:
                    await websocket.send(response.to_json())
            except (ValueError, TypeError, KeyError) as exc:
                await websocket.send(json.dumps({"kind": "ERROR", "payload": {"error": str(exc)}}))
