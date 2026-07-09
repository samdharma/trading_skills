import sys

from tscli.brokers.manual import ManualBrokerAdapter
from tscli.config import load_broker_config
from tscli.reports import ReportGenerator

BROKER_MAP = {
    "manual": ManualBrokerAdapter,
}


def build_subparser(subparsers):
    broker_parser = subparsers.add_parser("broker", help="Broker commands")
    broker_sub = broker_parser.add_subparsers(dest="broker_command")

    check = broker_sub.add_parser("check", help="Check broker connection")
    check.add_argument("--broker", choices=["manual", "opend", "ibkr"], default=None)
    check.add_argument("--output-dir", default="reports")

    positions = broker_sub.add_parser("positions", help="List positions")
    positions.add_argument("--broker", choices=["manual", "opend", "ibkr"], default=None)
    positions.add_argument("--output-dir", default="reports")


def resolve_adapter(cfg):
    cls = BROKER_MAP.get(cfg.broker, ManualBrokerAdapter)
    return cls()


def handle(args) -> int:
    cfg = load_broker_config(args)
    adapter = resolve_adapter(cfg)

    if args.broker_command == "check":
        connected = adapter.is_connected()
        data = {"adapter": adapter.name(), "connected": connected}
        gen = ReportGenerator(output_dir=args.output_dir)
        json_path, _md_path = gen.write(
            "broker-check",
            data,
            metadata={"broker_adapter": adapter.name()},
        )
        print(f"Connected: {connected}", file=sys.stderr)
        print(f"Report: {json_path}")
        return 0

    if args.broker_command == "positions":
        positions = adapter.get_positions()
        account = adapter.get_account()
        data = {
            "adapter": adapter.name(),
            "positions": [p.__dict__ for p in positions],
            "account": account.__dict__,
        }
        gen = ReportGenerator(output_dir=args.output_dir)
        json_path, _md_path = gen.write(
            "broker-positions",
            data,
            metadata={"broker_adapter": adapter.name()},
        )
        print(f"Report: {json_path}")
        return 0

    return 1
