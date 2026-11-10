# Mutation testing: StrykerJS

Reviewed **2026-11-10**. Decision: **add StrykerJS** under JavaScript and TypeScript, run on the files a pull request changed. That run fails a weak test that diff-cover passes at 100%. A whole-project run, incremental or not, lets the same test through. On a real project ([unjs/ufo](https://github.com/unjs/ufo)), mutating one changed file took 6 to 11 seconds.

Earlier notes ([cross-cutting](cross-cutting.md), [ecosystem gaps](ecosystem-gaps.md)) left mutation testing out as "slow, run on a schedule". That was read, not run. This page replaces it for JavaScript and TypeScript.

## The gap

[diff-cover](https://github.com/Bachmann1234/diff_cover) checks that the changed lines ran under test. It does not check that a test would fail if the code were wrong. Vitest's `expect.requireAssertions` closes part of that gap: a test with no assertion fails (ran on 5.0.5: `expected any number of assertion, but got none`). A test with a weak assertion, for example `toBeTypeOf("number")`, still passes both checks. Mutation testing is the check that catches it: Stryker changes the code and expects a test to fail.

## Currency

Checked against the GitHub and npm APIs on 2026-11-10.

[stryker-mutator/stryker-js](https://github.com/stryker-mutator/stryker-js) was created 2016-02-12. It is Apache-2.0 and not archived, with 3352 stars and 136 open issues. 11 issues are open with the `🐛 Bug` label and none with `💥 Crash`. There are no published security advisories. The latest release is [v10.1.1](https://github.com/stryker-mutator/stryker-js/releases/tag/v10.1.1), published 2026-10-23 by `Andreas02-dev`. The latest human commit is the same release. The commit before it is a vitest-runner fix, [cf5695e88f](https://github.com/stryker-mutator/stryker-js/commit/cf5695e88fac6063dc0fc172f4443fa513cd85f0): it reports mutant collection failures instead of surviving mutants. Renovate pushed after that. `nicojs` is the main human contributor. Over 2026-10-11 to 2026-11-09, npm counted 19.8 million downloads for `@stryker-mutator/core` and 14.2 million for `@stryker-mutator/vitest-runner`.

Alternatives: an npm search for "mutation testing" returned Stryker packages, Stryker's report libraries and unrelated tools. No maintained JavaScript mutation tester other than Stryker was found. [Stryker.NET](https://github.com/stryker-mutator/stryker-net) (5.0.0, 2026-09-11, 2.1k stars) and [stryker4s](https://github.com/stryker-mutator/stryker4s) (v1.1.1, 2026-07-30, 217 stars) are separate tools with their own CLIs. Neither was run.

## Executed checks

Ran StrykerJS **10.1.1** with `@stryker-mutator/vitest-runner` 10.1.1, vitest 5.0.5 and diff-cover 11.0.1. The machine was macOS 27.0.1 on an Apple M4 with Node.js 26.13.0. Reproduce with:

```sh
python3 research/fixtures/stryker/run.py /tmp/stryker-results
```

The base commit is [`app/`](fixtures/stryker/app/) plus 30 generated copies of `price.js`, each with a test that asserts results and the thrown error class. The config sets `thresholds.break: 80`. The pull request adds [`discount.js`](fixtures/stryker/pr/discount.js) with either [`weak.test.js`](fixtures/stryker/pr/weak.test.js), which asserts only the return type, or [`strong.test.js`](fixtures/stryker/pr/strong.test.js), which asserts values. The changed files come from `git diff --name-only --diff-filter=AM main...HEAD -- src/`.

| Case | Command | Exit | Score | Time |
|---|---|---|---|---|
| Base, whole project | `stryker run` | 0 | 87.5 (217 of 248) | 4.9 s |
| Weak test, coverage | `vitest run --coverage` | 0 | 100% of lines | 0.8 s |
| Weak test, diff-cover | `diff-cover coverage/cobertura-coverage.xml --compare-branch=main --fail-under=100` | 0 | `src/discount.js (100%)` | 0.1 s |
| Weak test, whole project | `stryker run` | 0 | 84.5 (218 of 258) | 4.9 s |
| Weak test, incremental | `stryker run --incremental` after a base run | 0 | 84.5; 248 of 258 results reused | 2.4 s |
| Weak test, changed files | `stryker run --mutate src/discount.js` | **1** | 10.0 (1 of 10) | 1.3 s |
| Strong test, changed files | `stryker run --mutate src/discount.js` | 0 | 90.0 (9 of 10) | 1.3 s |
| One file, whole | `stryker run --mutate src/price.js` | 0 | 87.5 (7 of 8) | 1.3 s |
| One file, line range | `stryker run --mutate src/price.js:5-5` | 0 | 100 (1 of 1) | 1.1 s |
| Pattern that matches nothing | `stryker run --mutate src/missing.js` | 1 | none | 1.1 s |

What the runs show:

- **The gate is the changed-files run.** Below the break threshold, Stryker logs `Final mutation score 10.00 under breaking threshold 80, setting exit code to 1`. The whole-project score dilutes the new file: 9 of its 10 mutants survived and the run still exited 0. `--incremental` makes the whole-project run faster by reusing earlier results. It does not change the score, so it does not make that run a pull request gate.
- **100 is not reachable in general.** The strong test leaves one survivor, `total <= 0` mutated to `total < 0`. It is equivalent: both return 0 for a total of 0. Set the break threshold below 100.
- **A range scores only itself.** `src/price.js:5-5` counted the single mutant on line 5 and left out the surviving error-message mutant on line 3. That makes a changed-lines gate possible on a legacy file whose old tests are weak. With only a few mutants in the range, the score moves in large steps. Turning diff hunks into ranges needs a script, which was not written here.
- **An empty selection is an error.** `src/missing.js` ran with the vitest runner's default related-tests mode, logged `No tests were executed`, and exited 1. A CI step has to skip Stryker when the pull request changes no source file. Other runners and an empty `mutate` list were not tried.

The times above are mostly startup. The functions have six lines and the tests take milliseconds, so they say nothing about cost on a real project.

## Cost on a real project

Ran on 2026-11-10 on the same machine, with ufo's own vitest 4.1.5. Reproduce with:

```sh
python3 research/fixtures/stryker/real.py /tmp/stryker-real
```

[`real.py`](fixtures/stryker/real.py) clones [unjs/ufo](https://github.com/unjs/ufo) at v1.6.4 (`f06c800d0c`) and installs it with lifecycle scripts disabled. It times the plain suite, then mutates one source file at a time, as a pull request that touched that file would. Stryker set `thresholds.break: 80` from a config file, because thresholds have no CLI flag. ufo's tests import `../src`, not single modules, so related-tests mode cannot narrow the tests much. That is closer to the worst case than a project whose tests import the module they test.

| Run | Lines | Mutants | Score | Covering tests per mutant | Exit | Time |
|---|---|---|---|---|---|---|
| `vitest run`, 489 tests | | | | | 0 | 1.0 s |
| `stryker run --mutate src/parse.ts` | 229 | 150 (129 killed, 6 survived, 15 no coverage) | 86.0 | 75.1 | 0 | 5.8 s |
| `stryker run --mutate src/utils.ts` | 775 | 470 (397 killed, 60 survived, 13 no coverage) | 84.5 | 18.1 | 0 | 11.3 s |

Stryker ran 9 test-runner processes on the 10-core M4. CI runners usually have fewer cores, so expect longer times there. Both files scored above 80, so the gate passed. ufo's tests take about 54 ms in vitest's own timing. A suite whose tests are slower per test (DOM, network mocks, a database) multiplies these times by roughly that ratio. That case was not measured.

In this pnpm project the config had to name the runner plugin. Without `"plugins": ["@stryker-mutator/vitest-runner"]`, the run exited 1 with `Cannot find TestRunner plugin "vitest". In fact, no TestRunner plugins were loaded`, although the package was installed with `pnpm add -D`. With that line it ran. The npm-installed fixture did not need it.

## Read, not run

- `--mutate` also accepts columns, `file:startLine:startColumn-endLine:endColumn` (from `stryker run --help`). Only line ranges were run.
- Stryker.NET `--since` and stryker4s were not checked.

## Limits

- The gate depends on a CI step that computes the changed files and skips Stryker when there are none. The step in [patterns](../docs/patterns.md#mutation-testing-on-changed-files) was run against this fixture: it listed nested files, left out `*.test.*`, `*.spec.*` and `*.d.ts`, exited 0 on an empty list, and failed with exit 128 on a missing base ref.
- A whole-file `--mutate` on an old file brings in that file's existing survivors. Use ranges, or accept that touching a weakly tested file fails the pull request.
- Mutating one widely imported module runs every related test for each mutant. Cost grows with mutants times related tests, not with the size of the diff.
- Equivalent mutants lower the maximum score.
- In the ufo pnpm install the runner had to be named in `plugins`. Other pnpm setups were not tried.
- A pull request that changes only tests has no changed source file, so it skips the gate. Only the scheduled whole-project run catches a weakened test for unchanged code.
- Cost was measured on a library with millisecond tests. Slow tests make each mutant slower in proportion.

## Decision

Add StrykerJS to JavaScript and TypeScript. The gate is a CI step that lists the source files changed against the base branch, skips Stryker when the list is empty, and otherwise runs `stryker run --mutate <files>` with `thresholds.break` set below 100. A whole-project or `--incremental` run is a report, not the gate. The other ecosystems' tools (Stryker.NET, cargo-mutants, PIT, mutmut, Infection) stay under review. Each needs its own changed-files run before a pick.
