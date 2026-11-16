# Soda: cross-consumer object-design checks

Reviewed 2026-11-16. Proposal: add Soda as a narrow companion for repeated owner-state decisions, while keeping Mago as the PHP toolchain recommendation. Disclosure: the contributor maintains Soda.

## Currency and sources

[Soda 1.4.0](https://github.com/cosmira/soda/releases/tag/v1.4.0) was released on 2026-11-16. The [release commit](https://github.com/cosmira/soda/commit/fa549a0d3d5d3467b4fbe78f5ea27ef61807bb7f) adds module boundaries and keeps shared analysis outside rule categories. The repository is not archived, had no open issues at review, and has no announced successor or deprecation; no comprehensive fork audit was performed. Maintenance is led by tabuna, with a contribution from ajlekseyn-coder. [Repository](https://github.com/cosmira/soda), [contributors](https://github.com/cosmira/soda/graphs/contributors), [open issues](https://github.com/cosmira/soda/issues).

## Focused execution

Ran Soda 1.4.0 with PHP 8.5.11 on macOS arm64. Only `RepeatedForeignStateDecision` was enabled; generated PHP was analyzed, not executed. The [runner](fixtures/soda/run.py) checks both the exit code and JSON diagnostic identity:

| Input | Exit | JSON violations |
|---|---|---|
| Three functions repeat the same compound predicate over public state of a local `Post` | 1 | `repeated_foreign_state_decision` |
| The same consumers call a predicate on `Post` instead | 0 | None |

With a Soda 1.4.0 checkout and its Composer dependencies installed:

```sh
python3 research/fixtures/soda/run.py --soda /path/to/soda/soda
```

This proves a narrow executable gate, not that every repeated predicate warrants a refactor. Its [documented analysis](https://github.com/cosmira/soda/blob/v1.4.0/docs/rules/repeated_foreign_state_decision.md) requires several distinct consumers and an uncomposed local owner with direct public fields or proven getters; dynamic, external, or ambiguous state is excluded.

## Alternatives and overlap

The following comparison is documentation-based; Mago and PHPMD were not executed here, and no speed benchmark was run.

| Tool | Scope and integration | Relation to this proposal |
|---|---|---|
| [Mago 1.60.2](https://github.com/carthage-software/mago/releases/tag/1.60.2) | Rust binary with lint, format, type analysis, and TOML-configured [dependency and structural guards](https://github.com/carthage-software/mago/blob/1.60.2/docs/content/en/tools/guard/overview.md) | Keep it for the general PHP toolchain. Soda's metrics, boundary checks, and ordinary lint rules overlap; this proposal selects a cross-consumer owner-state check rather than duplicating those jobs. No exhaustive rule-parity claim is made. |
| [PHPMD](phpmd-mago.md) | PHP runner with configurable metric budgets and design rules | Already researched here for additional numeric budgets. This proposal concerns the same predicate repeated across consumers, rather than another complexity or LOC threshold. |
| [Soda](https://github.com/cosmira/soda/blob/v1.4.0/docs/SODA_PHP_CONFIG.md) | PHP 8.2 and Composer; PHP rule objects select checks; non-zero exit and machine-readable reports | The demonstrated check identifies one owner-state decision spread across consumers. No formatting, type-checker replacement, or automatic refactoring is proposed. |

## Decision

Add Soda only for teams that want these object-design policies enforced. Select the required design rules explicitly and keep Mago for its existing job. Soda findings are policy heuristics, not proof of a behavioral defect; this run does not establish broad superiority over Mago or PHPMD.
