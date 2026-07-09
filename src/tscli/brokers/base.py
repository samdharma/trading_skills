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
