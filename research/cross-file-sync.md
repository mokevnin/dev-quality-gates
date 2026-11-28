# Cross-file sync and block rules

Reviewed 2026-11-27. **Decision: add [blockwatch](https://github.com/mennanov/blockwatch) under Custom rules.** Record [keep-sorted](https://github.com/google/keep-sorted) and [ifttt-lint](https://github.com/simonepri/ifttt-lint) in [not-adopted](../docs/not-adopted.md).

**Conflict of interest:** blockwatch is maintained by the author of this pull request.

## The gap

None of the currently listed tools enforce cross-file value equality, cross-file change coupling between code and docs, or inline block invariants across languages:

- **ast-grep** checks one file at a time (no cross-file resolution). See [research/custom-rules.md](custom-rules.md).
- **easement** checks import-graph boundaries across four languages, not value sync or documentation coupling.
- **Conftest** runs Rego policies over config files, not cross-file code-to-doc or diff-based coupling.
- **rumdl**, **lychee**, and **typos** lint Markdown style, links, and spelling, not whether documentation matches constants or config values in code.

## Executed comparison

Ran on 2026-11-27 on macOS arm64 using pinned releases:

- **blockwatch 0.22.0** (`uv tool run --from blockwatch-cli==0.22.0 blockwatch`)
- **keep-sorted v0.11.0** (`167f8ca`, GitHub release binary)
- **ifttt-lint 0.11.3** (GitHub release archive, SHA-256 verified)

Reproduce all 15 checks with:

```sh
python3 research/fixtures/blockwatch/run.py /tmp/blockwatch-results
```

| Scenario | blockwatch 0.22.0 | ifttt-lint 0.11.3 | keep-sorted v0.11.0 |
|---|---|---|---|
| Cross-file value sync (`PORT` in `settings.py`, `Dockerfile`, and `deploy.json` via `blockwatch.toml`), clean | Exit 0; SARIF 2.1.0 with 0 results | N/A | N/A |
| Same fixture after `PORT` drifts to `9090` (no diff needed) | Exit 1; JSON and SARIF report `same-as` on `Dockerfile` and `deploy.json` | Exit 0 (no `LINT.IfChange` markers; cannot compare values) | N/A |
| Diff coupling: edit `src/roles.py` without updating `docs/roles.md` | Exit 1 (`affects="docs/roles.md#/Roles"`; target Markdown has no comment tags) | Exit 1 (requires `LINT.IfChange`/`LINT.ThenChange` tags in both files) | N/A |
| Diff coupling: update both `src/roles.py` and `docs/roles.md` | Exit 0 | Exit 0 | N/A |
| SARIF output (`--format sarif`) | Supported (SARIF 2.1.0 on stderr) | Exit 2 (`invalid value 'sarif'`) | Not supported |
| Unsorted list with duplicate item | Exit 1 (`keep-sorted` and `keep-unique`); check-only | N/A | `--mode=lint` exits 1 with JSON fix; `--mode=fix` rewrites file and exits 0 |
| Broken target reference (`missing.py#/PORT`) | Exit 2 | Not run | Not run |

### Real-repository run

Ran `blockwatch 0.22.0` on a clean checkout of [mennanov/blockwatch](https://github.com/mennanov/blockwatch) at tag [v0.22.0](https://github.com/mennanov/blockwatch/releases/tag/v0.22.0) (commit `515960c`) on 2026-11-27:

- Clean run (`blockwatch --verbosity summary`): exit 0 — `59/185 files, 126 blocks (50 unchecked, 37 need --diff), 82 checks, 0 violations`.
- Drift check: changing `39 languages` to `38 languages` in `README.md` and running `git diff --patch | blockwatch --diff` exited 1 (`check-lua` via `scripts/check_language_count.lua`: `"the pitch claims 38 languages, but the list has 39"`).

## Alternatives (run and read)

| Tool | Last release | Last push | Licence | Stars | Comparison |
|---|---|---|---|---|---|
| [blockwatch](https://github.com/mennanov/blockwatch) | [v0.22.0](https://github.com/mennanov/blockwatch/releases/tag/v0.22.0) (2026-11-26) | 2026-11-26 | [MIT](https://github.com/mennanov/blockwatch/blob/v0.22.0/LICENSE) | 34 | **Ran.** Rust single binary. Cross-file `same-as` (no diff needed) and `affects` (diff-based), symbol targets (`file#/symbol`), `blockwatch.toml` virtual blocks for commentless files like JSON, plus `keep-sorted`, `keep-unique`, `line-pattern`, `line-count`, `check-lua`, and optional `check-ai`. JSON and SARIF 2.1.0 output. Check-only (no autofix). |
| [keep-sorted](https://github.com/google/keep-sorted) | [v0.11.0](https://github.com/google/keep-sorted/releases/tag/v0.11.0) (2026-11-14) | 2026-11-20 | Apache-2.0 | 406 | **Ran.** Go binary. Stronger when you only want sorted/deduplicated blocks because `--mode=fix` rewrites files in place and `--mode=lint` outputs JSON replacements. Does not check cross-file sync, diff coupling, regex, or custom rules. |
| [ifttt-lint](https://github.com/simonepri/ifttt-lint) | [v0.11.3](https://github.com/simonepri/ifttt-lint/releases/tag/v0.11.3) (2026-10-26) | 2026-10-26 | MIT | 30 | **Ran.** Rust binary implementing Google's `LINT.IfChange`/`LINT.ThenChange` comments with git and jj diff support and JSON output. Diff coupling only: no diff-free value equality, no symbol targets, no config blocks for JSON, and no SARIF. |
| [ifchange](https://github.com/slnc/ifchange) | Read only | 2026-11-11 | MIT | 7 | **Read only.** Smaller `LINT.IfChange`/`LINT.ThenChange` implementation; same scope limits as `ifttt-lint`. |

Repository figures are from `gh api` on 2026-11-27.

Claims **read** from [blockwatch docs](https://github.com/mennanov/blockwatch/blob/v0.22.0/docs/cli.md), [symbols](https://github.com/mennanov/blockwatch/blob/v0.22.0/docs/symbols.md), and [validators](https://github.com/mennanov/blockwatch/blob/v0.22.0/docs/validators/README.md) (not executed in the fixture): 39 supported languages, `--suppress`, `--suppress-from`, `severity`, `line-pattern`, `line-count`, `check-ai`, `blockwatch skill`, and the GitHub Action (`mennanov/blockwatch-action@v1`).

## Currency and open issues

Checked via `gh api` on 2026-11-27:

- Created 2025-03-14, not archived, no deprecation notice or fork/successor, MIT licence.
- Latest release: [v0.22.0](https://github.com/mennanov/blockwatch/releases/tag/v0.22.0) on 2026-11-26 (frequent releases through November 2026); 2 contributors, 34 stars.
- Open bug issues: [#138](https://github.com/mennanov/blockwatch/issues/138) (passing paths before `list` runs validation instead of `list`) and [#151](https://github.com/mennanov/blockwatch/issues/151) (git hooks check untracked files). Open feature request [#169](https://github.com/mennanov/blockwatch/issues/169) tracks `--fix` for sorting and deduplication.

## Limitations

- **Maintained by the PR author**, pre-1.0 (`v0.22.0`), small user base (34 stars), and one primary maintainer.
- **No autofix yet:** `keep-sorted` can fix unsorted blocks in place; `blockwatch` only reports them ([#169](https://github.com/mennanov/blockwatch/issues/169)).
- **No baseline file:** existing violations are suppressed per address (`--suppress` / `--suppress-from`) or lowered with `severity="warning"`.

Note for CI wiring: JSON diagnostics and SARIF logs write to `stderr` (`blockwatch --format sarif 2> blockwatch.sarif`), and all core validators run offline (`check-ai` only runs if a block opts in).

## Decision

Add **blockwatch** under **Custom rules** for cross-file value sync, code-to-doc change coupling, and inline block invariants. Keep **keep-sorted** and **ifttt-lint** in [not-adopted](../docs/not-adopted.md), noting that `keep-sorted` remains the right pick when you only need auto-formatted sorted blocks.
