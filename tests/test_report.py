import json
import tempfile
from pathlib import Path

from tscli.reports import ReportGenerator


def test_report_envelope():
    with tempfile.TemporaryDirectory() as tmp:
        gen = ReportGenerator(output_dir=tmp)
        json_path, md_path = gen.write(
            skill="market-regime",
            data={"posture": "neutral"},
            metadata={"run_at": "2026-07-09T09:30:00Z", "data_sources": ["yfinance"]},
        )
        assert Path(json_path).exists()
        assert Path(md_path).exists()
        with open(json_path) as f:
            payload = json.load(f)
        assert payload["schema_version"] == "1.0"
        assert payload["skill"] == "market-regime"
        assert payload["data"]["posture"] == "neutral"
