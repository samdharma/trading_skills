import sys

from tscli.reports import ReportGenerator


def build_subparser(subparsers):
    market_parser = subparsers.add_parser("market", help="Market analysis commands")
    market_sub = market_parser.add_subparsers(dest="market_command")

    regime = market_sub.add_parser("regime", help="Daily market regime snapshot")
    regime.add_argument("--output-dir", default="reports")
    regime.add_argument("--as-of", default=None)


def handle(args) -> int:
    if args.market_command == "regime":
        # Phase 1 skeleton: synthetic signals. Replace with real breadth/trend in Phase 2.
        data = {
            "posture": "neutral",
            "exposure_guidance": "50-75%",
            "breadth": {"signal": "neutral", "detail": "placeholder"},
            "trend": {"signal": "neutral", "detail": "placeholder"},
            "top": {"signal": "none", "detail": "placeholder"},
            "data_quality": "skeleton",
        }
        gen = ReportGenerator(output_dir=args.output_dir)
        json_path, _md_path = gen.write(
            "market-regime",
            data,
            metadata={"data_sources": ["skeleton"], "broker_adapter": "manual"},
        )
        print(f"Regime report: {json_path}", file=sys.stderr)
        print(f"Posture: {data['posture']}")
        return 0
    return 1
