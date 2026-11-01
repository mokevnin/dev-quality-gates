# Not adopted, and why

Tools we looked at and did **not** recommend, as of 2026-10-23. This keeps the same question from being asked again, and shows what would change the answer. It is a record of decisions, not a list of bad tools.

Reasons used below:

- **Superseded:** a newer tool covers it.
- **Overlap:** another recommendation already does the job.
- **Unverified:** not compared yet; sits in [Under review](../README.md#under-review).
- **Not enforcement:** it reports or advises, it does not fail a build.
- **Stale or risky:** maintenance or supply-chain signals.

## Rejected for now

| Tool | Reason | What would change the answer |
|---|---|---|
| [actionlint](https://github.com/rhysd/actionlint) | Superseded by jactionlint, whose `correctness` profile covers it. Last release 2026-03-30. | jactionlint becomes unmaintained. |
| [zizmor](https://github.com/zizmorcore/zizmor) (by default) | Overlap: jactionlint has a rule for each zizmor audit. Allowed as an addition in the cases listed in [research/github-actions.md](../research/github-actions.md). | An independent comparison finding real gaps in jactionlint. |
| [pinact](https://github.com/suzuki-shunsuke/pinact) | Overlap: `jactionlint --online --fix` pins tags to commit SHAs. | You want pinning without adopting a linter. |
| [cspell](https://github.com/streetsidesoftware/cspell) | Overlap with typos, which has fewer false positives and needs little setup. | You need project dictionaries or many natural languages. |
| [detect-secrets](https://github.com/Yelp/detect-secrets) | Stale: last release v1.5.0 on 2024-05-06. | A new release and a comparison with the other secret scanners. |
| [cocogitto](https://github.com/cocogitto/cocogitto), [convco](https://github.com/convco/convco), [committed](https://github.com/crate-ci/committed) | Rust Conventional Commits tools, but small (1.2k, 329 and 185 stars) and slower to release; cocogitto's last push is 2026-04. commitlint has about 44 million npm downloads a month. | One of them gains adoption and a release pace close to commitlint's, and you do not want Node. |
| [commitizen](https://github.com/commitizen-tools/commitizen) | Python tool for commit checks, version bumps and changelogs (3.5k stars, active). Overlaps commitlint plus a release tool. | A Python project with no Node in its toolchain. |
| [gitlint](https://github.com/jorisroovers/gitlint) | Stale: last release 2023-03, last push 2024-07. | New releases. |
| [conventional-pre-commit](https://github.com/compilerla/conventional-pre-commit) | A single pre-commit hook (559 stars); does not check a CI range the way commitlint does. | You only need the local hook. |
| [git-cliff](https://github.com/orhun/git-cliff) | A changelog generator (12k stars), not a linter. | Not applicable. |
| [Bandit](https://github.com/PyCQA/bandit) | Overlap with the Ruff `S` rules. | You need custom Bandit plugins. |
| [pydocstyle](https://github.com/PyCQA/pydocstyle) | Archived 2023-11-03; Ruff `D` rules replace it. | None. |
| [Psalm](https://github.com/vimeo/psalm) | Mago covers static analysis; Psalm 7.0 was still a release candidate when reviewed. | A stable 7.0 and a clear gap in Mago. |
| qossmic/deptrac | Archived and moved; use [deptrac/deptrac](https://github.com/deptrac/deptrac). | None. |
| [phpcpd](https://github.com/sebastianbergmann/phpcpd) | Archived 2023-01-10. | None. |
| [Brakeman](https://github.com/presidentbeef/brakeman) | Licence is non-commercial only (Brakeman Public Use License); commercial use needs a paid licence. Kept in [Under review](../README.md#under-review). | A licence change, or your use being non-commercial. |
| [Atlas](https://github.com/ariga/atlas) migration lint | Checks that matter for locks and downtime (`PG1xx`, `PG3xx`) are labelled Atlas Pro; extra checks need `atlas login` ([analyzers](https://atlasgo.io/lint/analyzers)). squawk covers PostgreSQL lock safety without that. | The checks you need move to the free edition. |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Latest release v8.30.1 (2026-03-21); Betterleaks is recommended instead and reads the same kind of config. | A new Gitleaks release line and a comparison. |
| [cargo-audit](https://github.com/rustsec/rustsec) | cargo-deny covers the RustSec advisory check and more. | You only want advisories and no policy file. |
| [ESLint](https://github.com/eslint/eslint) and [Prettier](https://github.com/prettier/prettier) | Superseded by Oxlint with oxfmt: one Rust toolchain for lint and format. ESLint 9 reached end of life in August 2026, and typescript-eslint does not support TypeScript 7 yet. Both are still active. | You rely on Vue, Svelte or Angular template linting or ESLint plugins that Oxlint lacks. |
| [PHPStan](https://github.com/phpstan/phpstan), [PHP-CS-Fixer](https://github.com/PHP-CS-Fixer/PHP-CS-Fixer), [Deptrac](https://github.com/deptrac/deptrac) | Overlap: Mago does static analysis, formatting and architecture rules in one binary. | Your framework needs a PHPStan extension (Larastan, Symfony) that Mago does not cover. |
| [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) | Superseded by rumdl, which reads markdownlint configuration and also formats. Still maintained. | rumdl has gaps for your custom rules. |
| [vulture](https://github.com/jendrikseipp/vulture) | Heuristic dead-code finder that needs a whitelist; Ruff covers unused imports and variables. | A reliable cross-module dead-code tool. |
| [deadcode](https://pkg.go.dev/golang.org/x/tools/cmd/deadcode) | Reports unreachable functions but exits 0 on findings (run on v0.52.0), so it cannot fail a build without a wrapper. Without `-test` and `-tags` it also flags functions that only tests call. [Details](../research/ecosystem-gaps.md#go). | A release that exits non-zero on findings. |
| [go-test-coverage](https://github.com/vladopajic/go-test-coverage) | Narrow, one main maintainer, GPL-3.0. A coverage floor can be set with `go test` and a short script (see [patterns](patterns.md)). | A wider user base. |
| [cargo-semver-checks](https://github.com/obi1kenobi/cargo-semver-checks) | Useful only for published libraries; not a general guardrail. | A library-focused section. |
| [Spectral](https://github.com/stoplightio/spectral) and [Redocly CLI](https://github.com/Redocly/redocly-cli) | Overlap with vacuum, which reads Spectral rulesets as a native binary. Both are actively released and far more downloaded (about 7 and 10 million npm downloads a month). | You depend on custom JavaScript rule functions, or on Redocly's bundling and docs tooling. |
| [SQLFluff](https://github.com/sqlfluff/sqlfluff) | Superseded for plain SQL linting by sqruff, a Rust tool with SQLFluff-style rules. SQLFluff is still the larger project (10k stars) and active. | You need dbt or Jinja templating, or a dialect sqruff lacks. |
| [openapi-changes](https://github.com/pb33f/openapi-changes) | Smaller alternative to oasdiff (361 stars). | A feature oasdiff lacks. |
| [gitlab-ci-local](https://github.com/firecow/gitlab-ci-local) | Runs GitLab pipelines locally for debugging (4.1k stars, active); it does not enforce a standard. | A guardrail mode. |
| [glsec](https://github.com/predictor2718/glsec) | Created 2026-10-15, no stars and no adopters yet; Plumber covers the same ground with real usage. | Adoption and a comparison with Plumber. |
| [gitlab-lint](https://github.com/elijah-roberts/gitlab-lint) | Stale (last push 2024-03) and only a syntax check through the GitLab API. | None. |
| [Dependabot](https://docs.github.com/en/code-security/dependabot) | GitHub-only. Renovate covers GitLab, Bitbucket and others with the same policy options. This repository still uses Dependabot because it is on GitHub only. | Your repositories are all on GitHub and you want zero setup. |
| [pre-commit](https://github.com/pre-commit/pre-commit) | hk is the pick and fits the mise toolchain. pre-commit is still maintained (15.7k stars) and has the largest hook catalogue. | You do not use mise, or need a hook that only exists as a pre-commit repository. |
| [prek](https://github.com/j178/prek) | A faster drop-in for pre-commit (8.7k stars), but it is a separate toolchain from mise and keeps `.pre-commit-config.yaml`. | You do not use mise, or want to reuse the pre-commit hook catalogue unchanged. |
| [Pyrefly](https://github.com/facebook/pyrefly), [pyright](https://github.com/microsoft/pyright), [mypy](https://github.com/python/mypy) | ty has more stars and downloads than Pyrefly. pyright (40 million downloads) and mypy (160 million) are the stable choices. mypy plugins are a limit of ty, not a reason to change the default: see [research/mypy-plugins.md](../research/mypy-plugins.md). | ty stays in beta, you need a stable 1.x today (Pyrefly), or a mypy plugin enforces a check ty does not run. Reproduced 2026-11-01: `pydantic.mypy` rejects an unannotated field and ty 0.0.95 does not. |
| [cargo-udeps](https://github.com/est31/cargo-udeps), [cargo-shear](https://github.com/Boshen/cargo-shear) | cargo-udeps needs nightly (more accurate); cargo-shear is smaller (577 stars). One unused-dependency tool is enough. | You need accuracy over speed (cargo-udeps). |
| [bundler-audit](https://github.com/rubysec/bundler-audit), [pip-audit](https://github.com/pypa/pip-audit), mix_audit, [OWASP Dependency-Check](https://github.com/dependency-check/DependencyCheck) | Overlap with OSV-Scanner, which reads the lockfiles of all these ecosystems. | OSV-Scanner misses an ecosystem you use. |
| [erb_lint](https://github.com/Shopify/erb_lint) | No release since 2025-01; Herb replaces it. | A new release. |
| [Steep](https://github.com/soutaro/steep) | Sorbet has far more adoption (158 million gem downloads against 6.9 million). | You standardise on RBS signatures. |
| [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) | No GitHub release since 2025-06, although commits continue; lab data varies between runs. | A release, or a performance-budget gate you need. |
| [i18next-cli](https://github.com/i18next/i18next-cli) | i18next only and young (244 stars). | Wider adoption. |
| [cargo-nextest](https://github.com/nextest-rs/nextest) | A test runner (faster, retries flaky tests), not a guardrail. | Not applicable. |
| [cargo-llvm-cov](https://github.com/taiki-e/cargo-llvm-cov) | Rust coverage floor; diff-cover reads its report and checks changed lines for every language. | You want only a Rust total threshold. |
| [ArchUnitTS](https://github.com/LukasNiessen/ArchUnitTS), [ts-arch](https://github.com/ts-arch/ts-arch) | Overlap with dependency-cruiser. ArchUnitTS is active (508 stars); ts-arch has had no release since 2024-12. [Details](../research/custom-rules.md). | You want rules as unit tests in the test runner rather than a separate command. |
| [arch-go](https://github.com/arch-go/arch-go) | Overlap with go-arch-lint, which has twice the stars. arch-go also checks function content and naming. | You want naming and function-size rules in the same tool. |
| [PyTestArch](https://github.com/zyskarch/pytestarch) | Overlap with import-linter; small (176 stars). | You want architecture rules as pytest tests. |
| [PHPat](https://github.com/carlosas/phpat) | Overlap: Mago `guard` covers architecture rules in the same binary. | Your framework needs PHPStan and Mago is not used. |
| [GritQL](https://github.com/biomejs/gritql), [Comby](https://github.com/comby-tools/comby) | Alternatives to ast-grep. GritQL is pre-1.0 (v0.0.3) with its own query language; Comby has had no release since 2022 and matches text patterns, not syntax trees. | GritQL reaches 1.0, or you need Comby's language-agnostic matching. |
| [React Doctor](https://github.com/millionco/react-doctor) | Overlaps the ESLint/Oxlint React rules and Knip. Licence is a "Modified MIT" with use restrictions (npm: "SEE LICENSE IN LICENSE"). Its score needs a remote API. Findings and exit codes ran on 0.9.18 ([research](../research/stack-javascript.md#react-doctor-reviewed-2026-10-26)). | Its React-specific rules prove to catch what eslint-plugin-react misses, or run as the Oxlint plugin without the remote score. |
| [ansible-review](https://github.com/willthames/ansible-review) | Stale wrapper around ansible-lint. PyPI 0.13.9 on 2018-11-25, last push 2021-04-01. On 2026-11-01 `ansible-review --help` exited 1 because `default_rulesdir` is gone from ansible-lint. [Details](../research/ansible.md). | A release that starts against current ansible-lint and checks something it does not. |
| [Steampunk Spotter](https://gitlab.com/xlab-steampunk/steampunk-spotter-client/spotter-cli) | Current CLI (6.6.0, 2026-10-14), but a scan needs their hosted API. The vendor says it does not replace ansible-lint. [Details](../research/ansible.md). | A local mode that fails the build without uploading the playbook. |
| [Molecule](https://github.com/ansible/molecule) | A test runner for roles and playbooks (v26.10.0, 2026-10-12), not a linter. | Not applicable. |

## Held back (Unverified)

Not rejected: these are in [Under review](../README.md#under-review) because we have not compared the candidates properly.

- **Trivy.** In March 2026 trivy-action tags and a release were compromised ([advisory](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23)). OSV-Scanner is recommended for lockfile vulnerabilities; for container images and IaC security Trivy, Grype and Checkov are still compared.
- **Dive.** Its CI thresholds fill an image-layer efficiency gap, but v0.13.1 has a reproduced JSON/CI bypass, old releases and unresolved extraction-security and Docker compatibility reports. [Review and alternatives](../research/dive.md). Reconsider after maintenance and compatibility evidence improves; no stability exception is claimed.
- **TruffleHog and Kingfisher.** Alternatives to Betterleaks; TruffleHog is AGPL-3.0.
- **Biome.** The other Rust JS toolchain; Oxlint with oxfmt is recommended.
- **Semgrep and Opengrep.** Needed only for data-flow rules; ast-grep covers syntax rules.
- **IaC and Kubernetes security, architecture, YAML, supply chain.** See the table in the README.

## Seen in sphericon, not taken

[sphericon](https://github.com/getsphericon/sphericon) is a source of candidates, not a list to copy.

| Item | Reason |
|---|---|
| vacuum, squawk, oxfmt, govulncheck, OpenSSF Scorecard, go-test-coverage | Not compared with alternatives yet, so not recommended. |
| release-please | Release automation, not enforcement. |
| CodeQL | Not checked against the other security scanners. |
| pinact, zizmor next to jactionlint | Overlap, see above. |

schemalens was adopted after the same review with its conflict of interest stated in the entry. What we did take: typos, ast-grep rules with tests, Dependabot `cooldown`, and the patterns in [patterns.md](patterns.md).

## Adding to this file

When a pull request rejects or replaces a tool, add a row with the reason and what would change the answer.
