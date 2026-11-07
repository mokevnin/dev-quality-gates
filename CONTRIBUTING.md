# Contributing

Thank you for helping. Please read this before opening a pull request.

**A new tool is not accepted because it is good. It must fill a gap, or show a compelling advantage over the current recommendation.** Most good tools will not be added, and that is the point of the list.

## What we accept

- A tool for a **missing category** (see [Under review](README.md#under-review)).
- A **replacement** for a current recommendation, with a written comparison.
- A fix for **outdated information**: a deprecated tool, a moved repository, a changed licence.
- **Removal** of an unmaintained tool.
- Better [selection criteria](#selection-criteria) or docs.
- A clarification of an existing entry: limits, conditions, overlap.

## What we reject

- Another alternative for a job that already has a recommendation, without a comparison.
- Tools that only advise and cannot fail a build.
- Tools with no public repository or documentation.
- Promotion of your own tool without the same evidence we would ask of anyone else.
- Bulk additions. One tool or one change per pull request.

## Requirements for a pull request

The [pull request template](.github/PULL_REQUEST_TEMPLATE.md) mirrors this list. Every point needs an answer in the description.

1. **Enforcement.** The tool automatically checks a development standard. Say which one.
2. **Public source.** There is an official public repository and documentation.
3. **Currency check.** Record the last release, recent meaningful commits, maintainer activity, archived or deprecated status, known successors or forks, and open critical issues. Activity older than 30 days is a reason to look closer, not an automatic rejection; stable tools can be exceptions if you say why. Once a tool is listed, the scheduled freshness check flags it after 90 days without a push. There is no minimum project age: a new tool or fork can beat an old one.
4. **Alternatives.** Name the main current alternatives and compare features, rule coverage, speed, integration and configuration.
5. **Overlap.** Say what it overlaps with among already recommended tools. If it replaces several checks, say which ones. Do not recommend two tools that mostly do the same thing.
6. **Why this one.** Explain why it should be added or should replace the current recommendation.
7. **Limits.** State the significant limitations and conditions of use.
8. **Style.** Follow the README format below and update `tools.json`.

## Research and docs pull requests

Most changes here are not new tools but research (`research/`), patterns (`docs/patterns.md`) and rejections (`docs/not-adopted.md`). They are reviewed on three points:

1. **Run or read.** Say which claims you ran (tool version, date, the command) and which you only read in documentation. A claim you ran outranks one you read.
2. **Sources.** A version, date, star count or licence links to its source or to the run that produced it.
3. **Conclusion.** The change ends in a decision: add, reject, or keep under review, with the reason.

A fixture that backs a claim goes in `research/fixtures/<topic>/` with a `run.py` that reproduces it.

## Review and merge

- `mise run check` must pass; CI runs the same set. The first pull request from a new contributor needs a maintainer to approve the workflow run before CI starts.
- Pull requests are squash-merged, one tool or topic each, so the title becomes the commit message: write it as a short sentence.
- A maintainer may push small fixes (typos, wording, formatting) to your branch instead of asking for another round.

## Local checks

This repository uses its own recommendations: [mise](https://mise.jdx.dev/) pins the tools and [hk](https://hk.jdx.dev/) runs the checks.

```sh
mise install
mise run setup   # pnpm install and the git hooks
mise run check   # every check, the same set CI runs
mise run fix     # apply automatic fixes
```

## Selection criteria

A tool is better when it:

- runs from the CLI, non-interactively, and exits non-zero on violations;
- works in CI and gives clear diagnostics;
- has machine-readable output (JSON, SARIF);
- can fix problems automatically where that is safe;
- allows custom rules;
- is fast and cheap to run;
- covers more checks than the tool it competes with;
- is a fast native binary (often Rust) that does lint, format and analysis together, when one exists for the ecosystem. A newer all-in-one tool that is pre-1.0 can still beat an older stack of narrow tools; say what is immature about it in `limitations`.

Not every point is required, but they decide close calls. Automated signals (a new release, no recent commits) are inputs, not verdicts. They do not replace a comparison.

## Entry format

The README list is **generated from `tools.json`**. Do not edit the entries in `README.md` by hand. Add or change a record, then run `pnpm install && pnpm run readme`.

| Field | Meaning |
|---|---|
| `id`, `name`, `repo` | Slug, display name, `owner/repo` on GitHub. |
| `category` | The README heading. A new one must also be added to `CATEGORY_ORDER` in `scripts/readme.ts`. |
| `last_reviewed` | Date (`YYYY-MM-DD`) you did the currency check. |
| `sources` | URLs or repository paths used for the decision. |
| `rationale` | One or two sentences: what the tool does. No versions, star counts, download numbers or maintenance notes; those belong in `limitations` or `research/`. Shown in the README. |
| `limitations` | What it does not do, in a sentence or two. Kept in `tools.json`, not shown in the README. |
| `details` | Optional path of a longer comparison in `research/`. |
| `stable_exception` | Optional `true` for a finished or slow-moving tool with old releases; mutes the push-age and release-age flags, not the review-date flag. Explain it in `limitations`. |

Say in `rationale` or `limitations` what you ran and what you only read: a tool you tested is stronger evidence than one described by its README. Longer comparisons go in `research/<topic>.md`.

`pnpm run check:registry` validates `tools.json` against `tools.schema.json` and fails if `README.md` is out of date. Scripts are TypeScript (`scripts/`), run directly by Node 24 and checked with `pnpm run typecheck`.

## Checks

The `Lint` workflow runs rumdl, lychee, typos, jactionlint on this repository's own workflows, and the registry check. Run them locally before you push. Pin every action in this repository to a full commit SHA with a version comment.

Dependabot pull requests merge themselves: the `Dependabot auto-merge` workflow turns on auto-merge, and GitHub squashes the pull request once the required `check` job passes. A failing check leaves it open for a human.

## Removing or replacing a tool

Open a pull request that edits the entry and `tools.json`. For a removal, link the evidence (archived repository, announced end of life, unfixed critical issue). For a replacement, include the comparison required above, and say what a user of the old tool has to change. Add a row to [docs/not-adopted.md](docs/not-adopted.md) for the tool that was rejected or replaced.

## Conduct

Be kind and be specific. Disagree with the evidence, not the person.
