# Rule index — bookminder project-memory skill (B-NN → source → provenance)

Compiled 2026-08-13 against tree at HEAD 754da3f (skill committed ff7317b), branch claude/bookminder-recall-5ite2s. Provenance types per compile policy: user-verbatim > user-paraphrase > agent-synthesis; threads.md entries are coordinator-recorded user rulings (user-paraphrase unless marked voice). DB-schema facts additionally carry a stamp: **verified@tree** (encoded in current code/fixtures, exercised by suite) | **hypothesis** (open, never settled) | **needs-live-DB** (established on a live library in 2025, requires fresh probe; no live DB exists in this environment).

## goals-and-history.md

| id | source | provenance |
|----|--------|------------|
| B-01 | threads.md:21 (Meta-goals, user voice); v2/day-002 philosophy loc day-002:L94 | user-verbatim |
| B-02 | threads.md:22, :26, :28 (pairing definition excluded — lives in pair-programming skill) | user-paraphrase of user rulings, root quotes user-verbatim |
| B-03 | threads.md:24 | user-paraphrase |
| B-04 | threads.md:25 (2026-08-13 book-grounding ruling; simulacra-shallowness) | user-paraphrase |
| B-05 | v2/day-018 phil loc day-018:L5021; day-009:L8039-L8041, L8222-L8223; day-013:L1446 | user-verbatim |
| B-06 | d006-R6, d006-R7, d006-R8 (v2/day-006.yaml) | user-verbatim |
| B-07 | d005-R8; day-006:L13 phil; day-005:L2228 phil | user-verbatim |
| B-08 | d007-R15 | user-verbatim |
| B-09 | threads.md:31-36 (Project history, user voice), threads.md:73/77 (2026-08 restorations); lapse anatomy per .coordination/bdd-style artifacts + TODO.md:19-20 | user-paraphrase + verified tree events |
| B-10 | threads.md:33 (hooks = most valuable innovation); skill-removals persistence.md fragment (stickiness law); threads.md:117 (thread 00 end-question) | user-paraphrase |

## repo-geography-and-fixtures.md

| id | source | provenance |
|----|--------|------------|
| B-20 | repo-map.md Orientation + Access strategy; d008-R19; skill-removals claims.md fragment (~290 lines); line count re-verified at HEAD (283 lines bookminder/) | agent-synthesis, verified@tree |
| B-21 | d002-R10, d017-R1, d020s5-R7, d014-R9 (scoped-grant lore), d017-R7, d006-R9; repo-map.md LAND MINES | user-verbatim (diary rules), agent-synthesis (sizes) |
| B-22 | git ls-files specs/ verified at HEAD; threads.md:77 (restore ruling); d020s2-R13 (subprocess coverage, re-verified: specs/cli_spec.py:1,19-38 uses subprocess at HEAD) | user-paraphrase + verified@tree |
| B-23 | d011-R16, d011-R17, d017-R10, d017-R11, d017-R15, d018-R11, d018-R20, d021-R15; status vocabulary deferred to CLAUDE.md <backlog_management> at HEAD (d011-R16's older vocab superseded) | user-verbatim |
| B-24 | d020s2-R14, d020s4-R17, d019-R21, d017-R8, d017-R9, d021-R20, d021-R19, d019-R19, d010 phil day-010:L186, d020s1-R18, d020s4-R12; all code claims re-verified (cli.py:17-52,33-45,49-50) | user-verbatim/paraphrase, verified@tree |
| B-25 | d009-R25, d007-R21, d020s2-R15; verified library.py:42-51 | user-verbatim, verified@tree |
| B-26 | d010-R17, d010-R21, d020s1-R19, d020s1-R20, d020s2-R16, d020s3-R11, d020s3-R12, d020s4-R10, d014-R7; seam WHY from canonical §2.2 lineage; module-constant caveat per ledger L-09 ruling; verified library.py:54-62 + fixture tree at HEAD | user-verbatim core, L-09 per ratified ledger |
| B-27 | d015-R4, d015-R5, d015-R10, d016-R1, d016-R2, d016-R3, d016-R4, d016-R15, d018-R12, d018-R13, d018-R14, d018-R15, d018-R17, d007-R19, d020s1-R21, d011-R20; USERNAME-fixed-at-HEAD re-verified (copy_book_to_fixture.sh:8 uses FIXTURE_USER) | user-verbatim majority, verified@tree |
| B-28 | d019-R18 demoted to re-census command (census claims rot: d011-R21 superseded by day-016 swap + day-019 census); d002-R13 (GOOS epub lore, re-expressed per its needs-rework note) | agent-synthesis, census = point-at-truth |
| B-29 | d021-R16 (incl. its needs-rework env caveat), day-011:L7172 phil, day-021:L7068 phil | user-verbatim |
| B-30 | d004-R15, d004-R17, d004-R18, d006-R5, d009-R26, d010-R23, d011-R22, d012-R10; pyproject pins re-verified (pyproject.toml:11 `==3.13.*`, :71 `py312`) | user-verbatim/paraphrase, verified@tree |
| B-31 | d003-R10, d003-R13, d003-R16, d015-R9, d018-R21, d005-R14, d006-R4 | user-verbatim |
| B-32 | user directive 2026-08-14, session a42b9c92 (transcript: claude-dev-log-diary/jsonl/cloud-2026/a42b9c92-c0e6-588e-bc6f-3d5e4f37b895.jsonl; mechanism doc claude-dev-log-diary/jsonl/README.md); post-compile addition, not from mining corpus | user-paraphrase |

## apple-books-domain.md (DB-schema stamps)

| id | source | provenance | stamp |
|----|--------|------------|-------|
| B-40 | d002-R12 (location), d008-R8 (glob) | user-verbatim (glob), agent-synthesis (census) | verified@tree (library.py:17-25; fixture trees mirror layout) |
| B-41 | d008-R9, d009-R20, d012-R14, d013-R18, d007-R17, d005-R7 | user-verbatim/paraphrase + agent-synthesis | needs-live-DB (1) — plist-vs-DB role claims observed 2025 |
| B-42 | d008-R10, d009-R22 | agent-synthesis | verified@tree (library.py:11,65-66; stable Core Data fact) |
| B-43 | d014-R3 (census reflex, per ratified ledger L-20), d011-R19, d012-R11, d012-R12, d013-R15, d013-R16, d015-R6, d015-R7, d016-R17, d015-R12 (DB-first method) | user-paraphrase (d014-R3) + user-verbatim (5-series quotes, demoted) | needs-live-DB (2) — 1/3/6 working set; hypothesis — ZSTATE 5 (L-20 demotion, duplicate-row observation attached) |
| B-44 | d019-R14, d019-R15, d019-R16, d012-R13, d013-R17, d018-R16, d016-R17 (cloud-filter scope); code divergence re-verified (library.py:76-77 vs :154-159) | user-paraphrase/verbatim | verified@tree (predicate encoding); needs-live-DB (3) — underlying mapping + per-title freshness; hypothesis — lifecycle |
| B-45 | ledger L-12 ruling (hedged form governs); docs/apple_books.md:60 vs :114-115 re-verified at HEAD | ratified ledger | needs-live-DB (4) |
| B-46 | d014-R4 (ZTITLE dupes), d011-R18 (ZISFINISHED, incl. its elision caveat), d009-R21 (ZLASTOPENDATE 221-row probe) | agent-synthesis | needs-live-DB (5) — all three column facts |
| B-47 | d019-R17 | user-paraphrase | hypothesis |
| B-48 | d015-R8, d018-R22 (computed-not-marked) | user-verbatim | hypothesis |
| B-49 | d010-R18, d010-R19, d010-R22, d020s1-R20 | user-verbatim + agent-synthesis | needs-live-DB (6) — live-machine states, unverifiable here |
| B-50 | d010-R20, d007-R16, d009-R24, d012-R15, d002-R12 (superseded plutil-bridge method noted) | user-verbatim | verified@tree (list-shape guard library.py:85-86; plistlib = stdlib fact) |
| B-51 | d009-R23, d020s2-R15 | user-verbatim | verified@tree (path="" library.py:73); the no-path-in-DB schema claim itself needs-live-DB (7) |
| B-52 | d016-R14, d012-R16, d014-R5, d014-R8 kernel (batching), d015-R12 | user-verbatim | n/a (practice) |
| B-53 | d008-R11, d014-R2, d019-R20, d021-R17, d021-R18, d013-R14, d013-R19, d013-R20, d018-R22 | user-verbatim | n/a (practice) |

## current-state-and-open-decisions.md

| id | source | provenance |
|----|--------|------------|
| B-60 | verified-residue.md (pointer), threads.md HANDOFF convention; CLAUDE.md build commands | agent-synthesis, point-at-truth |
| B-61 | ledger L-11 (OPEN, deferred to gardening by author 2026-08-13); README.md:53-58 + library.py:89,:105 + zero-caller grep re-verified at HEAD | ratified ledger, verified@tree |
| B-62 | ledger L-13 (OPEN, deferred); d021-R14; TODO.md:7-24 + stories/*.yaml statuses re-verified at HEAD | ratified ledger + user-verbatim, verified@tree |
| B-63 | verified-residue R1; threads.md:107 (P2, parked); cli.py:10 + library_spec.py:21 set-equality re-verified at HEAD | agent-synthesis + user-endorsed proposal, verified@tree |
| B-64 | ledger L-14..L-19 (rule-mechanical, gardening-gated); verified-residue.md pointer | ratified ledger |
| B-65 | threads.md:77 (restorations), :13 (stop-hook ruling), :4 (validator blind spot), :59 (graduation deferred); skill-removals persistence/claims/delegation fragments (substrate map, evidence-architecture pointer) | user-paraphrase + coordinator record |
| B-66 | threads.md:96-97 (memory-architecture insight, user-validated 2026-08-13) | user-paraphrase |

**needs-live-DB stamps: 7. hypothesis stamps: 4 (ZSTATE 5, sample lifecycle, B-47, B-48).**
