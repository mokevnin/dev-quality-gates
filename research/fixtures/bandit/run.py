#!/usr/bin/env python3
"""Compare Bandit and Ruff without executing the scanned Python files.

Requires uv and network on the first run. Use an empty output directory:
    python3 research/fixtures/bandit/run.py /tmp/bandit-results
"""

import json
import subprocess
import sys
from pathlib import Path

fixtures = Path(__file__).resolve().parent
output = Path(sys.argv[1]).resolve()
output.mkdir(parents=True, exist_ok=True)
if any(output.iterdir()):
    raise SystemExit("Use an empty output directory")

bandit = ["uv", "tool", "run", "--from", "bandit==1.9.4", "bandit"]
ruff = ["uv", "tool", "run", "--from", "ruff==0.17.4", "ruff"]
for command in (bandit, ruff):
    subprocess.run([*command, "--version"], check=True)

for name, bandit_ids, ruff_ids in (
    ("unsafe", {"B614", "B615"}, set()),
    ("safe", set(), set()),
    ("overlap", {"B307"}, {"S307"}),
):
    for tool, command, expected in (
        ("bandit", [*bandit, "-f", "json"], bandit_ids),
        ("ruff", [*ruff, "check", "--isolated", "--no-cache", "--preview",
                  "--select", "S", "--output-format", "json"], ruff_ids),
    ):
        result = subprocess.run(
            [*command, str(fixtures / f"{name}.py")],
            cwd=output, capture_output=True, text=True,
        )
        (output / f"{name}-{tool}.json").write_text(result.stdout)
        (output / f"{name}-{tool}.stderr").write_text(result.stderr)
        assert result.returncode == int(bool(expected)), (name, tool, result)
        report = json.loads(result.stdout)
        if tool == "bandit":
            assert report["errors"] == [], report["errors"]
            actual = {item["test_id"] for item in report["results"]}
        else:
            actual = {item["code"] for item in report}
        assert actual == expected, (name, tool, actual, expected)
        print(f"{name}: {tool} exits {result.returncode}, rules {sorted(actual)}")
