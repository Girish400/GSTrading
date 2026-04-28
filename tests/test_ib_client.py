import asyncio

from codextrading.config import AppConfig
from codextrading.ib_client import AsyncIBMarketDataClient


def test_market_data_client_updates_bid_and_ask() -> None:
    loop = asyncio.new_event_loop()
    try:
        client = AsyncIBMarketDataClient(AppConfig(symbols={"AAPL"}), loop)
        client._request_id_to_symbol[1] = "AAPL"

        client.tickPrice(1, 1, 184.25, None)
        client.tickPrice(1, 2, 184.30, None)

        snapshot = client._latest_by_symbol["AAPL"]
        assert snapshot.bid == 184.25
        assert snapshot.ask == 184.30
    finally:
        loop.close()
