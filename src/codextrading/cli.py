from __future__ import annotations

import argparse

from codextrading.config import AppConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Stream market data from Interactive Brokers using ibapi and asyncio."
    )
    parser.add_argument("--symbols", nargs="+", default=["AAPL"], help="Symbols to subscribe to.")
    parser.add_argument("--host", default="127.0.0.1", help="IB Gateway or TWS host.")
    parser.add_argument("--port", type=int, default=7497, help="IB Gateway or TWS API port.")
    parser.add_argument("--client-id", type=int, default=101, help="IB API client identifier.")
    parser.add_argument("--exchange", default="SMART", help="Contract exchange.")
    parser.add_argument("--currency", default="USD", help="Contract currency.")
    parser.add_argument(
        "--duration",
        type=int,
        default=15,
        help="Streaming duration in seconds for non-snapshot runs.",
    )
    parser.add_argument(
        "--generic-tick",
        nargs="*",
        default=[],
        help="Optional IB generic tick type codes.",
    )
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="Request a one-time market data snapshot instead of a timed stream.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Application log level.",
    )
    parser.add_argument(
        "--output-path",
        default=None,
        help="Optional file path for line-delimited JSON output.",
    )
    return parser


def parse_config(args: argparse.Namespace) -> AppConfig:
    symbols = {symbol.upper() for symbol in args.symbols}
    generic_ticks = {tick.strip() for tick in args.generic_tick if tick.strip()}
    return AppConfig(
        symbols=symbols,
        host=args.host,
        port=args.port,
        client_id=args.client_id,
        exchange=args.exchange,
        currency=args.currency,
        snapshot=args.snapshot,
        duration_seconds=args.duration,
        generic_ticks=generic_ticks,
        log_level=args.log_level,
        output_path=args.output_path,
    )
