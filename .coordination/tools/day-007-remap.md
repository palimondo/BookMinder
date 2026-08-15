# day-007.md line remap — pre-repair → repaired

Repair date 2026-08-15. Pre-repair blob `2b1776656183cce5c73dd82a7c89eed6c69eeec0` (8,127 lines; 8,126 newlines, the last line had no trailing newline). Repaired file: 6,701 lines (transcript body ends at 6,677; the editorial repair trailer follows).

Recovery of the exact pre-repair file: `git cat-file blob 2b1776656183cce5c73dd82a7c89eed6c69eeec0 > claude-dev-log-diary/day-007.md`

The file was four console pastes of one working day, each opening with a `Welcome to Claude Code!` banner box: P1 = 1-1669, P2 = 1670-3119, P3 = 3120-6213, P4 = 6214-8127. P4 opened by re-rendering the whole of P2 at a constant offset of 4544 before continuing with new material, so 6214-7663 was a duplicate rendering and was deleted. P4's tail is kept and shifts up by 1450; because P4's banner box sat inside the deleted prefix, that tail now continues directly from P3's last line without a banner of its own.

| Pre-repair lines | Repaired lines | Rule |
|---|---|---|
| 1-6213 | 1-6213 | identity (P1, P2, P3). Line 3116 alone gained the restored `> ` author-turn marker — see below — and is now byte-equal to pre-repair line 7660. |
| 6214-7663 | — | deleted (P4's re-rendering of P2). Word-for-word present in the kept body; its sole unique content is restored in place at line 3116. |
| 7664-8127 | 6214-6677 | repaired = pre-repair − 1450 (P4 tail). |

## The restored marker

The two renderings were not byte-identical — `diff` reports eight hunks over fifteen lines — but they were word-for-word identical: 8,102 versus 8,103 whitespace-collapsed tokens. Seven of the eight hunks were pure re-wrap, the same words broken at a different column. The eighth was the single differing token: pre-repair line 7660 carried the console's `> ` author-turn marker and pre-repair line 3116 did not, a defect in the earlier paste that dropped the only in-file evidence that the turn was the author's rather than the agent's.

Verified byte-for-byte before the deletion: line 7660 begins with `> `; line 7660 with those two characters removed equals line 3116 exactly; line 7661 equals line 3117 exactly. The marker was therefore restored at line 3116, which is now byte-identical to pre-repair line 7660. This is the only line in the repaired file whose bytes differ from the pre-repair capture, and P4's copy — the witness — remains permanently available at the blob above.

## Ref migration applied

132 `day-007:LNNNN` refs exist across `.coordination`. 113 are in the identity interval and were left untouched. 4 cited the marker line (`L7660`, `L7660-L7661`) and now resolve to `L3116`/`L3116-L3117`; these are exactly the citations that depend on the marker — rule `d007-R16`'s `because_source: user-verbatim` evidence, a `pairing_gems` entry, a disposition row, and one provenance record. 15 cited P4's tail and shift by −1450.

Live files migrated (16 refs, 27 individual numbers): `mining/v2/day-007.yaml` (14 refs) and `compile/disposition-pair-programming.md` (2 refs). Historical `provenance-verification-*.md` reports were annotated rather than rewritten, per the convention that they record verification acts performed against the pre-repair file: `bookminder-2` (marker ref), `pairing-1` and `tdd-bdd-3` (tail refs).

Ref surface forms present, both handled by the rewriter: `day-007:LNNNN` (61) and `day-007:LNNNN-LNNNN` (71).

## Residue deliberately left in place

Scattered smaller repetition between P2 and P3 survives — the largest is 419 tokens (~89 lines) — where the same tool output appears in both pastes rendered with relative versus absolute file paths. It is pre-existing, out of the authorized scope of this repair, and not the whole-paste structural duplication that was cut.
