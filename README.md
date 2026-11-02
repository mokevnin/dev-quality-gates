# Dev Quality Gates

An opinionated, continuously curated list of tools for **enforcing** software development standards.

Dev Quality Gates is not an Awesome List. It does not list every linter for every language. For each job it recommends one tool (rarely two) and says what it does.

## Principles

- **Opinionated.** One recommended tool per job. Several only when the jobs or the environments really differ.
- **Curated.** Every tool is checked against the [selection criteria](CONTRIBUTING.md#selection-criteria) before it is listed, and again on a schedule.
- **Coverage over quantity.** A tool that replaces three narrow checks beats three narrow tools.
- **Fast native toolchains first.** Modern stacks are converging on Rust-native tools that do lint, format and analysis in one binary (Ruff, Oxlint with oxfmt, Mago, rumdl). We prefer them over a pile of older single-purpose tools when they cover the same ground. Ecosystems without one (Ruby, Java, .NET, Swift) keep their standard tools.
- **Enforcement over advice.** A tool must fail a build (non-zero exit code) when a standard is violated. Reports that nobody reads do not count.
- **Agent-friendly.** Non-interactive, machine-readable output, clear diagnostics, and autofix where it is safe. AI coding agents are first-class users of these tools.
- **Honest about gaps.** A category with no verified recommendation stays empty rather than getting an outdated one.

This is **not a universal stack**. Do not install everything here. Pick the entries that match your project.

## Use it in your project

Ask your coding agent, from the root of your repository:

```text
Apply https://github.com/mokevnin/dev-quality-gates to this repository.
Read and follow https://raw.githubusercontent.com/mokevnin/dev-quality-gates/main/docs/adopt.md.
Show me the plan before you change anything.
```

The agent inspects the project, picks only the entries that fit, shows you the plan, wires the checks into hooks and CI, and proves that each one can fail. The instructions are in [docs/adopt.md](docs/adopt.md); to do it yourself, pick entries below by language and by cross-cutting category, then use the [setup patterns](docs/patterns.md).

## Recommendations

The entries below are **generated from [`tools.json`](tools.json)** (`pnpm run readme`), which also records the review date, sources and limitations of each tool.

<!-- tools:start -->

### GitHub Actions

- **[jactionlint](https://github.com/jdx/jactionlint)**: lints GitHub Actions workflows, composite actions and `dependabot.yml` for correctness, security and policy in one binary. `--fix` repairs what has a mechanical fix; with `--online` it also pins tags to commit SHAs. [Details](research/github-actions.md).

### GitLab CI

- **[Plumber](https://github.com/getplumber/plumber)**: security scanner for GitLab CI pipelines: checks `.gitlab-ci.yml`, resolved includes and project settings such as branch protection, and reports to the terminal, JSON, SARIF and GitLab SAST.

### JavaScript and TypeScript

- **[Knip](https://github.com/webpro-nl/knip)**: unused files, exports and dependencies.
- **[Oxlint and oxfmt](https://github.com/oxc-project/oxc)**: Rust-native linter (ESLint-compatible rules) and formatter (Prettier-compatible) from the Oxc toolchain. One fast toolchain instead of ESLint plus Prettier. [Details](research/stack-javascript.md).
- **[TypeScript](https://github.com/microsoft/TypeScript)**: type checking with `tsc --noEmit` and `strict`. [Details](research/stack-javascript.md).
- **[dependency-cruiser](https://github.com/sverweij/dependency-cruiser)**: import-graph rules (forbidden paths, cycles, orphans, dev dependencies in production code) with non-zero exit and JSON output; `--ignore-known` baselines legacy violations. [Details](research/stack-javascript.md).
- **[syncpack](https://github.com/JamieMason/syncpack)**: enforces one version of each dependency and consistent ranges across a monorepo. [Details](research/ecosystem-gaps.md).

### Python

- **[Ruff](https://github.com/astral-sh/ruff)**: linter and formatter that replaces Flake8, isort, pyupgrade and Black.
- **[ty](https://github.com/astral-sh/ty)**: fast Python type checker and language server from the authors of Ruff and uv.
- **[deptry](https://github.com/osprey-oss/deptry)**: unused, missing and transitive dependencies.
- **[import-linter](https://github.com/seddonym/import-linter)**: import contracts (layers, forbidden, independence, protected) that fail CI. [Details](research/stack-python-ruby-php.md).
- **[django-upgrade](https://github.com/adamchainz/django-upgrade)**: rewrites code to the idioms of your target Django version, and fails CI when files would change. [Details](research/ecosystem-gaps.md).
- **[django-migration-linter](https://github.com/David-Wobrock/django-migration-linter)**: flags Django migrations that are not backward compatible with the running code (`lintmigrations`). [Details](research/ecosystem-gaps.md).

### Go

- **[golangci-lint](https://github.com/golangci/golangci-lint)**: one runner for the Go linters and the formatter, with `golangci-lint custom` for your own analyzers.
- **[govulncheck](https://github.com/golang/vuln)**: reports known vulnerabilities in the Go modules and standard library you actually call, with call stacks, from the official Go vulnerability database. [Details](research/stack-go-rust-jvm-dotnet.md).
- **[go-arch-lint](https://github.com/fe3dback/go-arch-lint)**: architecture rules for Go in one `.go-arch-lint.yml`: components by path and the components and vendor packages each may import. Exits 1 on a violation, JSON output. [Details](research/ecosystem-gaps.md).

### Rust

- **[Clippy](https://github.com/rust-lang/rust-clippy)**: the official linter; run `cargo clippy -- -D warnings`.
- **[rustfmt](https://github.com/rust-lang/rustfmt)**: the official formatter; run `cargo fmt --check` in CI. [Details](research/stack-go-rust-jvm-dotnet.md).
- **[cargo-machete](https://github.com/bnjbvr/cargo-machete)**: finds unused dependencies in Cargo.toml quickly and without compiling, so it runs on stable Rust in CI.
- **[cargo-deny](https://github.com/EmbarkStudios/cargo-deny)**: one policy file for RustSec advisories, licences, banned or duplicate crates and allowed registries; non-zero exit on violation. [Details](research/stack-go-rust-jvm-dotnet.md).

### Ruby

- **[RuboCop](https://github.com/rubocop/rubocop)**: linter and formatter with autocorrect and custom cops.
- **[strong_migrations](https://github.com/ankane/strong_migrations)**: stops unsafe Rails migrations (locking indexes, column drops, type changes) while they run and names the safe alternative. [Details](research/ecosystem-gaps.md).
- **[Bullet](https://github.com/flyerhzm/bullet)**: detects N+1 queries and unused eager loading in Rails; with `Bullet.raise = true` in test the specs fail. [Details](research/ecosystem-gaps.md).
- **[i18n-tasks](https://github.com/glebm/i18n-tasks)**: `i18n-tasks health` fails on missing, unused and inconsistent translation keys and normalises locale files. [Details](research/ecosystem-gaps.md).
- **[Herb](https://github.com/marcoroth/herb)**: HTML-aware ERB parser with linter and formatter; replaces erb_lint. [Details](research/ecosystem-gaps.md).
- **[Sorbet](https://github.com/sorbet/sorbet)**: static type checker for Ruby; with tapioca it types gems and Rails. [Details](research/ecosystem-gaps.md).
- **[Packwerk](https://github.com/Shopify/packwerk)**: enforces package dependency and privacy rules in a Rails monolith. [Details](research/ecosystem-gaps.md).
- **[ArchSpec](https://github.com/crmne/archspec)**: architecture rules for Ruby in one `Archspec.rb`: components by glob, layers, `cannot_use`, `cannot_call`, naming, cycles and Rails presets. Exits 1 on a violation, JSON output, a todo file for existing apps. [Details](research/custom-rules.md).

### PHP

- **[Mago](https://github.com/carthage-software/mago)**: PHP toolchain in one binary: linter, formatter, static analyzer and architectural `guard` rules, with auto-fixes and a baseline.
- **[Rector](https://github.com/rectorphp/rector)**: automated upgrades and refactoring sets for PHP; `--dry-run` in CI shows pending changes. [Details](research/ecosystem-gaps.md).

### Java

- **[Error Prone](https://github.com/google/error-prone)**: bug patterns checked by the Java compiler on every build; raise a check to `ERROR` to fail the build. With NullAway as a plugin it also enforces null safety from `@Nullable` annotations. [Details](research/stack-go-rust-jvm-dotnet.md).
- **[Spotless](https://github.com/diffplug/spotless)**: `spotlessCheck` fails on unformatted code and `spotlessApply` fixes it; wraps google-java-format, ktlint, ktfmt and others behind one Gradle or Maven task. [Details](research/stack-go-rust-jvm-dotnet.md).
- **[ArchUnit](https://github.com/TNG/ArchUnit)**: layers, cycles and naming rules written as JUnit tests; a violated rule fails the test run. [Details](research/stack-go-rust-jvm-dotnet.md).

### Kotlin

- **[detekt](https://github.com/detekt/detekt)**: Kotlin static analysis for complexity, smells and bugs, with baselines and SARIF. [Details](research/ecosystem-gaps.md).

### .NET

- **[.NET SDK analyzers](https://github.com/dotnet/sdk)**: the analyzers built into the .NET SDK: code style enforced in the build, warnings as errors, `dotnet format --verify-no-changes`, and NuGet Audit warnings for vulnerable packages as errors. [Details](research/stack-go-rust-jvm-dotnet.md).

### Swift

- **[SwiftLint](https://github.com/realm/SwiftLint)**: style and convention rules built on SwiftSyntax; `--strict` fails on warnings, `--fix` corrects, SARIF/JSON reporters, custom rules in config. [Details](research/stack-go-rust-jvm-dotnet.md).

### Elixir

- **[Credo](https://github.com/rrrene/credo)**: the Elixir linter (consistency, readability, refactoring opportunities, custom checks). With the ExSlop plugin it also flags what code generators over-produce, such as blanket `rescue` and narrator comments. [Details](research/ecosystem-gaps.md).
- **[Sobelow](https://github.com/sobelow/sobelow)**: security scanner for Phoenix; `--exit` fails the build at a confidence level, SARIF output. [Details](research/ecosystem-gaps.md).
- **[Dialyxir](https://github.com/jeremyjh/dialyxir)**: runs Dialyzer from Mix: success-typing analysis, including the check that each `@spec` matches its code. `--format github` annotates pull requests and an ignore file baselines old warnings. [Details](research/ecosystem-gaps.md).

### Shell

- **[ShellCheck](https://github.com/koalaman/shellcheck)**: bugs and portability problems in `sh`, `bash`, `dash` and `ksh`.

### Databases

- **[database_consistency](https://github.com/djezzzl/database_consistency)**: compares ActiveRecord models with the database schema and reports missing null constraints, foreign keys and unique indexes, redundant indexes, mismatched enums and key types, and broken associations.
- **[schemalens](https://github.com/mokevnin/schemalens)**: compares a Go model (ent, gorm, bun) with the live PostgreSQL, MySQL or SQLite schema and reports every disagreement, such as missing foreign-key indexes, unenforced constraints and nullable columns for required fields. JSON and SARIF output, baseline.
- **[squawk](https://github.com/sbdchd/squawk)**: finds PostgreSQL migrations that lock tables or cause downtime, with JSON output and no database needed. [Details](research/cross-cutting.md).
- **[sqruff](https://github.com/quarylabs/sqruff)**: SQL linter and formatter with SQLFluff-style rules, a `--dialect` per project and autofix.

### API contracts

- **[oasdiff](https://github.com/oasdiff/oasdiff)**: compares two OpenAPI specs and reports the changes that break existing API clients (`breaking`) or all consumer-visible changes (`changelog`), with a GitHub Action and a pre-commit hook.
- **[vacuum](https://github.com/daveshanley/vacuum)**: single-binary linter for OpenAPI, AsyncAPI, Arazzo and JSON Schema that reads Spectral-style rulesets.
- **[Buf](https://github.com/bufbuild/buf)**: Protobuf lint, format and breaking-change detection against a previous version or git ref, in one CLI.

### Web quality

- **[Stylelint](https://github.com/stylelint/stylelint)**: CSS, SCSS and CSS-in-JS linter with autofix and custom rules. [Details](research/ecosystem-gaps.md).
- **[axe-core](https://github.com/dequelabs/axe-core)**: accessibility rules that fail tests when run through `@axe-core/playwright`. [Details](research/ecosystem-gaps.md).
- **[size-limit](https://github.com/ai/size-limit)**: fails the build when a bundle is over its size or load-time budget. [Details](research/ecosystem-gaps.md).

### Tests and coverage

- **[diff-cover](https://github.com/Bachmann1234/diff_cover)**: coverage gate for any stack: reads Cobertura, Clover, JaCoCo and lcov reports and fails when the lines changed in a pull request are covered below a threshold.

### Custom rules

- **[ast-grep](https://github.com/ast-grep/ast-grep)**: project-specific syntax rules written as YAML patterns, with tests for the rules themselves and SARIF output. Good for import-boundary and banned-call rules. [Details](research/custom-rules.md).
- **[easement](https://github.com/mokevnin/easement)**: one architecture config (`easement.yml`) for Go, TypeScript/JavaScript, Python and Java: components by path, allowed dependencies, public APIs and cycles, with a message shown for each violation. Supports a baseline and checking only what a pull request adds. [Details](research/custom-rules.md).

### Secrets

- **[Betterleaks](https://github.com/betterleaks/betterleaks)**: finds committed secrets in files, git history and pull requests, with optional live validation of credentials. Reads Gitleaks-style TOML rules. [Details](research/cross-cutting.md#1-secrets-scanning).

### Vulnerabilities

- **[OSV-Scanner](https://github.com/google/osv-scanner)**: known vulnerabilities in lockfiles and SBOMs across many ecosystems, with call analysis to reduce noise. [Details](research/cross-cutting.md#2-vulnerabilities-and-sca).

### Dependency updates

- **[Renovate](https://github.com/renovatebot/renovate)**: dependency update bot for GitHub, GitLab, Bitbucket, Azure DevOps, Gitea and Forgejo. Pinning, grouping and a minimum release age live in one config, which `renovate-config-validator` checks in CI.

### Docker, Terraform and Kubernetes

- **[Hadolint](https://github.com/hadolint/hadolint)**: Dockerfile best practices. [Details](research/cross-cutting.md).
- **[TFLint](https://github.com/terraform-linters/tflint)**: Terraform correctness and provider-specific rules through plugins. [Details](research/cross-cutting.md).
- **[Kubeconform](https://github.com/yannh/kubeconform)**: validates Kubernetes manifests against API and CRD schemas. [Details](research/cross-cutting.md).

### Config files

- **[check-jsonschema](https://github.com/python-jsonschema/check-jsonschema)**: validates YAML, JSON and TOML against JSON Schema, with ready hooks for common formats. [Details](research/cross-cutting.md).

### Policy

- **[Conftest](https://github.com/open-policy-agent/conftest)**: your own rules in Rego over YAML, JSON, HCL, Dockerfile, CODEOWNERS and 15 more formats. [Details](research/cross-cutting.md).

### Agent configuration

- **[agnix](https://github.com/agent-sh/agnix)**: lints CLAUDE.md, AGENTS.md, SKILL.md, hooks and MCP configs for Claude Code, Codex, Cursor, Copilot, OpenCode and Kiro, with `--fix`. Tested: errors exit 1; warnings exit 0 unless `--strict` is passed. [Details](research/cross-cutting.md).

### Toolchain

- **[mise](https://github.com/jdx/mise)**: one tool for the whole project toolchain, configured in `mise.toml`: installs and pins tool versions, switches them per directory, sets environment variables and runs tasks. CI uses the same versions as developers.

### Git hooks

- **[hk](https://github.com/jdx/hk)**: runs linters and formatters as Git hooks and CI checks from one `hk.pkl` file, in parallel. Ships about 170 ready-made steps (Ruff, Oxlint, rustfmt, golangci-lint, RuboCop, shellcheck, hadolint and more) plus file hygiene checks. [Details](research/rust-native.md).

### Git conventions

- **[commitlint](https://github.com/conventional-changelog/commitlint)**: checks that commit messages follow Conventional Commits, in a hook or over a CI range, with shareable configs.

### Documentation

- **[lychee](https://github.com/lycheeverse/lychee)**: broken links.
- **[typos](https://github.com/crate-ci/typos)**: low-noise spell checking of source code and docs.
- **[rumdl](https://github.com/rvben/rumdl)**: Markdown linter and formatter that reads markdownlint configuration. `rumdl check` exits 1 on violations, `rumdl fmt` fixes.

<!-- tools:end -->

## Under review

These categories matter but have **no recommendation yet**: the candidates were not compared well enough. Names are research leads, not endorsements. Working notes are in [`research/`](research/).

| Category | Candidates | Why it is still open |
|---|---|---|
| JavaScript dead code and architecture | fallow, knip, dependency-cruiser | fallow is a Rust all-in-one (dead code, cycles, boundaries, duplication) and could replace both of our picks, but it is 7 months old, has 5.6 million npm downloads a month against knip's 69 million, and its plugin coverage is unverified. |
| JavaScript / TypeScript extras | Biome, publint, arethetypeswrong | Oxlint with oxfmt is recommended; Biome is the other Rust toolchain. publint and arethetypeswrong apply only to published libraries. |
| Ruby security | Brakeman | Free for non-commercial use only; commercial use needs a paid licence. |
| PHP dependencies | composer-dependency-analyser, composer-unused, ComposerRequireChecker | [Eight executed fixtures](research/composer-dependencies.md) favour the analyser for combined unused, shadow and misplaced dependency checks. Release 1.8.4 predates fixes on master; framework and dynamic-use limits still need evaluation. `composer audit` covers a different job. |
| Kotlin, .NET, Elixir extras | ktlint, Konsist, Roslynator, Meziantou.Analyzer, ArchUnitNET, Dialyxir | Stable releases are old or pre-1.0, or they overlap the picks above. |
| Container images | Trivy, Grype | Trivy's GitHub Action and a release were compromised in March 2026 ([advisory](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23)); no clear winner yet. |
| Image layer efficiency | Dive | CI waste thresholds work, but `--json` bypasses them in v0.13.1. Last release March 2025; unresolved extraction-security and Docker compatibility reports. [Executed checks and alternatives](research/dive.md). |
| IaC and Kubernetes security | Checkov, Trivy config, kube-linter | Overlapping rules, no clear winner. |
| Custom rules with data-flow | Opengrep, Semgrep | Opengrep is a community fork; its cross-file limits and licence trade-offs need a closer look. |
| Architecture, other ecosystems | arch-go, tach | go-arch-lint is now listed; arch-go is the smaller Go alternative. tach is a Rust option for Python. |
| YAML style | yamllint | Not yet compared with schema validation. |
| Licences and supply chain | REUSE, Scorecard, Syft, ScanCode Toolkit | Mostly reporting tools; need an enforcement angle. |

## How this list is kept current

- [`tools.json`](tools.json) records the last review date, sources, rationale and limitations of each tool.
- A [weekly workflow](.github/workflows/freshness.yml) flags archived repositories, old pushes and stale releases. It is a signal, not a verdict: a quiet repository can be a finished one, and a busy one can be the wrong choice.
- Replacements need a written comparison. See [CONTRIBUTING.md](CONTRIBUTING.md).
- [`research/`](research/) holds working notes per stack (JavaScript, Python/Ruby/PHP, Go/Rust/JVM/.NET, cross-cutting). They are research leads: several tools there were compared on documentation only and are **not** recommendations until they appear in the list above.
- Tools we looked at and did not take are in [docs/not-adopted.md](docs/not-adopted.md).
- Step-by-step instructions for an agent that applies the list to a project are in [docs/adopt.md](docs/adopt.md).
- Reusable setup patterns (hooks, CI, generated-code gates) are in [docs/patterns.md](docs/patterns.md).

## License

[CC0 1.0](LICENSE): public domain. Take what is useful.
