# Safety

Kimi Trading Skills is intentionally conservative: it emits analysis, checklists, and order templates, but it **never** places live orders.

## Core safety rules

1. **No live order execution.** The skill does not call broker APIs to place, modify, or cancel orders.
2. **Manual confirmation required.** Every order template is emitted with `requires_manual_confirmation: true`.
3. **Decision gates pause.** When a workflow declares `decision_gate: true`, the skill stops and waits for your explicit approval.
4. **Default to manual mode.** If no broker credentials are set, commands fall back to `manual` mode.
5. **No hard-coded credentials.** API keys and broker credentials are read from environment variables only.

## What the skill can do

- Fetch market data and broker positions.
- Run screens and generate reports.
- Calculate position sizes and write order templates.
- Create, list, and close journal theses.
- Ask you for approval at decision gates.

## What the skill cannot do

- Place, modify, or cancel orders.
- Auto-approve workflow steps.
- Store credentials in files.

## Order templates

An order template is a structured recommendation, not an executed trade. It includes:

- Symbol, side, quantity, and price
- Stop loss and target levels
- Risk amount and position size rationale
- `requires_manual_confirmation: true`

You must copy the details into your broker platform to execute the trade.

## Data provenance

Kimi cites the source of every number it reports, such as:

- `yfinance`
- `opend`
- `ibkr`
- `public_csv`
- `llm`

This lets you verify conclusions independently.
