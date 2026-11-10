# Ecosystem gaps: what the main stacks treat as standard and we do not list

Research date: 2026-10-23. Method: GitHub API (stars, pushes, releases), registry APIs (npm, PyPI via pypistats, crates.io, RubyGems, NuGet, Packagist, Hex), READMEs and docs. **No third-party tool was installed or run**, so every claim about behaviour (exit codes, flags) rests on documentation unless marked otherwise.

## How to read the numbers

| Column | Meaning |
|---|---|
| Stars | GitHub stars today. Repos that moved show low stars (Sobelow) or are mirrors (html-validate). |
| Downloads | **Units differ by registry; do not compare across ecosystems.** npm and PyPI: last 30 days. Packagist: monthly. crates.io and Hex: last 90 days. RubyGems and NuGet: **all-time** (only useful to rank within one ecosystem). |
| Release | Latest release from the registry or GitHub Releases, with date. `(tag)` = GitHub tags API, which sorts by name, so the date is unknown. GitHub "latest release" is wrong for projects that stopped using it (standard, StyleCop), so registry versions are used there. |

## Decisions that apply everywhere

1. **osv-scanner (already listed) reads these lockfiles**, checked in its docs: `Gemfile.lock`, `uv.lock`, `poetry.lock`, `pnpm-lock`, `Cargo.lock`, `composer.lock`, `mix.lock`, `pom.xml`, `gradle.lockfile`, `go.mod`, `packages.lock.json`. So one tool per job means we do **not** add bundler-audit (GPL-3.0), pip-audit, `uv audit`, `composer audit`, mix_audit or OWASP Dependency-Check by default. Rows below say "overlap: osv-scanner".
2. **Plugins and formatters of tools already listed are edits to those entries, not new entries** (see "Edits to existing entries").
3. **Mutation testing** (mutmut, cargo-mutants, Stryker, Infection, PIT): no pick per stack yet. The earlier "slow, run on a schedule" was read, not run. A StrykerJS run limited to changed files worked as a pull request gate in seconds per file, and StrykerJS is now listed; see [stryker.md](stryker.md). The others need the same run.
4. **Library-only tools stay out** (cargo-hack, cargo-semver-checks, publint, arethetypeswrong), as already decided for cargo-semver-checks.

---

## Ruby and Rails

| Job | Candidate | Repo | Stars | Downloads | Release | Licence |
|---|---|---|---|---|---|---|
| Unsafe migrations | **strong_migrations** | ankane/strong_migrations | 4459 | 86M gem | 2.8.0, 2026-05-14 | MIT |
| N+1 queries | **Bullet** | flyerhzm/bullet | 7340 | 188M gem | 8.3.0, 2026-10-10 | MIT |
| N+1 (static) | rails_best_practices | flyerhzm/rails_best_practices | 4158 | n/a | (tag) v1.23.4, last push 2026-04-23 | MIT |
| I18n keys | **i18n-tasks** | glebm/i18n-tasks | 2158 | 35M gem | 1.1.2, 2025-11-27 | MIT |
| ERB lint | **Herb** | marcoroth/herb | 1333 | `@herb-tools/linter` 603k npm; 2.2M gem | 0.11.1, 2026-10-20 | MIT |
| ERB lint (old) | erb_lint | Shopify/erb_lint | 749 | 22M gem | 0.9.0, 2025-01-20 | MIT |
| Types | **Sorbet** (+ tapioca) | sorbet/sorbet | 3806 | `sorbet-runtime` 157M, `sorbet` 58M, `tapioca` 35M gem | daily builds, 2026-10-23 | Apache-2.0 |
| Types | Steep (RBS) | soutaro/steep | 1492 | 6.9M gem | 2.1.0, 2026-08-27 | MIT |
| Boundaries | **Packwerk** | Shopify/packwerk | 1927 | 23M gem | 3.3.1, 2026-08-26 | MIT |
| Boundaries (Rust) | pks | rubyatscale/pks | 10 (unverified, looks low) | n/a | 0.7.0, 2026-10-12 | MIT |
| SAST | Brakeman | presidentbeef/brakeman | 7285 | 244M gem | 8.1.0, 2026-09-30 | Brakeman Public Use License |
| Code smells | reek | troessner/reek | 4137 | 40M gem | 6.6.0, 2026-10-02 | MIT |
| Style variant | standard | standardrb/standard | 2928 | 53M gem | 1.57.0, 2026-10-05 | MIT |
| RuboCop plugins | rubocop-rails / rubocop-rspec / rubocop-performance | rubocop/* | 877 / 859 / 743 | 318M / 304M gem | 2.38.0 (2026-09-20) / 3.10.2 / 1.27.0 | MIT |
| Advisories | bundler-audit | rubysec/bundler-audit | 2764 | 150M gem | 0.9.3, 2025-11-28 | GPL-3.0 |

**Recommendations:**

- **strong_migrations** for Rails migrations. It raises during `db:migrate` on locking operations and gives the safe alternative. It works on Ruby migration DSL, so it does not overlap with squawk (SQL files). Limits: PostgreSQL, MySQL, MariaDB only; runs at migration time, so CI must run the migrations.
- **Bullet** for N+1 and unused eager loading. Set `Bullet.raise = true` in test so specs fail (README). Limits: finds only what the test suite exercises.
- **i18n-tasks** (`i18n-tasks health`, missing and unused keys, normalised files). The only mature option for Rails; last release is 11 months old but the repo is active.
- **Herb** over erb_lint. erb_lint has had no release since 2025-01; Herb is a C parser with linter, formatter and language server, and the linter has 600k npm downloads a month. Limits: pre-1.0; the formatter is marked experimental; the linter runs from npm (`npx @herb-tools/linter`), so Ruby-only CI needs Node.
- **Sorbet** (with tapioca for gems and Rails) over Steep: about 8x the stars-to-downloads pull, used by Stripe and Shopify. Limits: needs `sig` annotations and a typed-level migration; Steep and RBS are the standard-library direction, so revisit yearly.
- **Packwerk** for package boundaries and privacy. pks is a Rust drop-in about 10-20x faster per its README, but is tiny (10 stars, unverified); name it in the limits.
- **Brakeman**: licence unchanged. `LICENSE.md` is the "Brakeman Public Use License" (copyright Synopsys, 2019): commercial use requires a paid licence; the README says "free for non-commercial use". (A separate `MIT-LICENSE` file in the repo is from a bundled component, not the tool.) It is the only Rails SAST of weight, released 2026-09-30. Keep it in Under review with the licence warning; do not recommend for commercial work.
- **Reject:** reek (style noise, overlaps RuboCop Metrics), rails_best_practices (mostly superseded by rubocop-rails, no release signal since April), erb_lint (superseded), bundler-audit (overlap: osv-scanner, GPL), standard (a config of RuboCop; one tool per job).

Confidence: strong_migrations, Bullet, i18n-tasks high; Packwerk medium; Herb and Sorbet medium (pre-1.0 and heavy to adopt respectively); Brakeman licence high.

## Python and Django

| Job | Candidate | Repo | Stars | Downloads (30 d) | Release | Licence |
|---|---|---|---|---|---|---|
| Django upgrades | **django-upgrade** | adamchainz/django-upgrade | 1252 | 469k | 1.33.0 (tag), pushed 2026-10-15 | MIT |
| Django migrations | **django-migration-linter** | David-Wobrock/django-migration-linter | 623 | 3.4M | 6.0.0, 2026-01-04 | Apache-2.0 |
| Django types | django-stubs | typeddjango/django-stubs | 1979 | 10.4M | 6.1.2, 2026-10-05 | MIT |
| Template lint | djLint | djlint/djLint | 953 | 2.9M | 1.47.0, 2026-10-22 | GPL-3.0 |
| N+1 | nplusone | jmcarp/nplusone | 1069 | 442k | 1.0.0 (tag), last push 2022-11 | MIT |
| Coverage | coverage.py | nedbat/coveragepy | 3424 | 282M | 7.17.0, 2026-10-22 | Apache-2.0 |
| Coverage on changed lines | **diff-cover** | Bachmann1234/diff_cover | 849 | 24.2M | 10.6.0, 2026-09-22 | Apache-2.0 |
| Boundaries | import-linter (listed) | seddonym/import-linter | 1234 | 21.2M | 2.15 (tag) | BSD-2-Clause |
| Boundaries | tach | tach-org/tach | 2851 | 4.6M | 0.35.3, 2026-10-06 | MIT |
| Mutation | mutmut | boxed/mutmut | 1502 | 5.8M | 3.8.0, 2026-09-12 | BSD-3-Clause |
| Mutation | cosmic-ray | sixty-north/cosmic-ray | 662 | 579k | 8.7.0, 2026-08-09 | MIT |
| Advisories | pip-audit | pypa/pip-audit | 1381 | 26.7M | 2.10.1, 2026-06-10 | Apache-2.0 |
| Types | ty / Pyrefly / mypy / pyright | astral-sh/ty, facebook/pyrefly, python/mypy, microsoft/pyright | 19.9k / 7.1k / 20.7k / 15.7k | 41M / 7.8M / 160M / 40M | ty 0.0.91 (beta), **Pyrefly 1.4.0 (2026-10-15)**, mypy 2.4.0 (tag) | MIT / MIT / MIT / MIT |

**Recommendations:**

- **django-upgrade**: rewrites code to the idioms of your target Django version; `--target-version` and a non-zero exit when it changes files make it a CI check. Narrow but the clear standard (Adam Johnson). Confidence medium-high.
- **django-migration-linter**: Django-specific backward-incompatible migration detection (`lintmigrations`). It is a different job from squawk, which lints SQL; use it with squawk on `sqlmigrate` output only if you want both. Not run by us. Confidence medium.
- **diff-cover** as the language-agnostic coverage ratchet for changed lines (`--fail-under`). It reads Cobertura, JaCoCo, lcov-style XML reports (list of formats: unverified). Better than a global floor because it does not fail old code. Complements the "Coverage ratchet" pattern. Confidence medium.
- **uv**: `uv lock --check` and `uv sync --locked` are built in; document as a pattern, not an entry.
- **import-linter stays**; tach is a Rust option with a fifth of the downloads. No change.
- **Types: no clear winner.** Pyrefly is now 1.4.0 stable (not beta), ty is still 0.0.x. django-stubs works through the mypy plugin; Rust checkers do not run mypy plugins, so Django projects that want model-aware types still need mypy. Update the "Python types" row in Under review.
- **No clear winner:** N+1 for Django (nplusone is dead since 2022; django-perf-rec has 354 stars), mutation testing (mutmut leads; not run, see [stryker.md](stryker.md) for the changed-files gate), template lint (djLint is GPL-3.0 and covers many template languages, but formatting overlaps).
- **Reject:** pip-audit (overlap: osv-scanner).

## JavaScript and TypeScript (and web)

| Job | Candidate | Repo | Stars | Downloads (30 d) | Release | Licence |
|---|---|---|---|---|---|---|
| CSS lint | **Stylelint** | stylelint/stylelint | 11538 | 44.4M | 17.16.0, 2026-10-01 | MIT |
| Runtime a11y | **axe-core** (`@axe-core/playwright`) | dequelabs/axe-core | 7696 | 316M core; 53M playwright | 4.14.0, 2026-10-05 | MPL-2.0 |
| Performance budgets | **Lighthouse CI** | GoogleChrome/lighthouse-ci | 7117 | 7.1M | 0.15.1, **2025-06-26** (pushed 2026-10-23) | Apache-2.0 |
| Bundle size budget | **size-limit** | ai/size-limit | 7038 | 5.9M | 14.3.0, 2026-10-22 | MIT |
| Monorepo versions | **syncpack** | JamieMason/syncpack | 2104 | 11.0M | 15.3.3, 2026-08-09 | MIT |
| Monorepo versions | sherif | QuiiBz/sherif | 1192 | 2.3M | 1.13.0, 2026-07-04 | MIT |
| i18next keys | **i18next-cli** | i18next/i18next-cli | 244 | 3.5M | 1.80.0 (tag) | MIT |
| i18next keys (old) | i18next-parser | i18next/i18next-parser | n/a | 2.2M | n/a | MIT |
| Hardcoded strings | eslint-plugin-i18next | edvardchen/eslint-plugin-i18next | n/a | 6.1M | n/a | MIT |
| HTML validity | html-validate | html-validate/html-validate (GitHub mirror, 19 stars; main repo on GitLab) | n/a | 2.0M | 11.17.0 (tag) | MIT |
| Lockfile policy | lockfile-lint | lirantal/lockfile-lint | 870 | 1.6M | api 5.10.0, 2026-10-09 | Apache-2.0 |
| Type coverage | type-coverage | plantain-00/type-coverage | 1351 | 1.5M | 2.30.4 (tag) | MIT |
| Cycles, boundaries | madge / Sheriff / eslint-plugin-boundaries | pahen/madge, softarc-consulting/sheriff, javierbrea/eslint-plugin-boundaries | 10.2k / 325 / 1001 | 11.6M / 533k / 7.4M | madge 8.0.0 (tag, last push 2026-01); Sheriff 0.20.0; boundaries 7.3.0 | MIT |
| Mutation | Stryker | stryker-mutator/stryker-js | 3271 | 13.3M | 10.1.1, 2026-10-23 | Apache-2.0 |

**Recommendations:**

- **Stylelint**: the CSS/SCSS standard; Oxlint does no CSS, Biome's CSS rules are narrower. Limits: CSS only; add `stylelint --formatter json` for agents. Confidence high.
- **axe-core** through `@axe-core/playwright` for accessibility in tests (violations fail the test). Static JSX a11y rules already exist inside Oxlint (its `jsx-a11y` plugin is built in per the Oxlint docs); this is the runtime job. Limits: finds roughly the automatable part of WCAG, needs a Playwright suite; MPL-2.0. Confidence high.
- **size-limit** for bundle budgets (fails when a bundle exceeds the limit, also checks time to load). Works for apps and libraries. Confidence medium-high.
- **Lighthouse CI** (`lhci assert` with budgets) for Core Web Vitals regressions. Only mature option, but the last GitHub release is 16 months old while commits continue (npm publish workflow was added 2026-10-23). Flag it in limitations; confidence medium. The job is "no clear winner" if you need a maintained release line.
- **syncpack** over sherif: syncpack is Rust-based since v14 (repo has `Cargo.toml` and `crates/`), has 5x the downloads, and checks version consistency, ranges and formatting; sherif is zero-config and fast but narrower. Limits: monorepos only; package-manager catalogs (pnpm, Bun) reduce the need. Confidence medium.
- **i18next-cli** for i18next projects: `extract --ci` fails if files would change, `status` exits non-zero when translations are missing, `lint` finds hardcoded strings. Only 244 stars, but 3.5M downloads and it is the official i18next tool. Limits: i18next only (Lingui and FormatJS have their own CLIs). Confidence medium.
- **No entry:** html-validate (main repo on GitLab; hold), lockfile-lint (npm and yarn only; its docs say pnpm lockfiles cannot carry the attack; overlap with osv-scanner and `--ignore-scripts` policy), type-coverage (Oxlint and strict TypeScript cover the intent), Stryker (scheduled), madge, Sheriff and eslint-plugin-boundaries (overlap: dependency-cruiser; the last is ESLint-only). Not verified: whether type-coverage and Sheriff work with TypeScript 7.
- **Biome** remains the open alternative toolchain; unchanged.

## Go

| Job | Candidate | Repo | Stars | Release | Licence |
|---|---|---|---|---|---|
| Architecture | **go-arch-lint** | fe3dback/go-arch-lint | 616 | 1.19.0, 2026-09-07 | MIT |
| Architecture | arch-go | arch-go/arch-go (moved from fdaines) | 280 | 2.1.2, 2026-02-03 | MIT |
| Nil panics | NilAway | uber-go/nilaway | 3926 | no releases (tags only) | Apache-2.0 |
| Dead code | deadcode | golang/tools (`cmd/deadcode`) | 8008 | x/tools v0.52.0, 2026-10-10 | BSD-3-Clause |
| SQL queries | sqlc (`sqlc vet`, `sqlc diff`) | sqlc-dev/sqlc | 18406 | 1.31.1, 2026-04-22 | MIT |
| Release config | GoReleaser (`goreleaser check`) | goreleaser/goreleaser | 16117 | 2.19.0, 2026-10-22 | MIT |
| Formatting | gofumpt | mvdan/gofumpt | 4101 | 0.12.0, 2026-09-07 | BSD-3-Clause |
| Coverage | go-test-coverage | vladopajic/go-test-coverage | 242 | 2.20.1 | GPL-3.0 (already rejected) |

**Recommendations:**

- **go-arch-lint** is the better Go architecture tool today (2x the stars, monthly cadence; arch-go moved repositories and is smaller). Both are small, so confidence is low-medium; keep as a proposal with that flag, and note ArchUnit-like Go rules are also possible with ast-grep (listed).
- **gofumpt**: do not add. `golangci-lint fmt` has `gofumpt` as a formatter (listed in the golangci-lint formatter docs); edit the golangci-lint entry.
- **NilAway**: strong tool (Uber), but it has no releases and runs as a golangci-lint private plugin or standalone, which is heavy to set up. Keep in Under review.
- **deadcode**: reject as an enforcer. Verified by running v0.52.0 (Go 1.26) on a four-function module (2026-10-24): it prints `unreachable func: unused` and exits 0, so it reports and does not fail. The script around it is one line, `out=$(deadcode -test ./...) && [ -z "$out" ]`; the `&&` matters, because `deadcode` does exit 1 when packages fail to load (checked), and `;` would let that pass with empty output. Two flags decide whether the output is usable, both checked in the same run:
  - without `-test`, a function in a non-test file that only tests call is reported as dead;
  - without `-tags`, a function that only a build-tagged test calls (`//go:build integration`) is reported as dead, the same blindness golangci-lint has without `run.build-tags`. Pass every tag the test suite uses.

  It still cannot see a function whose only caller is its own test: `-test` makes that one reachable. Keep it out of the list (it does not fail a build by itself); a wrapper is enough if you want it.
- **sqlc vet** (CEL lint rules for queries) and **`goreleaser check`** are checks inside tools you already use. Document in patterns when the project uses sqlc or GoReleaser; not entries.

## Rust

| Job | Candidate | Repo | Stars | Downloads (90 d) | Release | Licence |
|---|---|---|---|---|---|---|
| Unused dependencies | **cargo-machete** | bnjbvr/cargo-machete | 1389 | 594k | 0.9.2, 2026-04-15 | MIT |
| Unused dependencies | cargo-shear | Boshen/cargo-shear | 577 | 62k | 1.14.0, 2026-09-22 | MIT |
| Unused dependencies | cargo-udeps | est31/cargo-udeps | 2144 | 111k | 0.1.61, 2026-04-29 | MIT/Apache-2.0 |
| Test runner | **cargo-nextest** | nextest-rs/nextest | 3359 | 1.86M | 0.9.149, 2026-10-20 | Apache-2.0 |
| Coverage threshold | **cargo-llvm-cov** | taiki-e/cargo-llvm-cov | 1482 | 1.88M | 0.9.1, 2026-09-06 | Apache-2.0 |
| Coverage | tarpaulin | xd009642/tarpaulin | 3022 | 301k | 0.37.5, 2026-09-27 | Apache-2.0 |
| Mutation | cargo-mutants | sourcefrog/cargo-mutants | 1353 | 366k | 27.1.0, 2026-06-02 | MIT |
| Supply chain audits | cargo-vet | mozilla/cargo-vet | 998 | 120k | 0.10.3, 2026-10-22 | Apache-2.0 |
| Feature matrix | cargo-hack | taiki-e/cargo-hack | 875 | 208k | 0.6.45, 2026-05-30 | Apache-2.0 |

**Recommendations:**

- **cargo-machete** for unused dependencies: fast and widely used (10x cargo-shear), CI exit code via `--with-metadata` and non-zero on findings (docs: unverified). It is regex-based, so it can report false positives, which are handled with a `package.metadata.cargo-machete.ignored` list. cargo-shear is the credible newer alternative (AST-based, by the Oxc author, declared feature-complete, also finds unlinked source files); this is a judgement call, flagged. cargo-udeps needs nightly.
- **cargo-nextest**: the practitioner standard test runner (about 3x faster, retries, flaky-test detection, JUnit output). It enforces by failing the test run, so it is a speed and signal tool. Optional entry; confidence medium.
- **cargo-llvm-cov** for coverage floors (`--fail-under-lines`, docs: unverified); preferred to tarpaulin on downloads and on accuracy of LLVM instrumentation.
- **Reject:** cargo-hack (library feature matrices), cargo-vet (needs an audit process and a team; cargo-deny already covers advisories and licences), cargo-mutants (no entry yet; not run on changed files, see [stryker.md](stryker.md)).

## JVM: Java and Kotlin

| Job | Candidate | Repo | Stars | Release | Licence |
|---|---|---|---|---|---|
| Null safety | **NullAway** (error-prone plugin) | uber/NullAway | 4124 | 0.14.3, 2026-10-22 | MIT |
| Style, naming, Javadoc | Checkstyle | checkstyle/checkstyle | 9616 | 14.3.0, 2026-09-27 | LGPL-2.1 |
| Rules and copy-paste | PMD | pmd/pmd | 5516 | 7.28.0, 2026-09-25 | BSD-style (reported NOASSERTION) |
| Bytecode bugs | SpotBugs | spotbugs/spotbugs | 3962 | 4.10.5, 2026-10-12 | LGPL-2.1 |
| Kotlin smells | **detekt** | detekt/detekt | 7102 | **1.23.8, 2025-02-21**; 2.0.0-alpha.6, 2026-08-04 | Apache-2.0 |
| Kotlin format | ktlint | pinterest/ktlint | 6766 | 1.8.0, 2025-11-14 | MIT |
| Kotlin architecture | Konsist | LemonAppDev/Konsist | 1748 | 0.18.1, 2026-10-10 | Apache-2.0 |
| Advisories | OWASP Dependency-Check | **dependency-check/DependencyCheck** (old jeremylong repo archived 2025) | 7738 | 13.0.0, 2026-08-03 | Apache-2.0 |
| Mutation | PIT | hcoles/pitest | 1877 | n/a | Apache-2.0 |
| Coverage | JaCoCo / Kover | jacoco/jacoco, Kotlin/kotlinx-kover | 4612 / 1645 | 0.8.15 / 0.9.11 | EPL / Apache-2.0 |

(Maven Central search returned stale versions, so these come from GitHub.)

**Recommendations:**

- **NullAway**: add as a companion to the listed error-prone (it runs as an error-prone check, so it is an edit of that entry or a one-line entry). Fails the compile on possible nulls; Uber-scale adopters. Limits: needs `@Nullable` conventions; Kotlin has its own null safety.
- **detekt** for Kotlin (complexity, smells, potential bugs): the de facto standard, 7k stars, active pushes. Stable release is old (1.23.8, Feb 2025) and 2.0 is in alpha since April; say so in limits. ktlint formatting is already reachable through the listed spotless, so no ktlint entry (one tool per job). Confidence medium.
- **Checkstyle, PMD, SpotBugs: no clear winner.** All are active, but spotless plus error-prone plus ArchUnit already cover format, bug patterns and architecture; Checkstyle adds naming and Javadoc rules, PMD adds a rule set and copy-paste detection, SpotBugs does bytecode flow analysis. Add one only if you need its specific rules.
- **OWASP Dependency-Check:** the repository moved to `dependency-check/DependencyCheck` (v13.0.0); the old `jeremylong` repo is archived (verified). Do not add by default: overlap with osv-scanner (`pom.xml`, `gradle.lockfile`); it needs an NVD API key or updates are "extremely slow" (its README). Use it only when you need CPE matching of jars without coordinates.
- **Konsist**: pre-1.0, overlaps ArchUnit (which already works on Kotlin bytecode). Hold.

## .NET

| Job | Candidate | Repo | Stars | Downloads (NuGet, all-time) | Release | Licence |
|---|---|---|---|---|---|---|
| Analyzer pack | **Roslynator** | dotnet/roslynator (JosefPihrt/Roslynator) | 3488 | 64M | 5.0.1, 2026-10-04 | Apache-2.0 (API shows NOASSERTION) |
| Analyzer pack | Meziantou.Analyzer | meziantou/Meziantou.Analyzer | 1215 | 27.8M | 3.0.316, 2026-10-21 | MIT |
| Analyzer pack | SonarAnalyzer.CSharp | SonarSource/sonar-dotnet | 921 | 115.8M | 10.35.0, 2026-09-28 | LGPL-3.0 (reported NOASSERTION) |
| Style | StyleCop.Analyzers | DotNetAnalyzers/StyleCopAnalyzers | 2859 | 283.6M | 1.1.118 (2019 stable), prereleases since | MIT |
| Architecture | **ArchUnitNET** | TNG/ArchUnitNET | 1390 | 10.4M | 0.13.4, 2026-08-19 | Apache-2.0 |
| Architecture (old) | NetArchTest | BenMorris/NetArchTest | 1791 | 18.9M | 1.3.2, **2021-05-23** | MIT |
| Formatter | CSharpier | belav/csharpier | 2350 | 21.4M | 1.3.0 | MIT |
| Mutation | Stryker.NET | stryker-mutator/stryker-net | 2110 | 9.2M | 5.0.0, 2026-09-11 | Apache-2.0 |

**Recommendations:**

- **Roslynator** as the one extra analyzer pack on top of the listed SDK analyzers: 500+ analyzers, builds with `dotnet build -warnaserror`, a NuGet reference so it runs in CI and the IDE. Meziantou is the more opinionated, smaller alternative; the choice between them is a judgement call (confidence medium-low). Limits: analyzers only fail the build when severities are set to error in `.editorconfig`.
- **ArchUnitNET** over NetArchTest (no release since 2021). Pre-1.0, same API ideas as the listed ArchUnit. Confidence medium.
- **No entry:** StyleCop (its stable line is from 2019), SonarAnalyzer (server-oriented), CSharpier (`dotnet format` ships in the SDK; style choice), Stryker.NET (scheduled).

## PHP

| Job | Candidate | Repo | Stars | Downloads | Release | Licence |
|---|---|---|---|---|---|---|
| Automated upgrades | **Rector** | rectorphp/rector | 10474 | 9.4M monthly | 2.7.0, 2026-10-06 | MIT |
| Advisories | `composer audit` | composer/composer | 29559 | built in | 2.10.3, 2026-08-27 | MIT |
| Unused / shadow deps | composer-dependency-analyser | shipmonk-rnd/composer-dependency-analyser | 635 | n/a | 1.8.4, 2025-11-25 | MIT |
| Mutation | Infection | infection/infection | 2263 | 1.9M monthly | 0.35.8, 2026-10-14 | BSD-3-Clause |
| Static analysis (listed) | PHPStan | phpstan/phpstan | 14134 | 16.9M monthly | 2.3.1 | MIT |

**Recommendation: Rector.** `vendor/bin/rector --dry-run` shows the diff and fails (non-zero) when changes are pending (README shows the dry-run; exit code is documented behaviour but unverified by us). It does a different job from Mago: automated framework and PHP version upgrades and refactoring sets. Limits: a rule-set tool, so results depend on the sets you choose; run `--dry-run` in CI, apply locally. Confidence medium-high.
`composer audit`: overlap with osv-scanner. composer-dependency-analyser: hold (small, last release 11 months ago). Infection: under review, see [stryker.md](stryker.md).

## Elixir and Phoenix

| Job | Candidate | Repo | Stars | Downloads (Hex, 90 d) | Release | Licence |
|---|---|---|---|---|---|---|
| Lint, style, consistency | **Credo** | rrrene/credo | 5228 | 4.8M | 1.7.19, 2026-06-25 | MIT |
| Phoenix security | **Sobelow** | **sobelow/sobelow** (old nccgroup repo stale since 2024) | 66 (new repo) | 1.7M | 0.16.0, 2026-09-30 | Apache-2.0 |
| Dialyzer wrapper | **Dialyxir** | jeremyjh/dialyxir | 1796 | 2.9M | 1.4.8, 2026-09-05 | Apache-2.0 |
| Dialyzer wrapper (incremental) | Assay | Ch4s3/assay | 13 | 8.6k | 0.7.0, 2026-08-13 | MIT |
| Advisories | mix_audit | mirego/mix_audit | 383 | 1.5M | 2.1.5, 2025-06-09 | BSD-3-Clause |
| Generated-code slop (Credo plugin) | **ExSlop** | elixir-vibe/ex_slop | 171 | 313k | 0.4.5, 2026-09-22 | MIT |
| Generated-code slop (standalone) | Credence | Cinderella-Man/credence | 78 | 16k | 0.8.1, 2026-07-02 | MIT (Hex metadata; no licence file on GitHub) |

**Recommendations:**

- **Credo**: the standard linter (`mix credo --strict`, JSON output, custom checks). Formatting is built in (`mix format --check-formatted`), as is `mix compile --warnings-as-errors` (and Elixir 1.20 adds more type-system warnings to the compiler). Confidence high.
- **ExSlop: add, as a Credo plugin inside the Credo entry** (as the RuboCop entry lists its plugins), not as a tool of its own: it runs in `mix credo`, so it adds checks but no runner. It targets what code generators over-produce and experienced Elixir developers rarely write: blanket `rescue`, `try` around a function with a non-raising variant, `Repo.all` then `Enum.filter`, queries inside `Enum.map`, narrator docs and comments, roundabout `Enum` pipelines.
  - Run on 2026-10-24 (Elixir 1.20.1, credo 1.7.19, ex_slop 0.4.5, [fixture](fixtures/ex-slop/run.py)): on code with six such patterns, `mix credo --strict` reported each through an ExSlop check (`BlanketRescue`, `TryRescueWithSafeAlternative`, `FilterNil`, `LengthComparison`, `SortThenReverse`, `NarratorDoc`) and exited 28; on the idiomatic rewrite it exited 0. `--format json` and `--format sarif` carry the findings. On a 60-file Phoenix application that already passed `credo --strict`, the plugin's 31 default checks reported nothing.
  - Read, not run: the plugin enables 31 of its 40 checks and leaves noisier ones (such as `StepComment`) opt-in; an explicit `checks.enabled` list in `.credo.exs` discards them, and ExSlop warns about that. A few semantic-performance checks overlap Credo's own refactors on purpose.
  - Currency: created 2026-03-07, 11 releases, v0.4.5 on 2026-09-22 fixed seven false-positive reports five days after they were filed ([ex_slop#16](https://github.com/elixir-vibe/ex_slop/pull/16)); no open issues; MIT.
  - Alternative: **Credence**, a standalone semantic linter for generated Elixir. It overlaps only ExSlop's performance checks (ExSlop credits it for those), needs its own runner next to Credo, and is far less used (16k against 313k Hex downloads in 90 days). Reject.
  - Limits: young and maintained by one organisation; heuristic checks on doc and comment content can misfire, so pin the version. Confidence medium.
- **Sobelow**: the Phoenix security scanner. It is alive (v0.16.0 on 2026-09-30 from the new `sobelow/sobelow` repo), so the earlier "old releases" worry is resolved. `--exit low|medium|high` makes it fail the build, `--format sarif|json` for tooling (README). Limits: Phoenix and Plug only; the new repo has few stars because it was moved. Confidence medium-high.
- **Dialyxir: add, for projects that write `@spec`.** It was held back because Dialyzer is slow and the compiler's gradual typing is growing; a run shows where each stands.
  - Run on 2026-10-24 (Elixir 1.20.1 on OTP 28.5, dialyxir 1.4.8, [fixture](fixtures/dialyxir/run.py)): `mix compile --warnings-as-errors` already fails on `:atom + 1` and on passing an atom to a function inferred to take a number, so Dialyzer is not needed for those. The compiler does not read `@spec`: a function returning a string under `@spec name() :: integer()`, and one that always raises under a spec promising `:ok`, compile cleanly. `mix dialyzer` reports both (`invalid_contract`, `no_return`) and exits 2. The first run took 155 s, almost all of it building the PLT; the second took 3 s. On the same code outside the fixture, `--format github` printed `::warning file=...` workflow annotations.
  - Read, not run: `--format ignore_file` writes entries for an ignore file that baselines old warnings; there is no JSON or SARIF format (`mix help dialyzer`).
  - Currency: 1.4.8 on 2026-09-05, commits on 2026-09-21, 74 open issues, Apache-2.0, 2.9M Hex downloads in 90 days.
  - Alternative: **Assay**, incremental Dialyzer with `github`, `sarif`, `ndjson` and `llm` output and a watch mode (README, not run). Better output for agents, but created 2025-12 with 13 stars and 8.6k downloads in 90 days; dialyze, the older wrapper, has had no release since 2019. Re-review Assay as it grows.
  - Limits: most useful where the project writes specs (the run covered specs only; Dialyzer also works without them); cache the PLT in CI; what only Dialyzer catches shrinks as the compiler's type system grows. Confidence medium-high.
- **Reject:** mix_audit (overlap: osv-scanner reads `mix.lock`; `mix hex.audit` covers retired packages, unverified by us).

## Not researched (flag)

C and C++ (clang-tidy, clang-format, cppcheck), Dart and Flutter (`dart analyze` is built in), Scala, Haskell. C/C++ is a real gap given its size; propose a separate pass.

---

## Edits to existing entries

| Entry | Edit |
|---|---|
| rubocop | Mention rubocop-rails (318M gem downloads), rubocop-rspec (304M), rubocop-performance as the way to cover Rails and RSpec; reject `standard` (config of the same tool), reek, rails_best_practices. |
| golangci-lint | State that `golangci-lint fmt` runs gofumpt, gci and goimports; do not add gofumpt. |
| error-prone | Add NullAway as the null-safety check. |
| osv-scanner | State the lockfile list above so users do not add pip-audit, bundler-audit, mix_audit, composer audit or OWASP Dependency-Check. |
| dependency-cruiser | Note that it covers what madge, Sheriff and eslint-plugin-boundaries do. |
| Under review table | Python types: Pyrefly is 1.4.0 stable. Elixir: Sobelow moved to `sobelow/sobelow` and is active. Kotlin/.NET: ArchUnitNET and detekt can leave the "unverified" bucket if the proposals below are accepted. Ruby: Brakeman stays, with the licence text above. |
| Docs | Add to `docs/patterns.md`: `uv lock --check`, `sqlc vet` and `sqlc diff`, `goreleaser check`, `mix format --check-formatted` and `mix compile --warnings-as-errors`, `composer audit` (scheduled). |

New categories needed in `CATEGORY_ORDER` (`scripts/readme.ts`): **Kotlin**, **Elixir**, **Web quality** (CSS, accessibility, performance budgets) and **Tests and coverage**. All other proposed entries use existing categories (Ruby, Python, JavaScript and TypeScript, Go, Rust, Java, .NET, PHP).

---

## Proposed README entries

Mark: every entry below was checked by documentation, repository and registry data on 2026-10-23. **Nothing was installed or run.**

### Ruby

- **[strong_migrations](https://github.com/ankane/strong_migrations)**: stops unsafe Rails migrations (locking indexes, column drops, type changes) while they run and names the safe alternative; 4.4k stars, MIT, active. It checks Ruby migrations, so it does not overlap with squawk. *Limits:* PostgreSQL, MySQL and MariaDB only; runs only when migrations run, so CI must run them.
- **[Bullet](https://github.com/flyerhzm/bullet)**: detects N+1 queries and unused eager loading; with `Bullet.raise = true` in test the specs fail. The standard Rails tool (7.3k stars, 188M gem downloads). *Limits:* finds only what tests exercise.
- **[i18n-tasks](https://github.com/glebm/i18n-tasks)**: `i18n-tasks health` fails on missing, unused and inconsistent translation keys and normalises locale files. The mature Rails option. *Limits:* Ruby and Rails; last release 2025-11.
- **[Herb](https://github.com/marcoroth/herb)**: HTML-aware ERB parser with linter and formatter; replaces erb_lint, which has had no release since 2025-01. 600k npm downloads a month. *Limits:* pre-1.0; formatter is experimental; the linter runs through npm.
- **[Sorbet](https://github.com/sorbet/sorbet)**: fast static type checker for Ruby (used by Stripe and Shopify); with tapioca it types gems and Rails. Chosen over Steep for adoption (158M vs 6.9M gem downloads). *Limits:* needs `sig` annotations and gradual strictness levels; Steep with RBS is the other direction.
- **[Packwerk](https://github.com/Shopify/packwerk)**: enforces package dependency and privacy rules in a Rails monolith. *Limits:* needs modularisation work; [pks](https://github.com/rubyatscale/pks) is a Rust drop-in claiming 10-20x speed but is very small (10 stars, unverified).

### Python

- **[django-upgrade](https://github.com/adamchainz/django-upgrade)**: rewrites code to the idioms of your target Django version, and fails CI when files would change. *Limits:* Django only; narrow by design.
- **[django-migration-linter](https://github.com/David-Wobrock/django-migration-linter)**: flags Django migrations that are not backward compatible with the running code (`lintmigrations`); 3.4M downloads a month. *Limits:* Django only; not verified by running; does not replace squawk for lock analysis on SQL.

### JavaScript and TypeScript

- **[syncpack](https://github.com/JamieMason/syncpack)**: Rust tool that enforces one version of each dependency and consistent ranges across a monorepo; 11M downloads a month. *Limits:* monorepos only; package-manager catalogs reduce the need; sherif is the narrower alternative.
- **[i18next-cli](https://github.com/i18next/i18next-cli)**: official i18next CLI; `extract --ci` fails on out-of-date key files, `status` fails on missing translations, `lint` finds hardcoded strings. *Limits:* i18next only; 244 stars, young; not run by us.

### Web quality (new category)

- **[Stylelint](https://github.com/stylelint/stylelint)**: CSS, SCSS and CSS-in-JS linter with autofix and custom rules; 44M downloads a month. Oxlint does no CSS. *Limits:* CSS only.
- **[axe-core](https://github.com/dequelabs/axe-core)**: accessibility rules that fail tests when run through `@axe-core/playwright` (53M downloads a month). Static JSX checks are in Oxlint. *Limits:* finds only the automatable part of WCAG; needs a browser test suite; MPL-2.0.
- **[size-limit](https://github.com/ai/size-limit)**: fails the build when a bundle is over its size or load-time budget. *Limits:* needs a build step and budgets chosen by you.
- **[Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)**: asserts performance, accessibility and best-practice budgets per pull request. The only mature option. *Limits:* last GitHub release 2025-06 (commits continue); lab data varies between runs.

### Tests and coverage (new category)

- **[diff-cover](https://github.com/Bachmann1234/diff_cover)**: fails when coverage of the lines changed in a pull request is under a threshold; reads coverage reports from many languages. Better than a global floor. *Limits:* needs a coverage report; supported report formats not verified.

### Go

- **[go-arch-lint](https://github.com/fe3dback/go-arch-lint)**: enforces package dependency rules from a YAML file; the more active of the two Go options (arch-go is smaller). *Limits:* small project (616 stars); low confidence.

### Rust

- **[cargo-machete](https://github.com/bnjbvr/cargo-machete)**: finds unused dependencies quickly (594k downloads in 90 days). *Limits:* regex-based, so false positives are possible; [cargo-shear](https://github.com/Boshen/cargo-shear) is a more accurate newer alternative.
- **[cargo-nextest](https://github.com/nextest-rs/nextest)**: the standard test runner: faster, retries flaky tests, JUnit output. *Limits:* a speed and signal tool; does not run doctests.
- **[cargo-llvm-cov](https://github.com/taiki-e/cargo-llvm-cov)**: coverage with a fail-under threshold using LLVM instrumentation. *Limits:* needs the llvm-tools component; flag names not verified.

### Java

- **[NullAway](https://github.com/uber/NullAway)**: compile-time null checks as an error-prone plugin; fails the build on possible null dereferences. *Limits:* needs `@Nullable` discipline; build with error-prone.

### Kotlin (new category)

- **[detekt](https://github.com/detekt/detekt)**: Kotlin static analysis for complexity, smells and bugs, with baselines and SARIF. The de facto standard. *Limits:* stable release 1.23.8 is from 2025-02 and 2.0 is in alpha; ktlint formatting comes through spotless.

### .NET

- **[Roslynator](https://github.com/dotnet/roslynator)**: 500+ extra analyzers on top of the SDK analyzers, enforced with `-warnaserror` and `.editorconfig` severities. *Limits:* only fails when you set severities to error; Meziantou.Analyzer is the smaller alternative.
- **[ArchUnitNET](https://github.com/TNG/ArchUnitNET)**: architecture rules as unit tests, the .NET sibling of ArchUnit; NetArchTest has had no release since 2021. *Limits:* pre-1.0.

### PHP

- **[Rector](https://github.com/rectorphp/rector)**: automated upgrades and refactoring sets; `--dry-run` in CI shows pending changes. A different job from Mago. *Limits:* depends on the rule sets you choose; fail-on-diff behaviour read from the docs only.

### Elixir (new category)

- **[Credo](https://github.com/rrrene/credo)**: the standard Elixir linter (consistency, readability, refactoring opportunities, custom checks); use with `mix format --check-formatted` and `mix compile --warnings-as-errors`. *Limits:* style and smell rules, not type checking.
- **[Sobelow](https://github.com/sobelow/sobelow)**: security scanner for Phoenix; `--exit` fails the build at a confidence level, SARIF output. Active again (0.16.0, 2026-09-30) after moving to this repository. *Limits:* Phoenix and Plug only; heuristic findings need a `.sobelow-skips` file.

---

## tools.json records

Categories marked NEW need `CATEGORY_ORDER` changes. Not run by us unless stated (none were).

```json
[
  {
    "id": "strong-migrations",
    "name": "strong_migrations",
    "repo": "ankane/strong_migrations",
    "category": "Ruby",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/ankane/strong_migrations", "https://rubygems.org/gems/strong_migrations", "research/ecosystem-gaps.md"],
    "rationale": "stops unsafe Rails migrations (locking indexes, column drops, type changes) while they run and names the safe alternative. It checks the Ruby migration DSL, so it does not overlap with squawk.",
    "limitations": "PostgreSQL, MySQL and MariaDB only; it checks only when migrations run, so CI must run them. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "bullet",
    "name": "Bullet",
    "repo": "flyerhzm/bullet",
    "category": "Ruby",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/flyerhzm/bullet", "https://rubygems.org/gems/bullet", "research/ecosystem-gaps.md"],
    "rationale": "detects N+1 queries and unused eager loading; with `Bullet.raise = true` in the test environment the specs fail. The standard Rails tool (7.3k stars, 188M gem downloads).",
    "limitations": "finds only what the tests exercise. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "i18n-tasks",
    "name": "i18n-tasks",
    "repo": "glebm/i18n-tasks",
    "category": "Ruby",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/glebm/i18n-tasks", "https://rubygems.org/gems/i18n-tasks", "research/ecosystem-gaps.md"],
    "rationale": "`i18n-tasks health` fails on missing, unused and inconsistent translation keys and normalises locale files. The mature option for Rails.",
    "limitations": "Ruby and Rails; last release 2025-11 although the repository is active. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "herb",
    "name": "Herb",
    "repo": "marcoroth/herb",
    "category": "Ruby",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/marcoroth/herb", "https://www.npmjs.com/package/@herb-tools/linter", "research/ecosystem-gaps.md"],
    "rationale": "HTML-aware ERB parser with a linter and formatter. It replaces erb_lint, which has had no release since 2025-01; the linter has about 600k npm downloads a month.",
    "limitations": "pre-1.0 (0.11); the formatter is marked experimental; the linter runs through npm, so Ruby-only CI needs Node. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "sorbet",
    "name": "Sorbet",
    "repo": "sorbet/sorbet",
    "category": "Ruby",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/sorbet/sorbet", "https://rubygems.org/gems/sorbet-runtime", "research/ecosystem-gaps.md"],
    "rationale": "fast static type checker for Ruby used by Stripe and Shopify; with tapioca it types gems and Rails. Chosen over Steep for adoption (158M against 6.9M gem downloads).",
    "limitations": "needs `sig` annotations and gradual strictness levels; Steep with RBS is the other direction. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "packwerk",
    "name": "Packwerk",
    "repo": "Shopify/packwerk",
    "category": "Ruby",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/Shopify/packwerk", "https://github.com/rubyatscale/pks", "research/ecosystem-gaps.md"],
    "rationale": "enforces package dependency and privacy rules in a Rails monolith, so modularisation does not erode.",
    "limitations": "needs modularisation work first; pks is a Rust drop-in claimed to be 10-20x faster but is very small (10 stars, unverified). Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "django-upgrade",
    "name": "django-upgrade",
    "repo": "adamchainz/django-upgrade",
    "category": "Python",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/adamchainz/django-upgrade", "https://pypistats.org/packages/django-upgrade", "research/ecosystem-gaps.md"],
    "rationale": "rewrites code to the idioms of the target Django version and fails CI when files would change.",
    "limitations": "Django only and narrow by design (469k downloads a month). Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "django-migration-linter",
    "name": "django-migration-linter",
    "repo": "David-Wobrock/django-migration-linter",
    "category": "Python",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/David-Wobrock/django-migration-linter", "https://pypistats.org/packages/django-migration-linter", "research/ecosystem-gaps.md"],
    "rationale": "flags Django migrations that are not backward compatible with the running code (`lintmigrations`); 3.4M downloads a month.",
    "limitations": "Django only; does not replace squawk for lock analysis of the generated SQL. Unverified: not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "syncpack",
    "name": "syncpack",
    "repo": "JamieMason/syncpack",
    "category": "JavaScript and TypeScript",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/JamieMason/syncpack", "https://www.npmjs.com/package/syncpack", "https://github.com/QuiiBz/sherif", "research/ecosystem-gaps.md"],
    "rationale": "Rust tool that enforces one version of each dependency and consistent ranges across a monorepo; 11M downloads a month, about 5x sherif.",
    "limitations": "monorepos only; package-manager catalogs (pnpm, Bun) reduce the need; sherif is the narrower zero-config alternative. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "i18next-cli",
    "name": "i18next-cli",
    "repo": "i18next/i18next-cli",
    "category": "JavaScript and TypeScript",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/i18next/i18next-cli", "https://www.npmjs.com/package/i18next-cli", "research/ecosystem-gaps.md"],
    "rationale": "official i18next CLI: `extract --ci` fails when key files are out of date, `status` fails on missing translations, `lint` finds hardcoded strings.",
    "limitations": "i18next only (Lingui and FormatJS have their own CLIs); 244 stars and young, though 3.5M downloads a month. Unverified: not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "stylelint",
    "name": "Stylelint",
    "repo": "stylelint/stylelint",
    "category": "Web quality",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/stylelint/stylelint", "https://www.npmjs.com/package/stylelint", "research/ecosystem-gaps.md"],
    "rationale": "CSS, SCSS and CSS-in-JS linter with autofix and custom rules; 44M downloads a month. Oxlint does no CSS.",
    "limitations": "CSS only. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "axe-core",
    "name": "axe-core",
    "repo": "dequelabs/axe-core",
    "category": "Web quality",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/dequelabs/axe-core", "https://github.com/dequelabs/axe-core-npm", "https://www.npmjs.com/package/@axe-core/playwright", "research/ecosystem-gaps.md"],
    "rationale": "accessibility rules that fail tests when run through `@axe-core/playwright` (53M downloads a month). Static JSX checks already exist inside Oxlint; this is the runtime job.",
    "limitations": "finds only the automatable part of WCAG and needs a browser test suite; MPL-2.0. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "size-limit",
    "name": "size-limit",
    "repo": "ai/size-limit",
    "category": "Web quality",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/ai/size-limit", "https://www.npmjs.com/package/size-limit", "research/ecosystem-gaps.md"],
    "rationale": "fails the build when a bundle exceeds its size or load-time budget; works for apps and libraries.",
    "limitations": "needs a build step and budgets you choose. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "lighthouse-ci",
    "name": "Lighthouse CI",
    "repo": "GoogleChrome/lighthouse-ci",
    "category": "Web quality",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/GoogleChrome/lighthouse-ci", "https://www.npmjs.com/package/@lhci/cli", "research/ecosystem-gaps.md"],
    "rationale": "`lhci assert` enforces performance, accessibility and best-practice budgets per pull request. The only mature option.",
    "limitations": "last GitHub release is 2025-06 although commits continue; lab results vary between runs. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "diff-cover",
    "name": "diff-cover",
    "repo": "Bachmann1234/diff_cover",
    "category": "Tests and coverage",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/Bachmann1234/diff_cover", "https://pypistats.org/packages/diff-cover", "research/ecosystem-gaps.md"],
    "rationale": "fails when coverage of the lines changed in a pull request is under a threshold; better than a global floor because old code is not penalised.",
    "limitations": "needs a coverage report; supported report formats were not verified. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "go-arch-lint",
    "name": "go-arch-lint",
    "repo": "fe3dback/go-arch-lint",
    "category": "Go",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/fe3dback/go-arch-lint", "https://github.com/arch-go/arch-go", "research/ecosystem-gaps.md"],
    "rationale": "enforces package dependency rules from a YAML file; the more active of the two Go options (arch-go has 280 stars and a February release).",
    "limitations": "small project (616 stars): low confidence. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "cargo-machete",
    "name": "cargo-machete",
    "repo": "bnjbvr/cargo-machete",
    "category": "Rust",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/bnjbvr/cargo-machete", "https://crates.io/crates/cargo-machete", "https://github.com/Boshen/cargo-shear", "research/ecosystem-gaps.md"],
    "rationale": "finds unused dependencies quickly; 594k downloads in 90 days, about 10x cargo-shear.",
    "limitations": "regex-based, so false positives are possible (an ignore list exists); cargo-shear is a newer AST-based alternative. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "cargo-nextest",
    "name": "cargo-nextest",
    "repo": "nextest-rs/nextest",
    "category": "Rust",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/nextest-rs/nextest", "https://crates.io/crates/cargo-nextest", "research/ecosystem-gaps.md"],
    "rationale": "the standard Rust test runner: faster than `cargo test`, retries and flags flaky tests, JUnit output; 1.9M downloads in 90 days.",
    "limitations": "a speed and signal tool rather than a rule checker; does not run doctests. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "cargo-llvm-cov",
    "name": "cargo-llvm-cov",
    "repo": "taiki-e/cargo-llvm-cov",
    "category": "Rust",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/taiki-e/cargo-llvm-cov", "https://crates.io/crates/cargo-llvm-cov", "research/ecosystem-gaps.md"],
    "rationale": "coverage with a fail-under threshold using LLVM instrumentation; 1.9M downloads in 90 days, 6x tarpaulin.",
    "limitations": "needs the llvm-tools component; the exact threshold flags were not verified. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "nullaway",
    "name": "NullAway",
    "repo": "uber/NullAway",
    "category": "Java",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/uber/NullAway", "https://github.com/google/error-prone", "research/ecosystem-gaps.md"],
    "rationale": "compile-time null checks as an error-prone plugin: fails the build on possible null dereferences. Used at Uber scale.",
    "limitations": "needs `@Nullable` discipline and error-prone in the build; not useful for Kotlin. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "detekt",
    "name": "detekt",
    "repo": "detekt/detekt",
    "category": "Kotlin",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/detekt/detekt", "https://github.com/pinterest/ktlint", "research/ecosystem-gaps.md"],
    "rationale": "Kotlin static analysis for complexity, smells and bugs, with baselines and SARIF. The de facto standard; formatting comes through spotless (ktlint).",
    "limitations": "the stable release 1.23.8 is from 2025-02 and 2.0 has been in alpha since April 2026. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "roslynator",
    "name": "Roslynator",
    "repo": "dotnet/roslynator",
    "category": ".NET",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/dotnet/roslynator", "https://www.nuget.org/packages/Roslynator.Analyzers", "research/ecosystem-gaps.md"],
    "rationale": "500+ extra analyzers on top of the SDK analyzers, enforced through `-warnaserror` and `.editorconfig` severities; 64M NuGet downloads.",
    "limitations": "analyzers only fail the build when severities are set to error; Meziantou.Analyzer is a smaller alternative.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "archunitnet",
    "name": "ArchUnitNET",
    "repo": "TNG/ArchUnitNET",
    "category": ".NET",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/TNG/ArchUnitNET", "https://www.nuget.org/packages/TngTech.ArchUnitNET", "research/ecosystem-gaps.md"],
    "rationale": "architecture rules as unit tests, the .NET sibling of ArchUnit; NetArchTest has had no release since 2021.",
    "limitations": "pre-1.0 (0.13). Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "rector",
    "name": "Rector",
    "repo": "rectorphp/rector",
    "category": "PHP",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/rectorphp/rector", "https://packagist.org/packages/rector/rector", "research/ecosystem-gaps.md"],
    "rationale": "automated PHP and framework upgrades and refactoring sets; `--dry-run` in CI shows pending changes. A different job from Mago.",
    "limitations": "results depend on the rule sets you choose; the fail-on-diff exit code was read from the docs only. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "credo",
    "name": "Credo",
    "repo": "rrrene/credo",
    "category": "Elixir",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/rrrene/credo", "https://hex.pm/packages/credo", "research/ecosystem-gaps.md"],
    "rationale": "the standard Elixir linter for consistency, readability and refactoring opportunities, with custom checks and JSON output. Use it with `mix format --check-formatted` and `mix compile --warnings-as-errors`.",
    "limitations": "style and smell rules, not type checking. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  },
  {
    "id": "sobelow",
    "name": "Sobelow",
    "repo": "sobelow/sobelow",
    "category": "Elixir",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/sobelow/sobelow", "https://hex.pm/packages/sobelow", "research/ecosystem-gaps.md"],
    "rationale": "security scanner for Phoenix; `--exit` fails the build at a confidence level and SARIF or JSON output is available. Active again (0.16.0, 2026-09-30) after moving to this repository.",
    "limitations": "Phoenix and Plug only; heuristic findings need a skips file. The new repository has few stars because it was moved. Read, not run.",
    "details": "research/ecosystem-gaps.md"
  }
]
```

## Open items for the owner

1. Verify by running: Herb linter exit codes, django-migration-linter, `rector --dry-run` exit code, cargo-machete CI flags, diff-cover input formats.
2. Roslynator: `dotnet/roslynator` and `JosefPihrt/Roslynator` both resolve to the same repository (3488 stars, v5.0.1); `dotnet/roslynator` is used.
3. Brakeman stays under review: licence unchanged (paid for commercial use).
4. C and C++, Dart, Scala, Haskell were not covered.
