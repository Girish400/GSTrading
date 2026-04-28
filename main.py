import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


def main() -> int:
    from codextrading.cli import build_parser, parse_config
    from codextrading.service import run_application

    parser = build_parser()
    config = parse_config(parser.parse_args())
    return run_application(config)


if __name__ == "__main__":
    raise SystemExit(main())
