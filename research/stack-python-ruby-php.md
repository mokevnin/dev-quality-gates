# Python, Ruby and PHP: guardrail tools

Reviewed 2026-10-23. Scope: Python, Ruby, PHP. Method: `gh api repos/...` (archived, pushed_at, stars, licence), latest GitHub release, registry JSON (PyPI, RubyGems, Packagist), the project's README or docs source, and a few web searches. The searches returned little of value, so most claims rest on primary sources (repo files and docs).

**Not done anywhere in this file:** no tool was installed or run (the disk was full during the session), so speed, false-positive rate and rule quality are not verified. "Self-reported" marks a claim taken from the tool's own docs. "Last push" is the GitHub `pushed_at` date. Star counts are from the API on the review date.

## Summary of picks

| Ecosystem | Job | Pick | Confidence |
|---|---|---|---|
| Python | Type checking | Pyrefly (pyright as the conservative alternative) | Low-medium: no clear winner |
| Python | Dead code | vulture | Medium |
| Python | Architecture | import-linter | Medium-high |
| Python | Security (code) | Ruff `S`; add Bandit B614/B615 for model loads and downloads ([recheck](bandit.md)) | Executed narrow comparison |
| Python | Docstrings, complexity | Ruff (`D`, `C901`), no pydocstyle, xenon, radon | Medium-high |
| Python | Lockfile freshness | `uv lock --check` / `uv sync --locked` | Medium |
| Python | Dependency vulnerabilities | Defer to the OSV-Scanner decision; pip-audit if you want a native tool | Low |
| Ruby | Lint | RuboCop (already listed) plus rubocop-rails, rubocop-rspec, rubocop-performance | High |
| Ruby | Security | Brakeman, **non-free for commercial use** | Medium, licence caveat |
| Ruby | Types | Sorbet | Medium |
| Ruby | Architecture | Packwerk | Medium |
| Ruby | ERB templates | No clear winner (erb_lint stalled, Herb pre-1.0) | Low |
| PHP | Static analysis | PHPStan (Larastan for Laravel) | High |
| PHP | Style | PHP-CS-Fixer (Pint if you use Laravel) | Medium-high |
| PHP | Automated refactoring and upgrades | Rector | High |
| PHP | Architecture | Deptrac | Medium-high |
| PHP | Dependency hygiene | composer-dependency-analyser | Medium |
| PHP | Dependency vulnerabilities | `composer audit` (built in) | High |
| PHP | Dead code | shipmonk/dead-code-detector (PHPStan extension) | Medium |

Newer all-in-one tools worth watching (not proposed): **Mago** (PHP), **pyscn** and **Skylos** (Python), **Herb** (Ruby ERB), **pks** (Rust Packwerk).

---

## Python

### Type checking

| Candidate | Latest release | Last push | Licence | Stars | Notes |
|---|---|---|---|---|---|
| [mypy](https://github.com/python/mypy) | 2.4.0 (2026-10-01, PyPI) | 2026-10-23 | MIT (`LICENSE` text; API says NOASSERTION) | 20.7k | Reference implementation, slowest. |
| [pyright](https://github.com/microsoft/pyright) | 1.1.414 (2026-09-09) | 2026-10-23 | MIT | 15.7k | Releases slowed to roughly monthly or less in 2026 (Jan, Apr, May, Jun, Aug, Sep); daily commits. JSON output (`--outputjson`), exit codes documented. No baseline, no SARIF. |
| [basedpyright](https://github.com/DetachHead/basedpyright) | 1.40.2 (2026-10-04) | 2026-10-04 | NOASSERTION (not read) | 3.6k | Pyright fork with baseline file and extra checks; single-maintainer fork. |
| [pyrefly](https://github.com/facebook/pyrefly) | 1.4.0 (2026-10-15) | 2026-10-23 | MIT | 7.1k | **Stable since 1.0.0 (2026-05-12)**, monthly minors. Output formats include `json`, `github`, `junit-xml`, `code-climate`, `sarif` (from its config docs). Has `baseline-error-level`, `pyrefly suppress`, `pyrefly init` (migrates mypy/pyright config). Default checker for Instagram; adopted by PyTorch and JAX (self-reported). Rust. |
| [ty](https://github.com/astral-sh/ty) | 0.0.91 (2026-10-22) | 2026-10-23 | MIT | 19.9k | **Beta** per its README; 1.0 not shipped. Astral says 10-100x faster than mypy and pyright (self-reported). |
| [zuban](https://github.com/zubanls/zuban) | 0.10.1 (2026-10-11) | 2026-10-23 | **AGPL-3.0-only** (or commercial) | 1.2k | Mypy-compatible mode; AGPL is a blocker for many companies. |

**Recommendation:** no clear winner. If one must be named, **Pyrefly**: stable, MIT, the best CI features of the group (SARIF, JSON, JUnit, baseline) and fast. **Pyright** is the safer pick if you want the most battle-tested checks and the least churn.
Reasons against the others: ty is beta; zuban is AGPL; mypy is slow and has no SARIF; basedpyright is a one-maintainer fork.

**Limits:** Pyrefly's own version policy says any release, including patch releases, may add new type errors, so pin the version and use `pyrefly suppress` when upgrading. Pyrefly is less proven than pyright on edge-case checks, which we could not test. Pyright in CI also needs Node or the PyPI wrapper.

**Confidence:** low-medium. Not verified: error counts on a real codebase, agreement with the typing conformance suite, Pyrefly's baseline behaviour in practice, whether pyright's release slowdown is a problem.

### Ruff gaps: what not to add

Ruff 0.17.2 is current (2026-10-22). Facts checked: output formats include `json`, `junit`, `github`, `gitlab`, `sarif`, `rdjson`; it implements `S` (flake8-bandit, 35 rule files in the repo versus 32 plugin files in Bandit), `C901` (mccabe), `D` (pydocstyle), `TID` (tidy-imports, banned imports).

| Standalone tool | Last release / push | Verdict |
|---|---|---|
| [Bandit](https://github.com/PyCQA/bandit) | [Rechecked 2026-11-10](bandit.md) | Conditional addition: B614/B615 catch model-load and download cases Ruff misses. The earlier file-count comparison did not establish rule parity. |
| [pydocstyle](https://github.com/PyCQA/pydocstyle) 6.3.0 | **archived**, last push 2023-11 | Replaced by Ruff `D`. |
| [xenon](https://github.com/rubik/xenon) 0.9.3 (2024-10), [radon](https://github.com/rubik/radon) 6.0.1 (2023-03) | last push 2024-10 | Stale; Ruff `C901` and `PLR09xx` give a hard threshold. |
| [flake8](https://github.com/PyCQA/flake8) 7.4.1, [pylint](https://github.com/pylint-dev/pylint) 4.1.3 (GPL-2.0) | active | Overlap. Pylint's cross-module checks are the only reason to keep it; not compared here. |
| [interrogate](https://github.com/econchick/interrogate) 1.7.0 (2024-04) | push 2026-10-06 | Docstring-coverage threshold; Ruff `D1xx` rules do the same per symbol. Stale release. |

**Remaining Ruff gaps** (stated in the existing entry): no type checking and no custom rules. For custom rules use ast-grep (already listed).

### Dead code

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [vulture](https://github.com/jendrikseipp/vulture) | 2.16 (2026-03-25) | 2026-10-12 | MIT | 4.9k |
| [Skylos](https://github.com/duriantaco/skylos) | 5.0.0 (2026-10-23) | 2026-10-23 | Apache-2.0 | 848 |
| [pyscn](https://github.com/ludo-technologies/pyscn) | 1.32.5 (2026-10-15) | 2026-10-21 | MIT | 1.1k |
| Ruff `F401`, `F841` | | | | local scope only |

**Recommendation: vulture.** Stable, simple, `--min-confidence` and generated whitelists. Ruff cannot find unused functions or classes across modules.
Skylos and pyscn are young. Skylos (dead code, secrets, security, plus `skylos done`, which flags deleted or skipped tests and loosened CI in agent branches) is the most agent-oriented thing found, but it is one project with 848 stars and a 5.0.0 release the day of review. pyscn bundles dead code, clones, complexity and layer rules with a `pyscn check` gate; it was created 2025-08 and 73 of the last 100 commits come from one person. Both belong on a watch list.

**Limits (vulture):** heuristic, so it needs a whitelist for framework entry points (Django, pytest fixtures). Exit code behaviour was not checked in this run.
**Confidence:** medium. Not verified: Skylos's accuracy claims, pyscn's exit codes.

### Architecture and imports

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [import-linter](https://github.com/seddonym/import-linter) | 2.15 (2026-09-04) | 2026-10-13 | BSD-2-Clause | 1.2k |
| [tach](https://github.com/tach-org/tach) | 0.35.3 (2026-10-06) | 2026-10-06 | MIT | 2.9k |
| [pyscn](https://github.com/ludo-technologies/pyscn) layer rules | see above | | MIT | 1.1k |

import-linter contract types (from its docs folder): `layers`, `forbidden`, `independence`, `protected`, `acyclic_siblings`, plus custom contracts. Tach enforces declared module dependencies, public interfaces and cycles; written in Rust. 82 of tach's last 100 commits are by one maintainer (DetachHead), and the repo moved from the `gauge-sh` org to `tach-org`; an open issue (#900) asks for a baseline system. Repo history suggests the company behind it wound down, but that is inferred, not confirmed.

**Recommendation: import-linter.** Older, steady commit rate (about 6 to 9 commits a month), contracts are config in `pyproject.toml` or `.importlinter`, and custom contracts are possible. Tach is the alternative if you want interface (public API) enforcement and speed.

**Limits:** import-linter checks imports, not calls or attribute access; large graphs are slow without its cache. Output formats beyond text and DOT were not checked.
**Confidence:** medium-high on the pick, low on relative speed.

### Packaging and lockfile checks

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [uv](https://github.com/astral-sh/uv) | 0.13.5 (2026-10-22) | 2026-10-23 | Apache-2.0 | 91k |
| [validate-pyproject](https://github.com/abravalheri/validate-pyproject) | 0.27 (2026-10-22) | 2026-10-22 | MPL-2.0 | 210 |
| [check-wheel-contents](https://github.com/jwodder/check-wheel-contents) | 0.6.3 (2025-08-02) | 2026-10-11 | MIT | 170 |
| [pip-tools](https://github.com/pypa/pip-tools) | 7.6.2 (2026-10-07) | 2026-10-21 | BSD-3-Clause | 8.0k |

uv's CLI reference lists `uv lock --check` ("check if the lockfile is up-to-date") and `uv sync --check`; `uv audit` exists (release notes mention advisory ID display and offline errors) but we did not check its maturity or exit codes.
**Recommendation:** use `uv lock --check` in CI as the lockfile gate if the project uses uv. validate-pyproject and check-wheel-contents are only for projects that publish packages; both are niche and not proposed.
**Limits:** only helps projects on uv; pip-tools is the equivalent for `requirements.txt` workflows (`pip-compile` plus a diff check, not verified).
**Confidence:** medium. Not verified: that `uv sync --locked` fails with a clear exit code on drift.

### Dependency vulnerabilities

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [pip-audit](https://github.com/pypa/pip-audit) | v2.10.1 (2026-06-10) | 2026-10-22 | Apache-2.0 | 1.4k |
| `uv audit` | in uv 0.13.x | | Apache-2.0 | |
| [safety](https://github.com/pyupio/safety) | 3.8.1 (2026-05-29) | 2026-09-04 | none detected | 2.0k |
| [OSV-Scanner](https://github.com/google/osv-scanner) | v2.7.0 (2026-10-12) | 2026-10-23 | Apache-2.0 | 11.3k |

pip-audit: PyPI JSON API or OSV as source, `--locked` for lockfiles, `--fix`, formats `columns`, `json`, `cyclonedx-json`, `cyclonedx-xml`, `markdown`.
**Recommendation:** do not add a Python-only tool before the repo decides on OSV-Scanner (the README lists "Vulnerabilities and images" as under review, and OSV-Scanner covers Python, Ruby and PHP lockfiles in one run). If the repo wants a native tool, pip-audit; it is maintained under PyPA.
**Confidence:** low. Not verified: OSV-Scanner lockfile support for `uv.lock`, `uv audit` stability.

### Tests: coverage and mutation

- `coverage.py` 7.17.0 (2026-10-22, Apache-2.0) has `[report] fail_under` (found in its docs). That is the coverage gate; no separate tool needed.
- Mutation: [mutmut](https://github.com/boxed/mutmut) 3.8.0 (2026-09-12, BSD-3-Clause, 1.5k stars) and [cosmic-ray](https://github.com/sixty-north/cosmic-ray) 8.7.0 (2026-08-09, MIT, 662 stars) are both active. Neither was run, so **no pick** (the earlier "slow" was read, not run; StrykerJS passed a changed-files run, see [stryker.md](stryker.md)).

---

## Ruby

### Linting and extensions

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [RuboCop](https://github.com/rubocop/rubocop) | v1.92.1 (2026-10-22) | 2026-10-23 | MIT | 12.9k |
| [rubocop-rails](https://github.com/rubocop/rubocop-rails) | v2.38.0 (2026-09-20) | 2026-10-15 | MIT | 877 |
| [rubocop-rspec](https://github.com/rubocop/rubocop-rspec) | v3.10.2 (2026-06-06) | 2026-10-22 | MIT | 859 |
| [rubocop-performance](https://github.com/rubocop/rubocop-performance) | v1.27.0 (2026-08-16) | 2026-09-09 | MIT | 743 |
| [rubocop-minitest](https://github.com/rubocop/rubocop-minitest) | v0.41.0 (2026-10-02) | 2026-10-02 | MIT | 167 |
| [rubocop-sorbet](https://github.com/Shopify/rubocop-sorbet) | v0.17.2 (2026-10-20) | 2026-10-23 | MIT | 201 |
| [Standard](https://github.com/standardrb/standard) | 1.57.0 (2026-10-05, RubyGems) | 2026-10-14 | MIT | 2.9k |
| [rails/rubocop-rails-omakase](https://github.com/rails/rubocop-rails-omakase) | v1.1.0 (2025-02-25) | 2026-01-18 | none detected | 565 |
| [fasterer](https://github.com/DamirSvrtan/fasterer) | 0.11.0 (2023-11) | 2024-06-14 | MIT | 1.8k |

RuboCop has a built-in SARIF 2.1.0 formatter (verified in its formatters doc and `lib/rubocop/formatter/sarif_formatter.rb`), plus JSON, JUnit, GitHub Actions and more, and a server mode since 1.31.
**Recommendation:** keep RuboCop; add rubocop-rails, rubocop-rspec (or rubocop-minitest) and rubocop-performance as the standard extension set. **Do not add** Standard (a config-free wrapper over RuboCop, so it overlaps and removes custom config), fasterer (stale, covered by rubocop-performance), or rubocop-rails-omakase (a style preset, not a check).
**Limits:** extensions are separate gems and must be listed under `plugins:` in `.rubocop.yml` (plugin API; the migration-guide page was not readable, so the exact version where `plugins:` started is unverified).
**Confidence:** high.

### Security

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [Brakeman](https://github.com/presidentbeef/brakeman) | v8.1.0 (2026-09-30) | 2026-10-22 | **Brakeman Public Use License** (Synopsys) | 7.3k |
| [bundler-audit](https://github.com/rubysec/bundler-audit) | v0.9.3 (2025-11-28) | 2026-10-23 | GPL-3.0 | 2.8k |
| [OSV-Scanner](https://github.com/google/osv-scanner) | v2.7.0 | 2026-10-23 | Apache-2.0 | 11.3k |

Brakeman: non-zero exit on warnings by default (`--no-exit-on-warn` disables it); formats `json`, `sarif`, `sonar`, `junit`, `github`, `codeclimate` and more; `--compare` against a previous JSON report. **Licence (read in `LICENSE.md`): "Commercial Uses ... require a commercial, non-free license"; free for non-commercial use.** The README says the same. RubyGems lists the licence as "Nonstandard". No verified free alternative with Rails-aware analysis was found (Semgrep/Opengrep Rails rules were not checked; Bearer was mentioned by a search result and not verified).
**Recommendation:** Brakeman for Rails apps, with the licence stated prominently. For gem vulnerabilities use bundler-audit or defer to the OSV-Scanner decision.
**Limits:** commercial use needs a paid licence (terms not fully analysed here); Rails only.
**Confidence:** medium. Open question for the maintainers: does a list with a "free tools" bias want a tool with this licence? The README already lists a GPL-3.0 tool (golangci-lint), so it is not a hard rule, but this restriction is stronger.

### Type checking

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [Sorbet](https://github.com/sorbet/sorbet) | 0.6.13591 (2026-10-23) | 2026-10-23 | Apache-2.0 | 3.8k |
| [Steep](https://github.com/soutaro/steep) | v2.1.0 (2026-08-27) | 2026-10-23 | MIT | 1.5k |
| [RBS](https://github.com/ruby/rbs) | v4.2.0 (2026-08-23) | 2026-10-23 | not read (API: NOASSERTION) | 2.2k |
| [TypeProf](https://github.com/ruby/typeprof) | v0.33.2 (2026-09-29) | 2026-09-29 | MIT | 833 |
| [Tapioca](https://github.com/Shopify/tapioca) (RBI generator for Sorbet) | v0.20.0 (2026-09-15) | 2026-10-20 | MIT | 874 |

**Recommendation: Sorbet.** Per-file strictness (`# typed:` sigils) allows gradual adoption and a ratchet in CI; Tapioca generates RBI files for gems and Rails; rubocop-sorbet adds style cops. Steep is active and uses the standard RBS signature files, so it is the right choice if you want signatures outside the code. No head-to-head run was done.
**Limits:** runtime `sig` blocks add boilerplate; Rails metaprogramming needs Tapioca DSL files kept current. TypeProf is described as experimental.
**Confidence:** medium. Not verified: JSON or SARIF output for `srb tc`, Rails 8 support.

### Architecture

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [Packwerk](https://github.com/Shopify/packwerk) | v3.3.1 (2026-08-26) | 2026-08-26 | MIT | 1.9k |
| [pks](https://github.com/rubyatscale/pks) | v0.7.0 (2026-10-12) | 2026-10-14 | MIT | 10 |
| [packwerk-extensions](https://github.com/rubyatscale/packwerk-extensions) | v0.4.0 (2026-09-25) | 2026-10-01 | MIT | 51 |

pks is a Rust reimplementation of Packwerk and packwerk-extensions, claiming 10-20x speed (self-reported, in its README) and shipping dependency, privacy, visibility, folder-privacy and layer checkers.
**Recommendation: Packwerk**, with packwerk-extensions for privacy and layers. Re-check pks when it has more users; 10 stars at v0.7.0 is too young. Packwerk's maintainers are active but few (the recent commits are Shopify staff merging dependabot PRs).
**Limits:** needs Zeitwerk (Rails 6+); checks constant references only.
**Confidence:** medium.

### ERB templates

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [erb_lint](https://github.com/Shopify/erb_lint) | v0.9.0 (2025-01-20) | 2026-04-20 | MIT | 749 |
| [Herb](https://github.com/marcoroth/herb) (linter, formatter, parser) | v0.11.1 (2026-10-20) | 2026-10-21 | MIT | 1.3k |
| [haml-lint](https://github.com/sds/haml-lint) | v0.78.0 (2026-08-20) | 2026-10-01 | MIT | 339 |

erb_lint: no release in 21 months; its last commits are dependabot bumps (2025-11, 2026-01), with 30 open issues. Herb: HTML+ERB parser with a linter (Node package `@herb-tools/linter`; output `detailed`, `simple`, JSON, JUnit, GitHub), formatter marked experimental, and an LSP. Its README claims Rails 8.2 framework defaults render templates with `Herb::Engine` (not verified).
**Recommendation:** no clear winner. erb_lint is the Ruby-only option but looks stalled; Herb is more active but pre-1.0 and needs Node for linting. Not proposed; keep as an "Under review" lead.
**Confidence:** low. Not verified: rule coverage of either, Herb exit codes.

### Code smells, best practices, other

- [Reek](https://github.com/troessner/reek) 6.6.0 (2026-10-02, MIT, 4.1k): active smell detector. Partial overlap with RuboCop `Metrics` cops; not compared, so not proposed.
- [rails_best_practices](https://github.com/flyerhzm/rails_best_practices) 1.23.4 (2026-04-23, MIT, 4.2k): overlaps rubocop-rails; no GitHub releases. Not proposed.
- [Mutant](https://github.com/mbj/mutant) 0.17.1: **commercial EULA**, free only for open source, $30/month per developer for commercial use (README). Not proposed.
- [strong_migrations](https://github.com/ankane/strong_migrations) 2.8.0 (2026-05-14, MIT, 4.5k): blocks unsafe Rails migrations at run time. A lead for the "SQL and migrations" category, not compared.
- SimpleCov 1.3.2 (2026-09-30, MIT): coverage thresholds (`minimum_coverage`) not verified in this run.

---

## PHP

### Static analysis

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [PHPStan](https://github.com/phpstan/phpstan) | 2.3.1 (2026-10-08) | 2026-10-23 | MIT | 14.1k |
| [Psalm](https://github.com/vimeo/psalm) | 6.20.1 stable (2026-10-20); 7.0.0-rc10 (2026-10-23) | 2026-10-23 | MIT | 5.9k |
| [Larastan](https://github.com/larastan/larastan) | v3.13.2 (2026-10-23) | 2026-10-23 | MIT | 6.5k |
| [Mago](https://github.com/carthage-software/mago) | 1.58.2 (2026-10-19) | 2026-10-23 | Apache-2.0 / MIT | 3.5k |

- PHPStan formatters in source: `raw`, `table`, `json`, `junit`, `checkstyle`, `github`, `gitlab`, `teamcity`, baseline formatters. **No SARIF.** Baseline file supported. Larastan 3.13.2 requires `phpstan/phpstan ^2.3.0`. Commit history shows two or more active contributors (Ondřej Mirtes, staabm).
- Psalm: its README names Daniil Gentili as "the only active maintainer", and 99 of the last 100 commits are his. Psalm 7 is at release candidate 10.
- Mago: a Rust toolchain with linter, formatter, analyzer and `guard` (architecture). Formats `github`, `gitlab`, `json`, `checkstyle`, `sarif`; baseline; `--fix`; `--minimum-fail-level`. Created 2024-10; 54 of the last 100 commits by the author. A 2025 third-party test found it faster but missing incremental analysis and some PHPStan rules (version 1.0 at the time; old).

**Recommendation: PHPStan**, with Larastan for Laravel. Reasons: widest extension ecosystem (checked: Larastan, `phpstan-strict-rules`, `phpstan-deprecation-rules`, `phpstan-phpunit`, `phpstan-symfony`, shipmonk dead-code-detector, type-coverage), a baseline for gradual adoption, strong maintainer base. Psalm has a bus-factor of one (unfinished 7.0 line, one maintainer). Mago is the one to watch: if its analyzer reaches parity it could replace PHPStan, Pint and Deptrac with one binary.
**Limits:** no SARIF output (use `github` or `checkstyle`/`json`); slow on large projects without result cache.
**Confidence:** high on PHPStan; Mago's maturity unverified.

### Code style

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [PHP-CS-Fixer](https://github.com/PHP-CS-Fixer/PHP-CS-Fixer) | v3.95.27 (2026-09-22) | 2026-10-09 | MIT | 13.6k |
| [Pint](https://github.com/laravel/pint) | v1.32.1 (2026-09-10) | 2026-10-14 | MIT | 3.2k |
| [PHP_CodeSniffer](https://github.com/PHPCSStandards/PHP_CodeSniffer) | 4.0.4 (2026-08-06) | 2026-10-21 | BSD-3-Clause | 1.6k |
| [ECS](https://github.com/easy-coding-standard/easy-coding-standard) (repo now `ecsphp/ecs`) | 13.3.9 (2026-10-23) | 2026-10-23 | MIT | 1.6k |
| [Slevomat coding standard](https://github.com/slevomat/coding-standard) | 8.31.1 (2026-07-31) | 2026-10-22 | MIT | 1.5k |
| Mago formatter | see above | | | |

PHP-CS-Fixer: `check` command and `--dry-run` fail on violations; formats `checkstyle`, `gitlab`, `json`, `junit`, `xml`; parallel by default; custom fixers supported (its docs mention AI-agent detection for the `@auto` format). Pint is built on PHP-CS-Fixer (README), has `--test`, `--format json`, `--parallel` (experimental) and Laravel presets. ECS runs PHP-CS-Fixer and PHPCS together.
**Recommendation: PHP-CS-Fixer**; use Pint instead for Laravel projects (it is the same engine with Laravel defaults, so run one of them, not both). PHPCS plus Slevomat only if you need sniffs PHP-CS-Fixer lacks; PHPCS has fixing (`phpcbf`) but you would then have two style tools, so do not default to it.
**Confidence:** medium-high. Not verified: whether Pint's output is stable for CI parsing, PHPCS's SARIF support.

### Automated refactoring and upgrades

[Rector](https://github.com/rectorphp/rector) 2.7.0 (2026-10-06, MIT, 10.5k stars, pushed 2026-10-23). `vendor/bin/rector process --dry-run` shows the diff without changing files (README); the non-zero exit code on pending changes was not read in the docs, so check it before relying on it. Supports PHP 5.3 to 8.5 upgrades and Symfony, PHPUnit and Doctrine rule sets; custom rules possible.
**Recommendation: Rector** (no real alternative; PHP-CS-Fixer's risky rules and Mago's fixes cover small parts). **Limits:** rules change code semantics, so run `--dry-run` in CI, apply fixes locally, and review the diff.
**Confidence:** high.

### Architecture

| Candidate | Latest release | Last push | Licence | Stars |
|---|---|---|---|---|
| [Deptrac](https://github.com/deptrac/deptrac) | 4.7.2 (2026-09-15) | 2026-09-20 | MIT | 3.0k |
| [Arkitect](https://github.com/phparkitect/arkitect) | 1.3.1 (2026-09-22) | 2026-10-19 | MIT | 936 |
| Mago `guard` | 1.58.2 | | | |

Deptrac **moved**: the old `qossmic/deptrac` repository is archived (last push 2025-02) and Packagist marks `qossmic/deptrac` abandoned in favour of `deptrac/deptrac`. Use the new name. Mago's docs say `mago guard` "covers the same ground as deptrac and arkitect" (self-reported) with layer rules and structural conventions (for example, controllers must be `final`).
**Recommendation: Deptrac.** Arkitect is the alternative when you want rules written as PHP code (class naming and structure) rather than layer config. **Limits:** Deptrac checks static dependencies only.
**Confidence:** medium-high.

### Dependency hygiene

| Candidate | Latest release | Last push | Licence | Stars | Unused | Shadow | Misplaced |
|---|---|---|---|---|---|---|---|
| [composer-dependency-analyser](https://github.com/shipmonk-rnd/composer-dependency-analyser) | 1.8.4 (2025-11-25) | 2026-08-11 | MIT | 635 | yes | yes | yes |
| [composer-unused](https://github.com/composer-unused/composer-unused) (repo moved from `icanhazstring`) | 0.9.7 (2026-10-23) | 2026-10-23 | MIT | 1.7k | yes | no | no |
| [ComposerRequireChecker](https://github.com/maglnet/ComposerRequireChecker) | 4.24.0 (2026-03-20) | 2026-10-16 | MIT | 1.0k | no | yes | no |

The feature matrix and timings (2 s versus 72 s and 124 s on 15,000 files) come from the shipmonk README, so they are **self-reported by the author of the winner**. The feature columns are consistent with each tool's own README. composer-unused recommends a PHAR install because it is sensitive to its dependency versions.
**Recommendation: composer-dependency-analyser**: one run covers what the other two split, zero Composer dependencies, PHP 7.2 to 8.5. This is the PHP counterpart of deptry. **Limits:** last release is November 2025 although the repo is still pushed to; static analysis misses dynamic class use.
**Confidence:** medium.

### Dependency vulnerabilities and abandoned packages

`composer audit` is built into [Composer](https://github.com/composer/composer) (stable 2.10.3, 2026-08-27; 2.11.0-RC1 published 2026-10-22). Docs on the main branch show `--audit-format` (`table`, `plain`, `json`, `summary`), `config.audit` with `fail` as the default for advisories, and a newer `config.policy` that adds blocking of flagged, abandoned and cooldown-period packages. Whether `config.policy` is in the stable 2.10 line was not verified.
**Recommendation:** use `composer audit` in CI; add no extra tool. [Roave/SecurityAdvisories](https://github.com/Roave/SecurityAdvisories) (pushed 2026-10-23, MIT, 2.9k stars) blocks installation of vulnerable versions via a conflict list; it duplicates what Composer now does, so not proposed. [phpcpd](https://github.com/sebastianbergmann/phpcpd) is archived (2023-01) and abandoned on Packagist: do not use.
**Confidence:** high for `composer audit`; low for `config.policy`.

### Dead code, type coverage, complexity, mutation

- [shipmonk/dead-code-detector](https://github.com/shipmonk-rnd/dead-code-detector) 1.4.2 (2026-09-21, MIT, 530 stars): PHPStan extension for unused methods, properties, constants and enum cases. Pick; limit: needs PHPStan, framework entry points require extension config.
- [TomasVotruba/type-coverage](https://github.com/TomasVotruba/type-coverage) 2.5.1 (2026-10-09, MIT, 226 stars): PHPStan extension that fails when return, param or property type coverage drops under a minimum. Useful but narrow; mention only.
- [PHPMD](https://github.com/phpmd/phpmd) 3.0.0 (2026-10-04, BSD-3-Clause, PHP 8.1 or later): the [2026-10-24 executed comparison](phpmd-mago.md) confirms additional NPath, direct LOC, numeric coupling and combined public-surface budgets. Cyclomatic complexity and member/parameter counts already overlap Mago; WMC aggregation differs. Not recommended: Mago stays the default PHP toolchain, and a narrow PHPMD companion is optional for teams that explicitly need those budgets. The review also covers 3.x migration and current parser/configuration limitations.
- [Infection](https://github.com/infection/infection) 0.35.8 (2026-10-14, BSD-3-Clause, 2.3k stars): mutation testing; `--min-msi` threshold not verified in this run. No pick (the earlier "slow" was read, not run; StrykerJS passed a changed-files run, see [stryker.md](stryker.md)).
- [GrumPHP](https://github.com/phpro/grumphp) v2.26.0 (2026-10-16, MIT, 4.3k stars): git-hook runner, belongs to the open "Git hooks" decision.

---

## Newer or overlapping tools: summary

| Tool | Replaces | Status | Why not proposed |
|---|---|---|---|
| Mago (PHP) | PHPStan + Pint/PHP-CS-Fixer + Deptrac + parts of PHPCS | 1.58.2, created 2024-10, SARIF and baseline | Parity with PHPStan extensions (Larastan, Symfony) unverified. Re-review in 3 to 6 months. |
| pyscn (Python) | vulture + xenon/radon + parts of import-linter | 1.32.5, created 2025-08, `pyscn check` gate | One main contributor; no comparison run. |
| Skylos (Python) | vulture + secrets/security + agent-branch checks | 5.0.0, 848 stars | Young; accuracy claims self-reported. |
| Herb (Ruby) | erb_lint and ERB formatting | 0.11.1 pre-1.0, Node linter | Pre-1.0; rule coverage not compared. |
| pks (Ruby) | Packwerk | 0.7.0, 10 stars | Too young. |
| ty (Python) | mypy/pyright | 0.0.91, beta | Not stable. |

**Deprecated or moved (verified):** `qossmic/deptrac` archived, moved to `deptrac/deptrac`; pydocstyle archived (2023); phpcpd archived and Packagist-abandoned; `icanhazstring/composer-unused` is now `composer-unused/composer-unused`; `symplify/easy-coding-standard` is now `easy-coding-standard/easy-coding-standard` (repo `ecsphp/ecs`); `fpgmaas/deptry` is `osprey-oss/deptry` (the README already uses the new name); better_html is marked DEPRECATED in its description; fasterer, xenon and radon are stale (no release since 2023-24). I found no 2026 supply-chain incident for these tools in this run, but my searches for incidents returned nothing relevant, so absence is **not verified**.

---

## Proposed README entries

Place each under the ecosystem heading shown. For Python, Ruby and PHP the README currently has only Ruff and deptry, and RuboCop; add a `### PHP` section.

### Python

- **[Pyrefly](https://github.com/facebook/pyrefly)**: type checker with stable releases since 1.0.0 (May 2026), SARIF, JSON and JUnit output, and a baseline for gradual adoption. Chosen over mypy (slow, no SARIF), ty (beta) and zuban (AGPL). *Limits:* any release may add type errors, so pin the version; pyright is the more battle-tested alternative. [Details](https://github.com/mokevnin/dev-quality-gates/blob/main/research/stack-python-ruby-php.md).
- **[vulture](https://github.com/jendrikseipp/vulture)**: unused functions, classes and variables across modules, which Ruff cannot see. *Limits:* heuristic; needs a whitelist for framework entry points.
- **[import-linter](https://github.com/seddonym/import-linter)**: import contracts (layers, forbidden, independence, protected) that fail CI. *Limits:* checks imports only; [tach](https://github.com/tach-org/tach) is the alternative for public-interface rules.

### Ruby

- **[Sorbet](https://github.com/sorbet/sorbet)**: static type checker with per-file strictness, so a codebase can adopt it gradually; Tapioca generates types for gems and Rails. *Limits:* `sig` boilerplate; Steep with RBS is the alternative.
- **[Packwerk](https://github.com/Shopify/packwerk)**: package boundaries and privacy for Rails apps. *Limits:* needs Zeitwerk; checks constant references only; [pks](https://github.com/rubyatscale/pks) is a young Rust port.
- **[Brakeman](https://github.com/presidentbeef/brakeman)**: Rails security scanner; exits non-zero on warnings; SARIF and JSON output. *Limits:* **free for non-commercial use only; commercial use needs a paid licence.** Rails only.

### PHP

- **[PHPStan](https://github.com/phpstan/phpstan)**: static analysis with levels and a baseline; the widest extension set (Larastan, Symfony, strict rules, dead-code detection). Chosen over Psalm (one active maintainer, 7.0 still in RC). *Limits:* no SARIF; use Larastan for Laravel.
- **[PHP-CS-Fixer](https://github.com/PHP-CS-Fixer/PHP-CS-Fixer)**: code style check and fix, parallel by default, custom fixers. *Limits:* Laravel projects should use [Pint](https://github.com/laravel/pint), the same engine with Laravel defaults; run one, not both.
- **[Rector](https://github.com/rectorphp/rector)**: automated PHP upgrades and refactoring; `--dry-run` as a CI gate. *Limits:* rules change semantics; review diffs; confirm the exit code on pending changes.
- **[Deptrac](https://github.com/deptrac/deptrac)**: layer dependency rules. *Limits:* use the `deptrac/deptrac` repository (the old `qossmic/deptrac` is archived); static dependencies only.
- **[composer-dependency-analyser](https://github.com/shipmonk-rnd/composer-dependency-analyser)**: unused, shadow and misplaced Composer dependencies in one fast run. *Limits:* timings are self-reported; last release November 2025. Use `composer audit` (built in) for vulnerabilities.

### Amendments to existing entries (not new entries)

- **RuboCop:** add to *Limits*: "SARIF output is built in. Add `rubocop-rails`, `rubocop-rspec` (or `rubocop-minitest`) and `rubocop-performance` as plugins; Standard and fasterer are not needed."
- **Ruff:** the `S` rules overlap Bandit but do not replace every check; see the [executed B614/B615 comparison](bandit.md). `D` replaces pydocstyle (archived), `C901` replaces xenon and radon; pair with vulture for dead code across modules.

### Rows for docs/not-adopted.md

| Tool | Reason | What would change the answer |
|---|---|---|
| pydocstyle | Archived 2023-11; Ruff `D`. | None. |
| xenon, radon | Stale (no release since 2023-24); Ruff `C901`. | A new release. |
| Standard (Ruby) | Wrapper over RuboCop; overlap. | You want zero configuration. |
| fasterer | Stale; rubocop-performance. | None. |
| Psalm | One active maintainer; 7.0 still RC. | Stable 7.0 and more maintainers. |
| qossmic/deptrac | Archived; moved. | None. |
| phpcpd | Archived; abandoned. | None. |
| Mutant | Commercial licence for closed-source use. | Licence change. |
| ty, zuban | Beta; AGPL. | ty 1.0; a licence change. |
| Mago, pyscn, Skylos, Herb, pks | Young; not compared on real code. | Parity evidence and a second review. |

---

## `tools.json` records

```json
[
  {
    "id": "pyrefly",
    "repo": "facebook/pyrefly",
    "category": "Python",
    "last_reviewed": "2026-10-23",
    "sources": [
      "https://github.com/facebook/pyrefly/releases/tag/1.0.0",
      "https://pyrefly.org/en/docs/configuration/",
      "research/stack-python-ruby-php.md"
    ],
    "rationale": "Stable since 1.0.0 (2026-05-12), MIT, monthly releases. Output formats include json, github, junit-xml, code-climate and sarif; baseline and suppress commands support gradual adoption.",
    "limitations": "Version policy allows new type errors in any release, so pin the version. Less proven than pyright on edge cases; no real-codebase comparison was run. Pyright is the conservative alternative."
  },
  {
    "id": "vulture",
    "repo": "jendrikseipp/vulture",
    "category": "Python",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/jendrikseipp/vulture", "research/stack-python-ruby-php.md"],
    "rationale": "Finds unused functions, classes and variables across modules, which Ruff F401 and F841 do not. Confidence threshold and generated whitelists.",
    "limitations": "Heuristic; framework entry points need a whitelist. Exit-code behaviour not verified in the review."
  },
  {
    "id": "import-linter",
    "repo": "seddonym/import-linter",
    "category": "Python",
    "last_reviewed": "2026-10-23",
    "sources": ["https://import-linter.readthedocs.io/", "research/stack-python-ruby-php.md"],
    "rationale": "Import contracts (layers, forbidden, independence, protected, acyclic siblings, custom) that fail CI. Steady commit rate; config in pyproject.toml or .importlinter.",
    "limitations": "Checks imports only, not calls. Tach (Rust, public-interface rules) is the alternative; it has a single main maintainer."
  },
  {
    "id": "sorbet",
    "repo": "sorbet/sorbet",
    "category": "Ruby",
    "last_reviewed": "2026-10-23",
    "sources": ["https://sorbet.org/docs/overview", "research/stack-python-ruby-php.md"],
    "rationale": "Gradual static typing with per-file strictness sigils; releases almost daily; Tapioca generates RBI for gems and Rails; rubocop-sorbet adds cops.",
    "limitations": "sig boilerplate; Rails metaprogramming needs Tapioca DSL files kept current. Steep with RBS is the alternative. Output formats for srb tc not verified."
  },
  {
    "id": "packwerk",
    "repo": "Shopify/packwerk",
    "category": "Ruby",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/Shopify/packwerk#readme", "research/stack-python-ruby-php.md"],
    "rationale": "Package boundaries and constant privacy for Rails apps; extensions add layers and visibility. Release 3.3.1 on 2026-08-26.",
    "limitations": "Needs Zeitwerk. Checks constant references only. pks is a Rust port with 10 stars at v0.7.0, too young."
  },
  {
    "id": "brakeman",
    "repo": "presidentbeef/brakeman",
    "category": "Ruby",
    "last_reviewed": "2026-10-23",
    "sources": [
      "https://github.com/presidentbeef/brakeman/blob/main/LICENSE.md",
      "https://github.com/presidentbeef/brakeman#readme",
      "research/stack-python-ruby-php.md"
    ],
    "rationale": "Rails security scanner; non-zero exit on warnings by default; SARIF, JSON, JUnit and other formats; --compare against a previous report.",
    "limitations": "Brakeman Public Use License: free for non-commercial use, commercial use requires a paid licence. Rails only. No verified free alternative was found."
  },
  {
    "id": "phpstan",
    "repo": "phpstan/phpstan",
    "category": "PHP",
    "last_reviewed": "2026-10-23",
    "sources": ["https://phpstan.org/", "research/stack-python-ruby-php.md"],
    "rationale": "Levels, baseline and the widest extension set (Larastan, Symfony, strict rules, deprecation rules, dead-code detector, type coverage). Formatters: json, junit, checkstyle, github, gitlab, teamcity. Several active maintainers.",
    "limitations": "No SARIF formatter. Slow on large projects without result cache. Psalm is a close alternative but has one active maintainer and 7.0 is still in RC."
  },
  {
    "id": "php-cs-fixer",
    "repo": "PHP-CS-Fixer/PHP-CS-Fixer",
    "category": "PHP",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/PHP-CS-Fixer/PHP-CS-Fixer/blob/master/doc/usage.rst", "research/stack-python-ruby-php.md"],
    "rationale": "Style check and fix with --dry-run or the check command; parallel by default; custom fixers; formats checkstyle, gitlab, json, junit, xml. Pint and ECS build on it.",
    "limitations": "No SARIF. Laravel projects should use Pint instead (same engine); run one of them. PHPCS with Slevomat covers sniffs it lacks but adds a second style tool."
  },
  {
    "id": "rector",
    "repo": "rectorphp/rector",
    "category": "PHP",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/rectorphp/rector#readme", "research/stack-python-ruby-php.md"],
    "rationale": "Automated PHP 5.3 to 8.5 upgrades and refactoring with Symfony, PHPUnit and Doctrine rule sets; --dry-run as a CI gate; custom rules.",
    "limitations": "Rules can change semantics, review diffs. Exit code on pending changes was not confirmed from the docs."
  },
  {
    "id": "deptrac",
    "repo": "deptrac/deptrac",
    "category": "PHP",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/deptrac/deptrac", "https://packagist.org/packages/qossmic/deptrac", "research/stack-python-ruby-php.md"],
    "rationale": "Layer dependency rules for PHP. Active (4.7.2, 2026-09-15). The old qossmic/deptrac repository is archived and Packagist points to deptrac/deptrac.",
    "limitations": "Static dependencies only. Arkitect covers class-structure rules; Mago guard is a young alternative."
  },
  {
    "id": "composer-dependency-analyser",
    "repo": "shipmonk-rnd/composer-dependency-analyser",
    "category": "PHP",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/shipmonk-rnd/composer-dependency-analyser#readme", "research/stack-python-ruby-php.md"],
    "rationale": "Detects unused, shadow and misplaced Composer dependencies in one run; composer-unused finds only unused, ComposerRequireChecker only shadow ones. No Composer dependencies of its own.",
    "limitations": "Comparison table and timings are by the tool's own author. Last release 2025-11-25. Static analysis misses dynamic class use."
  }
]
```

For the two amendments (RuboCop, Ruff), edit the existing `limitations` strings; no new records.

## What was not verified (all ecosystems)

- No tool was run: speed, false positives, exit codes of vulture, Rector, `uv sync --locked`, `srb tc`, Herb, and pyscn are unconfirmed.
- Web searches for 2026 incidents, successors and deprecations returned almost nothing useful; the absence of incidents is not evidence.
- Licence identifiers from the GitHub API were often `NOASSERTION` or `Other`; I read `LICENSE` text for mypy, zuban, Brakeman, Mutant, Standard and pyright only.
- Composer `config.policy` availability in the stable line; PHPCS and Pint SARIF support; SimpleCov `minimum_coverage`; Infection `--min-msi`.
- Whether Steep, Herb or Mago outperform the picks on real projects.
