# Broker Capability Matrix

This matrix describes what each supported broker adapter provides in `tscli`.

| Capability | Futubull OpenD | IB Gateway | Manual |
|------------|----------------|------------|--------|
| Account summary | Yes | Yes | Fixture only |
| Positions | Yes | Yes | Empty / fixture |
| Historical EOD bars | Yes | Yes | `yfinance` fallback |
| Intraday bars | Yes (limited) | Yes | No |
| Option chain | Partial | Yes | No |
| Order placement | **Not implemented** | **Not implemented** | N/A |
| Short inventory / locate | Manual note only | Manual note only | Default deny |

## Futubull OpenD notes

- OpenD must be running on the local machine before any command is executed.
- Default connection: `127.0.0.1:11111`.
- Requires a funded Futubull/Moomoo account and appropriate market-data subscription.
- Historical data availability depends on the account's subscription level.

## IB Gateway notes

- IB Gateway must be running and API connections enabled.
- Default connection: `127.0.0.1:7496`, client ID `1`.
- Requires a NASDAQ data subscription for US equity analysis.
- Historical bar requests are subject to IB pacing rules; the adapter caches results.

## Manual fallback

- Used when credentials are missing or when the user explicitly sets `--broker manual`.
- Returns empty positions unless a fixture file is supplied.
- Relies on `yfinance` and public CSVs for market analysis.
