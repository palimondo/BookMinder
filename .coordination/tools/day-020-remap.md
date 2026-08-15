# day-020.md line remap — pre-repair → repaired

Repair date 2026-08-15. Pre-repair blob `27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2` (56,185 lines, last changed in commit `4bd07ce`). Repaired file: 32,537 lines (transcript body ends at 32,475; editorial appendix and trailer follow).

Recovery of the exact pre-repair file: `git cat-file blob 27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2 > claude-dev-log-diary/day-020.md`

This table is the complete remap. A per-line map is mechanically derivable from it; none is committed by design.

| Pre-repair lines | Repaired lines | Rule |
|---|---|---|
| 1-31128 | 1-31128 | identity — S1, S2, and S3 refs all keep their line numbers. S3 (21810-31128) was byte-identical to the S5 prefix (45520-54838), and deleting S3+S4 moves S5's start to exactly 21810, so S3's line numbers now address the same bytes via S5. |
| 31129-45479 | — | deleted (S4, a re-render of S2). Zero refs exist in this interval. Content is byte-present in the kept body, with one exception: pre-repair line 31137, a glyph-only horizontal rule (`─` runs, no semantic content), which is dropped and recoverable only from the blob. |
| 45480-45519 | 32478-32517 | editorial appendix; repaired = pre-repair − 13002. Zero refs exist; mapping recorded for completeness. |
| 45520-56185 | 21810-32475 | repaired = pre-repair − 23710 (S5). |

## Ref migration applied

795 `day-020:LNNNN` refs exist across `.coordination`. 693 are in the identity interval and were left untouched (zero diff churn where nothing moved). 102 refs carry a number ≥45520: 71 of them live in the 8 live artifacts below and were shifted by −23710 (76 individual numbers, since some ranges have both endpoints ≥45520); the remaining 31 live in seven historical `provenance-verification-*.md` reports and were deliberately *not* migrated — rewriting them would falsify what was actually checked against the pre-repair file — so each of those files instead carries a prepended note recording the offset.

Live files migrated: `mining/v2/day-020-s5.yaml` (58 refs), `compile/disposition-pair-programming.md` (5), `compile/skill-v2-changelog-tdd-bdd.md` (3), `compile/disposition-tdd-bdd.md` (1), `compile/rule-index-pair-programming.md` (1), `compile/rule-index-tdd-bdd.md` (1), `compile/skill-v2-changelog-bookminder.md` (1), `compile/skill-v2-changelog-pair-programming.md` (1). `compile/contradiction-ledger.md` was in scope but needed no change — all three of its day-020 refs sit in the identity interval.

Ref surface forms present in the corpus, all handled by the rewriter: `day-020:LNNNN` (743), `day-020:LNNNN-LNNNN` (38), `day-020:LNNNN-NNNN` (16).
