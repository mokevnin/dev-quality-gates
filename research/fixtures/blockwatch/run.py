#!/usr/bin/env python3
"""Compare blockwatch 0.22.0 against google/keep-sorted v0.11.0 and simonepri/ifttt-lint 0.11.3.

Requires Python 3, git, uv (for blockwatch-cli==0.22.0), plus keep-sorted v0.11.0
and ifttt-lint 0.11.3 on PATH. Use an empty output directory:

    python3 research/fixtures/blockwatch/run.py /tmp/blockwatch-results
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent
OUTPUT = Path(sys.argv[1]).resolve()
if OUTPUT.exists() and any(OUTPUT.iterdir()):
    raise SystemExit("Use an empty output directory")
OUTPUT.mkdir(parents=True, exist_ok=True)
WORK = OUTPUT / "work"

BW = ["uv", "tool", "run", "--from", "blockwatch-cli==0.22.0", "blockwatch"]
KS = ["keep-sorted"]
IFTTT = ["ifttt-lint"]


def sh(cmd, cwd, text=None):
    return subprocess.run(cmd, cwd=cwd, input=text, capture_output=True, text=True)


def check_version(cmd, expected):
    out = sh([*cmd, "--version"], OUTPUT).stdout.strip()
    print(out, flush=True)
    if expected not in out:
        raise SystemExit(f"Expected {expected!r} from {cmd}, got {out!r}")


def commit(repo, message):
    if not (repo / ".git").exists():
        sh(["git", "init", "-q"], repo)
    sh(["git", "add", "."], repo)
    sh(["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-q", "-m", message], repo)


summary = []


def expect(name, cmd, cwd, code, text=None):
    res = sh(cmd, cwd, text=text)
    (OUTPUT / f"{name}.stdout").write_text(res.stdout)
    (OUTPUT / f"{name}.stderr").write_text(res.stderr)
    summary.append({"case": name, "exit": res.returncode})
    print(f"{name}: exit={res.returncode}", flush=True)
    if res.returncode != code:
        raise SystemExit(f"{name}: exit {res.returncode}, expected {code}\n{res.stdout}{res.stderr}")
    return res


check_version(BW, "blockwatch 0.22.0")
check_version(KS, "167f8ca")
check_version(IFTTT, "ifttt-lint 0.11.3")

# 1. Cross-file value sync without a diff (`same-as` + commentless JSON via blockwatch.toml)
sync = WORK / "sync"
shutil.copytree(FIXTURES / "sync", sync)
commit(sync, "init synced port")

clean = expect("sync-clean-sarif", [*BW, "--format", "sarif"], sync, 0)
assert json.loads(clean.stderr)["runs"][0]["results"] == []

(sync / "app/settings.py").write_text("PORT = 9090\n")
commit(sync, "bump port only in settings.py")

drift = expect("sync-drift-json", BW, sync, 1)
assert set(json.loads(drift.stderr)) == {"Dockerfile", "deploy.json"}

drift_sarif = expect("sync-drift-sarif", [*BW, "--format", "sarif"], sync, 1)
assert len(json.loads(drift_sarif.stderr)["runs"][0]["results"]) == 2

expect("sync-drift-ifttt-lint", [*IFTTT, "--diff", "HEAD~1...HEAD", "--format", "json"], sync, 0)

# 2. Diff coupling (`affects` to a Markdown heading vs ifttt-lint LINT.IfChange comments)
bw_repo = WORK / "coupling-bw"
(bw_repo / "src").mkdir(parents=True)
(bw_repo / "docs").mkdir(parents=True)
(bw_repo / "src/roles.py").write_text('# <block name="roles" affects="docs/roles.md#/Roles">\nROLES = ["admin"]\n# </block>\n')
(bw_repo / "docs/roles.md").write_text("# Roles\n\n- admin\n")
commit(bw_repo, "init")

(bw_repo / "src/roles.py").write_text('# <block name="roles" affects="docs/roles.md#/Roles">\nROLES = ["admin", "editor"]\n# </block>\n')
commit(bw_repo, "edit code only")
diff1 = sh(["git", "diff", "--patch", "HEAD~1...HEAD"], bw_repo).stdout
expect("coupling-bw-fail", [*BW, "--diff"], bw_repo, 1, text=diff1)

(bw_repo / "docs/roles.md").write_text("# Roles\n\n- admin\n- editor\n")
commit(bw_repo, "update docs")
diff2 = sh(["git", "diff", "--patch", "HEAD~2...HEAD"], bw_repo).stdout
expect("coupling-bw-pass", [*BW, "--diff"], bw_repo, 0, text=diff2)

ifttt_repo = WORK / "coupling-ifttt"
(ifttt_repo / "src").mkdir(parents=True)
(ifttt_repo / "docs").mkdir(parents=True)
(ifttt_repo / "src/roles.py").write_text("# LINT.IfChange(roles)\nROLES = [\"admin\"]\n# LINT.ThenChange(//docs/roles.md:roles)\n")
(ifttt_repo / "docs/roles.md").write_text("# Roles\n\n<!-- LINT.IfChange(roles) -->\n- admin\n<!-- LINT.ThenChange(//src/roles.py:roles) -->\n")
commit(ifttt_repo, "init")

(ifttt_repo / "src/roles.py").write_text("# LINT.IfChange(roles)\nROLES = [\"admin\", \"editor\"]\n# LINT.ThenChange(//docs/roles.md:roles)\n")
commit(ifttt_repo, "edit code only")
expect("coupling-ifttt-fail", [*IFTTT, "--diff", "HEAD~1...HEAD", "--format", "json"], ifttt_repo, 1)
expect("coupling-ifttt-sarif", [*IFTTT, "--diff", "HEAD~1...HEAD", "--format", "sarif"], ifttt_repo, 2)

(ifttt_repo / "docs/roles.md").write_text("# Roles\n\n<!-- LINT.IfChange(roles) -->\n- admin\n- editor\n<!-- LINT.ThenChange(//src/roles.py:roles) -->\n")
commit(ifttt_repo, "update docs")
expect("coupling-ifttt-pass", [*IFTTT, "--diff", "HEAD~2...HEAD", "--format", "json"], ifttt_repo, 0)

# 3. Sorted and unique block (`blockwatch` check-only vs `keep-sorted` autofix)
sort_bw = WORK / "sort-bw"
sort_bw.mkdir()
(sort_bw / "items.py").write_text('# <block name="items" keep-sorted="asc" keep-unique>\n"zebra",\n"apple",\n"apple",\n# </block>\n')
commit(sort_bw, "init")
sort_fail = expect("sort-bw-fail", BW, sort_bw, 1)
assert {v["code"] for v in json.loads(sort_fail.stderr)["items.py"]} == {"keep-sorted", "keep-unique"}

(sort_bw / "items.py").write_text('# <block name="items" keep-sorted="asc" keep-unique>\n"apple",\n"zebra",\n# </block>\n')
expect("sort-bw-pass", BW, sort_bw, 0)

sort_ks = WORK / "sort-ks"
sort_ks.mkdir()
ks_file = sort_ks / "items.py"
ks_file.write_text('# keep-sorted start\n"zebra",\n"apple",\n"apple",\n# keep-sorted end\n')
expect("sort-ks-lint-fail", [*KS, "--mode=lint", str(ks_file)], sort_ks, 1)
expect("sort-ks-fix", [*KS, "--mode=fix", str(ks_file)], sort_ks, 0)
expect("sort-ks-lint-pass", [*KS, "--mode=lint", str(ks_file)], sort_ks, 0)

# 4. Broken target reference exits 2 instead of silently passing
broken = WORK / "broken-ref"
broken.mkdir()
(broken / "app.py").write_text('# <block name="port" same-as="missing.py#/PORT">\nPORT = 8080\n# </block>\n')
commit(broken, "init")
expect("broken-ref-exits-2", BW, broken, 2)

(OUTPUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(f"All {len(summary)} checks passed.", flush=True)
