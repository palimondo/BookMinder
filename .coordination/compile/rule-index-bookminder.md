# Rule index — bookminder project-memory skill (B-NN → source → provenance)

Compiled 2026-08-13 against tree at HEAD 754da3f (skill committed ff7317b), branch claude/bookminder-recall-5ite2s. **v2 2026-08-14**: every corpus source transcript-verified (provenance-verification-bookminder-{1,2}.md) and the skill revised by the judge pass (skill-v2-changelog-bookminder.md); rows below carry the resulting relabels, dedups and re-filings. Non-corpus sources (threads.md rulings, ratified ledger, verified@tree stamps) were OUT OF SCOPE for that pass: rules resting only on them are marked **corpus-unverified (author-attested)** so the next verification era knows their status — they are author-ratified material, not defects. Provenance types per compile policy: user-verbatim > user-paraphrase > agent-synthesis; **agent-synthesis (Gemini relay)** marks text a third-party agent wrote and the author pasted — relayed, not asserted by him. DB-schema facts additionally carry a stamp: **verified@tree** (encoded in current code/fixtures, exercised by suite) | **hypothesis** (open, never settled) | **needs-live-DB** (established on a live library in 2025, requires fresh probe; no live DB exists in this environment).

day-020.md re-logs whole transcript regions at differing offsets, so its `s1`/`s2`/`s3`/`s4` mining ids are not independent evidence. Verified identities: d020s1-R18 = d020s4-R12 (one author turn), d020s2-R14 = d020s4-R17 (one edit sequence), and d020s1-R20 = d020s3-R11 = d020s4-R10 (one Gemini-written day-010 summary re-logged three times; primary evidence for its persona claims is day-010:L1261-L1290, the author's own `sudo ls -la` paste). Sources are counted once below.

## goals-and-history.md

| id | source | provenance |
|----|--------|------------|
| B-01 | threads.md:21 (Meta-goals, user voice — author-attested, corpus-unverified); v2/day-002 philosophy loc day-002:L94 (verified FAITHFUL) | user-verbatim |
| B-02 | threads.md:22, :26, :28 (pairing definition excluded — lives in pair-programming skill) — **corpus-unverified (author-attested)**, no corpus source | user-paraphrase of user rulings, root quotes user-verbatim |
| B-03 | threads.md:24 — **corpus-unverified (author-attested)** | user-paraphrase |
| B-04 | threads.md:25 (2026-08-13 book-grounding ruling; simulacra-shallowness) — **corpus-unverified (author-attested)** | user-paraphrase |
| B-05 | v2/day-018 phil loc day-018:L5021; day-009:L8039-L8041, L8222-L8223; day-013:L1446 — v2: deliverable-artifacts claim bounded per the author's same-breath qualifiers (day-018:L5048-L5060, day-009:L8038-L8039) | user-verbatim |
| B-06 | d006-R6, d006-R7, d006-R8 (v2/day-006.yaml) | user-verbatim |
| B-07 | d005-R8 (corpus `because` embellishes "BookMind failed" — compiled rule does not inherit it), day-006:L13 phil; day-005:L2228 phil | user-verbatim |
| B-08 | d007-R15 | user-verbatim |
| B-09 | threads.md:31-36 (Project history, user voice), threads.md:73/77 (2026-08 restorations); lapse anatomy per .coordination/bdd-style artifacts + TODO.md:19-20 — **corpus-unverified (author-attested)** | user-paraphrase + verified tree events |
| B-10 | threads.md:33 (hooks = most valuable innovation); skill-removals persistence.md fragment (stickiness law); threads.md:117 (thread 00 end-question) — **corpus-unverified (author-attested)** | user-paraphrase |

## repo-geography-and-fixtures.md

| id | source | provenance |
|----|--------|------------|
| B-20 | repo-map.md Orientation + Access strategy; d008-R19 (kernel corrected in v2: the attested lesson is "use the census `/hi` already produced", not venv noise — the "seventeen site-packages paths" detail was manufactured from a collapsed line); d006-R4 (line-count falsification, re-filed here from B-31 — the 531,358/294,940 counts behind the rejected "44% reduction" claim); skill-removals claims.md fragment (~290 lines); line count re-verified at HEAD (283 lines bookminder/) | user-verbatim (d008-R19), agent-synthesis (d006-R4, sizes), verified@tree |
| B-21 | d002-R10, d017-R1, d020s5-R7 (v2 scope correction: attests the background-subagent boundary only — foreground `rg … \| head` diary sweeps in the same window drew no objection), d014-R9 (scoped-grant lore; enforcement half day-014:L417-L419), d017-R7, d006-R9; repo-map.md LAND MINES | user-verbatim (diary rules), agent-synthesis (sizes) |
| B-22 | git ls-files specs/ verified at HEAD; threads.md:77 (restore ruling); d020s2-R13 (subprocess coverage, re-verified: specs/cli_spec.py:1,19-38 uses subprocess at HEAD) | user-paraphrase + verified@tree |
| B-23 | d011-R16 (corpus `because` misattributes Gemini's six-value vocabulary as user-verbatim; superseded by CLAUDE.md <backlog_management> at HEAD, which the skill points at), d011-R17, d017-R10, d017-R11, d017-R15, d018-R11, d018-R20, d021-R15 | user-verbatim |
| B-24 | d020s2-R14 (= d020s4-R17), d019-R21, d017-R8 (v2: restored its dropped negative — no `--flag`/`--status`/`--type` — and the approved plan's reading-status values, day-017:L1294-L1308; `--filter` is single-value at HEAD, cli.py:40-44), d017-R9, d021-R20, d021-R19, d019-R19, d010 phil day-010:L186, d020s1-R18 (= d020s4-R12); all code claims re-verified (cli.py:17-52,33-45,49-50) | user-verbatim/paraphrase, verified@tree |
| B-25 | d009-R25, d007-R21, d020s2-R15 (v2 relabel: agent-synthesis — both cited locs are the agent reading/editing its own code, no author turn; claim itself verified library.py:42-51) | user-verbatim (d009-R25, d007-R21), agent-synthesis (d020s2-R15), verified@tree |
| B-26 | d010-R17 (primary persona evidence day-010:L1261-L1290, author's sudo ls paste), d010-R21, d020s1-R19 (corpus `because` invents a "no falsy strings in Python" claim the author never made — compiled rule states only the three specced cases, library_spec.py:37-49, and does not inherit it), d020s1-R20 (= d020s3-R11 = d020s4-R10; v2 relabel: agent-synthesis (Gemini relay) — one summary re-logged three times; its error-message pair is now verified@tree at library.py:26-37 against the fixture tree), d020s2-R16, d020s3-R12, d014-R7, d011-R20 (corrupted-persona structure, re-filed here from B-27 where nothing used it); seam WHY from canonical §2.2 lineage; module-constant caveat per ledger L-09 ruling; verified library.py:54-62 + fixture tree at HEAD | user-verbatim core, agent-synthesis (relay cluster), L-09 per ratified ledger |
| B-27 | d015-R4, d015-R5, d015-R10, d016-R1, d016-R2, d016-R3, d016-R4, d016-R15, d018-R12, d018-R13, d018-R14, d018-R15, d018-R17, d007-R19, d020s1-R21 (corpus `because`'s "kept a test green for weeks" story is unevidenced — compiled rule carries only the leaf-`.gitkeep` form); USERNAME-fixed-at-HEAD re-verified (copy_book_to_fixture.sh:8 uses FIXTURE_USER) | user-verbatim majority, verified@tree |
| B-28 | d019-R18 demoted to re-census command (census claims rot: d011-R21 superseded by day-016 swap + day-019 census); d002-R13 (GOOS epub lore, re-expressed per its needs-rework note) | agent-synthesis, census = point-at-truth |
| B-29 | d021-R16 (incl. its needs-rework env caveat), day-011:L7172 phil, day-021:L7068 phil | user-verbatim |
| B-30 | d004-R15, d004-R17, d004-R18, d006-R5, d009-R26, d010-R23, d011-R22, d012-R10; pyproject pins re-verified (pyproject.toml:11 `==3.13.*`, :71 `py312`) | user-verbatim/paraphrase, verified@tree |
| B-31 | d003-R10, d003-R13, d003-R16, d015-R9, d018-R21, d005-R14 (d006-R4 re-filed to B-20 in v2 — B-31 carries no line-count content) | user-verbatim |
| B-32 | user directive 2026-08-14, session a42b9c92 (transcript: claude-dev-log-diary/jsonl/cloud-2026/a42b9c92-c0e6-588e-bc6f-3d5e4f37b895.jsonl; mechanism doc claude-dev-log-diary/jsonl/README.md); post-compile addition, not from mining corpus | user-paraphrase |
| B-67 (in goals-and-history.md) | user ruling 2026-08-14, session a42b9c92 ("This whole project is public. We are developing the methodology [in] the open."); post-compile addition, not from mining corpus | user-verbatim core |

## apple-books-domain.md (DB-schema stamps)

| id | source | provenance | stamp |
|----|--------|------------|-------|
| B-40 | d002-R12 (location), d008-R8 (glob) | user-verbatim (glob), agent-synthesis (census) | verified@tree (library.py:17-25; fixture trees mirror layout) |
| B-41 | d008-R9 (v2 relabel: agent-synthesis — day-008's conversation was lost to Cursor scrollback, day-008:L1521; only the agent's doc diff survives; claim independently carried by d009-R20), d009-R20, d012-R14 (the correction that makes it a rule is the author's "You're jumping to conclusions", day-013:L866, not the cited loc), d013-R18 (v2: plist-omission mechanism demoted to unexplained anomaly — author's verdict "still a mystery", day-013:L871-L872), d007-R17 (v2: `updateDate` reading demoted to the author's unverified hypothesis; the settled outcome is the YAGNI deletion of the sort feature, day-007:L2739/L2749), d005-R7 | user-verbatim/paraphrase + agent-synthesis | needs-live-DB (1) — plist-vs-DB role claims observed 2025 |
| B-42 | d008-R10, d009-R22 | agent-synthesis | verified@tree (library.py:11,65-66; stable Core Data fact) |
| B-43 | d014-R3 (census reflex, per ratified ledger L-20; v2 relabel: agent-synthesis — the batch supplies values, not semantics, and the sole author turn is about Postman), d011-R19, d012-R11 + d013-R15 (corpus `because`s' "two ZSTATE=5 rows" is wrong — dozens at day-011:L7422-L7628, 206 at day-015:L1542; d013-R15's quote and rule point opposite ways), d012-R12, d013-R16, d015-R6, d015-R7 (v2 relabel: agent-synthesis for the ZTITLE discriminator — the author's verbatim pointed at "entries and seriesid", the ZTITLE substitute is the agent's, written to docs unreviewed), d016-R17, d015-R12 (DB-first method — attests the one ZSERIESID breakthrough, day-015:L1708-L1715). v2 chronology fix: the duplicate-row batch (day-014:L735-L764) PRECEDES the ZSERIESID join (day-015:L1708-L1715) and the two are consistent; the compiled "later systematic re-probe" framing was inverted and is corrected in the skill | user-verbatim (author turns), agent-synthesis (mapping tables, discriminator) | needs-live-DB (2) — 1/3/6 working set; hypothesis — ZSTATE 5 (L-20 demotion; both observations attached in order) |
| B-44 | d012-R13 (primary: author's correction + live probes, day-012:L2975-L2997; d013-R17 is the same exchange replayed in day-013's recap, d019-R14 is Gemini's summary of it — one observation, counted once), d019-R15, d019-R16 (v2 relabel: agent-synthesis (Gemini relay) — lifecycle is a third-party reconstruction of a day-017 observation, no live before/after probe; skill hedges accordingly), d018-R16 (the only independent second episode, and the strongest turn), d016-R17 (v2: its "reverted for lacking a failing spec" `because` is invented — the author's revert was of an unauthorized premature change, day-016:L7169-L7170; skill now attributes it so); code divergence re-verified (library.py:76-77 vs :154-159) | user-verbatim (d012-R13, d018-R16), agent-synthesis (relay + lifecycle) | verified@tree (predicate encoding); needs-live-DB (3) — underlying mapping + per-title freshness; hypothesis — lifecycle (relay-sourced) |
| B-45 | ledger L-12 ruling (hedged form governs); docs/apple_books.md:60 vs :114-115 re-verified at HEAD — **corpus-unverified (author-attested)** | ratified ledger | needs-live-DB (4) |
| B-46 | d014-R4 (ZTITLE dupes), d011-R18 (ZISFINISHED, incl. its elision caveat), d009-R21 (ZLASTOPENDATE 221-row probe) | agent-synthesis | needs-live-DB (5) — all three column facts |
| B-47 | d019-R17 (v2 relabel: agent-synthesis (Gemini relay) — all three locs are agent text: the relayed log summary plus the agent's own requirements dialogue; v2 adds the same-session counter-observation, day-019:L1616-L1617, UI shows some samples at 1%) | agent-synthesis (Gemini relay) | hypothesis |
| B-48 | d015-R8, d018-R22 (computed-not-marked) | user-verbatim | hypothesis |
| B-49 | d010-R18, d010-R19, d010-R22, d020s1-R20 (relay copy — substance primary-verified at day-010:L961-L967, L1152-L1165) | user-verbatim + agent-synthesis | needs-live-DB (6) — live-machine states, unverifiable here |
| B-50 | d010-R20, d007-R16, d009-R24, d012-R15, d002-R12 (superseded plutil-bridge method noted) | user-verbatim | verified@tree (list-shape guard library.py:85-86; plistlib = stdlib fact) |
| B-51 | d009-R23 (v2 stamp split: the no-path-in-DB schema claim was never checked — agent's "might not have path info", day-009:L4459; the author's direction was to leave a FIXME/TODO, day-009:L4436-L4438), d020s2-R15 | user-verbatim | verified@tree (path="" library.py:73) for the code fact ONLY; the no-path-in-DB schema claim needs-live-DB (7) |
| B-52 | d016-R14, d012-R16, d014-R5, d014-R8 kernel (batching), d015-R12; the no-print-debugging clause is a deliberate cross-skill echo of tdd-bdd T-96 — its sources are d015-R1 (day-015:L897-L926, user-verbatim) and d014-R6 (day-014:L199-L204), added here in v2 so the clause's row shows its real backing | user-verbatim | n/a (practice) |
| B-53 | d008-R11 (v2: its named speculative sections — "Edge Cases", NULL-handling — restored to the skill text), d014-R2, d019-R20, d021-R17, d021-R18, d013-R14, d013-R19, d013-R20, d018-R22 | user-verbatim | n/a (practice) |

## current-state-and-open-decisions.md

| id | source | provenance |
|----|--------|------------|
| B-60 | verified-residue.md (pointer), threads.md HANDOFF convention; CLAUDE.md build commands — **corpus-unverified (author-attested)** | agent-synthesis, point-at-truth |
| B-61 | ledger L-11 (OPEN, deferred to gardening by author 2026-08-13); README.md:53-58 + library.py:89,:105 + zero-caller grep re-verified at HEAD — **corpus-unverified (author-attested)** | ratified ledger, verified@tree |
| B-62 | ledger L-13 (RESOLVED: revert-and-redo ruling landed in TODO.md + card statuses); d021-R14 RETIRED by author ruling 2026-08-16 (inciting incident resolved at source — statuses reconciled at HEAD; standing suspicion rule judged counterproductive, its clauses removed from B-62, B-23, and the router) — B-62 now **corpus-unverified (author-attested)** | ratified ledger, verified@tree |
| B-63 | verified-residue R1; threads.md:107 (P2, parked); cli.py:10 + library_spec.py:21 set-equality re-verified at HEAD — **corpus-unverified (author-attested)** | agent-synthesis + user-endorsed proposal, verified@tree |
| B-64 | ledger L-14..L-19 (rule-mechanical, gardening-gated); verified-residue.md pointer — **corpus-unverified (author-attested)** | ratified ledger |
| B-65 | threads.md:77 (restorations), :13 (stop-hook ruling), :4 (validator blind spot), :59 (graduation deferred); skill-removals persistence/claims/delegation fragments (substrate map, evidence-architecture pointer) — **corpus-unverified (author-attested)** | user-paraphrase + coordinator record |
| B-66 | threads.md:96-97 (memory-architecture insight, user-validated 2026-08-13) — **corpus-unverified (author-attested)** | user-paraphrase |

**needs-live-DB stamps: 7. hypothesis stamps: 4 (ZSTATE 5, sample lifecycle, B-47, B-48). Corpus-unverified (author-attested) rules: B-02, B-03, B-04, B-09, B-10, B-45, B-60, B-61, B-62 (since d021-R14's retirement), B-63, B-64, B-65, B-66, B-68 — plus the threads/ledger/tree halves of every other rule.**

## Footer roster — apple-books-domain.md id mapping

The domain page went through two rewrites. v3, under the author's ruling that facts live in-page, per-entry stamps go, and ids may be renumbered, split entries that carried several facts and renumbered them B-40..B-59 in page order. v4 retired the ids altogether: the page is now a model of the storage organized by the storage's own structure, and its section headings are the only anchors. The rows above stay keyed by the v2 ids as compile provenance; translate v2 → v3 → v4 section heading with this roster.

- B-40 → v3 B-40 → "What exists on disk"
- B-41 → v3 B-41 → "Books.plist" (the plist's fields and limits) and "The BKLibrary database" with "Reading-state columns" (where reading state lives); v3 B-42 → "Books.plist" (updateDate, the sort_by deletion); v3 B-43 → "What exists on disk" (never filter by on-disk existence)
- B-42 → v3 B-44 → "The BKLibrary database" (Apple epoch)
- B-43 → v3 B-45 → "ZSTATE"
- B-44 → v3 B-46 → "Samples" (first paragraph); v3 B-47 → "Cloud: display versus filter"
- B-45 → v3 B-48 → "ZCONTENTTYPE"
- B-46 → v3 B-49 → "Identity columns"; v3 B-50 → "Reading-state columns" (ZISFINISHED); v3 B-51 → "Reading-state columns" (ZLASTOPENDATE)
- B-47 → v3 B-52 → "Samples" (second paragraph) and "What exists on disk" (the AEAnnotation store)
- B-48 → v3 B-53 → "What the app computes"
- B-49 → v3 B-54 → "What exists on a machine, by user state"
- B-50 → v3 B-55 → "Books.plist" (mechanics paragraph)
- B-51 → v3 B-56 → "ZPATH"
- B-52 → v3 B-57 → "Working the database"
- B-53 → v3 B-58 → "Reading docs/apple_books.md"; v3 B-59 → "Editing docs/apple_books.md", with its UI-quirk clauses (the fake 1%, per-platform vocabularies, macOS "Complete" as a percentage) under "What the app computes"
- Retired: none; every v3 fact has a home. Fixture-derived facts with no prior row: ZISFINISHED NULL on unfinished rows and ZDATEFINISHED set on an unfinished row ("Reading-state columns"); ZPATH per row, including the DocumentRevisions path on one downloaded sample ("ZPATH"); the !cloud spec's dependence on the fixture ("Cloud: display versus filter"); the list-recent sample spec asserting no count ("Samples"); Books.swift as the fixture plist's Swift rendering ("Books.plist"). Doc-sourced claims with no prior row, stated as unprobed: the AEAnnotation file name and the BCRecentlyOpenedBooksDB store ("What exists on disk").
- Cross-references updated: current-state B-68 cites "Cloud: display versus filter"; the router page map was re-derived from the section structure; .coordination/apple-books-recon.md keys its checklist by these headings. The stamp column in the domain table above is retired from the skill; what still needs a live library is the recon checklist.
