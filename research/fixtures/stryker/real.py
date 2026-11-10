#!/usr/bin/env python3
"""Measure a changed-files StrykerJS 10.1.1 run on a real vitest project: unjs/ufo v1.6.4.

Requires git, Node.js >= 22 and pnpm. Clones ufo at a pinned commit into the output
directory, installs with lifecycle scripts disabled, adds the Stryker packages and
mutates one source file at a time, the way a pull request that touched it would.

    python3 research/fixtures/stryker/real.py /tmp/stryker-real
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

OUTPUT = Path(sys.argv[1]).resolve()
if OUTPUT.exists() and any(OUTPUT.iterdir()):
    raise SystemExit("Use an empty output directory")
OUTPUT.mkdir(parents=True, exist_ok=True)
WORK = OUTPUT / "ufo"
COMMIT = "f06c800d0c59f2a4a1b9ba65eb6cb61a84419be6"  # tag v1.6.4
FILES = ["src/parse.ts", "src/utils.ts"]
summary = {"repo": "unjs/ufo", "commit": COMMIT, "cpus": os.cpu_count(), "cases": []}


def sh(args, check=True):
    result = subprocess.run(args, cwd=WORK, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit(f"{args}: exit {result.returncode}\n{result.stdout}{result.stderr}")
    return result


def timed(name, args):
    started = time.monotonic()
    result = sh(args, check=False)
    seconds = round(time.monotonic() - started, 1)
    (OUTPUT / f"{name}.stdout").write_text(result.stdout)
    (OUTPUT / f"{name}.stderr").write_text(result.stderr)
    row = {"case": name, "exit": result.returncode, "seconds": seconds, "command": args}
    summary["cases"].append(row)
    return row


subprocess.run(["git", "clone", "-q", "https://github.com/unjs/ufo.git", str(WORK)], check=True)
sh(["git", "checkout", "-q", COMMIT])
sh(["pnpm", "install", "--frozen-lockfile", "--ignore-scripts"])
sh(["pnpm", "add", "-D", "--ignore-scripts",
    "@stryker-mutator/core@10.1.1", "@stryker-mutator/vitest-runner@10.1.1"])
summary["vitest"] = sh(["pnpm", "exec", "vitest", "--version"]).stdout.strip()

row = timed("suite", ["pnpm", "exec", "vitest", "run"])
print(json.dumps(row), flush=True)
if row["exit"] != 0:
    raise SystemExit("The plain test suite failed")

# Thresholds have no CLI flag, so they go in a config file, as they would in a project.
# Under pnpm the default plugin lookup failed with 'Cannot find TestRunner plugin "vitest"',
# so the runner plugin is named explicitly.
(WORK / "stryker.config.json").write_text(json.dumps({
    "plugins": ["@stryker-mutator/vitest-runner"],
    "testRunner": "vitest",
    "reporters": ["clear-text", "json"],
    "thresholds": {"high": 90, "low": 80, "break": 80},
}))
report = WORK / "reports/mutation/mutation.json"
for path in FILES:
    name = Path(path).stem
    report.unlink(missing_ok=True)
    row = timed(name, ["pnpm", "exec", "stryker", "run", "--mutate", path])
    if not report.exists():
        raise SystemExit(f"{name}: no report, exit {row['exit']}; see {name}.stdout")
    (OUTPUT / f"{name}.json").write_text(report.read_text())
    data = json.loads(report.read_text())
    counts = {}
    tests_per_mutant = []
    for entry in data["files"].values():
        for mutant in entry["mutants"]:
            counts[mutant["status"]] = counts.get(mutant["status"], 0) + 1
            tests_per_mutant.append(len(mutant.get("coveredBy") or []))
    detected = counts.get("Killed", 0) + counts.get("Timeout", 0)
    undetected = counts.get("Survived", 0) + counts.get("NoCoverage", 0)
    row["lines"] = len((WORK / path).read_text().splitlines())
    row["mutants"] = counts
    row["score"] = round(100 * detected / (detected + undetected), 2)
    row["covering_tests_per_mutant"] = round(sum(tests_per_mutant) / len(tests_per_mutant), 1)
    print(json.dumps(row), flush=True)

(OUTPUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
