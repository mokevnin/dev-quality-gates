# Mermaid diagrams in Markdown

Reviewed **2026-11-01**. Decision: **add mermaid-lint**. rumdl checks Markdown style and does not parse diagrams. A broken `mermaid` fence is a different failure, and it needs its own command.

`@mermaid-js/mermaid-cli` (`mmdc`) is the official renderer. It is not the gate. See [docs/not-adopted.md](../docs/not-adopted.md).

## Currency

Checked against the GitHub API on 2026-11-01.

[jasonworden/mermaid-lint](https://github.com/jasonworden/mermaid-lint) publishes `@mermaid-lint/cli`. The repository was created 2026-06-16, is not archived, and is MIT. It has 14 stars and 24 open issues. There are no GitHub security advisories. The latest release is [v0.53.1](https://github.com/jasonworden/mermaid-lint/releases/tag/v0.53.1), published 2026-08-13. The latest code commit is the same day: [c8884b0](https://github.com/jasonworden/mermaid-lint/commit/c8884b06c17679943eac9d4e05919f651057f431), `fix(core): explainRule() input validation via isRuleId guard`. `pushed_at` is 2026-09-11 because an open dependency-bump issue was filed, not because code landed. That is older than 30 days, so it needs a closer look, and it is not yet the 90-day freshness flag. Open issues include a false positive on math labels and a Windows path bug. Neither was reproduced here.

[mermaid-js/mermaid-cli](https://github.com/mermaid-js/mermaid-cli) v12.0.0 was published 2026-09-24. The repository was pushed 2026-10-28, is not archived, is MIT, and has about 5.1k stars. No successor was found. This is the maintained official CLI, and it renders.

Other diagram checkers turned up in a repository search and were not run: [sammcj/mermaid-check](https://github.com/sammcj/mermaid-check), [suwa-sh/md-mermaid-lint](https://github.com/suwa-sh/md-mermaid-lint), [probelabs/maid](https://github.com/probelabs/maid), [Yokozuna59/mermaid-lint](https://github.com/Yokozuna59/mermaid-lint). None is the official parser, and none is large enough to displace a tool that already calls it.

## What it enforces

`mermaid-lint` finds `mermaid` fences in Markdown and parses them with Mermaid. From `mermaid-lint --help` on 0.53.1:

| Exit | Meaning |
|---|---|
| 0 | Every diagram parsed. Warnings do not fail the run. |
| 1 | A diagram failed to parse, an error-severity rule fired, or `--strict` saw a warning. |
| 2 | Usage error, IO error, or no files matched. |

`--format json` prints a report and keeps stderr quiet. `--fix` rewrites mechanical faults in place (this run used an unclosed fence). There is no SARIF output. The package requires Node.js 22 or newer.

The command for CI is `mermaid-lint` on the Markdown paths, without `--strict` and without `--fix`. `--strict` also fails style warnings. A `graph` diagram is valid Mermaid and still warns `prefer-flowchart`; that warning must not fail a parse gate.

## Executed checks

Ran `@mermaid-lint/cli` **0.53.1** on Linux x86_64 with Node.js 24.18.0. Reproduce with:

```sh
python3 research/fixtures/mermaid/run.py /tmp/mermaid-results
```

| Case | Exit |
|---|---|
| `flowchart` with `A-->B` (`clean.md`) | 0 |
| `graph` with `A-->B` (`legacy.md`) | 0, plus a `prefer-flowchart` warning |
| same file with `--strict` | 1 |
| `graph` ending in `A--` (`broken.md`) | 1, one parse error in the JSON summary |
| Markdown with no diagram (`prose.md`) | 0 |
| path that does not exist | 2 |
| unclosed fence, then `--fix` | 0, and the file gained a closing fence |

[rumdl 0.3.0](https://github.com/rvben/rumdl) `rumdl check` on `clean.md` and `broken.md` exited 0. The broken fence is invisible to the Markdown linter.

## mermaid-cli, read but not run

`mmdc --help` from `@mermaid-js/mermaid-cli` 12.0.0 was run. The render was not: the package's Puppeteer install downloads a browser, and no Chrome was available. These points are from that help text and from `src/index.js` in the installed package, not from a failing render:

- Input ending in `.md` is treated as Markdown, and each diagram is rendered to an image. There is no check-only flag and no JSON report.
- Rendering calls `mermaid.render` inside Puppeteer. A comment in `src/index.js` says an invalid diagram throws. `error()` then prints to stderr and `process.exit(1)`. That exit was not reproduced.
- A Markdown run writes image files next to the output. That is a build step, not a lint.

## Limits

- mermaid-lint is young, small, and quiet since 2026-08-13. The open math-label and Windows-path issues were not reproduced.
- Warnings are not failures unless `--strict` is passed. Do not pass `--strict` if the only standard is "the diagram parses".
- No SARIF.
- `mmdc` remains the tool when the job is to render a diagram. It is the wrong tool when the job is to fail CI without a browser.
