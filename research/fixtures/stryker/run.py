#!/usr/bin/env python3
"""Reproduce the StrykerJS 10.1.1 gate checks in research/stryker.md.

Requires Node.js >= 22, npm, git and uv (for diff-cover). The first run installs
the pinned npm packages from app/package.json into the output directory.

The base commit is app/ plus FILLER generated modules with strong tests. The pull
request adds pr/discount.js with either pr/weak.test.js or pr/strong.test.js.

    python3 research/fixtures/stryker/run.py /tmp/stryker-results

real.py measures the same gate on a real project.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent
OUTPUT = Path(sys.argv[1]).resolve()
if OUTPUT.exists() and any(OUTPUT.iterdir()):
    raise SystemExit("Use an empty output directory")
OUTPUT.mkdir(parents=True, exist_ok=True)
WORK = OUTPUT / "work"
FILLER = 30
DIFF_COVER = os.environ.get("DIFF_COVER")
diff_cover = [DIFF_COVER] if DIFF_COVER else ["uvx", "diff-cover==11.0.1"]
summary = []


def sh(args, check=True):
    result = subprocess.run(args, cwd=WORK, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise SystemExit(f"{args}: exit {result.returncode}\n{result.stdout}{result.stderr}")
    return result


def score():
    report = json.loads((WORK / "reports/mutation/mutation.json").read_text())
    counts = {}
    for entry in report["files"].values():
        for mutant in entry["mutants"]:
            counts[mutant["status"]] = counts.get(mutant["status"], 0) + 1
    detected = counts.get("Killed", 0) + counts.get("Timeout", 0)
    undetected = counts.get("Survived", 0) + counts.get("NoCoverage", 0)
    total = detected + undetected
    return counts, round(100 * detected / total, 2) if total else None


def case(name, args, expected, mutation=False):
    if mutation:
        shutil.rmtree(WORK / "reports/mutation", ignore_errors=True)
    started = time.monotonic()
    result = sh(args, check=False)
    seconds = round(time.monotonic() - started, 1)
    (OUTPUT / f"{name}.stdout").write_text(result.stdout)
    (OUTPUT / f"{name}.stderr").write_text(result.stderr)
    row = {"case": name, "exit": result.returncode, "seconds": seconds, "command": args}
    if mutation and (WORK / "reports/mutation/mutation.json").exists():
        row["mutants"], row["score"] = score()
    summary.append(row)
    print(json.dumps(row), flush=True)
    if result.returncode != expected:
        raise SystemExit(f"{name}: exit {result.returncode}, expected {expected}")
    return result


def commit(message):
    sh(["git", "add", "-A"])
    sh(["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-q", "-m", message])


def changed_sources():
    names = sh(["git", "diff", "--name-only", "--diff-filter=AM", "main...HEAD", "--", "src/"])
    return names.stdout.split()


shutil.copytree(FIXTURES / "app", WORK)
(WORK / ".gitignore").write_text("node_modules/\ncoverage/\nreports/\n.stryker-tmp/\n")
source = (WORK / "src/price.js").read_text()
test = (WORK / "test/price.test.js").read_text()
for i in range(1, FILLER + 1):
    (WORK / f"src/price{i:02}.js").write_text(source.replace("function price", f"function price{i:02}"))
    (WORK / f"test/price{i:02}.test.js").write_text(
        test.replace("{ price }", f"{{ price{i:02} as price }}").replace("price.js", f"price{i:02}.js")
    )

sh(["npm", "install", "--no-audit", "--no-fund"])
versions = {
    "node": sh(["node", "--version"]).stdout.strip(),
    "stryker": sh(["npx", "stryker", "--version"]).stdout.strip(),
    "vitest": sh(["npx", "vitest", "--version"]).stdout.strip(),
    "diff-cover": sh([*diff_cover, "--version"]).stdout.strip(),
}
print(json.dumps(versions), flush=True)
if versions["stryker"] != "10.1.1":
    raise SystemExit(f"Expected StrykerJS 10.1.1, got {versions['stryker']}")

sh(["git", "init", "-q", "-b", "main"])
commit("base")

# Base branch: every module is tested properly. The incremental run seeds the file a CI cache would keep.
case("base-full", ["npx", "stryker", "run"], 0, mutation=True)
case("base-incremental-seed", ["npx", "stryker", "run", "--incremental"], 0, mutation=True)

# Pull request with a weak test: every line runs, only the return type is asserted.
sh(["git", "switch", "-q", "-c", "weak"])
shutil.copy(FIXTURES / "pr/discount.js", WORK / "src/discount.js")
shutil.copy(FIXTURES / "pr/weak.test.js", WORK / "test/discount.test.js")
commit("add discount with a weak test")
changed = changed_sources()
if changed != ["src/discount.js"]:
    raise SystemExit(f"Unexpected changed sources: {changed}")

case("weak-coverage", ["npx", "vitest", "run", "--coverage"], 0)
case("weak-diff-cover",
     [*diff_cover, "coverage/cobertura-coverage.xml", "--compare-branch=main", "--fail-under=100"], 0)
case("weak-full", ["npx", "stryker", "run"], 0, mutation=True)
case("weak-incremental", ["npx", "stryker", "run", "--incremental"], 0, mutation=True)
case("weak-changed-files", ["npx", "stryker", "run", "--mutate", ",".join(changed)], 1, mutation=True)

# The same pull request with real assertions passes the changed-files gate.
sh(["git", "switch", "-q", "-c", "strong", "main"])
shutil.copy(FIXTURES / "pr/discount.js", WORK / "src/discount.js")
shutil.copy(FIXTURES / "pr/strong.test.js", WORK / "test/discount.test.js")
commit("add discount with a strong test")
case("strong-changed-files", ["npx", "stryker", "run", "--mutate", ",".join(changed_sources())], 0,
     mutation=True)

# A mutation range scores only the mutants inside it. price.js keeps one surviving mutant on
# line 3 (the error message is never asserted); a range over line 5 leaves it out.
sh(["git", "switch", "-q", "main"])
case("range-whole-file", ["npx", "stryker", "run", "--mutate", "src/price.js"], 0, mutation=True)
case("range-line-5", ["npx", "stryker", "run", "--mutate", "src/price.js:5-5"], 0, mutation=True)

# Run under the vitest runner's default related-tests mode, a pattern that matches no file fails with "No tests were executed", so a CI step must skip
# Stryker itself when a pull request changes no source file.
case("no-match", ["npx", "stryker", "run", "--mutate", "src/missing.js"], 1, mutation=True)

(OUTPUT / "summary.json").write_text(json.dumps({"versions": versions, "cases": summary}, indent=2) + "\n")
