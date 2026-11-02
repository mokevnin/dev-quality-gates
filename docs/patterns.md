# Setup patterns

Tools alone do not enforce anything. These patterns decide when they run. They come from real repositories, for example [sphericon](https://github.com/getsphericon/sphericon), which runs jactionlint, zizmor, gitleaks, typos, knip, ast-grep, commitlint and golangci-lint together. Adapt, do not copy.

## Three tiers

1. **Staged-file hook (fast).** Only checks that run in seconds on changed files: secrets on staged content, linters, formatters, spell check, commit message format.
2. **Pre-push hook (slow).** Whole-project checks: type check, full linter, dependency tidiness.
3. **CI (complete).** Everything, including checks that need the network or a database. CI is the only gate that cannot be skipped.

A hook is a convenience. A check that exists only in a hook is not enforced.

## One toolchain file

Pin the versions of all tools in one file that both developers and CI read, such as a `mise.toml` (it also installs hk and the linters hk runs). CI then runs exactly what the hook ran (`hk check --all`). Add one aggregate task (`check`) that runs every check, and call that from CI.

## Generated code gate

Regenerate generated files in CI and fail if `git status --porcelain` shows a difference. This catches hand edits and stale output.

## Tests for the rules

Test custom rules. `ast-grep test` runs rule fixtures and snapshots; keep them in the repository next to the rules.

## Custom analyzers

`golangci-lint custom` builds a golangci-lint binary with your own analyzers. Pin its version to the one used by the rest of the toolchain, and check that pin in CI.

## Exceptions

Keep suppressions narrow (path and rule, not a whole directory), and record why. Prefer a baseline over disabling a rule when adopting a check on an old code base.

## Review dates on exceptions

The reason for a suppression is often an argument that can stop being true: "this bucket is a public static host", "no SSH server uses this package". A suppressed finding reports nothing, so nothing tells you when that happens.

Give every suppression a review date and fail the build when it has passed. Some tools have this built in: OSV-Scanner's `ignoreUntil` stops ignoring a vulnerability after the date. Others do not: a Checkov inline skip (`checkov:skip=<id>:<comment>`) has no expiry, so a date written there is only a comment. For those, a short script in CI does the job:

- every suppression has a date, in one fixed format (for example `(review YYYY-MM-DD)`);
- the date is real (`2026-02-31` must fail; V8's `Date` silently reads it as 2026-03-03, so check that the parsed date prints back as the same string);
- the date has not passed;
- the reason is more than a word, because most tools accept any text, even one character.

Run that script on a schedule as well as on pull requests. A date expires on the calendar, not in a diff, so a job that runs only when the suppressed files change can miss it for a long time. Read each suppression from a fixed list of places rather than by walking the whole repository with an exclusion list: an exclusion list is how a scanner reads nothing and still passes.

Dates are for suppressions that hide a security or risk finding: a vulnerability, an infrastructure check, a path excluded from a scanner. A style setting, a word in a spelling allowlist or a host excluded from the link check does not go stale in that way; a reason in a comment is enough.

## Dependabot cooldown

A `cooldown` with `default-days` in `dependabot.yml` delays updates to freshly published versions, which reduces exposure to compromised releases. jactionlint checks this (`dependabot-cooldown`). Renovate's equivalent is `minimumReleaseAge`.

## Reporting versus enforcing

Run slow scans that depend on external data (a vulnerability database, for example) on a schedule, not on every pull request. A new advisory can fail a build without any change on your side.

## Coverage ratchet

Set a coverage floor in the config (for example `.testcoverage.yml` for go-test-coverage). Raise it when coverage rises and never lower it. The floor leaves room below the measured value, so noise does not fail builds, but a drop does.

## Immutable migrations

A migration that has shipped must not change. Check it in CI against the base branch: fail when an existing migration file is modified, and allow a documented escape (for example a marker in the pull request body). Lint added migrations for locks and downtime (squawk for PostgreSQL).

## Conventional Commits and releases

commitlint on the pushed range makes the commit format mandatory. A release tool that reads those commits (for example release-please) then builds versions and changelogs from them. The enforcement is commitlint; the release tool is only a consumer, which is why it is not on the tool list.

## Rules for AI agents

Agents follow what the repository can check. In `AGENTS.md`:

- Name generated files and say they are never edited by hand; back it with the generated-code gate and a `DO NOT EDIT` header.
- Do not disable a lint rule. An exception is narrow (path and rule), carries a reason, and needs a human decision.
- Say which command runs every check (`mise run check`), and make CI run the same one.
- Lint the instruction files themselves (agnix) so that broken configuration does not fail silently.

An instruction without a check is advice. Prefer adding the check.

## Several agents on one machine

Heavy commands (type check, full lint, test suite) started by many agents at once starve each other. Run them through a small wrapper that holds one of a few machine-wide `flock` slots, and skip the queue in CI. Do not nest the wrapper: a heavy command started inside a held slot runs at once, so tasks that call tasks cannot deadlock.
