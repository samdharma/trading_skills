import json
import subprocess
import sys
import tempfile
from pathlib import Path


def test_cli_version():
    result = subprocess.run(
        [sys.executable, "-m", "tscli", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "0.1.0" in result.stdout


def test_broker_check_manual():
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "tscli",
                "broker",
                "check",
                "--broker",
                "manual",
                "--output-dir",
                tmp,
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
