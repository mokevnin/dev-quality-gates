#!/usr/bin/env python3
"""Compare mypy 2.4.1 and ty 0.0.95 on plugin-only checks and protobuf stubs.

Requires uv and network on the first run. Writes a virtualenv and generated
stubs under the output directory, not next to these sources.

    python3 research/fixtures/mypy-plugins/run.py /tmp/mypy-plugin-results
"""

import os
import subprocess
import sys
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent
OUTPUT = Path(sys.argv[1]).resolve()
if OUTPUT.exists() and any(OUTPUT.iterdir()):
    raise SystemExit("Use an empty output directory")
OUTPUT.mkdir(parents=True)
VENV = OUTPUT / "venv"
GENERATED = OUTPUT / "generated"
GENERATED.mkdir()

PACKAGES = [
    "mypy==2.4.1",
    "ty==0.0.95",
    "pydantic==2.14.2",
    "mypy-protobuf==3.6.0",
    "grpcio-tools==1.85.1",
    "protobuf==7.36.2",
]


def run(command, *, cwd=FIXTURES, env=None):
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    return result


uv = os.environ.get("UV", "uv")
install = run([uv, "venv", "--python", "3.12", str(VENV)])
if install.returncode != 0:
    raise SystemExit(install.stderr)
install = run([uv, "pip", "install", "--python", str(VENV / "bin" / "python"), *PACKAGES])
if install.returncode != 0:
    raise SystemExit(install.stderr)

env = os.environ.copy()
env["PATH"] = f"{VENV / 'bin'}{os.pathsep}{env.get('PATH', '')}"
env["MYPYPATH"] = str(GENERATED)
protoc = run(
    [
        str(VENV / "bin" / "python"),
        "-m",
        "grpc_tools.protoc",
        "-I",
        str(FIXTURES),
        f"--python_out={GENERATED}",
        f"--mypy_out={GENERATED}",
        str(FIXTURES / "hello.proto"),
    ],
    env=env,
)
if protoc.returncode != 0:
    raise SystemExit(protoc.stderr)

plugin_config = OUTPUT / "plugin.ini"
plugin_config.write_text("[mypy]\nplugins = pydantic.mypy\nstrict = true\n")
no_plugin = OUTPUT / "no-plugin.ini"
no_plugin.write_text("[mypy]\nstrict = true\n")

mypy = str(VENV / "bin" / "mypy")
ty = str(VENV / "bin" / "ty")
cases = [
    ("proto-bad-mypy", [mypy, "proto_bad.py"], 1),
    ("proto-bad-ty", [ty, "check", "--python", str(VENV), "proto_bad.py", "--extra-search-path", str(GENERATED)], 1),
    ("proto-ok-mypy", [mypy, "proto_ok.py"], 0),
    ("proto-ok-ty", [ty, "check", "--python", str(VENV), "proto_ok.py", "--extra-search-path", str(GENERATED)], 0),
    ("untyped-mypy-plugin", [mypy, "--config-file", str(plugin_config), "pydantic_untyped.py"], 1),
    ("untyped-mypy", [mypy, "--config-file", str(no_plugin), "pydantic_untyped.py"], 0),
    ("untyped-ty", [ty, "check", "--python", str(VENV), "pydantic_untyped.py"], 0),
    ("frozen-mypy-plugin", [mypy, "--config-file", str(plugin_config), "pydantic_frozen.py"], 1),
    ("frozen-mypy", [mypy, "--config-file", str(no_plugin), "pydantic_frozen.py"], 0),
    ("frozen-ty", [ty, "check", "--python", str(VENV), "pydantic_frozen.py"], 1),
]
for name, command, expected in cases:
    result = run(command, env=env)
    (OUTPUT / f"{name}.stdout").write_text(result.stdout)
    (OUTPUT / f"{name}.stderr").write_text(result.stderr)
    print(name, result.returncode, flush=True)
    if result.returncode != expected:
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(f"{name}: exit {result.returncode}, expected {expected}")
