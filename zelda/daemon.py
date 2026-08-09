import asyncio
import logging

from zelda.config import ZeldaConfig
from zelda.network_daemon import run


if __name__ == "__main__":
    config = ZeldaConfig.from_env()
    logging.basicConfig(level=getattr(logging, config.log_level), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    asyncio.run(run(config))
