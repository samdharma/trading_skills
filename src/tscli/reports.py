import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class ReportGenerator:
    output_dir: str | Path = "reports"
    schema_version: str = "1.0"

    def __post_init__(self):
        self.output_dir = Path(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _now(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    def build_envelope(
        self,
        skill: str,
        data: dict,
        metadata: dict | None = None,
    ) -> dict:
        return {
            "schema_version": self.schema_version,
            "skill": skill,
            "metadata": {
                "run_at": datetime.now(timezone.utc).isoformat(),
                "data_sources": [],
                **(metadata or {}),
            },
            "data": data,
        }

    def write(
        self,
        skill: str,
        data: dict,
        metadata: dict | None = None,
    ) -> tuple[str, str]:
        envelope = self.build_envelope(skill, data, metadata)
        ts = self._now()
        base = f"{skill}_{ts}"
        json_path = self.output_dir / f"{base}.json"
        md_path = self.output_dir / f"{base}.md"

        with open(json_path, "w") as f:
            json.dump(envelope, f, indent=2, sort_keys=True)

        with open(md_path, "w") as f:
            f.write(f"# {skill} report\n\n")
            f.write(f"- **Run at:** {envelope['metadata']['run_at']}\n")
            sources = ", ".join(envelope["metadata"]["data_sources"]) or "none"
            f.write(f"- **Data sources:** {sources}\n\n")
            f.write("```json\n")
            f.write(json.dumps(envelope, indent=2, sort_keys=True))
            f.write("\n```\n")

        return str(json_path), str(md_path)
