# day-020.md Repair Report — execution record

Executed 2026-08-15 against `.coordination/day-020-repair-plan.md` (the adversarially reviewed design). Repo `/home/user/BookMinder`, branch `claude/bookminder-recall-5ite2s`. Remap table: `.coordination/tools/day-020-remap.md`.

Pre-repair anchors, asserted before anything ran: `claude-dev-log-diary/day-020.md` blob `27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2`, 56,185 lines, working tree clean. Recovery: `git cat-file blob 27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2 > claude-dev-log-diary/day-020.md`. Every gate below was run against that blob (`ORIG`), never against the working file.

## Deviations from the plan

One plan sentinel was wrong and is corrected here. The plan's G1/G4 assert that pre-repair line 56179 contains `/exit`; it does not — `/exit` is at pre-repair line **56178** (`grep -n '/exit'` returns `56178:> /exit`; line 56179 is `  ⎿  (no content)`). The blob hash matched exactly, so the file is byte-for-byte what the reviewer measured; the reviewer mis-transcribed the line number by one. The repaired landmark is therefore `/exit` at new line **32468** (= 56178 − 23710), not 32469. Nothing else depends on this number: the build recipe uses only the ranges 1-21809 and 45520-56185, and the plan's body-end figure (new 32475 = 56185 − 23710) is correct.

The plan's G9 second clause ("no `day-020:L` number ... in [31129,45519]" in live files) is un-satisfiable as written and was replaced by its evident intent. After deleting 23,710 lines the repaired file runs to 32,475, so new lines 31129-32475 are valid repaired content (they are pre-repair 54839-56185). A migrated ref landing there is correct, not stale. The gate actually run: no live ref exceeds the transcript body end (measured maximum across all live files: exactly 32475), and no live ref cites deleted content — proven exhaustively by G7 rather than by a numeric range test.

The plan's approximate per-interval ref counts (`S1≈225 / S2≈343`) measure as S1 218 / S2 324; both are marked approximate in the plan and neither is load-bearing. The exact counts the design rests on all reproduced: S3 151, S4 **0**, S5 102, total 795.

The plan's F6 states that range refs are written "without a second `L`". Both forms exist: `day-020:LNNNN-LNNNN` (38 occurrences) and `day-020:LNNNN-NNNN` (16). The rewriter handles both, plus the 743 single-line refs. Had it handled only one form, 38 range endpoints would have been silently missed — this is exactly the failure mode F6 warned about, one form off.

## Gate results

**G0 — preconditions.** `git diff --quiet` clean; blob = `27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2` (matches plan); 56,185 lines; validator baseline `day-020-s{1..5}.yaml: OK` ×5, exit 0.

**G1 — structure re-verification against ORIG.** `cmp <(sed -n '21810,31128p') <(sed -n '45520,54838p')` exits 0 — S3 is byte-identical to the S5 prefix. `diff <(sed -n '7206,21809p') <(sed -n '31129,45519p') | grep -E '^[0-9]'` outputs exactly `8a9`, `14353,14598c14354`, `14604a14361,14391` — the three hunks the plan predicted, nothing else. Line 1 is `claude`. Line 56178 is `> /exit ` (see deviation above).

**G2 — build.** Deterministic recipe run verbatim from the plan: `sed -n '1,21809p;45520,56185p'` of ORIG, then the appendix marker, the one-line origin note, `sed -n '45480,45519p'` of ORIG, the end-appendix marker, and the trailer. Result: 32,537 lines.

**G3 — byte-reconstruction identity (master gate).** `cmp <(sed -n '1,21809p;45520,56185p' ORIG) <(head -n 32475 new)` exits 0 — the entire kept transcript is byte-identical to the concatenation of the kept pre-repair ranges. `cmp <(sed -n '45480,45519p' ORIG) <(sed -n '32478,32517p' new)` exits 0 — the appendix window is a verbatim capture. New line 32476 is the appendix marker; new line 32518 is `════ END APPENDIX ════`.

**G4 — sentinels.** New 4986 = old 4986 byte-equal (`> <bash-input>gemini --help</bash-input>`, old-UI content intact). New 21722 = old 21722 byte-equal (inside the 49-message list only S2 renders). Linchpin three-way: new 21810 = old 21810 = old 45520, all byte-equal — the coincidence the whole identity remap rests on. New 32468 is `> /exit `. New 32475 = old 56185 byte-equal.

**G5 — ref inventory (taken before any ref was touched).** 795 `day-020:L` refs across 21 files in `.coordination` (797 including the two inside the repair plan itself, which are excluded). Refs with any endpoint in the deleted S4 interval [31129,45519]: **0**. Segment-crossing ranges: exactly one, `day-020:L14501-L21810` in `mining/v2/day-020-s3.yaml`, whose endpoint 21810 is byte-stable under the identity map. Refs with a number ≥45520: 102, distributed 58 (`day-020-s5.yaml`) + 13 (live compile files) + 31 (`provenance-verification-*.md`) — matching the plan exactly.

**G6 — migration.** Rewriter subtracted 23710 from every captured number ≥45520 in the 8 live files named in the plan (plus `contradiction-ledger.md`, in scope but unchanged — all three of its refs are in the identity interval). Result: 71 refs rewritten across 8 files, 76 individual numbers changed, 71 changed lines by `git diff --numstat` (5+1+1+1+1+1+3+58). Zero changes in identity-region refs; zero changes in any `provenance-verification-*.md`.

**G7 — per-ref positional byte-equality (the gate `validate_mining.py` structurally cannot be).** For all 795 pre-repair refs, enumerated from `HEAD`, the script asserted that ORIG at the original line range is byte-equal to the repaired file at the remapped line range. Result: **795/795 passed**, zero failures. Zero refs mapped into the appendix (as predicted). Additionally, an on-disk expectation check confirmed that all 21 ref-carrying files now hold exactly the expected values — migrated in live files, unchanged in historical ones: 21/21. This is the only check that guards `loc`/`evidence` entries carrying no quote, and it proves every citation in the corpus still addresses the exact bytes it addressed before the repair.

**G8 — validator regression.** `python .coordination/tools/validate_mining.py .coordination/mining/v2/day-020-s{1,2,3,4,5}.yaml` → 5×OK, exit 0, matching the G0 baseline. Necessary, not sufficient — per F4 this gate normalizes whitespace and glyphs and then substring-searches the whole body, so it would pass even with every loc rewritten to garbage. G7 is the migration proof; this is the regression check.

**G9 — stale scan (intent form, see deviations).** Maximum `day-020:L` number across all live files: 32475, exactly the transcript body end. No live ref points past EOF; no live ref cites deleted content. The seven historical `provenance-verification-*.md` files retain numbers above 32475 by design, and each now carries the M4 annotation recording the −23710 offset.

**M4 — historical annotation.** The plan's note line was prepended verbatim to the seven `provenance-verification-*.md` files that contain refs ≥45520: `bookminder-1`, `pairing-1`, `pairing-2`, `tdd-bdd-1`, `tdd-bdd-2`, `tdd-bdd-3`, `tdd-bdd-4`. `provenance-verification-bookminder-2.md` was deliberately not annotated: all three of its day-020 refs are in the identity interval and remain correct against the repaired file without qualification.

## Content disposition

Deleted: pre-repair 21810-31128 (S3) and 31129-45519 (S4), 23,710 lines. Everything in S3 survives byte-identically as the S5 prefix at unchanged line numbers. Everything in S4 is byte-present in the kept body except the appendix window and one line.

The one dropped line is pre-repair **31137**, a horizontal rule consisting solely of U+2500 box-drawing characters. It has no semantic content — it normalizes to empty under the validator's glyph stripping — and it is recoverable from the blob in one command. This is the entire content cost of the repair.

The appendix window (pre-repair 45480-45519, now new 32478-32517) is deliberately a superset: it is the union of the scout's estimated bound (45480-45517) and this review's diff-derived bound (45482 ∪ 45489-45519), taken as one contiguous run. A superset cannot lose content, and contiguity keeps the excerpt a verbatim capture of S4's tail rather than a curated selection. Its unique content is the expanded Task prompt and the `01:50` wall-clock reading.

## Corpus-wide duplication scan

`.coordination/tools/dupescan.py` was upgraded before this repair to shingle a whitespace-collapsed token stream rather than lines, so that a block re-emitted by the console at a different wrap width or indent level is detected rather than scored as original content. Run over all 21 `day-*.md` files, the only structural duplication it finds is day-020 (S2/S4 and S3/S5, both repaired here) and one block in day-007 (examined, **not** repaired — see below). Everything else it reports is legitimate repetition and was left alone: an agent quoting an earlier day file back into its own transcript, `Welcome to Claude Code!` banners at session restarts, re-run tool output, and compaction summaries re-displayed at a different indent.

## day-007.md — repaired under an amended design

day-007.md was first examined under the premise that lines 6396-7658 are byte-identical to 1852-3114. **That premise was false**, the cut was stopped before any edit, and the finding was escalated. The author then ruled on an amended design, executed here. Pre-repair blob `2b1776656183cce5c73dd82a7c89eed6c69eeec0` (8,127 lines; 8,126 newlines, no trailing newline on the last line). Remap table: `.coordination/tools/day-007-remap.md`.

**Measured structure.** Four console pastes, banner boxes opening at lines 2, 1670, 3120 and 6214: P1 = 1-1669, P2 = 1670-3119, P3 = 3120-6213, P4 = 6214-8127. The real duplication is P2 against P4's prefix (6214-7663) at a constant offset of 4544, 1,450 lines each — not the remembered ranges. `cmp` of the remembered ranges differs at char 11923; `diff` of the true ranges reports 8 hunks over 15 lines; the maximal byte-identical sub-run is only 2605-3115 ↔ 7149-7659 (511 lines).

**Why the plain rule could not be applied.** At token level the two renderings are word-for-word identical — 8,102 versus 8,103 whitespace-collapsed tokens — differing by exactly one inserted token: the `> ` author-turn marker present only in P4, at line 7660. Of 132 day-007 refs, all four inside the proposed delete range point at that one line, and they are precisely the refs that depend on the marker for author attribution: rule `d007-R16` carries `because_source: user-verbatim` with evidence at 7660-7661, the same line is a `pairing_gems` entry, `disposition-pair-programming.md` dispositions it, and `provenance-verification-bookminder-2.md` records the quote verified "exact @ (wrap)". A plain offset remap would have sent them to line 3116, which holds the same words *without* the marker — failing positional byte-equality on 4 of 132 refs and erasing the only in-file evidence that the turn is the author's. This is F1 of the day-020 plan in the concrete.

**Amended design (author's ruling).** Treat the missing `> ` at line 3116 as a rendering defect in the earlier paste rather than as content, restore it from P4 — the witness — and only then delete P4's duplicated prefix.

**Marker verification (blocking, run before any edit).** All four assertions pass: pre-repair line 7660 begins with `> `; line 7660 with those two characters removed equals line 3116 exactly; line 7661 equals line 3117 exactly; and `"> " + line 3116` reproduces line 7660 byte-for-byte (163 bytes → 165, delta exactly 2). Zero corpus refs cover the restoration site, so no existing citation is disturbed by the edit.

**Build and structure gates.** Kept 1-3115 verbatim; restored `> ` at 3116; kept 3117-6213 verbatim; deleted 6214-7663 (1,450 lines); kept 7664-8127 as new 6214-6677. All structure gates pass, including the strongest available statement of scope: **exactly one body line differs from what a pure delete-only build would have produced** — the restoration, and nothing else. Body 6,677 lines, file 6,701 with the trailer. Because P4's banner box sat inside the deleted prefix, the surviving tail continues directly from P3's last line without a banner; this is stated in the file's trailer.

**Ref migration.** 113 identity refs untouched; the 4 marker refs remapped 7660→3116 / 7661→3117; the 15 tail refs shifted −1450. 16 refs (27 individual numbers) rewritten across two live files, `mining/v2/day-007.yaml` and `compile/disposition-pair-programming.md`. Three historical reports annotated rather than rewritten: `provenance-verification-bookminder-2`, `-pairing-1`, `-tdd-bdd-3`. Maximum day-007 ref in live files afterwards: 6488, inside the 6,677-line body.

**G7 — per-ref positional byte-equality.** All 132 pre-repair refs, enumerated from the pre-migration commit, compared between the pre-repair blob at their original range and the repaired file at their remapped range: **132/132 pass**. For the four marker refs the comparison is old-line versus new-line *after* the restoration, and it holds byte-for-byte by construction. On-disk values as expected in 17/17 files.

**Dupescan on the repaired file.** The 8,006-token structural duplication is gone; the largest remaining day-007 region is 419 tokens. What survives is scattered P2↔P3 repetition of the same tool output rendered with relative versus absolute file paths — pre-existing, outside the authorized scope, and not whole-paste duplication. No structural duplication remains in the corpus for either repaired file.

**Validator regression.** `validate_mining.py` over the full corpus: 24/24 OK, exit 0. The day-020 gate was re-run after the day-007 migration and still reports 795/795 and 21/21, confirming no cross-contamination between the two repairs.

The line refs `day-007:L7660-L7661` appearing in this section are deliberately pre-repair citations: they name the witness line as it existed in the blob above, and resolve to line 3116-3117 in the repaired file.
