import argparse

from tscli import __version__
from tscli.commands import broker, market


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tscli", description="Trading Skills CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    broker.build_subparser(subparsers)
    market.build_subparser(subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    if args.command == "broker":
        return broker.handle(args)
    if args.command == "market":
        return market.handle(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
