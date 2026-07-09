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
