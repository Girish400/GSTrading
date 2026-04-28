from codextrading.cli import build_parser, parse_config


def test_parse_config_normalizes_symbols_and_generic_ticks() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "--symbols",
            "aapl",
            "msft",
            "--generic-tick",
            "233",
            "236",
            "",
            "--duration",
            "30",
        ]
    )

    config = parse_config(args)

    assert config.symbols == {"AAPL", "MSFT"}
    assert config.generic_ticks == {"233", "236"}
    assert config.duration_seconds == 30
