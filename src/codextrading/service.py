from __future__ import annotations

import asyncio
import logging

from codextrading.config import AppConfig
from codextrading.ib_client import AsyncIBMarketDataClient


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


async def run_market_data_session(config: AppConfig) -> int:
    loop = asyncio.get_running_loop()
    client = AsyncIBMarketDataClient(config=config, loop=loop)
    try:
        client.connect_and_start()
        client.request_market_data()
        await client.consume()
        return 0
    finally:
        client.disconnect_and_stop()


def run_application(config: AppConfig) -> int:
    configure_logging(config.log_level)
    return asyncio.run(run_market_data_session(config))
