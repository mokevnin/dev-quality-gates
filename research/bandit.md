# Bandit: checks beyond Ruff

Reviewed 2026-11-10. **Decision: add Bandit conditionally for B614/B615.** Keep Ruff as the default linter and formatter. Select the missing Bandit checks for projects that load PyTorch models or download from Hugging Face. Do not run both full security suites by default.

## Executed comparison

Ran Bandit 1.9.4 and Ruff 0.17.4 on Python 3.14.7 on 2026-11-10. The [fixture runner](fixtures/bandit/run.py) pins both tools and checks exit codes, rule IDs and empty Bandit error lists. It scans the files without executing them; no model download or PyTorch installation occurs.

```sh
python3 research/fixtures/bandit/run.py /tmp/bandit-results
```

The runner uses `bandit -f json FILE` and `ruff check --isolated --no-cache --preview --select S --output-format json FILE`. Thus Ruff runs all available `S` checks, including preview rules, without project configuration.

| Input | Bandit result | Ruff result |
|---|---|---|
| `torch.load(..., weights_only=False)` and `hf_hub_download(..., revision="main")` | Exit 1; B614 and B615 | Exit 0; no findings |
| Explicit `weights_only=True` and a literal commit revision | Exit 0; no findings | Exit 0; no findings |
| `eval(input())` | Exit 1; B307 | Exit 1; S307 |

This proves two useful gaps and one overlap, not complete rule parity. The earlier comparison of plugin-file counts in [the Python notes](stack-python-ruby-php.md) could not establish equivalent coverage.

## Rule-ID comparison

On 2026-11-10 the test IDs listed by `bandit -h` (1.9.4) were matched against `ruff rule --all` (0.17.4), where Ruff `Snnn` mirrors Bandit `Bnnn`. Only four Bandit tests have no `S` counterpart:

- B613 (trojan source): Ruff covers it outside `S` with [`PLE2502`](https://docs.astral.sh/ruff/rules/bidirectional-unicode/).
- B703 (Django `mark_safe`): overlaps [`S308`](https://docs.astral.sh/ruff/rules/suspicious-mark-safe-usage/).
- B614 and B615: no Ruff equivalent; the fixture above confirms both.

So B614 and B615 are the whole gap, not a sample of it. The matching is by ID only; it does not compare how each pair of rules behaves.

## Alternatives and integration

| Tool | Coverage and configuration | Speed and integration |
|---|---|---|
| Bandit | Python security AST checks; [custom Python plugins](https://bandit.readthedocs.io/en/latest/plugins/index.html), severity/confidence filters, YAML/TOML configuration. B614/B615 detect the cases above. | Python process; CLI and pre-commit integration. JSON tested; SARIF requires the extra package dependencies (docs only). |
| [Ruff](https://docs.astral.sh/ruff/rules/) | General lint and format; many Bandit-style checks under `S`. No external custom-rule plugins. TOML configuration. | Native Rust binary; reuse the existing linter. JSON and exit codes tested above. No speed benchmark here. |
| [Semgrep](https://semgrep.dev/docs/semgrep-code/overview) / [Opengrep](https://github.com/opengrep/opengrep) | Custom pattern and data-flow rules across languages. Broader analysis requires a rule set and edition-specific scope review. | CLI/CI alternatives when data-flow analysis is required. Not executed or timed here; not needed for these two bundled Bandit checks. |

Bandit does not replace Ruff formatting or general lint. It also does not replace OSV-Scanner dependency checks or a dedicated secret scanner. Custom plugins are another documented benefit, but this review does not test them.

For the demonstrated gap, select only B614 and B615, and do not pass `--exit-zero` in CI. A file Bandit cannot parse is reported in the JSON `errors` list, but when it produces no finding Bandit still exits 0 ([#1326](https://github.com/PyCQA/bandit/issues/1326); reproduced with 1.9.4 on 2026-11-10). Fail the job on errors as well as findings:

```sh
status=0
bandit -r src -t B614,B615 -f json -o bandit.json || status=$?
jq -e '.errors == []' bandit.json > /dev/null || status=1
exit "$status"
```

Adjust `src` to the project source directory. Run on 2026-11-10: exit 1 on a syntax error alone, exit 1 on a B614 finding, exit 0 on a clean directory. Ruff in the same pipeline also fails on syntax errors, so the check matters most when Bandit scans files Ruff excludes.

## Currency and open issues

Read the public repository, release, commit and issue records on 2026-11-10:

- [Official repository](https://github.com/PyCQA/bandit) and [documentation](https://bandit.readthedocs.io/en/latest/): public, not archived, no deprecation notice. [Licence](https://github.com/PyCQA/bandit/blob/1.9.4/LICENSE): Apache-2.0.
- Latest release: [1.9.4, 2026-02-25](https://github.com/PyCQA/bandit/releases/tag/1.9.4). Latest core-code commits found are from 2026-02-23: [B106 line-number fix](https://github.com/PyCQA/bandit/pull/1360), [Python AST compatibility](https://github.com/PyCQA/bandit/pull/1355), and [B615 false-positive fix](https://github.com/PyCQA/bandit/pull/1358).
- Maintainer `ericwb` merged those fixes. [Recent commits](https://github.com/PyCQA/bandit/commits/main/) through 2026-11-09 update CI dependencies; they do not demonstrate recent rule development. No successor or maintained replacement fork was identified in these project records. Ruff is the main overlapping alternative.
- Open [#1326](https://github.com/PyCQA/bandit/issues/1326) reports zero exit on scan failures. Open [#1467](https://github.com/PyCQA/bandit/issues/1467) reports baseline matching that can hide repeated findings. Avoid a baseline for this narrow gate.
- Open [#1381](https://github.com/PyCQA/bandit/issues/1381) follows up a security advisory without public technical details. Its severity and resolution cannot be established from that issue. This is not a claim that no critical issues exist.
- Open [#1293](https://github.com/PyCQA/bandit/issues/1293) reports B614 false positives for `torch.jit.load`. The fixture tests explicit `torch.load` arguments, not every PyTorch API.

The release and meaningful core activity are older than 30 days. The narrow, executed coverage gap justifies a conditional entry, not a general replacement or a freshness exception. Keep scheduled age warnings enabled.

## Limits

Bandit uses syntax-based heuristics, not whole-program data-flow analysis. It can miss vulnerabilities and report safe code. No automatic fixes are offered. The [B614](https://bandit.readthedocs.io/en/latest/plugins/b614_pytorch_load.html) and [B615](https://bandit.readthedocs.io/en/latest/plugins/b615_huggingface_unsafe_download.html) documentation describes the intended checks; only the table above was executed. A literal revision passes the syntax check, but Bandit does not verify the downloaded model or its publisher.

Reconsider this addition if Ruff covers these cases, or Bandit's maintenance and unresolved issues outweigh the narrow benefit.
