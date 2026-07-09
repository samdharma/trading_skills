# Kimi Trading Skills — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `tscli` Python CLI scaffold, broker-adapter abstraction, report envelope, and the first two commands (`broker check` and `market regime`) so the Kimi skill can execute real commands.

**Architecture:** A thin `argparse` command router dispatches to submodules under `src/tscli/`. A `BrokerAdapter` protocol isolates Futubull OpenD, IB Gateway, and manual fallback. Every command returns a typed dict that `ReportGenerator` serializes to JSON + Markdown with a stable envelope.

**Tech Stack:** Python 3.9+, `uv`, `argparse`, `jsonschema`, `pyyaml`, `requests`, `yfinance`, `pytest`, `ruff`.

## Global Constraints

- Python >= 3.9.
- No live order execution; only templates and analysis reports.
- Default broker adapter is `manual` when credentials are missing.
- Every command emits both JSON and Markdown reports under `reports/`.
- Report envelope must contain `schema_version`, `skill`, `metadata`, and `data`.
- Code must pass `ruff` with line length 100.
- Tests run with `uv run pytest -q`.

---

## File Structure

| Path | Responsibility |
|------|----------------|
| `pyproject.toml` | Project metadata, dependencies, entry point `tscli`, ruff/pytest config |
| `src/tscli/__init__.py` | Version constant |
| `src/tscli/cli.py` | `argparse` router and top-level `main()` |
| `src/tscli/config.py` | Environment/config loader (`TSCLI_*` env vars) |
| `src/tscli/brokers/base.py` | `BrokerAdapter` protocol + `Position`, `AccountSummary`, `Bar` dataclasses |
| `src/tscli/brokers/manual.py` | `ManualBrokerAdapter` default-deny / fixture mode |
| `src/tscli/brokers/opend.py` | `FutubullOpenDAdapter` stub with connection validation |
| `src/tscli/brokers/ibkr.py` | `IbGatewayAdapter` stub with connection validation |
| `src/tscli/reports.py` | `ReportGenerator` — JSON + Markdown envelope |
| `src/tscli/commands/market.py` | `market regime` command |
| `src/tscli/commands/broker.py` | `broker check` and `broker positions` commands |
| `tests/test_cli.py` | CLI smoke tests |
| `tests/test_broker_manual.py` | Manual broker adapter tests |
| `tests/test_report.py` | Report envelope schema tests |

---

### Task 1: Project scaffold and CLI entry point

**Files:**
- Create: `pyproject.toml`
- Create: `src/tscli/__init__.py`
- Create: `src/tscli/cli.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Produces: `tscli --help` prints version and subcommands; `tscli --version` returns `0.1.0`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_cli.py
import subprocess
import sys


def test_cli_version():
    result = subprocess.run(
        [sys.executable, "-m", "tscli", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "0.1.0" in result.stdout
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_cli.py::test_cli_version -v`
Expected: FAIL with `No module named tscli`.

- [ ] **Step 3: Write minimal implementation**

```toml
# pyproject.toml
[project]
name = "tscli"
version = "0.1.0"
description = "Code-first trading assistant CLI"
requires-python = ">=3.9"
dependencies = [
    "jsonschema>=4.25.1",
    "pyyaml>=6.0",
    "requests>=2.31.0",
    "yfinance>=0.2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "ruff==0.9.6",
]

[project.scripts]
tscli = "tscli.cli:main"

[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 100
target-version = "py39"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

```python
# src/tscli/__init__.py
__version__ = "0.1.0"
```

```python
# src/tscli/cli.py
import argparse
import sys

from tscli import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tscli", description="Trading Skills CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("broker", help="Broker commands")
    subparsers.add_parser("market", help="Market analysis commands")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    print(f"Command: {args.command}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_cli.py::test_cli_version -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml src/tscli/__init__.py src/tscli/cli.py tests/test_cli.py
git commit -m "feat(cli): scaffold tscli project and version flag"
```

---

### Task 2: Report envelope and generator

**Files:**
- Create: `src/tscli/reports.py`
- Create: `tests/test_report.py`
- Create: `reports/.gitkeep`

**Interfaces:**
- Produces: `ReportGenerator.write(skill, data, output_dir, metadata=None)` returns `(json_path, md_path)`.
- Produces: Report envelope dict with `schema_version`, `skill`, `metadata`, `data`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_report.py
import json
import tempfile
from pathlib import Path

from tscli.reports import ReportGenerator


def test_report_envelope():
    with tempfile.TemporaryDirectory() as tmp:
        gen = ReportGenerator(output_dir=tmp)
        json_path, md_path = gen.write(
            skill="market-regime",
            data={"posture": "neutral"},
            metadata={"run_at": "2026-07-09T09:30:00Z", "data_sources": ["yfinance"]},
        )
        assert Path(json_path).exists()
        assert Path(md_path).exists()
        with open(json_path) as f:
            payload = json.load(f)
        assert payload["schema_version"] == "1.0"
        assert payload["skill"] == "market-regime"
        assert payload["data"]["posture"] == "neutral"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_report.py::test_report_envelope -v`
Expected: FAIL with `ModuleNotFoundError: tscli.reports`.

- [ ] **Step 3: Write minimal implementation**

```python
# src/tscli/reports.py
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class ReportGenerator:
    output_dir: str | Path = "reports"
    schema_version: str = "1.0"

    def __post_init__(self):
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _now(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    def build_envelope(
        self,
        skill: str,
        data: dict,
        metadata: dict | None = None,
    ) -> dict:
        return {
            "schema_version": self.schema_version,
            "skill": skill,
            "metadata": {
                "run_at": datetime.now(timezone.utc).isoformat(),
                "data_sources": [],
                **(metadata or {}),
            },
            "data": data,
        }

    def write(
        self,
        skill: str,
        data: dict,
        metadata: dict | None = None,
    ) -> tuple[str, str]:
        envelope = self.build_envelope(skill, data, metadata)
        ts = self._now()
        base = f"{skill}_{ts}"
        json_path = self.output_dir / f"{base}.json"
        md_path = self.output_dir / f"{base}.md"

        with open(json_path, "w") as f:
            json.dump(envelope, f, indent=2, sort_keys=True)

        with open(md_path, "w") as f:
            f.write(f"# {skill} report\n\n")
            f.write(f"- **Run at:** {envelope['metadata']['run_at']}\n")
            f.write(f"- **Data sources:** {', '.join(envelope['metadata']['data_sources']) or 'none'}\n\n")
            f.write("```json\n")
            f.write(json.dumps(envelope, indent=2, sort_keys=True))
            f.write("\n```\n")

        return str(json_path), str(md_path)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_report.py::test_report_envelope -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/tscli/reports.py tests/test_report.py reports/.gitkeep
git commit -m "feat(reports): add JSON + Markdown report envelope"
```

---

### Task 3: Broker adapter base and manual adapter

**Files:**
- Create: `src/tscli/brokers/base.py`
- Create: `src/tscli/brokers/manual.py`
- Create: `src/tscli/brokers/__init__.py`
- Create: `tests/test_broker_manual.py`

**Interfaces:**
- Produces: `BrokerAdapter` protocol with `name()`, `is_connected()`, `get_positions()`, `get_account()`.
- Produces: `ManualBrokerAdapter` returns empty positions/account.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_broker_manual.py
from tscli.brokers.manual import ManualBrokerAdapter


def test_manual_adapter_name():
    adapter = ManualBrokerAdapter()
    assert adapter.name() == "manual"
    assert adapter.is_connected() is True
    assert adapter.get_positions() == []
    account = adapter.get_account()
    assert account.cash == 0.0
    assert account.equity == 0.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_broker_manual.py::test_manual_adapter_name -v`
Expected: FAIL with import errors.

- [ ] **Step 3: Write minimal implementation**

```python
# src/tscli/brokers/base.py
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Position:
    symbol: str
    qty: float
    avg_entry_price: float
    current_price: float
    market_value: float


@dataclass(frozen=True)
class AccountSummary:
    cash: float
    equity: float
    buying_power: float
    portfolio_value: float


@dataclass(frozen=True)
class Bar:
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class BrokerAdapter(Protocol):
    def name(self) -> str: ...
    def is_connected(self) -> bool: ...
    def get_positions(self) -> list[Position]: ...
    def get_account(self) -> AccountSummary: ...
    def get_historical_bars(self, symbol: str, bar_size: str, lookback_days: int) -> list[Bar]: ...
```

```python
# src/tscli/brokers/__init__.py
from tscli.brokers.base import AccountSummary, Bar, BrokerAdapter, Position
from tscli.brokers.manual import ManualBrokerAdapter

__all__ = ["AccountSummary", "Bar", "BrokerAdapter", "ManualBrokerAdapter", "Position"]
```

```python
# src/tscli/brokers/manual.py
from tscli.brokers.base import AccountSummary, Position


class ManualBrokerAdapter:
    def name(self) -> str:
        return "manual"

    def is_connected(self) -> bool:
        return True

    def get_positions(self) -> list[Position]:
        return []

    def get_account(self) -> AccountSummary:
        return AccountSummary(cash=0.0, equity=0.0, buying_power=0.0, portfolio_value=0.0)

    def get_historical_bars(self, symbol: str, bar_size: str, lookback_days: int) -> list:
        return []
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_broker_manual.py::test_manual_adapter_name -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/tscli/brokers/ tests/test_broker_manual.py
git commit -m "feat(brokers): add BrokerAdapter protocol and manual fallback"
```

---

### Task 4: `tscli broker check` command

**Files:**
- Create: `src/tscli/commands/broker.py`
- Create: `src/tscli/commands/__init__.py`
- Modify: `src/tscli/cli.py` to wire `broker check`
- Create: `src/tscli/config.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: `ManualBrokerAdapter`, `ReportGenerator`, `config.load_broker_config()`.
- Produces: `tscli broker check --broker manual` prints connection status and writes a report.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_cli.py
import json
import subprocess
import sys
import tempfile


def test_broker_check_manual():
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [
                sys.executable, "-m", "tscli",
                "broker", "check",
                "--broker", "manual",
                "--output-dir", tmp,
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        files = list(Path(tmp).glob("*.json"))
        assert len(files) == 1
        payload = json.loads(files[0].read_text())
        assert payload["skill"] == "broker-check"
        assert payload["data"]["adapter"] == "manual"
        assert payload["data"]["connected"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_cli.py::test_broker_check_manual -v`
Expected: FAIL with unrecognized arguments.

- [ ] **Step 3: Write minimal implementation**

```python
# src/tscli/config.py
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class BrokerConfig:
    broker: str
    opend_host: str = "127.0.0.1"
    opend_port: int = 11111
    ibkr_host: str = "127.0.0.1"
    ibkr_port: int = 7496
    ibkr_client_id: int = 1


def load_broker_config(args) -> BrokerConfig:
    return BrokerConfig(
        broker=getattr(args, "broker", None) or os.getenv("TSCLI_BROKER", "manual"),
        opend_host=os.getenv("TSCLI_OPEND_HOST", "127.0.0.1"),
        opend_port=int(os.getenv("TSCLI_OPEND_PORT", "11111")),
        ibkr_host=os.getenv("TSCLI_IBKR_HOST", "127.0.0.1"),
        ibkr_port=int(os.getenv("TSCLI_IBKR_PORT", "7496")),
        ibkr_client_id=int(os.getenv("TSCLI_IBKR_CLIENT_ID", "1")),
    )
```

```python
# src/tscli/commands/__init__.py
from tscli.commands import broker, market

__all__ = ["broker", "market"]
```

```python
# src/tscli/commands/broker.py
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
    if cfg.broker == "manual":
        return cls()
    # Stubs for opend/ibkr return manual-like fallback in Phase 1
    return cls()


def handle(args) -> int:
    cfg = load_broker_config(args)
    adapter = resolve_adapter(cfg)

    if args.broker_command == "check":
        connected = adapter.is_connected()
        data = {"adapter": adapter.name(), "connected": connected}
        gen = ReportGenerator(output_dir=args.output_dir)
        json_path, md_path = gen.write("broker-check", data, metadata={"broker_adapter": adapter.name()})
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
        json_path, md_path = gen.write("broker-positions", data, metadata={"broker_adapter": adapter.name()})
        print(f"Report: {json_path}")
        return 0

    return 1
```

Modify `src/tscli/cli.py`:

```python
import argparse
import sys

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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_cli.py::test_broker_check_manual -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/tscli/cli.py src/tscli/config.py src/tscli/commands/broker.py tests/test_cli.py
git commit -m "feat(broker): add broker check command with manual adapter"
```

---

### Task 5: `tscli market regime` skeleton command

**Files:**
- Create: `src/tscli/commands/market.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Produces: `tscli market regime --output-dir <dir>` writes a report with posture, breadth, trend, top signals.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_cli.py
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def test_market_regime_manual():
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [sys.executable, "-m", "tscli", "market", "regime", "--output-dir", tmp],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        files = list(Path(tmp).glob("*.json"))
        assert len(files) == 1
        payload = json.loads(files[0].read_text())
        assert payload["skill"] == "market-regime"
        assert "posture" in payload["data"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_cli.py::test_market_regime_manual -v`
Expected: FAIL with unrecognized arguments.

- [ ] **Step 3: Write minimal implementation**

```python
# src/tscli/commands/market.py
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
        json_path, md_path = gen.write(
            "market-regime",
            data,
            metadata={"data_sources": ["skeleton"], "broker_adapter": "manual"},
        )
        print(f"Regime report: {json_path}", file=sys.stderr)
        print(f"Posture: {data['posture']}")
        return 0
    return 1
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_cli.py::test_market_regime_manual -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/tscli/commands/market.py tests/test_cli.py
git commit -m "feat(market): add market regime skeleton command"
```

---

### Task 6: Linting and test harness

**Files:**
- Create: `.pre-commit-config.yaml`
- Create: `scripts/run_all_tests.sh`
- Modify: `pyproject.toml` (add pytest config if missing)

**Interfaces:**
- Produces: `bash scripts/run_all_tests.sh` exits 0; `ruff check src tests` exits 0.

- [ ] **Step 1: Write the failing test / lint check**

```bash
uv run ruff check src tests
```
Expected: may fail on missing newline or style issues.

- [ ] **Step 2: Fix any lint issues**

Run `uv run ruff format src tests` and `uv run ruff check --fix src tests` until clean.

- [ ] **Step 3: Add test runner script**

```bash
# scripts/run_all_tests.sh
#!/bin/bash
set -euo pipefail
uv run ruff check src tests
uv run ruff format --check src tests
uv run pytest -q
```

Make executable:

```bash
chmod +x scripts/run_all_tests.sh
```

- [ ] **Step 4: Verify full suite passes**

Run: `bash scripts/run_all_tests.sh`
Expected: All tests pass, ruff clean.

- [ ] **Step 5: Commit**

```bash
git add scripts/run_all_tests.sh .pre-commit-config.yaml pyproject.toml
git commit -m "chore(ci): add ruff, pytest, and test runner"
```

---

## Self-Review

1. **Spec coverage:**
   - CLI scaffold and entry point: Task 1.
   - Report envelope: Task 2.
   - Broker adapter abstraction + manual fallback: Task 3.
   - `broker check` command: Task 4.
   - `market regime` skeleton: Task 5.
   - Quality gates: Task 6.

2. **Placeholder scan:** No TBD/TODO/fill-in-details. The `market regime` command uses synthetic signals explicitly labeled `data_quality: skeleton` and is scheduled for replacement in Phase 2.

3. **Type consistency:** `BrokerAdapter` protocol, `ManualBrokerAdapter`, and report generator all use the same `Position`, `AccountSummary`, and envelope shape defined in the spec.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-07-09-kimi-trading-skills-phase1.md`.

Two execution options:

1. **Subagent-Driven (recommended)** — dispatch a fresh subagent per task, review between tasks.
2. **Inline Execution** — execute tasks in this session using `superpowers:executing-plans`.
