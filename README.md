# Kimi Trading Skills

A code-first, CLI-driven trading assistant for Kimi Code CLI, ported from [Claude Trading Skills](https://tradermonty.github.io/claude-trading-skills/en/).

It is built around a Python CLI called `tscli` and a Kimi skill that tells the agent which commands to run. All analysis outputs are JSON + Markdown reports, and LLM prompts are stored as external markdown templates.

## Supported brokers and data

- **Futubull via OpenD** (Moomoo-compatible)
- **Interactive Brokers via IB Gateway** (NASDAQ data subscription)
- **Manual / fixture mode** for offline use
- **No Finviz or FMP subscription required** — replaced by `yfinance`, broker data, public CSVs, web search, and LLM reasoning

## Install on another Mac

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/trading_skills.git
cd trading_skills

# 2. Run the install script (needs uv: https://docs.astral.sh/uv/)
bash scripts/install-kimi-skill.sh
```

The script:
- installs Python dependencies with `uv sync --extra dev`,
- symlinks the skill into `~/.kimi-code/skills/kimi-trading-skills`.

Then start Kimi with the skill loaded:

```bash
# From any directory
kimi --skills-dir ~/.kimi-code/skills

# Or from the repo root
kimi --skills-dir ./skills
```

## Quick start

Inside a Kimi session you can ask things like:

- "Run a daily market regime check."
- "Check my broker connection in manual mode."
- "Show my positions."

Those requests map to `tscli` commands the agent executes:

```bash
uv run tscli broker check --broker manual --output-dir reports/
uv run tscli market regime --output-dir reports/
uv run tscli broker positions --broker manual --output-dir reports/
```

Additional commands such as `screen momentum`, `portfolio analyze`, and `trade plan` are on the roadmap.

Every command writes timestamped JSON and Markdown reports under `reports/`.

## Documentation

- **User docs:** `docs/user/README.md`
- **Getting started:** `docs/user/getting-started.md`
- **Design spec:** `docs/superpowers/specs/2026-07-09-kimi-trading-skills-design.md`

## Project layout

```
.
├── src/tscli/              # Python CLI implementation
├── skills/kimi-trading-skills/   # Kimi skill file + references + workflows
├── docs/user/                    # User documentation
├── docs/superpowers/specs/       # Design specification
├── docs/superpowers/plans/       # Implementation plans
├── pyproject.toml
└── scripts/
    ├── install-kimi-skill.sh
    └── run_all_tests.sh
```

## Tests

```bash
bash scripts/run_all_tests.sh
```

This runs `ruff check`, `ruff format --check`, and `pytest`.

## Safety note

This tool emits analysis, checklists, and order templates only. It does **not** place, modify, or cancel orders.
