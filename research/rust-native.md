# Rust-native and fast native tools: sweep of missed or wrongly prioritised picks

Date: 2026-10-23. Method: `gh api` (stars, licence, last release, README), npm downloads API (last month), pypistats (last month), crates.io API (`recent_downloads`, ~90 days, not 30 days: marked "crates*"). No tool was installed or run. Everything below rests on metadata and READMEs, not on running the tools. Download numbers include CI and transitive pulls, so they are a rough popularity signal only.

Summary: the current picks mostly hold. One real finding (fallow for JS/TS dead code, architecture and duplication), two tentative additions (ty over Pyrefly; sqruff vs SQLFluff has no clear winner), and a lot of "no, and why".

## 1. JavaScript / TypeScript lint and format: Oxlint + oxfmt vs Biome

| Candidate | Stars | npm/month | Last release | Licence |
|---|---|---|---|---|
| [Oxlint / oxfmt](https://github.com/oxc-project/oxc) | 23.2k | oxlint 101.6M, oxfmt 64.3M, oxlint-tsgolint 45.0M | oxlint 1.89.0, 2026-10-19 | MIT |
| [Biome](https://github.com/biomejs/biome) | 26.0k | 70.7M | 2.6.2, 2026-10-21 | Apache-2.0 (MIT/Apache) |
| dprint | 4.1k | 1.2M | 0.64.3, 2026-10-23 | MIT |
| ESLint / Prettier (reference) | n/a | 672.9M / 569.7M | active | MIT |

Recommendation: keep Oxlint with oxfmt. Reason: higher downloads than Biome for both lint and format, type-aware linting through `oxlint-tsgolint` (built on the TypeScript 7 Go port), and an ESLint-compatible rule and plugin story. Biome is a legitimate peer (more stars, one config, CSS/JSON/GraphQL support). Limits: Biome's single binary covers CSS and GraphQL; Oxlint has no ESLint-plugin parity for Vue/Svelte templates. dprint is a formatter host with plugins and overlaps oxfmt, Ruff and rumdl: not needed. Confidence: medium-high.

## 2. Dead code, architecture and duplication in JS/TS: fallow vs knip + dependency-cruiser (NEW FINDING)

| Candidate | Stars | npm/month | Last release | Licence |
|---|---|---|---|---|
| [fallow](https://github.com/fallow-rs/fallow) (Rust) | 5.2k | 5.65M | v3.35.0, 2026-10-22 | MIT |
| [knip](https://github.com/webpro-nl/knip) (current) | 12.5k | 69.2M | 6.42.1, 2026-10-19 | ISC |
| [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) (current) | not re-measured | not re-measured | in tools.json | MIT |

fallow (created 2026-03-17, so about 7 months old) is one Rust binary that does: unused files, exports, types, class/enum members and dependencies (with `fix` and dry-run); circular dependencies; boundary rules with `bulletproof`, `layered`, `hexagonal`, `feature-sliced` presets; duplication; complexity hotspots; a changed-files PR gate (`fallow audit`, exit 1 on findings in changed files only, inherited findings excluded). Ships GitHub Action, LSP, MCP server and an `agent install` command. `fallow migrate` converts knip, jscpd and stylelint configs. No TypeScript compiler needed.

Recommendation: fallow should replace dependency-cruiser (architecture and cycles) with high confidence for the "one tool, many jobs" principle, and is a credible replacement for knip as well. This is the textbook case of principle 2 (new Rust all-in-one vs two older tools). Caveats that decide the knip swap: knip has 12x the downloads, three more years of framework plugin coverage, and a larger user base; fallow's framework plugin coverage and false-positive rate were NOT verified (README asks users to report missing plugins). Suggested wording: list fallow as the one tool, keep knip named in `limitations` as the fallback for projects where a framework plugin is missing. If the owner wants only evidence-safe changes: swap dependency-cruiser now, mark knip swap "decide after a trial on a real repo". Confidence: medium (medium-low on the knip part).

## 3. Python types: ty vs Pyrefly vs pyright/mypy

| Candidate | Stars | PyPI/month | Last release | Licence |
|---|---|---|---|---|
| [ty](https://github.com/astral-sh/ty) | 19.9k | 41.0M | 0.0.91, 2026-10-22 | MIT |
| [Pyrefly](https://github.com/facebook/pyrefly) | 7.1k | 7.8M | 1.4.0, 2026-10-15 | MIT |
| pyright | 15.7k | 40.3M | 1.1.414, 2026-09-09 | MIT (GitHub shows NOASSERTION) |
| mypy | 20.7k | 160.5M | no GitHub "latest release" object | MIT (GitHub shows NOASSERTION) |

Recommendation: ty, as the pick that belongs with Ruff and uv (same vendor, same install path, 41M downloads, 5x Pyrefly). It is explicitly beta with `0.0.x` versioning and breaking changes allowed. Pyrefly declared itself stable at 1.0 and is the safer answer if you refuse beta tools. mypy still has 4x ty's downloads, so it is not "dead", just older and slower. Limits: ty beta (rule and CLI churn); Pyrefly is Meta-driven with a smaller user base. Confidence: medium-low (a defensible tie; I pick ty by popularity and the Ruff/uv ecosystem). If the owner prefers a stable API, choose Pyrefly instead.

## 4. Git hooks: hk vs prek vs pre-commit vs Lefthook

| Candidate | Stars | Downloads/month | Last release | Licence |
|---|---|---|---|---|
| [hk](https://github.com/jdx/hk) (Rust) | 1.3k | crates* 1.5k (npm `hk` 31, unrelated) | v2.8.1, 2026-10-23 | MIT |
| [prek](https://github.com/j178/prek) (Rust) | 8.7k | PyPI 16.4M, npm @j178/prek 0.49M, crates* 9.1k | v0.5.7, 2026-10-21 | MIT |
| [pre-commit](https://github.com/pre-commit/pre-commit) | 15.7k | PyPI 145.6M | v4.7.0, 2026-10-13 | MIT |
| [Lefthook](https://github.com/evilmartians/lefthook) (Go) | 8.9k | npm 22.3M + 0.83M | v2.2.2, 2026-10-13 | MIT |

Recommendation: hk (owner decision: mise and its tools are our recommended toolchain). One `hk.pkl` runs the same steps in the hook and in CI (`hk check --all`), in parallel with read/write file locks, and is installed and pinned with `mise use hk` next to the linters it runs. It is smaller than prek (1.3k stars against 8.7k, about a sixth of its crates downloads), does not install linters (they must be on `PATH`, which mise solves), and does not reuse the pre-commit hook catalogue. prek stays the fallback for projects without mise that want that catalogue; Lefthook remains the plain YAML runner. Confidence: medium (adoption gap accepted for toolchain fit).

## 5. Secrets: Betterleaks vs Kingfisher vs ripsecrets vs Gitleaks vs TruffleHog

| Candidate | Stars | Downloads | Last release | Licence |
|---|---|---|---|---|
| [Betterleaks](https://github.com/betterleaks/betterleaks) (Go) | 2.3k | v1.9.0 release assets 322k total | v1.9.0, 2026-09-29 | MIT |
| [Kingfisher](https://github.com/mongodb/kingfisher) (Rust, MongoDB) | 1.3k | crates* 52 (distributed mostly as binary/PyPI `kingfisher-bin`, not measured) | v2.14.0, 2026-10-20 | Apache-2.0 |
| [ripsecrets](https://github.com/sirwart/ripsecrets) (Rust) | 0.9k | crates* 5.0k | v0.1.11, 2025-05-27 | MIT |
| Gitleaks | 30.3k | npm 83.5k | v8.30.1, 2026-03-21 | MIT |
| TruffleHog | 28.7k | not measured | v3.99.4, 2026-10-22 | AGPL-3.0 |
| noseyparker | 2.3k | n/a | archived 2026-02-21 | Apache-2.0 |

Recommendation: keep Betterleaks (gitleaks-config compatible, MIT, active). Kingfisher is the strongest Rust contender (live credential validation, blast-radius mapping, revocation, SARIF/JSON, MongoDB backing, very active) but has fewer stars and a bigger scope than a CI gate needs; ripsecrets is fast but its last release is 5 months old and rules are few; noseyparker is archived. Kingfisher is worth naming in Betterleaks' `limitations` as the choice when you want to know which leaked credentials are still live. Confidence: medium.

## 6. SQL: sqruff vs SQLFluff (style), squawk (migration safety, already listed)

| Candidate | Stars | Downloads/month | Last release | Licence |
|---|---|---|---|---|
| [SQLFluff](https://github.com/sqlfluff/sqlfluff) | 10.0k | PyPI 9.36M | 4.4.0, 2026-10-02 | MIT |
| [sqruff](https://github.com/quarylabs/sqruff) (Rust) | 1.4k | PyPI 0.15M, crates* 5.0k | v0.43.0, 2026-10-22 | Apache-2.0 |
| [squawk](https://github.com/sbdchd/squawk) (already listed) | 1.2k | npm 3.30M | v2.70.0, 2026-10-15 | Apache-2.0 |

Recommendation: no clear winner for style linting. SQLFluff has 60x sqruff's downloads, 7x the stars, mature dialect and templater (dbt, Jinja) support. sqruff is a Rust reimplementation, much faster, `lint` and `fix`, LSP, but pre-1.0 with narrower dialect/templater coverage. If you must pick one by the owner's principles: sqruff for plain SQL files, SQLFluff for dbt/Jinja. Do not add a SQL style entry until someone runs both on a real schema. squawk stays as is. Confidence: low.

## 7. Python architecture: tach vs import-linter (current)

| Candidate | Stars | PyPI/month | Last release | Licence |
|---|---|---|---|---|
| [tach](https://github.com/tach-org/tach) (Rust core) | 2.9k | 4.57M | v0.35.3, 2026-10-06 | MIT |
| import-linter (current) | n/a here | 21.2M | in tools.json | BSD-2 |

Recommendation: keep import-linter (4.6x downloads, stable contract types, 1.x). tach is the modern option (module interfaces, public API enforcement, fast, pre-1.0 at 0.35), good alternative for large monorepos. No swap. Confidence: medium-low.

## 8. TOML: tombi vs taplo vs dprint

| Candidate | Stars | Downloads/month | Last release | Licence |
|---|---|---|---|---|
| [tombi](https://github.com/tombi-toml/tombi) (Rust) | 1.2k | npm 16.7k + scoped 1.7k, crates* 86 | v1.9.1, 2026-10-23 | MIT |
| [taplo](https://github.com/tamasfe/taplo) (Rust) | 2.4k | npm @taplo/cli 364k, crates* 208k | 0.10.0, 2025-05-23 | MIT |
| dprint (toml plugin) | 4.1k | npm 1.2M | 0.64.3, 2026-10-23 | MIT |

Recommendation: no clear winner, no entry. taplo has the usage but its last release is 17 months old; tombi is actively released, adds linting, JSON-schema validation and an LSP, but is small. The area is low-priority (Ruff and Cargo already own `pyproject.toml`/`Cargo.toml` hygiene; `check-jsonschema` is already listed for schema validation). Revisit when tombi gets traction. Confidence: low.

## 9. Env files, YAML, shell, Docker, commits, supply chain: Rust replacements?

| Job | Rust candidate | Stars | Downloads | Verdict |
|---|---|---|---|---|
| .env lint | [dotenv-linter](https://github.com/dotenv-linter/dotenv-linter) v4.0.0 (2025-10-18), MIT | 2.1k | crates* 29.5k, npm 63k | works, narrow, last release a year old: no entry |
| YAML style | [ryl](https://github.com/owenlamont/ryl) v0.26.0 (2026-10-18), MIT | 91 | PyPI 20k vs yamllint 24.4M | README says edge cases "still maturing": no, keep yamllint as under review |
| Shell | none found (ShellCheck is Haskell, 40.2k stars, v0.11.0 2025-08-04); `shellcheck-rs` repo not found | | | no Rust replacement; keep ShellCheck |
| Dockerfile | none found | | | keep hadolint |
| Commit messages | [commitlint-rs](https://github.com/KeisukeYamashita/commitlint-rs) v0.2.4, 73 stars | 73 | | no; commitlint npm 44M. cocogitto/committed already rejected |
| SBOM / vuln | none replaces Syft/Trivy/Grype; `cargo-auditable`, `cargo-cyclonedx` are Rust-only | | | keep current |
| Markdown | rumdl (already listed) v0.3.0, 1.6k stars, PyPI 0.63M, MIT (LICENSE file is MIT; GitHub API shows NOASSERTION) | | | keep; still pre-1.0 |
| GH Actions | zizmor v1.31.1, 6.8k stars, MIT, crates* 47k | | | owner decision: keep jactionlint; no change |
| typos / lychee / ast-grep | already listed. typos 4.2k stars, PyPI 0.99M, crates* 134k; lychee 4.0k stars; ast-grep 16.3k stars, npm 7.58M | | | keep |

## 10. Rust-ecosystem extras (ours: clippy, rustfmt, cargo-deny)

| Candidate | Stars | crates* (90 d) | Last release | Licence | Enforcement angle |
|---|---|---|---|---|---|
| [cargo-nextest](https://github.com/nextest-rs/nextest) | 3.4k | 1.86M | 0.9.149, 2026-10-20 | Apache-2.0 | test runner: fast, retries, flaky-test marking, JUnit; fails build, but it is a runner, not a rule engine |
| [cargo-mutants](https://github.com/sourcefrog/cargo-mutants) | 1.4k | 366k | v27.1.0, 2026-06-02 | MIT | exits non-zero when mutants survive (needs test-suite time) |
| [cargo-machete](https://github.com/bnjbvr/cargo-machete) | 1.4k | 594k | v0.9.2, 2026-04-15 | MIT | unused deps, fast, regex-based, `--fix`, can false-positive |
| [cargo-shear](https://github.com/Boshen/cargo-shear) (Oxc author) | 0.6k | 62k | v1.14.0, 2026-09-22 | MIT | unused deps via AST, `--fix`, no nightly |
| [cargo-udeps](https://github.com/est31/cargo-udeps) | 2.1k | 111k | v0.1.61, 2026-04-29 | NOASSERTION | needs nightly |
| [cargo-vet](https://github.com/mozilla/cargo-vet) | 1.0k | 120k | v0.10.3, 2026-10-22 | Apache-2.0 | audit-based supply-chain policy; heavy process |
| [cargo-hack](https://github.com/taiki-e/cargo-hack) | 0.9k | 208k | v0.6.45, 2026-05-30 | Apache-2.0 | feature-powerset checks; libraries only |
| cargo-semver-checks | 1.7k | n/a | v0.51.0, 2026-10-03 | Apache-2.0 | libraries only (already in not-adopted) |

Recommendations:

- Unused dependencies: cargo-machete as the one pick (10x cargo-shear's downloads, simple, `--fix`). Watch cargo-shear; it is the more accurate, newer one. Confidence: medium-low. Real gap in our Rust section: cargo-deny does not detect unused dependencies.
- cargo-nextest, cargo-mutants, cargo-vet, cargo-hack: no entry. nextest is a runner (popular and excellent, but test running is not a standards check); mutants was not run on changed files ([stryker.md](stryker.md)); vet needs an audit process; hack is for libraries.

## 11. Task runners, bundlers, runtimes (only if enforcement-relevant)

just (36.4k stars, crates* 559k, CC0), mise (35.3k stars, MIT), Deno (108.7k stars; `deno lint`/`deno fmt` only for Deno projects), rolldown (14.0k stars, npm 443.7M, MIT), `@typescript/native-preview` (25.4M, already covered by our TypeScript 7 pick): none is an enforcement tool. No entries. mise is not an enforcement tool but is recommended as the toolchain installer for hk and the linters (see the Toolchain entry).

## Changes to our current picks

| Current entry | Change | Why | Confidence |
|---|---|---|---|
| dependency-cruiser | Replace with fallow | Rust, boundaries presets, cycles, plus dead code and duplication in one binary; PR gate on changed files | medium |
| knip | Replace with fallow, or keep as named fallback until fallow is trialled | fallow covers the same job plus more; knip has 12x downloads and mature plugins | medium-low |
| oxlint (with oxfmt) | Keep | beats Biome on downloads; Biome stays named in limitations | medium-high |
| betterleaks | Keep; mention Kingfisher for live validation | Kingfisher is the strongest Rust rival but not more popular | medium |
| import-linter | Keep | tach is pre-1.0 and 4.6x smaller | medium-low |
| jactionlint | Keep (owner decision) | zizmor is 6.8k stars but owner decided | n/a |
| rumdl, ruff, mago, typos, lychee, ast-grep, squawk | Keep | confirmed active; rumdl is MIT despite NOASSERTION | high |
| Under review: Git hooks | Resolve to hk, with mise | owner decision: mise and its tools are recommended; prek has 8.7k stars against hk's 1.3k | medium |
| Under review: Python types | Resolve to ty (or Pyrefly if stable API is required) | ty has 5x downloads, 2.8x stars, but beta | medium-low |
| Under review: Biome | Close as "Superseded/Overlap" | see section 1 | medium-high |
| Under review: SQL style, TOML, YAML style | Leave open | no clear winner | low |
| Rust section | Add cargo-machete | gap: unused dependencies | medium-low |

## Proposed README entries

- **[fallow](https://github.com/fallow-rs/fallow)**: finds unused files, exports and dependencies, circular imports, layer and boundary violations (presets: bulletproof, layered, hexagonal, feature-sliced), duplication and complexity in JavaScript and TypeScript, in one Rust binary with `fix`, a changed-files PR gate that exits non-zero, an LSP and an MCP server. Chosen as one tool instead of knip plus dependency-cruiser. *Limits:* created March 2026; framework plugin coverage and false-positive rate not verified by us; knip has far more users and plugins.
- **[hk](https://github.com/jdx/hk)**: runs Git hooks and project checks from one `hk.pkl` in parallel with file locks, and runs the same steps in CI. Installed with mise. Chosen as the primary runner because mise and its tools are our recommended toolchain. *Limits:* 1.3k stars; does not install linters; does not reuse pre-commit hooks.
- **[mise](https://github.com/jdx/mise)**: pins tool versions and runs tasks in one `mise.toml`. *Limits:* installer and task runner only.
- **[ty](https://github.com/astral-sh/ty)**: Python type checker from the Ruff and uv team, in Rust, with a language server; fails the build on type errors. Chosen over Pyrefly and mypy for adoption (41M PyPI downloads a month) and fit with Ruff. *Limits:* beta, `0.0.x` versions with breaking changes; use Pyrefly (stable 1.x) if you need a stable API.
- **[cargo-machete](https://github.com/bnjbvr/cargo-machete)**: finds dependencies in `Cargo.toml` that the code does not use and fails the build; `--fix` removes them. Chosen for speed and adoption over cargo-shear and cargo-udeps (which needs nightly). *Limits:* regex-based, so macros can give false positives; ignore list needed; use cargo-shear if that bites.

```json
[
  {
    "id": "fallow",
    "name": "fallow",
    "repo": "fallow-rs/fallow",
    "category": "JavaScript and TypeScript",
    "last_reviewed": "2026-10-23",
    "sources": [
      "https://github.com/fallow-rs/fallow",
      "https://www.npmjs.com/package/fallow",
      "research/rust-native.md"
    ],
    "rationale": "finds unused files, exports and dependencies, circular imports, boundary violations (bulletproof, layered, hexagonal, feature-sliced presets), duplication and complexity in one Rust binary, with `fix`, a changed-files PR gate that exits non-zero, an LSP and an MCP server. One tool instead of knip plus dependency-cruiser.",
    "limitations": "created March 2026 (v3.35.0, 5.2k stars, 5.65M npm downloads a month against knip's 69M); framework plugin coverage and false-positive rate not verified. Keep knip as the fallback if a framework plugin is missing.",
    "details": "research/rust-native.md"
  },
  {
    "id": "mise",
    "name": "mise",
    "repo": "jdx/mise",
    "category": "Toolchain",
    "last_reviewed": "2026-10-24",
    "sources": [
      "https://github.com/jdx/mise",
      "https://mise.jdx.dev/"
    ],
    "rationale": "Pins the versions of tools (and hk, and the linters hk runs) in one `mise.toml` and runs tasks, so developers, hooks and CI use identical versions; `mise run check` is the single entry point. By the author of hk and jactionlint; 35.3k stars, MIT.",
    "limitations": "It is an installer and task runner, not a checker, so it enforces nothing by itself. Tools installed from GitHub releases or language registries still need version pinning and review like any dependency."
  },
  {
    "id": "hk",
    "name": "hk",
    "repo": "jdx/hk",
    "category": "Git hooks",
    "last_reviewed": "2026-10-24",
    "sources": [
      "https://github.com/jdx/hk",
      "https://hk.jdx.dev/",
      "research/rust-native.md"
    ],
    "rationale": "Runs Git hooks and project checks from one `hk.pkl` (Pkl) file, in parallel, with read/write file locks so fixers do not collide. The same steps run in the hook (`hk check`, `hk fix`) and in CI (`hk check --all`). Installed and version-pinned through mise (`mise use hk`), which we recommend; v2.8.1 on 2026-10-23, MIT.",
    "limitations": "1.3k stars, against 8.7k for prek and 8.9k for Lefthook. Does not install linters: they must be on `PATH`, so pin them in `mise.toml`. Config is Pkl, not `.pre-commit-config.yaml`, so the pre-commit hook catalogue is not reused. Hooks can be bypassed (`--no-verify`), so run `hk check --all` in CI. `hk fix` leaves fixes unstaged unless `--stage` is passed; installing hooks globally needs Git 2.54 or newer. The speed benchmark on hk's site is the author's own.",
    "details": "research/rust-native.md"
  },
  {
    "id": "ty",
    "name": "ty",
    "repo": "astral-sh/ty",
    "category": "Python",
    "last_reviewed": "2026-10-23",
    "sources": [
      "https://github.com/astral-sh/ty",
      "https://pypistats.org/packages/ty",
      "https://github.com/facebook/pyrefly",
      "research/rust-native.md"
    ],
    "rationale": "Python type checker and language server in Rust from the Ruff and uv team; fails the build on type errors. 41M PyPI downloads a month against Pyrefly's 7.8M and 19.9k stars.",
    "limitations": "beta, `0.0.x` versioning with breaking changes allowed. Pyrefly (Meta, stable 1.x) is the alternative if you need a stable API.",
    "details": "research/rust-native.md"
  },
  {
    "id": "cargo-machete",
    "name": "cargo-machete",
    "repo": "bnjbvr/cargo-machete",
    "category": "Rust",
    "last_reviewed": "2026-10-23",
    "sources": [
      "https://github.com/bnjbvr/cargo-machete",
      "https://crates.io/crates/cargo-machete",
      "research/rust-native.md"
    ],
    "rationale": "finds dependencies in `Cargo.toml` that the code does not use and exits non-zero; `--fix` removes them. Fast and 10x more downloaded than cargo-shear; cargo-udeps needs nightly.",
    "limitations": "regex-based, so macro-generated uses can be false positives (use the ignore list or `--with-metadata`); cargo-shear is the AST-based alternative.",
    "details": "research/rust-native.md"
  }
]
```

## Not verified

- fallow accuracy, framework coverage and speed claims, hk against Lefthook parity, ty and Pyrefly diagnostics quality, sqruff dialect coverage: README and metadata only.
- dependency-cruiser and import-linter figures were not re-measured; taken from our existing entries.
- crates* = crates.io `recent_downloads` (about 90 days), not 30 days. Kingfisher's main channels (GitHub releases, `kingfisher-bin` on PyPI) were not measured. TruffleHog, Gitleaks and Betterleaks real-world usage are not comparable on download numbers.
- The web search for Rust rewrites of ShellCheck, hadolint, commitlint and gitleaks returned nothing useful; "none found" there means my GitHub name probes and that one search, not an exhaustive check.
