# Rule index — tdd-bdd skill

Every T-NN in `.claude/skills/tdd-bdd/` traced to its sources. Provenance ranks per compile policy: user-verbatim > user-paraphrase > agent-synthesis; ledger resolutions override all. Flags: detector-covered (F1-red-first-grammar / F2-assertion-integrity / F3-minimality / F4-layering / F5-claim-vs-action / F6-refactor-honesty), detector_candidate (mechanically checkable, no established family), rubric-item (LLM-judge assessable), UNFALSIFIABLE (no test exists — flagged per the author's own falsifiability principle).

| T | source | provenance | flag |
|---|--------|------------|------|
| T-01 | v2/day-009.yaml d009-R1 (day-009:L945-L946) | user-verbatim | detector-covered F1 |
| T-02 | CLAUDE.md:123-124 + ledger L-14 | author-restored CLAUDE.md + ledger | detector-covered F1 |
| T-03 | v2/day-019.yaml d019-R8 (day-019:L1951, L3899) | user-verbatim | detector-covered F1 |
| T-04 | v2/day-012.yaml d012-R5 (L1338); v2/day-019.yaml d019-R7 (L1859); v2/day-018.yaml d018-R1 (L1242) | user-verbatim | detector-covered F1 |
| T-05 | ledger L-05 (winner: v2/day-009.yaml d009-R2, day-009:L7329-L7331) | user-verbatim via ledger | detector_candidate (fake-green: hardcoded literal matching acceptance expectation) |
| T-06 | ledger L-02 (author ruling 2026-08-13; root v2/day-007.yaml d007-R3, day-007:L570-L573) | author-ruled + user-verbatim | UNFALSIFIABLE (a permission whose phase boundary has no crisp test; only the say-so clause is observable) |
| T-07 | v2/day-017.yaml d017-R13 (day-017:L1877) | user-verbatim | rubric-item |
| T-08 | v2/day-015.yaml d015-R13 (day-015:L691) | user-verbatim | rubric-item |
| T-09 | v2/day-011.yaml d011-R8 (L7172); v2/day-012.yaml d012-R9 (L2804) | user-verbatim | detector-covered F5 |
| T-10 | v2/day-002.yaml d002-R1 (L1516); v2/day-017.yaml d017-R14 (L1556); v2/day-010.yaml d010-R1 (L2881) | user-verbatim | detector-covered F1 |
| T-11 | v2/day-002.yaml d002-R2 (day-002:L1768) | user-verbatim | detector-covered F1 |
| T-12 | v2/day-019.yaml d019-R2 (day-019:L336) | user-paraphrase | detector-covered F1 |
| T-13 | v2/day-019.yaml d019-R3 (L3806); v2/day-021.yaml d021-R6 (L4170) | user-verbatim | rubric-item |
| T-14 | ledger L-14; CLAUDE.md:127, :235-238; threads.md:27 rationale | author-restored + user-paraphrase | detector-covered F1 |
| T-15 | v2/day-012.yaml d012-R6 (L1772); v2/day-019.yaml d019-R4 (L3718); CLAUDE.md:128 | user-verbatim | detector-covered F3 |
| T-16 | v2/day-012.yaml d012-R7 (day-012:L1975) | user-verbatim | detector-covered F3 |
| T-17 | v2/day-018.yaml d018-R6 (L817); v2/day-016.yaml d016-R9 (L6889); CLAUDE.md:129-130 | user-verbatim | detector-covered F1 |
| T-18 | v2/day-019.yaml d019-R6 (L3131); v2/day-018.yaml d018-R7 (L1125) | user-verbatim | rubric-item |
| T-19 | v2/day-020-s1.yaml d020s1-R3 (L1394); s2-R1 (L10111); s4-R1 (L23603) | user-verbatim | detector-covered F1 |
| T-20 | v2/day-020-s1.yaml d020s1-R13 (L1823); s4-R3 (L24302); CLAUDE.md:132 (per L-14: third commit) | user-verbatim | detector-covered F6 |
| T-21 | v2/day-010.yaml d010-R9 (L3944); v2/day-020-s3.yaml d020s3-R19 (L14822); s5-R9 (L55723) | agent-synthesis | detector-covered F6 |
| T-22 | v2/day-017.yaml d017-R4 (L1608), d017-R5 (L1609); v2/day-020-s2.yaml d020s2-R12 (L11629) | user-verbatim + user-paraphrase | detector_candidate (old name surviving a rename commit) |
| T-23 | v2/day-020-s2.yaml d020s2-R11 (L10211); s4-R4 (L23690) | user-verbatim | detector-covered F5 |
| T-24 | v2/day-020-s3.yaml d020s3-R8 (day-020:L16895) | user-verbatim | rubric-item |
| T-25 | v2/day-010.yaml d010-R8 (day-010:L2908) | user-verbatim | detector_candidate (phase statement present in transcript) |
| T-26 | v2/day-021.yaml d021-R3 (L3576), d021-R4 (L3613) | user-verbatim | detector-covered F5 |
| T-27 | v2/day-009.yaml d009-R12 (L7453); v2/day-007.yaml d007-R5 (L1055-L1056); CLAUDE.md tdd_discipline checklist | user-verbatim | detector-covered F5 |
| T-28 | v2/day-003.yaml d003-R1 (L1674-L1693); v2/day-004.yaml d004-R3 (L5520), d004-R4 (L5652) | user-verbatim | detector_candidate (gate-integrity: skip flags / no-verify in transcript) |
| T-29 | v2/day-003.yaml d003-R3 (L1273-L1397); v2/day-004.yaml d004-R1 (L5387), R2 (L5363), R5, R7 (L2886), R8 (L722), R9 (L4254); v2/day-002.yaml d002-R18 (L1518); v2/day-006.yaml d006-R3 (L1795) | user-verbatim | detector-covered F5 |
| T-30 | v2/day-006.yaml d006-R2 (day-006:L3277) | user-verbatim | detector-covered F5 |
| T-31 | v2/day-003.yaml d003-R15 (day-003:L147-L166, L259-L283) | agent-synthesis | detector-covered F5 |
| T-32 | v2/day-020-s1.yaml d020s1-R25 (L7061); s4-R18 (L30976); s5-R6 (L55976) | user-verbatim + agent-synthesis | detector_candidate (hand-reversal diff vs revert commit in DAG) |
| T-33 | v2/day-021.yaml d021-R12 (day-021:L7469) | user-verbatim | detector-covered F1 |
| T-34 | v2/day-006.yaml d006-R1 (day-006:L2996) | user-verbatim | detector-covered F5 |
| T-35 | v2/day-002.yaml d002-R6 (day-002:L926); CLAUDE.md code_style Tests | user-verbatim | detector_candidate (filename check) |
| T-36 | v2/day-009.yaml d009-R8 (L5508); v2/day-017.yaml d017-R2 (L2453); v2/day-020-s1.yaml d020s1-R14 (L2528); s2-R8 (L12825) | user-verbatim | detector_candidate (spec-tree-naming: mechanism nouns in names) |
| T-37 | v2/day-007.yaml d007-R10 (day-007:L2712-L2713) | user-verbatim | detector_candidate (nesting depth) |
| T-38 | ledger L-06; v2/day-017.yaml d017-R3 (L2127); v2/day-020-s2.yaml d020s2-R10 (L13202); v2/day-011.yaml d011-R3 (L11634), R4 (L12323), R5 (L5461); CLAUDE.md:100-101 | user-verbatim via ledger | detector_candidate (docstring on non-skipped spec) |
| T-39 | v2/day-012.yaml d012-R4 (L1244); v2/day-010.yaml d010-R2 (L2829) | user-paraphrase + agent-synthesis | detector_candidate (pass/skip-only bodies) |
| T-40 | v2/day-012.yaml d012-R3 (day-012:L1074) | user-verbatim | detector_candidate (two-move landing in DAG) |
| T-41 | v2/day-002.yaml d002-R5 (L2400); v2/day-019.yaml d019-R13 (L4355) | user-verbatim | detector-covered F3 |
| T-42 | v2/day-007.yaml d007-R11 (day-007:L2712) | user-verbatim | detector_candidate (per-test imports) |
| T-43 | v2/day-020-s1.yaml d020s1-R4 (L1271); s2-R2 (L9791); s4-R2 (L23459) | user-verbatim | rubric-item |
| T-44 | v2/day-009.yaml d009-R13 (day-009:L945) | user-verbatim | rubric-item |
| T-45 | ledger L-16; v2/day-005.yaml d005-R12 (day-005:L1555) | user-verbatim via ledger | detector_candidate (annotations in spec files) |
| T-46 | v2/day-009.yaml d009-R9 (day-009:L5426) | user-verbatim | detector_candidate (specs importing underscore names) |
| T-47 | v2/day-011.yaml d011-R7 (L1673); v2/day-020-s3.yaml d020s3-R6 (L14533) | user-verbatim | rubric-item |
| T-48 | v2/day-021.yaml d021-R1 (day-021:L1302) | user-verbatim | detector-covered F3 |
| T-49 | v2/day-012.yaml d012-R1 (day-012:L946) | user-verbatim | detector_candidate (spec-preservation: diff deletes existing it_ functions) |
| T-50 | v2/day-019.yaml philosophy (L4702); v2/day-018.yaml d018-R5 (L578) | user-verbatim | rubric-item |
| T-51 | v2/day-002.yaml d002-R3 (day-002:L1625-L1637) | agent-synthesis | detector-covered F2 |
| T-52 | ledger L-01 (ratified 2026-08-13); v2/day-019.yaml d019-R10 (L5011) | author-ruled + user-verbatim | detector-covered F2 |
| T-53 | ledger L-01(b); v2/day-020-s1.yaml d020s1-R11 (L2575); s2-R9 (L13073) | user-verbatim via ledger | detector-covered F2 |
| T-54 | v2/day-015.yaml d015-R2 (L1060-L1061); v2/day-016.yaml d016-R7 (L2642) | user-verbatim | detector-covered F2 |
| T-55 | v2/day-011.yaml d011-R1 (L2091), d011-R2 (L3629) | agent-synthesis | detector-covered F2 |
| T-56 | v2/day-020-s5.yaml d020s5-R4 (day-020:L56044) | user-verbatim | rubric-item |
| T-57 | v2/day-019.yaml d019-R1 (day-019:L303, L574) | user-paraphrase | detector-covered F2 |
| T-58 | v2/day-009.yaml d009-R3 (day-009:L7266-L7326) | user-verbatim | detector-covered F2 |
| T-59 | v2/day-018.yaml d018-R4 (L592), d018-R2 (L1260), d018-R3 (L516) | user-verbatim | detector-covered F2 |
| T-60 | v2/day-020-s1.yaml d020s1-R5 (L6763), R6 (L6817); s3-R1 (L21047), R2 (L21101); s4-R5 (L30732) | user-verbatim | detector-covered F2 |
| T-61 | v2/day-011.yaml d011-R10 (L11951); v2/day-020-s5.yaml d020s5-R5 (L56005) | agent-synthesis | detector-covered F4 |
| T-62 | v2/day-020-s1.yaml d020s1-R12 (L2257); s2-R3 (L12182); s3-R7 (L14591); s4-R13 (L24954) | user-verbatim | rubric-item |
| T-63 | v2/day-021.yaml d021-R8 (L3437), d021-R7 (L2203) | user-verbatim | detector_candidate (unused mock configuration) |
| T-64 | v2/day-010.yaml d010-R6 (day-010:L5782) | user-verbatim | detector-covered F2 |
| T-65 | v2/day-007.yaml d007-R6 (day-007:L884-L1084) | agent-synthesis | detector-covered F5 |
| T-66 | v2/day-019.yaml d019-R9 (L4471); v2/day-020-s1.yaml d020s1-R1 (L372) | user-verbatim | detector-covered F4 |
| T-67 | v2/day-005.yaml d005-R5 (day-005:L2148-L2150) | user-verbatim | detector-covered F4 |
| T-68 | v2/day-005.yaml d005-R6 (day-005:L2082-L2150) | user-verbatim | rubric-item |
| T-69 | v2/day-007.yaml d007-R4 (day-007:L658-L659) | user-verbatim | detector-covered F4 |
| T-70 | v2/day-020-s1.yaml d020s1-R10 (L3643); s3-R4 (L15196); s4-R8 (L27222) | user-verbatim | detector-covered F4 |
| T-71 | v2/day-020-s1.yaml d020s1-R2 (L2424); s2-R7 (L12486); s3-R5 (L15990); s4-R6 (L25125) | user-verbatim | detector-covered F4 |
| T-72 | ledger L-09; v2/day-010.yaml d010-R5 (L5911); v2/day-009.yaml d009-R11 caveat (L5037, L6043-L6061) | user-verbatim via ledger | detector-covered F4 |
| T-73 | v2/day-009.yaml d009-R10 (day-009:L6566-L6606) | agent-synthesis | detector_candidate (monkeypatch + subprocess in one spec) |
| T-74 | v2/day-010.yaml d010-R4 (day-010:L3304) | user-verbatim | detector-covered F4 |
| T-75 | v2/day-002.yaml d002-R14 (L2128); v2/day-016.yaml d016-R6 (L1237) | user-verbatim + agent-synthesis | detector_candidate (absolute home paths / usernames in tree) |
| T-76 | v2/day-010.yaml d010-R7 (L1549); v2/day-015.yaml d015-R3 (L1314-L1318); v2/day-020-s1.yaml d020s1-R7 (L4632); s3-R3 (L17043); s4-R9 (L28428) | user-verbatim + agent-synthesis | detector_candidate (fixture-provenance: hand-authored fixture rows) |
| T-77 | v2/day-013.yaml d013-R2 (L709-L869); v2/day-012.yaml d012-R8 (L2255) | user-verbatim | detector-covered F5 |
| T-78 | v2/day-021.yaml d021-R21 (day-021:L7068) | user-verbatim | detector_candidate (wall-clock time in specs over frozen fixtures) |
| T-79 | v2/day-020-s4.yaml d020s4-R11 (day-020:L30571) | user-verbatim | detector_candidate (spec-referenced empty dirs untracked) |
| T-80 | v2/day-019.yaml d019-R12 (day-019:L4651) | user-verbatim | rubric-item |
| T-81 | v2/day-019.yaml d019-R11 (L4869); v2/day-021.yaml d021-R10 (L2348) | user-verbatim + user-paraphrase | rubric-item |
| T-82 | v2/day-021.yaml d021-R9 (day-021:L2215) | user-verbatim | detector_candidate (patch-handle naming) |
| T-83 | v2/day-020-s1.yaml d020s1-R9 (L2796); s2-R6 (L13169); s4-R7 (L25950); v2/day-021.yaml d021-R2 (L2889) | user-verbatim + user-paraphrase + agent-synthesis | detector-covered F4 |
| T-84 | v2/day-020-s1.yaml d020s1-R8 (L522); s2-R4 (L8178), R5 (L8801) | user-verbatim | rubric-item |
| T-85 | v2/day-016.yaml d016-R8 (L7169); v2/day-007.yaml d007-R7 (L1799-L1800); CLAUDE.md package_structure | user-verbatim | detector-covered F3 |
| T-86 | v2/day-009.yaml d009-R4 (L6672-L6674); v2/day-002.yaml d002-R15 (L2174-L2194); v2/day-007.yaml d007-R8 (L1859-L1863); v2/day-020-s4.yaml d020s4-R15 (L24864) | user-verbatim + user-paraphrase + agent-synthesis | detector-covered F3 |
| T-87 | v2/day-009.yaml d009-R6 (L5531), R7 (L4645); v2/day-020-s3.yaml d020s3-R9 (L16931); s5-R2 (L55643) | user-verbatim + agent-synthesis | detector-covered F5 |
| T-88 | v2/day-020-s5.yaml d020s5-R1 (L55187); v2/day-007.yaml d007-R7 (L1799); v2/day-019.yaml d019-R5 (L2473) | user-verbatim | detector-covered F3 |
| T-89 | v2/day-009.yaml d009-R5 (L6334-L6335); v2/day-011.yaml d011-R6 (L2216); v2/day-020-s5.yaml d020s5-R3 (L54929) | user-verbatim | detector-covered F3 |
| T-90 | v2/day-021.yaml d021-R5 (L4169), d021-R6 (L4170) | user-verbatim | rubric-item |
| T-91 | v2/day-010.yaml d010-R3 (day-010:L1875) | agent-synthesis | detector-covered F2 |
| T-92 | v2/day-007.yaml d007-R9 (day-007:L2707-L2708) | user-verbatim | detector-covered F3 |
| T-93 | v2/day-002.yaml d002-R16 (L1023); v2/day-003.yaml d003-R9 (L2118); v2/day-004.yaml d004-R16 (L4781); v2/day-015.yaml d015-R11 (L3113-L3197) | user-verbatim | detector-covered F3 |
| T-94 | v2/day-018.yaml d018-R8 (day-018:L1167) | user-verbatim | detector-covered F3 |
| T-95 | v2/day-020-s4.yaml d020s4-R19 (day-020:L23626) | user-verbatim | rubric-item |
| T-96 | v2/day-015.yaml d015-R1 (L897-L926); v2/day-014.yaml d014-R6 (L199-L204) | user-verbatim + agent-synthesis | detector_candidate (production-file edits during exploratory probing) |
| T-97 | v2/day-010.yaml d010-R11 (day-010:L4372) | agent-synthesis | detector_candidate (lint-suppression markers added) |
| T-98 | v2/day-003.yaml d003-R5 (day-003:L491-L531) | user-verbatim | detector-covered F5 |
| T-99 | v2/day-021.yaml d021-R11 (day-021:L2432) | user-verbatim | detector-covered F3 |

Tallies: 99 rules. detector-covered 57 (F1: 11, F2: 11, F3: 12, F4: 9, F5: 12, F6: 2), detector_candidate 24, rubric-item 17, UNFALSIFIABLE 1 (T-06).
