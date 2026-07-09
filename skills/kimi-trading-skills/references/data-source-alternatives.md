# Data-Source Alternatives

The original *Claude Trading Skills* relies heavily on **Financial Modeling Prep (FMP)** and optionally **Finviz**. This project removes both. The table below maps each dropped source to the replacement used by `tscli`.

| Original source | Used for | Replacement | Notes |
|-----------------|----------|-------------|-------|
| FMP EOD prices | Price history, quote | `yfinance` | Free, unofficial Yahoo Finance wrapper. |
| FMP company profile | Sector, market cap, industry | `yfinance` `.info` | Cached per run. |
| FMP earnings calendar | Earnings dates | `yfinance` earnings + web search | Less complete; web search fills gaps. |
| FMP income statement | EPS / revenue growth | `yfinance` fundamentals | Available for most US equities. |
| FMP S&P 500 constituents | Universe definition | Static JSON snapshot + `yfinance` | Updated manually or via public source. |
| FMP institutional holders | Holder trends | Web search / broker data | Not available for all tickers. |
| FMP treasury rates | Yield curve | Public CSV (e.g., FRED) | Downloaded on demand. |
| Finviz screener | Filter-based screening | `yfinance`-based screeners | Re-implement common filters in Python. |
| Finviz news / sentiment | News aggregation | Web search + LLM summarization | No Finviz Elite required. |
| Alpaca (original) | Broker data, short inventory | Futubull OpenD / IB Gateway | User's funded brokers. |

## Fallback chain

For any data request, `tscli` tries sources in this order:

1. **Broker adapter** (OpenD / IB Gateway) if connected.
2. **`yfinance`** for price, fundamentals, and earnings.
3. **Public CSV / web search** for macro and breadth data.
4. **Fixture / manual mode** if all else fails, with a clear caveat in the report.

## Limitations

- `yfinance` is rate-limited and unofficial. Do not use it for high-frequency decisions.
- Free data may lag or miss small-cap / delisted securities.
- When data is missing, the report must record `data_quality: partial` and explain the gap.
