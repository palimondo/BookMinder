# Rule index — tdd-bdd skill

Every T-NN in `.claude/skills/tdd-bdd/` traced to its sources. Provenance ranks per compile policy: user-verbatim > user-paraphrase > agent-synthesis; ledger resolutions override all. Flags: detector-covered (F1b-red-first-in-time (transcript; replaced the retired F1 commit-grammar family per commit-after-red-review.md) / F2-assertion-integrity / F3-minimality / F4-layering / F5-claim-vs-action / F6-refactor-honesty), detector_candidate (mechanically checkable, no established family), rubric-item (LLM-judge assessable), UNFALSIFIABLE (no test exists — flagged per the author's own falsifiability principle).

| T | source | provenance | flag |
|---|--------|------------|------|
| T-01 | v2/day-009.yaml d009-R1 (day-009:L945-L946) | user-verbatim (because: agent-synthesis) | rubric-item (F1 retired; F1b examined: boundary choice needs story-card semantics, red-first component subsumed by F1b edit-before-red) |
| T-02 | CLAUDE.md:123-124 + ledger L-14 (2026-08-14 flip keeps the red-acceptance allowance) | author-restored CLAUDE.md + ledger | rubric-item (F1 retired; F1b examined: feature-completeness not transcript-decidable, fake-green is F2 territory) |
| T-03 | v2/day-019.yaml d019-R8 (day-019:L1951, L3899) | user-verbatim | rubric-item (F1 retired; F1b examined: acceptance-vs-unit not path-derivable in the concern-based spec tree, ordering subsumed by edit-before-red) |
| T-04 | v2/day-012.yaml d012-R5 (L1338); v2/day-019.yaml d019-R7 (L1859); v2/day-018.yaml d018-R1 (L1242) | user-verbatim (because: agent-synthesis in d012-R5, d018-R1) | rubric-item (F1 retired; F1b examined: sanctioned deliberately-red acceptance spec defeats failing-count thresholds) |
| T-05 | ledger L-05 (winner: v2/day-009.yaml d009-R2, day-009:L7329-L7331) | user-verbatim via ledger | detector_candidate (fake-green: hardcoded literal matching acceptance expectation) |
| T-06 | ledger L-02 (author ruling 2026-08-13; root v2/day-007.yaml d007-R3, day-007:L570-L573) | author-ruled + user-verbatim | UNFALSIFIABLE (a permission whose phase boundary has no crisp test; only the say-so clause is observable) |
| T-07 | v2/day-017.yaml d017-R13 (day-017:L1877) | user-verbatim | rubric-item |
| T-08 | v2/day-015.yaml d015-R13 (day-015:L691; quote at L787-L788) | user-verbatim | rubric-item |
| T-09 | v2/day-011.yaml d011-R8 (L7172); v2/day-012.yaml d012-R9 (L2804) | user-verbatim | detector-covered F5 |
| T-10 | v2/day-002.yaml d002-R1 (L1516); v2/day-010.yaml d010-R1 (L2872-L2881, revert L2928) | user-verbatim | detector-covered F1b |
| T-11 | v2/day-002.yaml d002-R2 (day-002:L1768) | user-verbatim | detector-covered F1b |
| T-12 | v2/day-019.yaml d019-R2 (day-019:L336) | agent-synthesis (agent self-narration; no author turn in window) | detector-covered F1b |
| T-13 | v2/day-019.yaml d019-R3 (L3806); v2/day-021.yaml d021-R6 (L4170) | user-verbatim | rubric-item |
| T-14 | author ruling 2026-08-14 (commit-after-RED retired; threads.md "COMMIT-AFTER-RED RETIRED" + "RULING CONFIRMED"); ledger L-14 flipped; CLAUDE.md tdd_discipline (Run & Verify RED) + git_workflow (stable points) — rewritten 2026-08-15 to surviving core: RED proven by the observed failing run, quoted; commit clause retired, spec lands with the GREEN commit | author-ruled | detector-covered F1b |
| T-15 | v2/day-012.yaml d012-R6 (L1772); v2/day-019.yaml d019-R4 (L3718); CLAUDE.md:128 | user-verbatim | detector-covered F3 |
| T-16 | v2/day-012.yaml d012-R7 (day-012:L1975) | user-verbatim | detector-covered F3 |
| T-17 | v2/day-018.yaml d018-R6 (L817); v2/day-016.yaml d016-R9 (L6889); CLAUDE.md:128-129 | user-verbatim | detector-covered F1b |
| T-18 | v2/day-019.yaml d019-R6 (L3131; because's "three times" unsupported — one instance at loc); v2/day-018.yaml d018-R7 (L1125) | user-verbatim (because: agent-synthesis in d019-R6) | rubric-item |
| T-19 | v2/day-020-s1.yaml d020s1-R3 (L1394; same turn re-exported: s2-R1 L10111, s4-R1 L23603 — one episode) | user-verbatim | rubric-item (F1 retired; F1b examined: positive obligation with no transcript event marking its absence) |
| T-20 | v2/day-020-s1.yaml d020s1-R13 (L1823; same turn re-exported: s4-R3 L24302 — one episode; all-sites clause at L1862/L24347); CLAUDE.md:131 (commit after refactor; third-commit clause dropped 2026-08-15 per author ruling) | user-verbatim | detector-covered F6 |
| T-21 | v2/day-010.yaml d010-R9 (L3944); v2/day-020-s3.yaml d020s3-R19 (L14822); s5-R9 (L55723) | agent-synthesis | detector-covered F6 |
| T-22 | v2/day-017.yaml d017-R4 (L1608), d017-R5 (L1609); v2/day-020-s2.yaml d020s2-R12 (L11629) | user-verbatim + user-paraphrase | detector_candidate (old name surviving a rename commit) |
| T-23 | v2/day-020-s2.yaml d020s2-R11 (L10211; same turn re-exported: s4-R4 L23690 — one episode) | user-verbatim | detector-covered F5 |
| T-24 | v2/day-020-s3.yaml d020s3-R8 (day-020:L16895) | user-verbatim | rubric-item |
| T-25 | v2/day-010.yaml d010-R8 (day-010:L2908) | user-verbatim (because: agent-synthesis) | detector_candidate (phase statement present in transcript) |
| T-26 | v2/day-021.yaml d021-R3 (L3576), d021-R4 (L3613) | user-verbatim (because: agent-synthesis) | detector-covered F5 |
| T-27 | v2/day-009.yaml d009-R12 (L7453); v2/day-007.yaml d007-R5 (L1055-L1056); CLAUDE.md tdd_discipline checklist | user-verbatim | detector-covered F5 |
| T-28 | v2/day-003.yaml d003-R1 (L1674-L1693); v2/day-004.yaml d004-R3 (L5520), d004-R4 (L5652) | user-verbatim | detector_candidate (gate-integrity: skip flags / no-verify in transcript) |
| T-29 | v2/day-003.yaml d003-R3 (L1273-L1397); v2/day-004.yaml d004-R1 (L5387), R2 (L5363), R5, R7 (L2886), R8 (L722), R9 (L4254); v2/day-002.yaml d002-R18 (L1518) | user-verbatim | detector-covered F5 |
| T-30 | v2/day-006.yaml d006-R2 (day-006:L3277) | user-verbatim | detector-covered F5 |
| T-31 | v2/day-003.yaml d003-R15 (day-003:L147-L166, L259-L283) | agent-synthesis | detector-covered F5 |
| T-32 | v2/day-020-s1.yaml d020s1-R25 (L7061; same turn re-exported: s4-R18 L30976 — one episode); s5-R6 (L55976, distinct episode) | user-verbatim + agent-synthesis | detector_candidate (hand-reversal diff vs revert commit in DAG) |
| T-33 | v2/day-021.yaml d021-R12 (day-021:L7469) | user-verbatim (because: agent-synthesis, day-021:L7474-L7484) | detector-covered F1b |
| T-34 | v2/day-006.yaml d006-R1 (day-006:L2996) | user-verbatim | detector-covered F5 |
| T-35 | v2/day-002.yaml d002-R6 (day-002:L926); CLAUDE.md code_style Tests | user-verbatim | detector_candidate (filename check) |
| T-36 | v2/day-009.yaml d009-R8 (L5508); v2/day-017.yaml d017-R2 (L2453); v2/day-020-s1.yaml d020s1-R14 (L2528; same turn re-exported: s2-R8 L12825 — three episodes total) | user-verbatim (mechanism-noun enumeration: agent-synthesis, day-009:L7319) | detector_candidate (spec-tree-naming: mechanism nouns in names) |
| T-37 | v2/day-007.yaml d007-R10 (day-007:L2712-L2713, interleaving clause) | user-verbatim (interleaving); depth cap agent-synthesis from the accepted restructure (day-007:L2757-L2807; canonical §2.1, unratified) | detector_candidate (nesting depth) |
| T-38 | ledger L-06; v2/day-017.yaml d017-R3 (L2127); v2/day-020-s2.yaml d020s2-R10 (L13202); v2/day-011.yaml d011-R3 (L11634), R4 (L12323), R5 (L5461); CLAUDE.md:100-101 | user-verbatim via ledger | detector_candidate (docstring on non-skipped spec) |
| T-39 | v2/day-012.yaml d012-R4 (L1244, rendered --spec symptom, no author turn at loc); v2/day-010.yaml d010-R2 (L2829, uncorrected in window) | user-paraphrase + agent-synthesis | detector_candidate (pass/skip-only bodies) |
| T-40 | v2/day-012.yaml d012-R3 (day-012:L1074, names + pass bodies); d012-R5 (L1338, skip-marker half) | user-verbatim | detector_candidate (two-move landing in DAG) |
| T-41 | v2/day-002.yaml d002-R5 (L2400); v2/day-019.yaml d019-R13 (L4355) | user-verbatim | detector-covered F3 |
| T-42 | v2/day-007.yaml d007-R11 (day-007:L2712; module-level resolution was the agent's, unobjected) | user-verbatim (because: agent-synthesis) | detector_candidate (per-test imports) |
| T-43 | v2/day-020-s1.yaml d020s1-R4 (L1271; same turn re-exported: s2-R2 L9791, s4-R2 L23459 — one episode, taught-once) | user-verbatim | rubric-item |
| T-44 | v2/day-009.yaml d009-R13 (day-009:L945) | user-verbatim | rubric-item |
| T-45 | ledger L-16; v2/day-005.yaml d005-R12 (day-005:L1555) | user-verbatim via ledger | detector_candidate (annotations in spec files) |
| T-46 | v2/day-009.yaml d009-R9 (day-009:L5426) | user-verbatim | detector_candidate (specs importing underscore names) |
| T-47 | v2/day-011.yaml d011-R7 (L1673; entry's because embellished — the corrupted-DB scenario survived the challenge, L1702-L1718); v2/day-020-s3.yaml d020s3-R6 (L14533) | user-verbatim | rubric-item |
| T-48 | v2/day-021.yaml d021-R1 (day-021:L1302) | user-verbatim | detector-covered F3 |
| T-49 | v2/day-012.yaml d012-R1 (day-012:L946) | user-verbatim | detector_candidate (spec-preservation: diff deletes existing it_ functions) |
| T-50 | v2/day-019.yaml philosophy (L4702); v2/day-018.yaml d018-R5 (L578) | user-verbatim | rubric-item |
| T-51 | v2/day-002.yaml d002-R3 (day-002:L1625-L1637) | agent-synthesis | detector-covered F2 |
| T-52 | ledger L-01 (ratified 2026-08-13); v2/day-019.yaml d019-R10 (L5011) | author-ruled + user-verbatim | detector-covered F2 |
| T-53 | ledger L-01(b); v2/day-020-s1.yaml d020s1-R11 (L2575; same turn re-exported: s2-R9 L13073 — one episode; FIXME suggestion retracted in-thread at L2605, rule reworded accordingly) | user-verbatim via ledger | detector-covered F2 |
| T-54 | v2/day-015.yaml d015-R2 (L1060-L1061); v2/day-016.yaml d016-R7 (L2642) | user-verbatim | detector-covered F2 |
| T-55 | v2/day-011.yaml d011-R1 (L2091), d011-R2 (L3629) | agent-synthesis | detector-covered F2 |
| T-56 | v2/day-020-s5.yaml d020s5-R4 (day-020:L32334) | user-verbatim | rubric-item |
| T-57 | v2/day-019.yaml d019-R1 (day-019:L303, L574) | agent-synthesis (diagnosis is the agent's own council voice; author supplied dissatisfaction at L546/L614, not the rule) | detector-covered F2 |
| T-58 | v2/day-009.yaml d009-R3 (day-009:L7266-L7326) | user-verbatim | detector-covered F2 |
| T-59 | v2/day-018.yaml d018-R4 (L592), d018-R2 (L1260), d018-R3 (L516) | user-verbatim | detector-covered F2 |
| T-60 | v2/day-020-s1.yaml d020s1-R5 (L6763; same turn re-exported: s3-R1 L21047), R6 (L6817; same turn re-exported: s3-R2 L21101, s4-R5 L30732) — two episodes total | user-verbatim | detector-covered F2 |
| T-61 | v2/day-011.yaml d011-R10 (L11951; anti-pattern created at L3650-L3654, never author-corrected) | agent-synthesis | detector-covered F4 |
| T-62 | v2/day-020-s1.yaml d020s1-R12 (L2257; same turn re-exported: s2-R3 L12182, s4-R13 L24954); s3-R7 (L14591, distinct equal-strength episode) — two episodes total | user-verbatim | rubric-item |
| T-63 | v2/day-021.yaml d021-R8 (L3437), d021-R7 (L2203) | user-verbatim | detector_candidate (unused mock configuration) |
| T-64 | v2/day-010.yaml d010-R6 (day-010:L5782, the question; correction at L5866, L5911-L5912) | user-verbatim (because: agent-synthesis) | detector-covered F2 |
| T-65 | v2/day-007.yaml d007-R6 (day-007:L884-L1084) | agent-synthesis | detector-covered F5 |
| T-66 | v2/day-019.yaml d019-R9 (L4471); v2/day-020-s1.yaml d020s1-R1 (L372) | user-verbatim | detector-covered F4 |
| T-67 | v2/day-005.yaml d005-R5 (day-005:L2148-L2150) | user-verbatim | detector-covered F4 |
| T-68 | v2/day-005.yaml d005-R6 (day-005:L2082-L2150) | user-verbatim | rubric-item |
| T-69 | v2/day-007.yaml d007-R4 (day-007:L658-L659) | user-verbatim | detector-covered F4 |
| T-70 | v2/day-020-s1.yaml d020s1-R10 (L3643; same turn re-exported: s3-R4 L15196, s4-R8 L27222 — one episode; s4-R8's own "never the specific message text" wording overreaches, compiled text follows s1-R10) | user-verbatim | detector-covered F4 |
| T-71 | v2/day-020-s1.yaml d020s1-R2 (L2424; same turn re-exported: s2-R7 L12486, s4-R6 L25125); s3-R5 (L15990, distinct episode) — two episodes total | user-verbatim | detector-covered F4 |
| T-72 | ledger L-09; v2/day-010.yaml d010-R5 (L5911); v2/day-009.yaml d009-R11 caveat (L5037; quote at L5191, L6043-L6061) | user-verbatim via ledger | detector-covered F4 |
| T-73 | v2/day-009.yaml d009-R10 (day-009:L6566-L6606) | agent-synthesis | detector_candidate (monkeypatch + subprocess in one spec) |
| T-74 | v2/day-010.yaml d010-R4 (day-010:L3304) | user-verbatim | detector-covered F4 |
| T-75 | v2/day-002.yaml d002-R14 (L2128); v2/day-016.yaml d016-R6 (L1237) | user-verbatim + agent-synthesis | detector_candidate (absolute home paths / usernames in tree) |
| T-76 | v2/day-010.yaml d010-R7 (L1549, agent-only anti-pattern, no teaching turn); v2/day-015.yaml d015-R3 (L1314-L1318); v2/day-020-s1.yaml d020s1-R7 (L4632; same turn re-exported: s3-R3 L17043, s4-R9 L28428 — one episode; git-invisibility clause at L4634) | user-verbatim + agent-synthesis | detector_candidate (fixture-provenance: hand-authored fixture rows) |
| T-77 | v2/day-013.yaml d013-R2 (L709-L869); v2/day-012.yaml d012-R8 (L2255) | user-verbatim | detector-covered F5 |
| T-78 | v2/day-021.yaml d021-R21 (day-021:L7068) | user-verbatim | detector_candidate (wall-clock time in specs over frozen fixtures) |
| T-79 | v2/day-020-s4.yaml d020s4-R11 (day-020:L30571) | user-verbatim (because: agent-synthesis; transcript gives only "Git tracks files, not directories") | detector_candidate (spec-referenced empty dirs untracked) |
| T-80 | v2/day-019.yaml d019-R12 (day-019:L4651) | user-verbatim | rubric-item |
| T-81 | v2/day-019.yaml d019-R11 (L4869); v2/day-021.yaml d021-R10 (L2348) | user-verbatim + user-paraphrase | rubric-item |
| T-82 | v2/day-021.yaml d021-R9 (day-021:L2215) | user-verbatim | detector_candidate (patch-handle naming) |
| T-83 | v2/day-020-s1.yaml d020s1-R9 (L2796, agent rationalisation; same agent turn re-exported: s4-R7 L25950); s2-R6 (L13169, earlier moment of same arc); v2/day-021.yaml d021-R2 (L2889) | user-verbatim + user-paraphrase + agent-synthesis | detector-covered F4 |
| T-84 | v2/day-020-s1.yaml d020s1-R8 (L522; same turn re-exported: s2-R4 L8178); s2-R5 (L8801, distinct turn) — two episodes total | user-verbatim | rubric-item |
| T-85 | v2/day-016.yaml d016-R8 (L7169); v2/day-007.yaml d007-R7 (L1799-L1800); CLAUDE.md package_structure | user-verbatim | detector-covered F3 |
| T-86 | v2/day-009.yaml d009-R4 (L6672-L6674); v2/day-002.yaml d002-R15 (L2174-L2194); v2/day-007.yaml d007-R8 (L1859-L1863); v2/day-020-s4.yaml d020s4-R15 (L24864) | user-verbatim + user-paraphrase + agent-synthesis | detector-covered F3 |
| T-87 | v2/day-009.yaml d009-R6 (L5531), R7 (L4645); v2/day-020-s3.yaml d020s3-R9 (L16931); s5-R2 (L55643) | user-verbatim + agent-synthesis | detector-covered F5 |
| T-88 | v2/day-020-s5.yaml d020s5-R1 (L55187); v2/day-007.yaml d007-R7 (L1799); v2/day-019.yaml d019-R5 (L2473) | user-verbatim | detector-covered F3 |
| T-89 | v2/day-009.yaml d009-R5 (L6334-L6335); v2/day-011.yaml d011-R6 (retrofit at L2216-L2857, agent-only; "Violation" verdict imported from day-009 TODO.md, quote not at loc); v2/day-020-s5.yaml d020s5-R3 (L54929) | user-verbatim + agent-synthesis | detector-covered F3 |
| T-90 | v2/day-021.yaml d021-R5 (L4169), d021-R6 (L4170) — one author turn split across two entries; commit-message clause dropped (agent's own amend habit at L4348-L4362, no author source) | user-verbatim | rubric-item |
| T-91 | v2/day-010.yaml d010-R3 (day-010:L1875, uncorrected agent skip, still present at session end); enforced episode day-010:L2823-L2908 with d010-R2 (skip-as-stand-in clause: skip-bodied spec committed beside shipped code, condemned L2881-L2889, reverted L2908) | agent-synthesis + user-verbatim | detector-covered F2 |
| T-92 | v2/day-007.yaml d007-R9 (day-007:L2707-L2708) | user-verbatim | detector-covered F3 |
| T-93 | v2/day-002.yaml d002-R16 (L1023); v2/day-003.yaml d003-R9 (L2118); v2/day-004.yaml d004-R16 (L4781); v2/day-015.yaml d015-R11 (L3113-L3197) | user-verbatim | detector-covered F3 |
| T-94 | v2/day-018.yaml d018-R8 (day-018:L1167) | user-verbatim | detector-covered F3 |
| T-95 | v2/day-020-s4.yaml d020s4-R19 (day-020:L23626; git-blame gate at L23689-L23696) | user-verbatim | rubric-item |
| T-96 | v2/day-015.yaml d015-R1 (L897-L926); v2/day-014.yaml d014-R6 (L199-L204) | user-verbatim + agent-synthesis | detector_candidate (production-file edits during exploratory probing) |
| T-97 | v2/day-010.yaml d010-R11 (day-010:L4372) | agent-synthesis | detector_candidate (lint-suppression markers added) |
| T-98 | v2/day-003.yaml d003-R5 (day-003:L491-L531) | user-verbatim | detector-covered F5 |
| T-99 | v2/day-021.yaml d021-R11 (day-021:L2432; scope narrowed to shared fixtures/cross-spec helpers — inline data builders exempt per T-81, day-019:L4869-L4928) | user-verbatim | detector-covered F3 |
| T-100 | v2/day-006.yaml d006-R3 (day-006:L1793-L1797; corrections at L2956-L2988) | user-verbatim | detector-covered F5 |

Tallies: 100 rules. detector-covered 53 (F1b: 6, F2: 11, F3: 12, F4: 9, F5: 13, F6: 2), detector_candidate 24, rubric-item 22, UNFALSIFIABLE 1 (T-06).

v2 revision note (transcript-level provenance verification, 2026-08-14): day-020.md contains five renderings of one conversation (banners at L3/L7207/L21811/L31130/L45521), so day-020 multi-source rows above are deduplicated to episodes — "same turn re-exported" marks locs that are one authorial moment, not corroboration. Sources removed on verification: d017-R14 from T-10 (quote belongs to T-22's turn), d020s5-R5 from T-61 (line inside a rejected diff), d006-R3 from T-29 (relocated to new T-100). No rule was left without support.

v2.1 retirement cascade note (2026-08-15, per author ruling recorded in threads.md "COMMIT-AFTER-RED RETIRED" + "RULING CONFIRMED"): the commit-after-RED step is retired. T-14 rewritten to its surviving core (RED proven by the observed failing run, quoted; the failing spec lands with the GREEN commit) — no rule was purely the commit ceremony, so no row is retired outright; T-20's third-commit clause dropped. The F1 commit-grammar detector family is retired as an instrument (.coordination/commit-after-red-review.md); its successor is the transcript family F1b (.coordination/detectors/README.md, f1b_red_first_in_time.md), which covers T-10, T-11, T-12, T-14, T-17, T-33 — those rows now read detector-covered F1b. The five formerly F1-flagged rules F1b cannot mechanize (T-01, T-02, T-03, T-04, T-19) are re-flagged rubric-item with per-row reasons.
