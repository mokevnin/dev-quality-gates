# mypy plugins and ty

Reviewed **2026-11-01**. Decision: **do not add mypy**. ty stays the type checker. It does not load mypy plugins, and that is a limit, not a second recommendation.

Generated protobuf stubs are not the gap. mypy-protobuf writes `.pyi` files, and ty reads them.

## Currency

Read from the GitHub API on 2026-11-01.

- [ty 0.0.95](https://github.com/astral-sh/ty/releases/tag/0.0.95) was published 2026-10-29. The repository was pushed 2026-10-31, is not archived, and had 20002 stars.
- mypy 2.4.1, pydantic 2.14.2, and mypy-protobuf 3.6.0 are the versions that were run. `ty check --help` on 0.0.95 has no plugin option.

## Executed checks

Linux x86_64, CPython 3.12. Reproduce with:

```sh
python3 research/fixtures/mypy-plugins/run.py /tmp/mypy-plugin-results
```

The script builds a virtualenv, generates `hello_pb2.pyi` with `protoc-gen-mypy`, and runs the commands below.

| Case | mypy 2.4.1 with `pydantic.mypy` | mypy 2.4.1, strict, no plugin | ty 0.0.95 |
|---|---|---|---|
| `HelloRequest(name=1)` | exit 1 | not run separately | exit 1 |
| `HelloRequest(name="a")` | exit 0 | not run separately | exit 0 |
| Pydantic field `age = 1` with no annotation | exit 1, `pydantic-field` | exit 0 | exit 0 |
| Assign to a field of a `frozen=True` model | exit 1 | exit 0 | exit 1 |

The protobuf rows used the generated stub and no mypy plugin. Both checkers agree: a string is accepted, an int is rejected.

The unannotated field is a plugin-only diagnostic. Without `pydantic.mypy`, strict mypy treats `age = 1` as an inferred int and exits 0. ty does the same. Loading the plugin makes mypy exit 1 with `Untyped fields disallowed`.

The frozen model is the other way around. mypy reports it only when the plugin is loaded. ty reports `invalid-assignment` with no plugin.

## What was not run

Django and `django-stubs` were not run. [research/ecosystem-gaps.md](ecosystem-gaps.md) already says Rust checkers do not load that plugin. This run does not add evidence for or against that sentence.

grpc stubs were not compared. The message stub above does not import `grpc`.
