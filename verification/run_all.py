"""Run scientific diagnostics; optional JSON report records the actual outputs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write the complete JSON report")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    reports = {}
    for name in ("check_pair_sampler.py", "check_channels.py"):
        completed = subprocess.run(
            [sys.executable, str(root / name)],
            check=True, capture_output=True, text=True,
        )
        reports[name] = json.loads(completed.stdout)
    report = {
        "scope": "Finite scientific diagnostics; see analytic proofs for asymptotic and diamond-norm claims.",
        "status": "pass",
        "checks": reports,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
