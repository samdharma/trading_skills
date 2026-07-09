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
