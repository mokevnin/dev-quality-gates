# Cross-cutting categories

Reviewed 2026-10-23. Scope: non-language-specific jobs from the README "Under review" table, plus categories we had not listed. Figures (release, last push, stars, licence) come from `gh api` on the review date. Claims taken from a README or docs are marked as such; claims I could not confirm are marked **unverified**. "Last release" is GitHub's latest non-prerelease.

Decision rule used: one preferred tool per job, or "no clear winner" with the condition that decides it.

## 1. Secrets scanning

| Tool | Last release | Last push | Licence | Stars | Note |
|---|---|---|---|---|---|
| [Gitleaks](https://github.com/gitleaks/gitleaks) | v8.30.1, 2026-03-21 | 2026-10-23 | MIT | 30.3k | Recent commits are Dependabot merges (checked the last ~30). Repo moved to a `gitleaks` org; original author wrote Betterleaks after saying he no longer fully controls the repo and name (press reports, not primary). |
| [Betterleaks](https://github.com/betterleaks/betterleaks) | v1.9.0, 2026-09-29; v2.0.0-rc.4 (pre-release) 2026-10-20 | 2026-10-22 | MIT | 2.3k | Created 2026-02-03. README: "maintained by the folks who made Gitleaks, including the original author"; Aikido-sponsored. Reads `gitleaks:allow` comments. Has `.pre-commit-hooks.yaml`, git/dir/GitHub/GitLab sources, optional live validation (`-v`) and analysis (`-a`). |
| [Kingfisher](https://github.com/mongodb/kingfisher) | v2.14.0, 2026-10-20 | 2026-10-20 | Apache-2.0 | 1.3k | Rust, MongoDB-owned. Git history, SARIF/JSON, live validation, revocation. Speed claims are from its own benchmark. |
| [TruffleHog](https://github.com/trufflesecurity/trufflehog) | v3.99.4, 2026-10-22 | 2026-10-23 | **AGPL-3.0** | 28.7k | Best verification coverage; AGPL is a problem for embedding or redistributing, fine for internal CI. |
| [Titus](https://github.com/praetorian-inc/titus) | v1.2.11, 2026-10-08 | 2026-10-20 | Apache-2.0 | 749 | Young, Praetorian. Not compared in depth. |
| [detect-secrets](https://github.com/Yelp/detect-secrets) | v1.5.0, 2024-05-06 | 2026-04-02 | Apache-2.0 | 4.7k | Stale release (already in not-adopted). |
| [Nosey Parker](https://github.com/praetorian-inc/noseyparker) | v0.24.0, 2025-05-08 | 2026-02-21 | Apache-2.0 | 2.3k | **Archived.** Skip (Titus is its successor, by the same company; unverified). |

**Recommendation: Betterleaks, pinned to the stable v1 line until v2 leaves release-candidate.** It keeps Gitleaks' model (regex rules, TOML config, allow comments) so migration is cheap, it is MIT, same author, and actively released, while Gitleaks itself is in maintenance mode (no feature release since March 2026). Kingfisher is the credible alternative if you want speed and revocation and do not care about Gitleaks continuity.

Limits and risks:

- Betterleaks is 8 months old and its stable channel is still v1.9.0; the README already documents v2 as "stable" while GitHub only has release candidates. Pin the version and the Action by SHA.
- v2 changes defaults (no provider requests unless `-v`; custom config must be selected explicitly; new JSON schema).
- Recall figures (98.6% on CredData) come from the project and press, not an independent run. **Unverified.**
- Not verified: exact exit-code semantics for v1 (docs say exit code depends only on findings in v2), baseline support.
- Pre-commit scanning is bypassable; run the same scan in CI over the PR range.

Confidence: medium-high that Gitleaks is in maintenance mode; medium on Betterleaks vs Kingfisher (no benchmark run by me).

## 2. Vulnerabilities and SCA

| Tool | Last release | Last push | Licence | Stars |
|---|---|---|---|---|
| [OSV-Scanner](https://github.com/google/osv-scanner) | v2.7.0, 2026-10-12 | 2026-10-23 | Apache-2.0 | 11.3k |
| [Trivy](https://github.com/aquasecurity/trivy) | v0.76.1, 2026-10-21 | 2026-10-23 | Apache-2.0 | 38.7k |
| [Grype](https://github.com/anchore/grype) | v0.121.0, 2026-10-19 | 2026-10-23 | Apache-2.0 | 13.1k |
| [Syft](https://github.com/anchore/syft) (SBOM generator) | v1.55.0, 2026-10-19 | 2026-10-23 | Apache-2.0 | 9.7k |
| [Renovate](https://github.com/renovatebot/renovate) | 44.181.0, 2026-10-23 | 2026-10-23 | AGPL-3.0 | 22.9k |

Trivy incident (advisory GHSA-69fq-xp46-6x23, CVE-2026-33634, critical; read in full): on 2026-03-19 a malicious Trivy v0.69.4 binary was live about 3 hours; 76 of 77 `trivy-action` tags were force-pushed (about 12 hours); `setup-trivy` tags were replaced. A second event on 2026-03-22/23 pushed malicious v0.69.5/v0.69.6 images to Docker Hub with separately stolen credentials. The advisory says credential rotation after an earlier 2026-03-01 disclosure "was not atomic". Aqua enabled GitHub immutable releases on 2026-03-03/04; I confirmed the current latest release (v0.76.1) is marked immutable via the API. The advisory does not declare the incident closed and says artifacts may linger in caches. Safe references: binaries v0.69.2/v0.69.3 and images by digest. trivy-action tags 0.0.1 to 0.34.2 are affected; some old tags (v0.0.10, v0.34.1, v0.34.2) are still not restored.

**Recommendations:**

- **Dependency vulnerabilities in lockfiles: OSV-Scanner.** Lockfile and SBOM scanning across 11+ ecosystems, call analysis to cut false positives (README), `--licenses` allowlist check, offline mode, guided remediation (experimental). One tool also gives a licence gate.
- **Container images: no clear winner between Trivy and Grype.** Trivy covers more (OS packages, secrets, misconfig, licences) and has the larger community, but has the incident history: if you use it, run the binary pinned to a version and checksum or by image digest, never `trivy-action` by tag, and never `latest`. Grype (+ Syft for SBOMs) is narrower and I found no comparable incident in my searches (**unverified**; I did not audit Anchore's supply chain).
- Dependabot and Renovate are update bots, not gates. Renovate is AGPL-3.0. Not proposed.
- Syft is an SBOM generator (no failing exit by itself): not proposed.

Limits: OSV-Scanner depends on the OSV database and lockfile coverage; it does not scan OS packages in images the way Trivy and Grype do. Not verified: relative detection quality (no benchmark run), `--fail-on` style severity thresholds in OSV-Scanner.

## 3. Docker, Terraform / OpenTofu, Kubernetes

| Tool | Last release | Last push | Licence | Stars | Job |
|---|---|---|---|---|---|
| [Hadolint](https://github.com/hadolint/hadolint) | v2.15.1, 2026-07-31 | 2026-10-19 | GPL-3.0 | 12.5k | Dockerfile lint (runs ShellCheck on `RUN`, README claim from memory, **unverified here**) |
| [TFLint](https://github.com/terraform-linters/tflint) | v0.65.0, 2026-10-22 | 2026-10-22 | MPL-2.0 | 5.8k | Terraform correctness; plugin rulesets per provider |
| [Checkov](https://github.com/bridgecrewio/checkov) | 3.3.30, 2026-10-20 | 2026-10-22 | Apache-2.0 | 9.1k | IaC security: Terraform/plan, CFN, K8s, Helm, Dockerfile, Bicep, OpenTofu (README) |
| Trivy `config` | see section 2 | | Apache-2.0 | | IaC security, same binary as the vulnerability scanner |
| [kube-linter](https://github.com/stackrox/kube-linter) | v0.8.3, 2026-03-10 | 2026-10-21 | Apache-2.0 | 3.5k | K8s/Helm best practices; non-bot commits as late as 2026-09-18 |
| [Kubeconform](https://github.com/yannh/kubeconform) | v0.8.0, 2026-06-04 | 2026-06-13 | Apache-2.0 | 3.2k | Manifest schema validation (CRDs via schema locations) |
| [Kubescape](https://github.com/kubescape/kubescape) | v4.0.16, 2026-10-14 | 2026-10-23 | Apache-2.0 | 11.8k | Frameworks (NSA/CIS), cluster and manifest scanning |
| [Polaris](https://github.com/FairwindsOps/polaris) | v10.2.5, 2026-09-18 | 2026-10-08 | Apache-2.0 | 3.4k | K8s best practices, similar to kube-linter |

**Recommendations:**

- **Dockerfile: Hadolint.** It checks Dockerfile style and best practice; Trivy/Checkov Dockerfile checks are security-focused (comparison of rule counts not done, **unverified**). Limit: GPL-3.0; the last release is 3 months old but commits continue.
- **Terraform/OpenTofu correctness: TFLint.** Security: no clear winner between Checkov and Trivy `config`. Pick Trivy `config` only if you already run Trivy for images (one tool, Rego custom checks); pick Checkov when you want IaC-only scope, graph-based checks and Python/YAML custom policies. Checkov is maintained by Prisma Cloud and the README carries upsell banners; the OSS tool is Apache-2.0 and fully functional (README).
- **Kubernetes: Kubeconform (validity) + kube-linter (policy).** They do different jobs; kube-linter has custom checks via templates (docs, **unverified here**). Polaris overlaps with kube-linter; Kubescape is broader but cluster-oriented and heavier. Do not add either by default.

Limits: TFLint needs `tflint --init` to fetch plugin binaries from GitHub (supply-chain surface; pin versions). Kubeconform is idle since June (stable-tool exception candidate; Kubernetes schemas move slowly). Not verified: OpenTofu support in TFLint, rule-count comparison between Checkov and Trivy.

## 4. Git hook runners

| Tool | Last release | Last push | Licence | Stars | Created |
|---|---|---|---|---|---|
| [pre-commit](https://github.com/pre-commit/pre-commit) | v4.7.0, 2026-10-13 | 2026-10-20 | MIT | 15.7k | 2014 |
| [Lefthook](https://github.com/evilmartians/lefthook) | v2.2.2, 2026-10-13 | 2026-10-21 | MIT | 8.9k | 2019 |
| [hk](https://github.com/jdx/hk) | v2.8.1, 2026-10-23 | 2026-10-23 | MIT | 1.3k | 2025-01 |
| [prek](https://github.com/j178/prek) | v0.5.7, 2026-10-21 | 2026-10-23 | MIT | 8.7k | 2024-10 |

**Recommendation: hk** (owner decision: mise and its tools are our recommended toolchain). README and docs: steps are written once in `hk.pkl` (Pkl) and run in the hook (`hk check`, `hk fix`) and in CI (`hk check --all`); independent steps run in parallel, and read/write file locks stop fixers from colliding; installed with `mise use hk`.

Why not the others: prek is a faster drop-in for pre-commit with a much larger user base (8.7k stars against 1.3k), the fallback for projects without mise that want the pre-commit hook catalogue. pre-commit is the maximum-stability fallback (11 years old, but slower and Python-based). Lefthook runs local commands in parallel with no hook-repo ecosystem.

Limits: hk is smaller than prek and Lefthook, does not install the linters (they must be on `PATH`; pin them in `mise.toml`), and has no pre-commit catalogue. Hooks are bypassable with `--no-verify`: always run `hk check --all` in CI. Not verified: the speed benchmark (published by hk's author), hk vs Lefthook parity.

## 5. YAML, JSON and config files

| Tool | Last release | Last push | Licence | Stars |
|---|---|---|---|---|
| [check-jsonschema](https://github.com/python-jsonschema/check-jsonschema) | 0.38.2, 2026-09-23 | 2026-10-21 | Apache-2.0 (GitHub shows NOASSERTION; LICENSE file is Apache-2.0) | 347 |
| [yamllint](https://github.com/adrienverge/yamllint) | v1.38.0, 2026-01-13 | 2026-09-19 | GPL-3.0 | 3.5k |
| [taplo](https://github.com/tamasfe/taplo) | 0.10.0, 2025-05-23 | 2026-07-28 | MIT | 2.4k |

**Recommendation: check-jsonschema** for structural validity of YAML/JSON/TOML against a JSON Schema (local or remote, cached; ships pre-commit hooks such as `check-github-workflows`, README). Add yamllint only if you want YAML style rules (line length, indentation, duplicate keys). Overlap: jactionlint already covers workflows and `dependabot.yml`; use check-jsonschema for everything else (Renovate config, `.pre-commit-config.yaml`, your own schemas).

Limits: 347 stars and mostly one maintainer (Stephen Rosen, from the LICENSE header); remote schemas add a network dependency (vendor them offline). taplo has had no release for 17 months; not proposed. Not verified: breadth of its bundled schema catalogue; exit-code semantics (hooks rely on them).

## 6. API contracts

| Tool | Last release | Last push | Licence | Stars |
|---|---|---|---|---|
| [Spectral](https://github.com/stoplightio/spectral) | v6.17.0, 2026-10-01 | 2026-10-22 | Apache-2.0 | 3.2k |
| [vacuum](https://github.com/daveshanley/vacuum) | v0.35.1, 2026-10-23 | 2026-10-23 | MIT | 1.1k |
| [Redocly CLI](https://github.com/Redocly/redocly-cli) | 2.71.0, 2026-10-23 | 2026-10-23 | MIT | 1.5k |
| [Buf](https://github.com/bufbuild/buf) | v1.75.0, 2026-10-22 | 2026-10-23 | Apache-2.0 | 11.5k |
| [oasdiff](https://github.com/oasdiff/oasdiff) | v1.34.1, 2026-10-21 | 2026-10-22 | Apache-2.0 | 1.4k |

**Recommendation (OpenAPI/AsyncAPI/Arazzo lint): Spectral.** README: OpenAPI 2, 3.0, 3.1, 3.2, AsyncAPI, Arazzo; its YAML rulesets and JS custom functions are the de facto format that other linters imitate. vacuum is "inspired by Spectral", reads Spectral-style rulesets (with documented compatibility limits), is a single fast Go binary, and is the better pick if you cannot install Node or lint huge specs; it has one dominant contributor (1,602 commits of the top author). Redocly CLI has its own rule/plugin model and bundling/docs features; choose it only if you already use Redocly docs.
**Breaking-change gate (separate job): oasdiff** compares two spec versions and has a `--fail-on` flag (verified in `internal/flags.go`, behaviour not run). **Protobuf: Buf** (lint and `buf breaking`; no peer compared, so listed but not paired).

Limits: Spectral output beyond JSON/SARIF not verified here; Stoplight is part of SmartBear (**unverified** ownership detail from memory). I did not run vacuum against Spectral rulesets.

## 7. SQL and migrations

| Tool | Last release | Last push | Licence | Stars |
|---|---|---|---|---|
| [squawk](https://github.com/sbdchd/squawk) | v2.70.0, 2026-10-15 | 2026-10-23 | Apache-2.0 | 1.2k |
| [SQLFluff](https://github.com/sqlfluff/sqlfluff) | 4.4.0, 2026-10-02 | 2026-10-23 | MIT | 10.0k |
| [Atlas](https://github.com/ariga/atlas) | v1.3.0, 2026-08-02 | 2026-10-21 | Apache-2.0 | 8.8k |

**Atlas lint is partly paywalled.** From the official analyzers page: base checks (destructive changes, data-dependent changes, backward-incompatible changes, naming conventions, non-linear changes, SQL injection) are not badged Pro. Marked **Atlas Pro**: blocking-changes, restrictive changes, concurrent-index policy (Postgres), nested transactions, statement rules, ownership policy, vulnerable extensions, the `check` policy block, and force/allowlist options. The page also says additional checks "require `atlas login`" with a free trial for new accounts. `migrate lint` needs a dev database (`--dev-url docker://...`). The README says Atlas Pro seats stopped being free in September 2024 (blog post in search results).

**Recommendations:**

- **Migration safety (PostgreSQL): squawk.** Rules for locks and downtime (README), reporters tty/gcc/json/gitlab, `--pg-version`, include/exclude rules, GitHub Action. No database needed. Limit: PostgreSQL only; no autofix.
- **SQL style/formatting across dialects: SQLFluff** (multi-dialect, autofix). Limit: slow on large repos (**unverified**); it is a style job, separate from migration safety.
- **Atlas: not adopted** unless you adopt it for schema management; its free lint is a subset and the best checks are paid.

Not verified: that squawk exits non-zero on violations by default (standard, but I read only the CLI help), SQLFluff speed.

## 8. Policy as code

| Tool | Last release | Last push | Licence | Stars |
|---|---|---|---|---|
| [Conftest](https://github.com/open-policy-agent/conftest) | v0.71.1, 2026-10-06 | 2026-10-23 | Apache-2.0 (LICENSE file; GitHub shows NOASSERTION) | 3.3k |
| [OPA](https://github.com/open-policy-agent/opa) | v1.21.4, 2026-10-23 | 2026-10-23 | Apache-2.0 | 12.4k |
| [Kyverno](https://github.com/kyverno/kyverno) | v1.19.2, 2026-10-20 | 2026-10-23 | Apache-2.0 | 8.3k |

**Recommendation: Conftest** for custom, repo-specific rules over structured files in Rego. Per conftest.dev it parses CODEOWNERS, CUE, CycloneDX, Dockerfile, .env, HCL/HCL2, HOCON, ignore files, INI, JSON, Jsonnet, nginx, properties, SPDX, TextProto, TOML, VCL, XML and YAML; outputters include json and github. That makes it the escape hatch for "our Terraform must have tag X" or "CODEOWNERS must cover /infra". Kyverno is a Kubernetes admission/policy engine: relevant only if you run clusters; not a repo-level gate by default.

Limits: Rego has a learning curve; agents write it less reliably than YAML rules (ast-grep, Spectral rulesets). Not verified: exit code on failures and SARIF output (the page does not document them; I believe non-zero on failure, **unverified**).

## 9. Supply chain and licences

| Tool | Last release | Last push | Licence | Stars |
|---|---|---|---|---|
| [OpenSSF Scorecard](https://github.com/ossf/scorecard) | v5.6.0, 2026-10-12 | 2026-10-23 | Apache-2.0 | 5.8k |
| [Allstar](https://github.com/ossf/allstar) | v4.6, 2026-08-31 | 2026-10-21 | Apache-2.0 | 1.5k |
| [REUSE tool](https://github.com/fsfe/reuse-tool) | v6.2.0, 2025-10-27 | 2026-10-13 | mixed (no single SPDX) | 596 |
| [Apache SkyWalking Eyes](https://github.com/apache/skywalking-eyes) | v0.9.0, 2026-09-01 | 2026-10-23 | Apache-2.0 | 317 |
| [ORT](https://github.com/oss-review-toolkit/ort) | 97.2.0, 2026-10-22 | 2026-10-23 | Apache-2.0 | 2.1k |
| [ScanCode Toolkit](https://github.com/aboutcode-org/scancode-toolkit) | v32.5.0, 2026-01-15 | 2026-10-23 | Apache-2.0 + CC-BY-4.0 (LICENSE files) | 2.7k |
| [licensee](https://github.com/licensee/licensee) | v10.1.0, 2026-08-07 | 2026-10-19 | MIT | 917 |

- **Scorecard**: produces a 0 to 10 score per check; I found no built-in "fail below threshold" in the README (**unverified**; you would script it on the JSON). It reports, it does not gate. Allstar is the enforcing sibling but is a GitHub App for org-level settings. Neither proposed.
- **Dependency licences: OSV-Scanner `--licenses="MIT,Apache-2.0"`** (README) already gates these. ORT and ScanCode are heavy compliance suites; use them only with a legal requirement.
- **File-level licence compliance: REUSE** (`reuse lint`, SPDX tags per file) when you publish open source. **Licence header text: SkyWalking Eyes** `header check` (also `dependency check`); warning from its README: fix mode always exits 0, so use check mode in CI. Pick REUSE for SPDX-tag compliance, SkyWalking Eyes when a fixed header text is required.
- licensee only detects a project's licence file; not proposed.

## 10. Custom rules with data-flow: Semgrep vs Opengrep

| Tool | Last release | Last push | Licence | Stars |
|---|---|---|---|---|
| [Semgrep](https://github.com/semgrep/semgrep) | v1.182.0, 2026-10-20 | 2026-10-23 | LGPL-2.1 (engine) | 17.2k |
| [Opengrep](https://github.com/opengrep/opengrep) | v1.32.0, 2026-10-22 | 2026-10-23 | LGPL-2.1 | 3.2k |

Facts: Semgrep's own docs confirm CE engine is LGPL-2.1. Semgrep CE is single-file; cross-file dataflow is in the paid product (search-result summaries of Semgrep docs). Semgrep-maintained registry rules moved to the Semgrep Rules License v1.0, which is not an open-source licence (same source). Opengrep (forked January 2025 by several AppSec vendors) reads existing Semgrep rules, supports `--taint-intrafile` (inter-method taint, higher-order functions in 12 languages, per its README), outputs JSON and SARIF. The vendor-run benchmark (Aikido: 7/9 vs 4/9 multi-hop taint cases) is not independent.

**Recommendation: Opengrep** for custom data-flow rules (source to sink in one file), alongside ast-grep for pure syntax rules. Same rule syntax means you can still write rules in the Semgrep format and move later. Limits: intra-file only (no cross-file); governance is vendor-consortium, not a foundation; rule packs need to be written or taken from sources whose licence you checked. Not verified: independent benchmark, Windows behaviour, rule-pack licensing of Opengrep's own rules.

## Newly discovered categories and tools, ranked by value

1. **Agent instruction and config linting: [agnix](https://github.com/agent-sh/agnix).** v0.59.2 (2026-10-23), Apache-2.0/MIT dual, 457 stars, created 2026-01-30, one main author (1,134 contributions), 10 open issues. README: 702 rules for CLAUDE.md, AGENTS.md, SKILL.md, hooks, MCP configs, Cursor, Copilot, Codex, OpenCode, Kiro; `--fix`, `--fix-safe`, `--strict` (warnings fail), `--format github`, pre-commit hook, GitHub Action, LSP. Highest value for agent-assisted development because broken agent configs fail silently. Other candidates found by search (agents-md-linter and others) have 0 to 5 stars: ignored. Limits: young, rule counts have varied between sources, rules chase vendors' fast-moving formats; exit code on errors is expected but I did not run it. **Proposed.**
2. **API breaking-change gate: oasdiff** (above). Proposed as thin-comparison second tier.
3. **EditorConfig enforcement: [editorconfig-checker](https://github.com/editorconfig-checker/editorconfig-checker)** v4.0.2 (2026-09-19), MIT, 653 stars. README: `-fix`, output formats default/codeclimate/gcc/github-actions. Cheap, language-agnostic. Peers not compared (formatters like Biome/Ruff cover only their own languages).
4. **File and directory naming: [ls-lint](https://github.com/loeffel-io/ls-lint)** v2.3.2 (2026-10-17), MIT, 2.4k stars. README: one `.ls-lint.yml`, very fast, single binary and npm package. No peer compared.
5. **Code duplication: [jscpd](https://github.com/kucherenko/jscpd)** v5.4.2 (2026-10-20), MIT, 6.4k stars. README: 220+ languages, threshold input, SARIF, baseline, also dead-code and complexity. Complexity gates elsewhere are per language (Ruff, golangci-lint); [lizard](https://github.com/terryyin/lizard) (1.24.2, 2026-10-22, 2.6k stars, licence NOASSERTION, cross-language complexity) is a candidate, not compared.
6. **Mutation testing (per language, not cross-cutting): [Stryker](https://github.com/stryker-mutator/stryker-js)** v10.1.1 (2026-10-23), **[cargo-mutants](https://github.com/sourcefrog/cargo-mutants)** v27.1.0 (2026-06-02), **[PIT](https://github.com/hcoles/pitest)** 1.30.1 (2026-10-14), **[mutmut](https://github.com/boxed/mutmut)** 3.8.0 (2026-09-12), [gremlins](https://github.com/go-gremlins/gremlins) v0.6.0 (Go, pre-1.0, 449 stars). Gate verified in docs: Stryker `thresholds.break` exits 1 below the score; PIT `mutationThreshold` fails the build; cargo-mutants exits 2 on missed mutants. mutmut gate not verified. Slow: use on changed files only. Belongs in per-language sections, not here. StrykerJS was later run: [stryker.md](stryker.md).
7. **Agent-skill and MCP scanning: [Cisco skill-scanner](https://github.com/cisco-ai-defense/skill-scanner)** (2.3.1, 2026-10-21, 2.6k stars, Apache-2.0 LICENSE file though GitHub shows NOASSERTION; SARIF, exit codes, best-effort detection per its own warning) and [Cisco mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner) (4.8.7, 1.1k stars). **[Snyk agent-scan](https://github.com/snyk/agent-scan)** (v0.6.9, 3.2k stars; formerly Invariant `mcp-scan`) needs a `SNYK_TOKEN` and its README says CLI output is experimental and not to be used in production workflows: not proposed. Heuristic detection, so "no findings" is not a guarantee. Not proposed until compared by running them on known-bad skills.
8. **Agent sandboxing: [sandbox-runtime](https://github.com/anthropics/sandbox-runtime)** (v0.0.81, 2026-10-20, Apache-2.0, 5.9k stars). OS-level filesystem and network restriction (`sandbox-exec`/bubblewrap, proxy filtering) for agents, MCP servers and arbitrary processes. README labels it a beta research preview. It prevents rather than detects, so it fits "guardrails", but it is pre-1.0 and made for Claude Code; no peer compared. Watch list.
9. **Accessibility and performance budgets:** [axe-core](https://github.com/dequelabs/axe-core) v4.14.0 (MPL-2.0), [pa11y-ci](https://github.com/pa11y/pa11y-ci) 5.0.0 (LGPL-3.0), [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) v0.15.1 (last release 2025-06-26, pushes ongoing; `lhci assert` budgets, from memory). All need a browser and a running site; web-only. Not compared. Watch list.
10. **CODEOWNERS validation:** [codeowners-validator](https://github.com/mszostok/codeowners-validator) last release 2022-04-16, last push 2024-05-01: stale, do not use. GitHub reports CODEOWNERS syntax errors in its UI (from memory, **unverified** as a CI gate). Conftest can parse CODEOWNERS for custom rules. No recommendation.
11. **ADR and architecture decisions:** [adr-tools](https://github.com/adr/adr-tools) is archived (last push 2020); [log4brains](https://github.com/thomvaill/log4brains) last release 2024-12-17. No enforcing tool found. Leave to dependency-cruiser, ArchUnit and import-linter (already in Under review).
12. **Prompt-injection and LLM red-teaming** ([garak](https://github.com/NVIDIA/garak) v0.17.1, [PyRIT](https://github.com/microsoft/PyRIT) v1.1.0, [promptfoo](https://github.com/promptfoo/promptfoo) 0.125.0): these test an LLM application, not a development standard. [llm-guard](https://github.com/protectai/llm-guard) is archived. Out of scope.
13. **PR size, flaky-test detection, commit/PR bots:** [Danger JS](https://github.com/danger/danger-js) (14.0.6, 2026-08-27, MIT) can enforce PR rules in code, but I found no verified, maintained single-purpose tool for PR size limits or flaky-test detection. No recommendation; I did not search these exhaustively.

## What I did not verify

- No tool was installed or run. Exit codes, SARIF support and flags come from READMEs, docs pages or CLI help, as stated per item.
- No independent benchmark of secret scanners, SCA databases, hook runners or IaC rule counts.
- Gitleaks maintainer status is inferred from commit history, release dates and press reports; I did not read maintainers' own statements.
- Ownership claims marked "from memory" (Stoplight/SmartBear, Lighthouse CI assertions, Hadolint ShellCheck integration).
- Betterleaks v2 final release date is unknown; track it.

## Proposed README entries

Ready to paste into the matching categories (new categories: Secrets, Vulnerabilities, Docker and Kubernetes, Terraform, Git hooks, Config files, API contracts, SQL, Policy, Licences, Agent configuration, Custom rules).

```markdown
### Secrets

- **[Betterleaks](https://github.com/betterleaks/betterleaks)**: finds committed secrets in files, git history and pull requests, with optional live validation of credentials. Chosen over Gitleaks because it is built by Gitleaks' original author, reads the same kind of TOML rules and `gitleaks:allow` comments, and is still released, while Gitleaks has had no feature release since March 2026. *Limits:* created February 2026; the stable line is v1.9.0 while v2 is in release-candidate, so pin the version; recall claims are the project's own; TruffleHog (AGPL-3.0) and Kingfisher (Apache-2.0) are the alternatives. [Details](research/cross-cutting.md#1-secrets-scanning).

### Vulnerabilities

- **[OSV-Scanner](https://github.com/google/osv-scanner)**: known vulnerabilities in lockfiles and SBOMs across many ecosystems, with call analysis to reduce noise and a `--licenses` allowlist check. *Limits:* not an image scanner; if you scan container images use Trivy (never `trivy-action` by tag, pin to a version or digest after the March 2026 compromise) or Grype. [Details](research/cross-cutting.md#2-vulnerabilities-and-sca).

### Docker, Terraform and Kubernetes

- **[Hadolint](https://github.com/hadolint/hadolint)**: Dockerfile best practices. *Limits:* GPL-3.0; security-focused IaC checks belong to Trivy or Checkov.
- **[TFLint](https://github.com/terraform-linters/tflint)**: Terraform correctness and provider-specific rules through plugins. *Limits:* `tflint --init` downloads plugins, so pin them; for IaC security add Trivy `config` (if you already run Trivy) or Checkov (no clear winner).
- **[Kubeconform](https://github.com/yannh/kubeconform)**: validates Kubernetes manifests against API and CRD schemas. *Limits:* validity only; last release June 2026.
- **[kube-linter](https://github.com/stackrox/kube-linter)**: best-practice and security checks on manifests and Helm charts. *Limits:* manifests only, no cluster scanning; overlaps with Checkov and Trivy `config`.

### Git hooks

- **[hk](https://github.com/jdx/hk)**: runs Git hooks and project checks from one `hk.pkl` in parallel with file locks, with the same steps in CI. Installed with mise. *Limits:* smaller than prek and Lefthook; does not install linters; hooks can be bypassed, so run `hk check --all` in CI. prek is the fallback without mise, pre-commit the conservative one.

### Config files

- **[check-jsonschema](https://github.com/python-jsonschema/check-jsonschema)**: validates YAML, JSON and TOML against JSON Schema, with ready hooks for common formats. *Limits:* mostly a one-maintainer project; remote schemas need network or vendoring; style rules need yamllint.

### API contracts

- **[Spectral](https://github.com/stoplightio/spectral)**: lints OpenAPI 2/3.x, AsyncAPI and Arazzo with YAML rulesets and custom JS functions. Chosen as the de facto ruleset format that vacuum also reads. *Limits:* needs Node; vacuum is the faster single-binary option; for breaking-change checks add oasdiff.

### SQL

- **[squawk](https://github.com/sbdchd/squawk)**: finds PostgreSQL migrations that lock tables or cause downtime, with JSON output and no database needed. *Limits:* PostgreSQL only, no autofix; SQLFluff covers style. Atlas lint is not adopted: its stronger checks need Atlas Pro and a login.

### Policy

- **[Conftest](https://github.com/open-policy-agent/conftest)**: your own rules in Rego over YAML, JSON, HCL, Dockerfile, CODEOWNERS and 15 more formats. *Limits:* Rego is harder to write than YAML rules; documented outputs are json and github (exit code and SARIF unverified). Kyverno is for Kubernetes admission only.

### Licences

- **[REUSE tool](https://github.com/fsfe/reuse-tool)**: `reuse lint` fails when a file lacks SPDX licence and copyright data. *Limits:* only for projects that follow the REUSE spec; use Apache SkyWalking Eyes when you need a fixed licence header text (its fix mode always exits 0), and OSV-Scanner for dependency licences.

### Agent configuration

- **[agnix](https://github.com/agent-sh/agnix)**: lints CLAUDE.md, AGENTS.md, SKILL.md, hooks and MCP configs for Claude Code, Codex, Cursor, Copilot, OpenCode and Kiro, with `--fix` and `--strict`. *Limits:* created January 2026, one main maintainer; rules track fast-changing vendor formats.

### Custom rules (data-flow)

- **[Opengrep](https://github.com/opengrep/opengrep)**: custom source-to-sink rules in Semgrep rule syntax with intra-file taint tracking, JSON and SARIF. Chosen over Semgrep CE, whose free tier is single-file and whose registry rules are under a non-open licence. *Limits:* no cross-file analysis; vendor-consortium fork from 2025; use ast-grep for syntax-only rules.
```

## Proposed tools.json records

```json
[
  {
    "id": "betterleaks",
    "repo": "betterleaks/betterleaks",
    "category": "Secrets",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/betterleaks/betterleaks#readme", "https://github.com/betterleaks/betterleaks/blob/main/docs/v2_migration.md", "https://github.com/mongodb/kingfisher#readme", "research/cross-cutting.md"],
    "rationale": "Secrets scanner by Gitleaks' original author; keeps Gitleaks-style rules and allow comments, MIT, active releases, git/dir/PR/GitHub sources, optional live validation. Gitleaks has had no feature release since 2026-03-21.",
    "limitations": "Created 2026-02-03. Stable release is v1.9.0 while v2.0.0 is in release-candidate; pin the version. Recall figures are self-reported. Alternatives: Kingfisher (Apache-2.0), TruffleHog (AGPL-3.0)."
  },
  {
    "id": "osv-scanner",
    "repo": "google/osv-scanner",
    "category": "Vulnerabilities",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/google/osv-scanner#readme", "https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23", "research/cross-cutting.md"],
    "rationale": "Lockfile and SBOM vulnerability scanning across 11+ ecosystems with call analysis, offline mode and a licence allowlist check. Chosen for repos; no supply-chain incident found.",
    "limitations": "Not an OS-package or image scanner. Guided remediation is experimental. For images use Trivy (pinned by version or digest, never trivy-action by tag) or Grype."
  },
  {
    "id": "hadolint",
    "repo": "hadolint/hadolint",
    "category": "Docker, Terraform and Kubernetes",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/hadolint/hadolint#readme", "research/cross-cutting.md"],
    "rationale": "Dockerfile best-practice linter; Trivy and Checkov Dockerfile checks are security-oriented.",
    "limitations": "GPL-3.0. Last release 2026-07-31, commits ongoing. Rule-count comparison with Trivy and Checkov not done."
  },
  {
    "id": "tflint",
    "repo": "terraform-linters/tflint",
    "category": "Docker, Terraform and Kubernetes",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/terraform-linters/tflint#readme", "research/cross-cutting.md"],
    "rationale": "Terraform correctness linter with provider-specific rule plugins; complements, not replaces, Checkov or Trivy config security scanning.",
    "limitations": "tflint --init downloads plugins from GitHub; pin them. Security scanning is a separate tool (no clear winner between Trivy config and Checkov). OpenTofu support not verified."
  },
  {
    "id": "kubeconform",
    "repo": "yannh/kubeconform",
    "category": "Docker, Terraform and Kubernetes",
    "last_reviewed": "2026-10-23",
    "stable_exception": true,
    "sources": ["https://github.com/yannh/kubeconform#readme", "research/cross-cutting.md"],
    "rationale": "Validates Kubernetes manifests against API and CRD schemas; does a different job from kube-linter.",
    "limitations": "Validity only, no best-practice or security checks. Last release 2026-06-04, last push 2026-06-13."
  },
  {
    "id": "kube-linter",
    "repo": "stackrox/kube-linter",
    "category": "Docker, Terraform and Kubernetes",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/stackrox/kube-linter#readme", "research/cross-cutting.md"],
    "rationale": "Best-practice and security checks on Kubernetes manifests and Helm charts; lighter than Kubescape and Polaris, which overlap with it.",
    "limitations": "Manifests only. Overlaps with Checkov and Trivy config. Last release 2026-03-10; non-bot commits continue (2026-09)."
  },
  {
    "id": "hk",
    "repo": "jdx/hk",
    "category": "Git hooks",
    "last_reviewed": "2026-10-24",
    "sources": ["https://github.com/jdx/hk", "https://hk.jdx.dev/", "research/cross-cutting.md"],
    "rationale": "Git hooks and project checks from one hk.pkl, parallel with file locks, same steps in CI; installed with mise, our recommended toolchain.",
    "limitations": "1.3k stars. Does not install linters (pin them in mise.toml). No pre-commit hook catalogue. Hooks can be bypassed; run hk check --all in CI. prek is the fallback without mise."
  },
  {
    "id": "check-jsonschema",
    "repo": "python-jsonschema/check-jsonschema",
    "category": "Config files",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/python-jsonschema/check-jsonschema#readme", "research/cross-cutting.md"],
    "rationale": "Validates YAML, JSON and TOML against JSON Schema with ready pre-commit hooks; structural validity, which yamllint does not cover.",
    "limitations": "347 stars, mostly one maintainer. Remote schemas need network or vendoring. No style rules (yamllint). Overlaps jactionlint for workflows and dependabot.yml."
  },
  {
    "id": "spectral",
    "repo": "stoplightio/spectral",
    "category": "API contracts",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/stoplightio/spectral#readme", "https://github.com/daveshanley/vacuum#readme", "https://github.com/Redocly/redocly-cli#readme", "research/cross-cutting.md"],
    "rationale": "De facto ruleset format for OpenAPI 2/3.x, AsyncAPI and Arazzo, with custom JS functions; vacuum and others imitate it.",
    "limitations": "Needs Node. vacuum is faster and a single binary with documented compatibility limits. Breaking-change checks need oasdiff; protobuf needs Buf."
  },
  {
    "id": "squawk",
    "repo": "sbdchd/squawk",
    "category": "SQL",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/sbdchd/squawk#readme", "https://atlasgo.io/lint/analyzers", "research/cross-cutting.md"],
    "rationale": "Finds PostgreSQL migrations that lock tables or risk downtime; JSON reporter, no database needed. Atlas lint is partly Pro-only and needs a dev database.",
    "limitations": "PostgreSQL only, no autofix. SQL style is a separate job (SQLFluff). Exit code on violations not run, only read from CLI help."
  },
  {
    "id": "conftest",
    "repo": "open-policy-agent/conftest",
    "category": "Policy",
    "last_reviewed": "2026-10-23",
    "sources": ["https://www.conftest.dev/", "research/cross-cutting.md"],
    "rationale": "Custom Rego policies over YAML, JSON, HCL, Dockerfile, CODEOWNERS, SPDX and more formats; the general escape hatch for repo-specific rules.",
    "limitations": "Rego learning curve. Documented outputs json and github; exit code and SARIF not verified. Kyverno is Kubernetes admission only."
  },
  {
    "id": "reuse-tool",
    "repo": "fsfe/reuse-tool",
    "category": "Licences",
    "last_reviewed": "2026-10-23",
    "stable_exception": true,
    "sources": ["https://github.com/fsfe/reuse-tool#readme", "https://github.com/apache/skywalking-eyes#readme", "research/cross-cutting.md"],
    "rationale": "reuse lint fails when files lack SPDX licence and copyright information; standard-based. SkyWalking Eyes is the alternative for fixed header text.",
    "limitations": "Last release 2025-10-27. Only for projects following the REUSE spec. Dependency licences are checked by OSV-Scanner."
  },
  {
    "id": "agnix",
    "repo": "agent-sh/agnix",
    "category": "Agent configuration",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/agent-sh/agnix#readme", "research/cross-cutting.md"],
    "rationale": "Lints CLAUDE.md, AGENTS.md, SKILL.md, hooks and MCP configs for several agent tools, with --fix and --strict, pre-commit hook and GitHub Action. Other agent-config linters found have 0 to 5 stars.",
    "limitations": "Created 2026-01-30, one main maintainer. Rule counts differ between sources. Exit codes not run. Rules track fast-changing vendor formats."
  },
  {
    "id": "opengrep",
    "repo": "opengrep/opengrep",
    "category": "Custom rules",
    "last_reviewed": "2026-10-23",
    "sources": ["https://github.com/opengrep/opengrep#readme", "https://docs.semgrep.dev/faq/comparisons/opengrep", "research/cross-cutting.md"],
    "rationale": "Semgrep-compatible rules with intra-file taint tracking, JSON and SARIF, LGPL-2.1; Semgrep CE is single-file and its registry rules are under a non-open licence.",
    "limitations": "No cross-file analysis. Fork created 2024-12 by a vendor consortium. Taint benchmark is vendor-run. Use ast-grep for syntax-only rules."
  }
]
```

Not proposed (kept for the second tier or not-adopted): Trivy (conditional on image scanning), Grype, Checkov, Kyverno, Kubescape, Polaris, Redocly CLI, vacuum, Atlas, SQLFluff, yamllint, taplo, Gitleaks, Kingfisher, TruffleHog, Titus, detect-secrets, Scorecard, Allstar, ORT, ScanCode, licensee, Snyk agent-scan, Cisco scanners, sandbox-runtime, Renovate, Syft, oasdiff, Buf, editorconfig-checker, ls-lint, jscpd, lizard, mutation-testing tools.
