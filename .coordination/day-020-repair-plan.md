# day-020.md Repair Plan — Adversarial Review and Final Design

Reviewer: independent adversarial pass, 2026-08-15. Repo `/home/user/BookMinder`, branch `claude/bookminder-recall-5ite2s`.
Pre-repair anchors (verified): HEAD `62b039cec12049e200b850bbac78910081aaff64`; `claude-dev-log-diary/day-020.md` blob `27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2` (last changed in `4bd07ce`); 56,185 lines.
Recovery at any time: `git cat-file blob 27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2 > claude-dev-log-diary/day-020.md`.

Every load-bearing claim below marked [verified] was re-measured in this review with the command shown or named; scout claims I could not cheaply re-derive are marked [scout] and the design is constructed so that none of them is load-bearing.

## 1. Attack findings — what I rejected in the plan under review, and why

### F1. The wrap-insensitive shingle reconstruction engine (Phase 1) is rejected: overbuilt and actively dangerous

The measured structure of the corruption is block-level, not shingle-level: S3 (L21810-31128) is byte-identical to the S5 prefix (L45520-54838) [verified: `cmp` of the two `sed -n` extracts, zero differing bytes], and S4 differs from S2 by exactly 3 diff hunks [verified: `diff` of extracts reports hunks `8a9`, `14353,14598c14354`, `14604a14361,14391`, nothing else]. A general normalization-driven dedup engine solves a harder problem than exists, and its failure mode is catastrophic: the corpus contains compaction summaries that silently spell-correct quoted author turns ("possitions" → "positions"), so a wrap/spelling-insensitive normalizer can classify the summary as a duplicate of the raw turns and delete the only lines that verbatim-back the summary-sourced `quote:` fields. Fixed line-range extraction plus a byte-identity gate is strictly stronger, auditable in one line, and cannot false-merge. "Keep most complete rendering per region" at sub-segment granularity would also interleave renderings into a body no honest label can describe.

### F2. The splice (S4's unique lines into S2's body) is rejected: it forges a console state, and the evidence shows it buys nothing

A spliced S2 would be an edited artifact presented in the position of a verbatim paste — the worst provenance outcome: the file's body would no longer be a capture of any console state that ever existed, and every future consumer inherits that doubt. The measurements make the splice unnecessary anyway: S4's content not byte-present in the kept body is bounded [verified, via the S2-vs-S4 diff] to old L45482 ∪ L45489-45519 (one-line compaction banner variant; author-turn context; `01:50` wall-clock; the expanded Task prompt) plus old L31137, which is a glyph-only horizontal-rule line with zero semantic content (it even normalizes to empty under the validator's glyph stripping) [verified: printed S2/S4/S5 banner regions side by side]. And exactly zero of the 795 corpus refs point anywhere into S4 (L31129-45519), including range endpoints [verified: interval scan over every extracted ref]. A clearly-labeled end-of-file appendix carrying the S4 variant window verbatim achieves zero content loss with zero edits inside any verbatim region.

Adjudication of the alternatives the author asked about:
- Keep-4-segments (S1+S2+S4+S5 with labels): rejected. Retains 14,351 lines of near-duplicate (S4≈S2), defeating the "clean transcript" goal, and buys nothing — S4 holds zero refs and only ~40 lines of variant content.
- S1+S2+S5 at 99.7%, discard the 38 lines: rejected. Violates zero content loss (the expanded Task prompt and the `01:50` timestamp exist nowhere else) to save ~15 lines of appendix markers. False economy.
- No-file-surgery (annotate + rely on downstream dedup): the steelman is real — locs were evidently already canonicalized downstream (shard s4's YAML has 112 day-020 mentions yet zero locs land in the S4 interval [verified]), so nothing is currently broken. But the 23,710 redundant lines re-tax every future consumer: every new mining pass, grep, or human reader must re-derive the segment map or re-mine duplicates, and the file misrepresents the session as ~5x its length. Because the chosen repair is delete-only and byte-provable against a git-pinned blob, source repair carries essentially the same risk as no-surgery while removing the recurring cost. Source repair wins — but only in its delete-only form; any editing form would flip this adjudication.

### F3. Per-line remap machinery is rejected: the measured ref topology needs a 3-row interval table

The structure hands us an accident of arithmetic that the plan under review never noticed: deleting S3+S4 (23,710 lines) makes new-S5 start at exactly L21810 — precisely where S3 started — and S3 is byte-identical to S5's prefix. Therefore the identity map holds byte-for-byte for every old line ≤31128: all S1 refs, all S2 refs, and all 151 S3 refs point at unchanged line numbers with unchanged content. S4 has zero refs. Only the 102 refs with lines ≥45520 move, all by the single constant −23710. [verified: 795 refs total, per-interval counts S1≈225 / S2≈343 / S3:151 / S4:0 / S5:102; the only segment-crossing range is `day-020:L14501-21810`, whose endpoint L21810 is byte-stable under the identity map.] A 56k-row per-line map is unauditable by eye and adds a generation step that can itself be wrong; the interval table below is the entire remap and a human can check it in ten seconds. (A per-line map remains mechanically derivable from the table if any future tool wants one — derive, don't commit.)

### F4. `validate_mining.py` as "mechanical proof" of migration is rejected: it is structurally incapable of catching a wrong loc

[verified by reading `.coordination/tools/validate_mining.py` in full] The quote gate normalizes away ALL whitespace and box glyphs and then does a whole-body substring search; the `loc` field is checked for format only and never used positionally. The gate therefore passes even if every single loc were rewritten to garbage line numbers, as long as the quoted text exists somewhere in the file — which a delete-only repair guarantees. Re-running it after migration is a necessary regression check (and the baseline matters: pre-repair it reports 5/5 shards OK, exit 0 [verified by running it]), but presenting it as proof of migration correctness is exactly the false confidence the author feared. The actual proof is gate G7 below: per-ref positional byte-equality between the new file and the pre-repair blob at the original loc — a check the reviewed plan lacked entirely, and the only check that guards `loc`/`evidence` fields that carry no quote.

### F5. Phase 2(b) "dedup re-run reports zero internal duplication" is rejected: the gate is un-passable as written

Legitimate internal repetition survives in a correct repair: compaction summaries verbatim-quote author turns (S2's 49-message list restates 49 real turns), commands repeat, and S1/S2/S5 are overlapping renderings of one session — S2 and S5 each re-render from the session start [verified: S2 and S5 both open with the Welcome banner and `/hi is running`]. A zero-duplication gate either fails forever or pressures a worker into deleting legitimate content to satisfy it. It is replaced by G3 (byte-reconstruction identity), which proves exactly what was removed and that nothing else changed — a stronger claim than any dedup statistic.

### F6. Under-protections in the reviewed plan (fixed in the design)

- No pinned pre-repair blob SHA; "git history preserves it" was asserted, never anchored. Fixed: blob SHA in this plan, the file trailer, the report, and both commit messages; G0 asserts it before anything runs.
- Ref formats never enumerated. Reality [verified]: all 795 refs are absolute `day-020:LNNNN` or `day-020:LNNNN-NNNN` (range form without a second `L`); the `day-020-sN:LNNNN` shard-relative form the validator tolerates is unused; the mining `.js` tools build locs programmatically and contain no literal ones; no locs exist outside `.coordination` (day-021.md and gemini-summary-day-020-021.md mention day-020 without line numbers [verified]). A rewriter that only handles `L\d+` would silently miss range endpoints.
- No validator baseline before repair, so any post-repair failure would be unattributable. Fixed: baseline recorded (5/5 OK).
- "Header notes in day-020.md" — a note at the TOP of the file would shift every line and destroy the identity map for the 693 untouched refs. All annotation goes at the END of the file.
- Scout's "unique holder" claims are rendering-form claims, not content claims: the model-switch facts S1 holds as `<local-command-stdout>Set model to …` also exist in S2/S3 as `⎿ Set model to …` lines [verified: grep shows both forms], and the "for the record, show me the full summary" author turn attributed to the S4-unique window also exists in S5 at old L54832 [verified]. Harmless here because S1 and S5 are kept wholesale — but it confirms shingle-level uniqueness claims must never drive deletion decisions (F1).

### F7. Retained from the reviewed plan (credit where due)

Historical `provenance-verification-*.md` reports stay unmigrated with a one-line annotation — correct: they record verification acts performed against the pre-repair file, and rewriting their locs would falsify what was actually checked. Also retained: `duplicate_of:` mining annotations are marked, never deleted; shard ids (`d020s1…`) stay stable; the repair commit documents method and pre-repair SHA; repair and migration are separate commits.

## 2. Chosen design: delete-only repair with labeled appendix

No line inside any kept region is edited, moved, or rewrapped. The repair deletes two contiguous duplicate blocks and appends clearly-labeled editorial material after the transcript ends. The result is honestly describable in one sentence: "the original hand-assembled paste sequence, minus two proven-duplicate pastes, with the sole 40-line variant window preserved in a marked appendix."

New file layout (all numbers exact and gate-checked):

| New lines | Content | Source (pre-repair blob 27a5ad7) |
|---|---|---|
| 1-21809 | S1+S2 verbatim (identity) | old 1-21809 |
| 21810-32475 | S5 verbatim | old 45520-56185 (offset −23710) |
| 32476 | `════ EDITORIAL APPENDIX — NOT CONSOLE OUTPUT (added by repair 2026-08-15) ════` | — |
| 32477 | one-line origin note (see build recipe) | — |
| 32478-32517 | S4 variant window verbatim (40 lines) | old 45480-45519 |
| 32518 | `════ END APPENDIX ════` | — |
| 32519-end | repair trailer: method, blob SHA, rederivation command, remap table | — |

Deleted: old 21810-31128 (S3, byte-identical to kept S5 prefix) and old 31129-45519 (S4, byte-covered by kept body except the appendix window and the glyph-only rule at old 31137, which is documented in the report and dropped). The appendix window 45480-45519 is deliberately the union of the scout's estimate (45480-45517) and this review's diff-derived bound (45482 ∪ 45489-45519), taken as one contiguous run — a superset cannot lose content, and contiguity keeps the excerpt a verbatim capture of S4's tail rather than a curated selection. Session landmarks after repair: `/exit` at new L32469 (= 56179 − 23710); transcript body ends at new L32475.

Remap (complete — this table IS the remap, committed as part of the report):

| Old lines | New lines | Rule |
|---|---|---|
| 1-31128 | 1-31128 | identity (S1, S2, and S3 refs — S3 content survives byte-identically via the S5 prefix at the same line numbers) |
| 31129-45479 | — (no refs exist) | content byte-present in kept body; report documents old 31137 exception |
| 45480-45519 | 32478-32517 | appendix, new = old − 13002; no refs exist, mapping recorded for completeness |
| 45520-56185 | 21810-32475 | new = old − 23710 |

Ref migration: rewrite only refs ≥45520, only in live files: `mining/v2/day-020-s5.yaml` (58 refs) and 7 live compile files (13 refs: rule-index-tdd-bdd, rule-index-pair-programming, disposition-tdd-bdd, disposition-pair-programming, skill-v2-changelog-{bookminder,pair-programming,tdd-bdd}) — 71 rewrites total, each a constant −23710 on every number in the ref including range endpoints. The 31 refs ≥45520 inside `provenance-verification-*.md` stay untouched; each such file gets one prepended annotation line (exact text in protocol step M4). All other refs in all files (724 of 795) are inside the identity region and are not touched — zero diff churn where nothing moved.

Two commits, independently revertable, each naming the other's purpose:
1. `claude-dev-log-diary/day-020.md` (repaired) + `.coordination/day-020-repair-report.md` — message states method, pre-repair blob `27a5ad7…`, commit `4bd07ce`, and the one-line rederivation command.
2. Ref migration (8 live files) + annotations (7 historical reports) — message states the −23710 rule and the 71-rewrite count.

## 3. Verification protocol — every check falsifiable, every gate blocking

Run from `/home/user/BookMinder`. `ORIG` is always the pre-repair blob, never the working file: `git cat-file blob 27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2 > "$SCRATCH/orig.md"`. Any gate failing = STOP, restore with the recovery command in the header, report; no gate may be waived or weakened by the worker.

G0 — Preconditions (blocking). `git diff --quiet -- claude-dev-log-diary/day-020.md` succeeds; `git rev-parse HEAD:claude-dev-log-diary/day-020.md` = `27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2`; `wc -l < claude-dev-log-diary/day-020.md` = 56185; `python .coordination/tools/validate_mining.py .coordination/mining/v2/day-020-s{1,2,3,4,5}.yaml` prints 5×OK and exits 0. (If the blob differs, the file changed since this review — re-run the review, do not proceed.)

G1 — Structure re-verification against ORIG (blocking).
- `cmp <(sed -n '21810,31128p' "$SCRATCH/orig.md") <(sed -n '45520,54838p' "$SCRATCH/orig.md")` exits 0.
- `diff <(sed -n '7206,21809p' "$SCRATCH/orig.md") <(sed -n '31129,45519p' "$SCRATCH/orig.md") | grep -E '^[0-9]'` outputs exactly three hunk headers: `8a9`, `14353,14598c14354`, `14604a14361,14391`.
- `sed -n '1p' "$SCRATCH/orig.md"` = `claude`; `sed -n '56179p' "$SCRATCH/orig.md"` contains `/exit`.

G2 — Build (deterministic recipe; blocking on any command error).
```
{ sed -n '1,21809p;45520,56185p' "$SCRATCH/orig.md"
  echo '════ EDITORIAL APPENDIX — NOT CONSOLE OUTPUT (added by repair 2026-08-15) ════'
  echo 'Variant window from deleted duplicate rendering S4: pre-repair lines 45480-45519 of blob 27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2. Sole S4 content not byte-present in the body above (expanded Task prompt + 01:50 wall-clock); adjacent context lines included for contiguity.'
  sed -n '45480,45519p' "$SCRATCH/orig.md"
  echo '════ END APPENDIX ════'
  cat "$SCRATCH/trailer.txt"
} > claude-dev-log-diary/day-020.md
```
`trailer.txt` (written first): `════ REPAIR TRAILER — EDITORIAL, NOT CONSOLE OUTPUT ════` then, in prose: repair date and method (delete-only, adversarially reviewed plan at `.coordination/day-020-repair-plan.md`, report at `.coordination/day-020-repair-report.md`); pre-repair blob and recovery command verbatim from this plan's header; the remap table from section 2; the sentence "All pre-repair locs ≤31128 are unchanged; locs ≥45520 shifted by −23710; lines 31129-45519 were duplicates of content above, except the appendix window."

G3 — Byte-reconstruction identity (blocking; the master gate).
- `cmp <(sed -n '1,21809p;45520,56185p' "$SCRATCH/orig.md") <(head -n 32475 claude-dev-log-diary/day-020.md)` exits 0.
- `cmp <(sed -n '45480,45519p' "$SCRATCH/orig.md") <(sed -n '32478,32517p' claude-dev-log-diary/day-020.md)` exits 0.
- `sed -n '32476p'` = the appendix marker; `sed -n '32518p'` = `════ END APPENDIX ════`.

G4 — Sentinels (blocking; guards off-by-one in G2's ranges from both ends).
- `sed -n '4986p'` contains `<bash-input>gemini --help</bash-input>` (S1 old-UI content intact).
- `sed -n '21722p'` new = old byte-equal (inside the 49-message list only S2 renders).
- Three-way check at the linchpin line: new L21810 = old L21810 = old L45520, byte-equal (proves the S3-identity coincidence the whole remap rests on).
- `sed -n '32469p'` contains `/exit`; new L32475 = old L56185 byte-equal.

G5 — Ref inventory (blocking; before touching any ref).
`grep -rEoh 'day-020:L[0-9]+(-L?[0-9]+)?' .coordination` (excluding this plan and the report) yields exactly 795 refs; zero refs have any endpoint in [31129,45519]; the only segment-crossing range is `day-020:L14501-21810`; exactly 102 refs have a number ≥45520, distributed 58 (s5.yaml) + 13 (live compile) + 31 (provenance-verification-*). Any drift from these numbers means the corpus changed since this review — STOP and re-derive.

G6 — Migration (blocking). Rewriter handles both forms `day-020:L(\d+)` and `day-020:L(\d+)-(\d+)`, subtracts 23710 from every captured number ≥45520, touches only the 8 live files named in section 2. Post-condition: exactly 71 numbers changed (diff-count them); zero changes in identity-region refs; zero changes in provenance-verification files.

G7 — Per-ref positional byte-equality (blocking; the gate validate_mining.py cannot be). For every one of the 795 refs (live files: post-migration values; historical files: pre-repair values against ORIG only), a script asserts: the content of the new file at the (migrated) line range is byte-equal to ORIG at the original line range; appendix-mapped refs (none expected) compare against new 32478-32517. Every ref must pass; print pass-count 795/795. This single check proves every citation in the corpus still points at the exact bytes it pointed at before the repair — including `loc`/`evidence` entries that carry no quote.

G8 — Validator regression (blocking, explicitly necessary-not-sufficient per F4). Re-run the G0 validator command: 5×OK, exit 0, matching baseline.

G9 — Stale scan (blocking). In live files: no `day-020:L` number >32475 remains and none in [31129,45519] (nothing can cite deleted or beyond-EOF lines). In provenance-verification-*.md: numbers >32475 permitted only because M4's annotation line is present in that file — check both.

M4 — Historical annotation. Prepend to each of the 7 `provenance-verification-*.md`: `> NOTE (2026-08-15): line refs in this report cite the pre-repair day-020.md (blob 27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2). Locs ≤31128 are unchanged in the repaired file; locs ≥45520 correspond to repaired line minus offset — subtract 23710. See .coordination/day-020-repair-report.md.`

G10 — Artifacts and commits (blocking). `.coordination/day-020-repair-report.md` exists containing: the remap table, gate outputs (G1-G9 verbatim command results), the ref inventory counts, the old-31137 divider disposition, and the appendix-window derivation. Commit 1 then commit 2 as specified in section 2, staged file-by-name (never `git add .`), then push. If `claude-dev-log-diary/README.md` exists, add a two-line pointer to the trailer and report in commit 2; if not, skip (the in-file trailer travels with the file).

## 4. Open risks

- External citations outside this repo (author's private notes, other machines) using old ≥45520 locs will be off by 23710. Mitigated, not eliminated: the trailer and annotations state the constant; the pre-repair blob remains one git command away.
- The scout's 99.7%-coverage figure was computed with 12-word shingles and is not independently re-derived here — but the design never relies on it: S3 is covered by `cmp`, S4 by the 3-hunk diff bound plus the superset appendix, and S1/S2/S5 are kept wholesale. Content-loss risk is closed by construction.
- Shard YAML `file:` fields say `day-020-sN`; the validator resolves these to `day-020.md` via its fallback chain (verified in code, lines 61-67). If that fallback is ever removed, shard validation breaks — unrelated to this repair but worth knowing.
- Future mining of the repaired file will produce locs ≤~32530 that are unambiguous; but tooling that hardcoded 56185 or segment boundaries (none found in `.coordination/tools` [verified: the .js miners contain no literal day-020 locs]) would need updating if it exists elsewhere.
- The one glyph-only dropped line (old 31137) is unrecoverable from the repaired file alone — by design; it is recoverable from the blob and documented in the report. If anyone ever disputes "zero content loss", the dispute resolves against `git cat-file blob 27a5ad7…` in seconds; that command is the real safety net of this entire design.
