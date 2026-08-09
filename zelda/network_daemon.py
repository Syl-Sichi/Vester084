import asyncio
import logging
import os

from websockets.server import serve

from zelda.events.bus import Event
from zelda.network_runtime import NetworkRuntime
from zelda.service import ZeldaService

logger = logging.getLogger("zelda.network_daemon")


def build_runtime(service: ZeldaService) -> NetworkRuntime:
    health_port = int(os.environ.get("ZELDA_HEALTH_PORT", "8766"))
    return NetworkRuntime(service.handle_command, health_host="127.0.0.1", health_port=health_port)


async def run() -> None:
    service = ZeldaService()
    runtime = build_runtime(service)
    await runtime.start(serve)
    service.event_bus.publish(Event("network.started"))
    logger.info("Z.E.L.D.A. network daemon is ready")
    try:
        await asyncio.to_thread(service.stop_event.wait)
    finally:
        service.event_bus.publish(Event("network.stopping"))
        await runtime.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(run())
