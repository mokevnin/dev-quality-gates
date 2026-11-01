#!/usr/bin/env python3
"""Reproduce mermaid-lint 0.53.1 on the fixtures in this directory.

Requires Node.js >= 22. The first run downloads @mermaid-lint/cli@0.53.1.
Set MERMAID_LINT to an already installed mermaid-lint binary to skip npx.

    python3 research/fixtures/mermaid/run.py /tmp/mermaid-results
"""

import json
import os
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent
OUTPUT = Path(sys.argv[1]).resolve()
if OUTPUT.exists() and any(OUTPUT.iterdir()):
    raise SystemExit("Use an empty output directory")
OUTPUT.mkdir(parents=True, exist_ok=True)

binary = os.environ.get("MERMAID_LINT")
command_prefix = [binary] if binary else ["npx", "--yes", "@mermaid-lint/cli@0.53.1"]


def run(args, cwd=FIXTURES):
    result = subprocess.run(
        [*command_prefix, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result


clean = run(["--format", "json", "clean.md"])
report = json.loads(clean.stdout)
version = report["version"]
print(f"mermaid-lint {version}", flush=True)
if version != "0.53.1":
    raise SystemExit(f"Expected 0.53.1, got {version}")

cases = [
    ("clean", ["--format", "json", "clean.md"], 0),
    ("legacy", ["--format", "json", "legacy.md"], 0),
    ("legacy-strict", ["--strict", "--quiet", "legacy.md"], 1),
    ("broken", ["--format", "json", "broken.md"], 1),
    ("prose", ["--quiet", "prose.md"], 0),
    ("missing", ["does-not-exist.md"], 2),
]
summary = []
for name, args, expected in cases:
    result = run(args) if name != "clean" else clean
    (OUTPUT / f"{name}.stdout").write_text(result.stdout)
    (OUTPUT / f"{name}.stderr").write_text(result.stderr)
    summary.append({"case": name, "exit": result.returncode, "command": [*command_prefix, *args]})
    print(name, result.returncode, flush=True)
    if result.returncode != expected:
        raise SystemExit(f"{name}: exit {result.returncode}, expected {expected}")

broken_report = json.loads((OUTPUT / "broken.stdout").read_text())
if broken_report["summary"]["errors"] != 1:
    raise SystemExit("broken.md did not report exactly one error")

fix_dir = OUTPUT / "fix"
fix_dir.mkdir()
# Kept out of the fixture tree: an unclosed fence fails this repo's own rumdl check.
(fix_dir / "unclosed.md").write_text("# Unclosed fence\n\n```mermaid\nflowchart TD\n  A-->B\n")
fixed = run(["--fix", "--quiet", "unclosed.md"], cwd=fix_dir)
print("fix", fixed.returncode, flush=True)
if fixed.returncode != 0:
    raise SystemExit(f"fix: exit {fixed.returncode}")
if not (fix_dir / "unclosed.md").read_text().rstrip().endswith("```"):
    raise SystemExit("fix did not close the fence")
summary.append({"case": "fix", "exit": fixed.returncode, "command": [*command_prefix, "--fix", "--quiet", "unclosed.md"]})
(OUTPUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
