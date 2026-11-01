#!/usr/bin/env python3
"""Reproduce the ansible-lint runs cited in research/ansible.md.

Requires ansible-lint 26.10.1 and yamllint 1.38.0 on PATH. Copies fixtures
into the output directory before running, because --fix rewrites files.

    python3 research/fixtures/ansible/run.py /tmp/ansible-lint-results
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent
OUTPUT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
if OUTPUT is None or OUTPUT.exists():
    raise SystemExit("Pass an empty output directory")
OUTPUT.mkdir()
HOME = OUTPUT / "home"
HOME.mkdir()
ENV = os.environ.copy()
ENV["HOME"] = str(HOME)
ENV["XDG_CACHE_HOME"] = str(OUTPUT / "cache")


def version(command: list[str], expected: str) -> None:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    text = result.stdout + result.stderr
    print(text.strip(), flush=True)
    if expected not in text:
        raise SystemExit(f"Unexpected version from {command}: {text}")


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["ansible-lint", "--offline", *args],
        cwd=cwd,
        env=ENV,
        capture_output=True,
        text=True,
    )


def expect(name: str, result: subprocess.CompletedProcess[str], code: int, text: str = "") -> None:
    blob = result.stdout + result.stderr
    (OUTPUT / f"{name}.stdout").write_text(result.stdout)
    (OUTPUT / f"{name}.stderr").write_text(result.stderr)
    print(name, result.returncode, flush=True)
    if result.returncode != code or (text and text not in blob):
        raise SystemExit(f"{name}: exit {result.returncode}, wanted {code} and {text!r}")


version(["ansible-lint", "--version"], "26.10.1")
version(["yamllint", "--version"], "1.38.0")

work = OUTPUT / "work"
shutil.copytree(FIXTURES, work, ignore=shutil.ignore_patterns("run.py"))

expect("clean", run(["-f", "pep8", "playbook.yml"], work / "clean"), 0)
expect("bad", run(["-f", "pep8", "playbook.yml"], work / "bad"), 2, "no-changed-when")
expect("profile-min", run(["--profile", "min", "-f", "pep8", "playbook.yml"], work / "bad"), 0, "production")
expect("profile-basic", run(["--profile", "basic", "-f", "pep8", "playbook.yml"], work / "bad"), 2, "name[play]")
expect("fix", run(["--fix", "playbook.yml"], work / "fix"), 8)
fixed = (work / "fix" / "playbook.yml").read_text()
if "ansible.builtin.debug" not in fixed:
    raise SystemExit("fix: --fix did not rewrite the module name")
expect("discover", run(["-f", "pep8"], work / "discover"), 2, "notes.yaml")
expect("custom", run(["-r", "rules", "-f", "pep8", "playbook.yml"], work / "custom"), 2, "no-debug")
expect("config-schema", run(["-f", "pep8"], work / "config-schema"), 3)
expect("config-broken", run(["-f", "pep8"], work / "config-broken"), 1)
missing = run(["-f", "pep8", str(OUTPUT / "no-such.yml")], work / "clean")
expect("missing", missing, 2, "load-failure")

json_run = run(["-f", "json", "playbook.yml"], work / "bad")
expect("json", json_run, 2)
parsed = json.loads(json_run.stdout)
if not isinstance(parsed, list) or not parsed:
    raise SystemExit("json: expected a non-empty list")

yamllint = subprocess.run(
    ["yamllint", str(work / "discover" / "notes.yaml")],
    capture_output=True,
    text=True,
)
print("yamllint", yamllint.returncode, flush=True)
if yamllint.returncode != 1 or "key-duplicates" not in yamllint.stdout:
    raise SystemExit(f"yamllint: exit {yamllint.returncode}")
