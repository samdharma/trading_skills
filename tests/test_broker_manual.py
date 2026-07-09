from tscli.brokers.manual import ManualBrokerAdapter


def test_manual_adapter_name():
    adapter = ManualBrokerAdapter()
    assert adapter.name() == "manual"
    assert adapter.is_connected() is True
    assert adapter.get_positions() == []
    account = adapter.get_account()
    assert account.cash == 0.0
    assert account.equity == 0.0
