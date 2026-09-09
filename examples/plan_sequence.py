import json
from pathlib import Path

from orchestrator.dry_run import DryRunPlanner


if __name__ == "__main__":
    manifest_path = Path(__file__).with_name("first_autonomous_sequence.json")
    manifest = json.loads(manifest_path.read_text())
    plan = DryRunPlanner().plan(manifest)
    print(json.dumps(plan, indent=2))
