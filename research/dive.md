# Dive: image layer efficiency gates

Reviewed **2026-10-24**. Decision: **Under review**, not a recommendation. Dive fills a separate job from Dockerfile linting and vulnerability scanning, and its CI enforcement works when invoked correctly. However, maintenance, compatibility and security questions remain unresolved; the evidence does not establish eligibility for a `stable_exception`.

## Currency

- Latest release: [v0.13.1, 2025-03-29](https://github.com/wagoodman/dive/releases/tag/v0.13.1). The project is MIT-licensed and its README still describes it as beta quality.
- Latest default-branch commit: [d6c6919, 2025-05-16](https://github.com/wagoodman/dive/commit/d6c691947f8fda635c952a17ee3b7555379d58f0), a dependency update. The latest human code change found was Alex Goodman's [command refactor on 2025-04-08](https://github.com/wagoodman/dive/commit/788fcd383407818ab64ef53a70bda0bec695de8e).
- Alex Goodman published the latest release; the history also includes community contributors. The repository is not archived, but current maintainer responsiveness was not established. No official deprecation announcement or designated successor was found.
- The joschi fork was [reintegrated in March 2025](https://github.com/wagoodman/dive/pull/570); [joschi/dive](https://github.com/joschi/dive) is now archived. It is not an actively maintained replacement.

These observations came from the GitHub API for the [latest release](https://github.com/wagoodman/dive/releases/latest) and the [commit history](https://github.com/wagoodman/dive/commits/main), repository pages and [licence](https://github.com/wagoodman/dive/blob/v0.13.1/LICENSE), not release-age heuristics alone.

## What it enforces

`dive --ci IMAGE` or `CI=true dive IMAGE` skips the interactive UI and checks three configurable thresholds:

| Rule | Default | Failure condition in v0.13.1 |
|---|---|---|
| `lowestEfficiency` | `0.9` | Efficiency is below the threshold. |
| `highestWastedBytes` | `disabled` | Estimated wasted bytes exceed the threshold. |
| `highestUserWastedPercent` | `0.1` | Estimated user waste ratio exceeds the threshold. |

Equality passes. CLI flags or a `.dive-ci` YAML file configure the rules; `disabled` explicitly skips one. Success returns 0; failed thresholds and image fetch/analysis errors return 1. See the [README](https://github.com/wagoodman/dive#ci-integration), [rule implementation](https://github.com/wagoodman/dive/blob/v0.13.1/runtime/ci/rule.go) and [evaluator](https://github.com/wagoodman/dive/blob/v0.13.1/runtime/ci/evaluator.go).

This is a guardrail for files overwritten or removed across image layers. It is not a total image-size budget, a CVE scan, or an automatic image optimizer. JSON output is available; no built-in SARIF output was found. Sources include local Docker, Docker archives and Podman on Linux.

## Executed checks

Ran installed Dive **0.13.1** on macOS arm64 against generated Docker archives. The fixtures contain only known byte strings; no daemon, registry access, application image or interactive extraction is needed. Run the exact reproduction with:

```sh
python3 research/dive-ci.py
```

The fixture creates a 4,096-byte retained file and a 65,536-byte file removed by a later layer. Dive reports 65,536 wasted bytes and 5.8824% efficiency.

| Case | Observed exit code |
|---|---|
| Clean image, minimum efficiency 0.95 and maximum waste 20KB | 0 |
| Waste fixture, same thresholds | 1 |
| Waste fixture, minimum efficiency 0 and maximum waste 100KB | 0 |
| Waste fixture, maximum waste exactly 65,536 bytes; other rules disabled | 0 |
| Waste fixture, user waste ratio maximum 0.1; other rules disabled | 1 |
| Waste fixture, failing thresholds plus `--json report.json` | **0: CI rules bypassed** |
| Missing image archive | 1 |

The fixture's second layer has no file payload, so the user waste ratio is infinite; it checks rejection, not realistic calibration. The clean single-layer image has an undefined user ratio, so that rule is explicitly disabled in the other cases. The JSON report was parsed and its `inefficientBytes` checked. These small fixtures establish exit behavior, not performance or compatibility with every image format.

## Integration limits

1. **JSON bypasses CI evaluation.** In v0.13.1, [runtime/run.go](https://github.com/wagoodman/dive/blob/v0.13.1/runtime/run.go) exports JSON and returns before reaching the CI evaluator. This was reproduced above. Run enforcement and JSON export separately; `CI=true` does not make a JSON-export invocation a gate.
2. **A missing CI configuration silently selects defaults.** [cmd/ci.go](https://github.com/wagoodman/dive/blob/v0.13.1/cmd/ci.go) does this even for an explicitly named missing `--ci-config` file. Check that the policy file exists before invoking Dive. Omitting a rule retains its default; use `disabled` to skip it. An explicit general `--config` read/parse error can also exit 0 in [cmd/root.go](https://github.com/wagoodman/dive/blob/v0.13.1/cmd/root.go); that error path was read, not executed here.
3. **Waste is a heuristic.** [image.go](https://github.com/wagoodman/dive/blob/v0.13.1/dive/image/image.go) and [efficiency.go](https://github.com/wagoodman/dive/blob/v0.13.1/dive/filetree/efficiency.go) use different calculations for waste and efficiency. Repeated paths can count all copies, not just reclaimable copies. The user ratio excludes the first layer, not every layer inherited from the base image. Calibrate thresholds on the actual image; do not promise an exact reduction in registry bytes.
4. **Analysis has a cost.** Dive reads layer archives and builds file metadata. Time and memory depend on image contents. No representative speed, peak-memory or alternatives benchmark was run, so no performance advantage is claimed.

For an existing installation, a policy invocation can use:

```sh
test -f .dive-ci
dive --ci --ci-config .dive-ci --source docker-archive image.tar
```

Propagate the first command's failure in the surrounding CI step (for example, use a shell with `set -e`). Export JSON in a separate invocation after the gate. Archive mode removes the need to grant the analyzer Docker socket access; it does not establish that arbitrary untrusted archives are safe.

## Open reports

These are unresolved upstream reports, not independently reproduced vulnerabilities or general compatibility verdicts:

- [#722](https://github.com/wagoodman/dive/issues/722): path traversal in interactive file extraction, reported 2026-09-24. The report describes arbitrary file writes when the user extracts from a malicious image. The [extraction implementation](https://github.com/wagoodman/dive/blob/v0.13.1/dive/image/docker/image_archive.go) uses a prefix check before filesystem writes. The CI fixture does not invoke interactive extraction; no exploit was run.
- [#718](https://github.com/wagoodman/dive/issues/718): missing blobs with Docker 28.4 images, reported 2026-08-25. Test the exact Docker/archive format used by your pipeline.
- [#684](https://github.com/wagoodman/dive/issues/684): apparent waste overcounting relative to efficiency, reported 2026-02-22. This reinforces the accounting limitation above.
- [#606](https://github.com/wagoodman/dive/issues/606): commenting out the user-waste rule leaves its default enabled. Explicitly disable rules instead.

## Alternatives and overlap

The alternatives below were compared through official documentation and source, not executed side by side. No speed ranking is justified.

| Tool | Coverage, integration and configuration | Comparison with Dive |
|---|---|---|
| [SlimToolkit](https://github.com/slimtoolkit/slim#basic-usage-info) `xray` / `lint` | Layer/file inspection and JSON reports; Apache-2.0. Latest release found: [1.40.11, 2024-02-02](https://github.com/slimtoolkit/slim/releases/tag/1.40.11). The toolkit also provides image minification. | No documented built-in equivalent of Dive's three waste thresholds was found. A custom report-policy wrapper would be needed. Minification is a different job. It is not demonstrably fresher by release date. |
| [container-diff](https://github.com/GoogleContainerTools/container-diff) | Filesystem/package/size/history analysis and image comparison with JSON; Apache-2.0. Archived; its README points to diffoci. | Not a maintained replacement for a new waste gate. |
| [diffoci](https://github.com/reproducible-containers/diffoci) | Docker/OCI image comparison for reproducibility; supports registry and local engines; Apache-2.0, not archived, activity through 2026-10-19. | A useful different guardrail: differences between two images, rather than waste within one image's layers. |
| [docker image history](https://docs.docker.com/reference/cli/docker/image/history/) | Built-in layer history and sizes, with machine-readable formatting. | Does not calculate overwritten/deleted-file waste or enforce waste limits; needs custom analysis and policy. |
| [docker buildx du](https://docs.docker.com/reference/cli/docker/buildx/du/) | Builder cache disk usage and structured output. | Measures the builder cache, not the production image's layer efficiency. |
| [Hadolint](https://github.com/hadolint/hadolint) | Existing recommendation for Dockerfile rules. | Complementary: it cannot inspect actual image layers to calculate waste. |
| [Trivy](https://trivy.dev/docs/latest/scanner/misconfiguration/), [Grype](https://github.com/anchore/grype), [Docker Scout](https://docs.docker.com/scout/) | Vulnerabilities and, for some tools, infrastructure configuration checks. | Complementary security jobs. They do not replace a layer-efficiency budget. |

## What would change the decision

- An upstream release or maintained successor addresses the reported extraction risk and current Docker/archive compatibility.
- CI policy enforcement cannot silently be bypassed by JSON export, or a documented and tested integration isolates the two modes and checks policy loading.
- Representative image fixtures validate waste accounting and compatibility, with enough maintenance activity to support adoption.

Then add a scoped recommendation through `tools.json` and regenerate README. Until then, record the evidence under **Under review**; there is no registry entry or stability exception in this change.
