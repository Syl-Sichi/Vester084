"""Optional WebSocket transport adapter for the mobile protocol.

The protocol itself stays transport agnostic. This adapter uses the optional
`websockets` package and converts one TransportFrame to one WebSocket message.
"""

from zelda.mobile.transport import TransportFrame


class WebSocketTransport:
    def __init__(self, websocket) -> None:
        self.websocket = websocket
        self.connected = True

    async def send(self, frame: TransportFrame) -> None:
        if not self.connected:
            raise RuntimeError("transport is not connected")
        await self.websocket.send(frame.encode())

    async def receive(self) -> TransportFrame:
        if not self.connected:
            raise RuntimeError("transport is not connected")
        data = await self.websocket.recv()
        if isinstance(data, str):
            data = data.encode("utf-8")
        return TransportFrame.decode(data)

    async def close(self) -> None:
        self.connected = False
        await self.websocket.close()


async def serve_websocket(handler, host: str = "127.0.0.1", port: int = 8765):
    """Run a WebSocket server when the optional dependency is installed."""
    try:
        from websockets.asyncio.server import serve
    except ImportError as exc:
        raise RuntimeError("install the optional 'websockets' dependency") from exc
    return await serve(handler, host, port)
