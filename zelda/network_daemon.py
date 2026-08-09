import asyncio
import logging

from websockets.server import serve

from zelda.network_runtime import NetworkRuntime
from zelda.service import ZeldaService

logger = logging.getLogger("zelda.network_daemon")


def build_runtime(service: ZeldaService) -> NetworkRuntime:
    def handle_command(command: str):
        return service.handle_command(command)

    import os
    health_port = int(os.environ.get("ZELDA_HEALTH_PORT", "8766"))
    return NetworkRuntime(handle_command, health_host="127.0.0.1", health_port=health_port)


async def run() -> None:
    service = ZeldaService()
    runtime = build_runtime(service)
    await runtime.start(serve)
    service.event_bus.publish(service.event_bus.Event("network.started")) if hasattr(service.event_bus, "Event") else None
    try:
        await asyncio.to_thread(service.stop_event.wait)
    finally:
        await runtime.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(run())
