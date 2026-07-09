# AGENTS.md

Guidelines for AI agents working on `trading_skills`.

## Project

Code-first trading assistant for Kimi Code CLI.
- Python CLI: `tscli` in `src/tscli/`
- Kimi skill: `skills/kimi-trading-skills/`
- Design docs: `docs/superpowers/`
- User docs: `docs/user/`

## Tech stack

- Python >= 3.9, managed with `uv`
- `argparse` for CLI commands
- `pytest`, `ruff` for tests and lint
- Reports: JSON + Markdown under `reports/`

## Commands

```bash
# Install dependencies
uv sync --extra dev

# Run all checks and tests
bash scripts/run_all_tests.sh

# Run a CLI command
uv run tscli --help
uv run tscli broker check --broker manual
uv run tscli market regime
```

## Code conventions

- Line length: 100 (`ruff`)
- Target Python: 3.9
- Use type hints where reasonable.
- Keep CLI commands deterministic; LLM judgement lives in prompts under `references/prompts/`.
- Every CLI writes a JSON report with envelope `{schema_version, skill, metadata, data}`.

## Documentation rules

- Markdown only, GitHub-flavored.
- Use Mermaid for diagrams; no ASCII charts.
- Validate Mermaid syntax with `mmdc` before committing.

## Constraints

- Supported brokers: Futubull OpenD, IB Gateway, and `manual` fallback.
- No Finviz or FMP subscriptions; use `yfinance`, broker data, public CSVs, web search, and LLM.
- No live order execution. Emit order templates and analysis only.

## Safety

- Default broker mode is `manual` when credentials are missing.
- Respect workflow `decision_gate` steps; do not auto-approve.
- Never hard-code credentials; use environment variables.

## Git

- Do not commit or push unless explicitly asked.
- Keep commits small and focused.
