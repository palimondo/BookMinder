# Disposition — every skill_target:tdd-bdd corpus entry

Each of the 194 tdd-bdd-targeted rules in .coordination/mining/v2/ dispositioned against the compiled skill. compiled = primary source of a T rule; merged-duplicate = absorbed into an existing T rule; rejected = not compiled, reason given; reroute = belongs to another compile target. Ledger resolutions noted where they governed the outcome.

| corpus rule | disposition |
|---|---|
| d002-R1 | compiled -> T-10 |
| d002-R2 | compiled -> T-11 |
| d002-R3 | compiled -> T-51 |
| d002-R4 | merged-duplicate -> T-38 (blanket docstring ban superseded by ledger L-06; surviving kernel — no docstrings on implemented specs — lives in T-38) |
| d002-R5 | compiled -> T-41 |
| d002-R6 | compiled -> T-35 |
| d002-R14 | compiled -> T-75 |
| d002-R15 | merged-duplicate -> T-86 |
| d002-R16 | compiled -> T-93 |
| d002-R18 | merged-duplicate -> T-29 |
| d003-R1 | compiled -> T-28 |
| d003-R3 | compiled -> T-29 |
| d003-R5 | compiled -> T-98 |
| d003-R9 | merged-duplicate -> T-93 |
| d003-R15 | compiled -> T-31 |
| d004-R1 | merged-duplicate -> T-29 |
| d004-R2 | merged-duplicate -> T-29 |
| d004-R3 | merged-duplicate -> T-28 |
| d004-R4 | merged-duplicate -> T-28 |
| d004-R5 | merged-duplicate -> T-29 |
| d004-R6 | merged-duplicate -> T-29 (migration-diff verification folded into execute-and-observe family) |
| d004-R7 | merged-duplicate -> T-29 |
| d004-R8 | merged-duplicate -> T-29 |
| d004-R9 | merged-duplicate -> T-29 |
| d004-R16 | merged-duplicate -> T-93 |
| d005-R5 | compiled -> T-67 |
| d005-R6 | compiled -> T-68 |
| d006-R1 | compiled -> T-34 |
| d006-R2 | compiled -> T-30 |
| d006-R3 | compiled -> T-100 (v2: methodology-improvement claims split out of T-29 per provenance verification — T-29 governs executing a change before calling it ready, not claiming method efficacy; incomparable-stages clause added) |
| d007-R3 | compiled -> T-06 (as ratified by ledger L-02: phase-scoped exemption, miner narrowing rejected) |
| d007-R4 | compiled -> T-69 |
| d007-R5 | merged-duplicate -> T-27 |
| d007-R6 | compiled -> T-65 |
| d007-R7 | compiled -> T-88 (also feeds T-85/T-86) |
| d007-R8 | merged-duplicate -> T-86 |
| d007-R9 | compiled -> T-92 |
| d007-R10 | compiled -> T-37 |
| d007-R11 | compiled -> T-42 |
| d007-R18 | rejected (language/code-style rule — isinstance over cast — outside the TDD/BDD discipline surface; belongs with code-style guidance) |
| d008-R16 | reroute:project-memory (discovery-document hedging discipline — documentation claims, not spec discipline) |
| d008-R17 | reroute:project-memory (speculative content in discovery docs; its spec-side kernel — evidence before guards — is carried by T-87) |
| d009-R1 | compiled -> T-01 |
| d009-R2 | compiled -> T-05 (as ratified by ledger L-05) |
| d009-R3 | compiled -> T-58 |
| d009-R4 | merged-duplicate -> T-86 |
| d009-R5 | compiled -> T-89 |
| d009-R6 | compiled -> T-87 |
| d009-R7 | merged-duplicate -> T-87 |
| d009-R8 | compiled -> T-36 |
| d009-R9 | compiled -> T-46 |
| d009-R10 | compiled -> T-73 |
| d009-R11 | compiled -> T-72 (module-constant seam carries in-process-only caveat per ledger L-09) |
| d009-R12 | compiled -> T-27 |
| d009-R13 | compiled -> T-44 |
| d010-R1 | merged-duplicate -> T-10 |
| d010-R2 | merged-duplicate -> T-39 (v2: also feeds T-91's skip-as-stand-in clause, with the enforcement at day-010:L2881-L2908) |
| d010-R3 | compiled -> T-91 |
| d010-R4 | compiled -> T-74 |
| d010-R5 | compiled -> T-72 (front-door seam wins per ledger L-09) |
| d010-R6 | compiled -> T-64 |
| d010-R7 | compiled -> T-76 |
| d010-R8 | compiled -> T-25 |
| d010-R9 | compiled -> T-21 |
| d010-R11 | compiled -> T-97 |
| d011-R1 | compiled -> T-55 |
| d011-R2 | merged-duplicate -> T-55 |
| d011-R3 | merged-duplicate -> T-38 |
| d011-R4 | merged-duplicate -> T-38 |
| d011-R5 | merged-duplicate -> T-38 |
| d011-R6 | merged-duplicate -> T-89 |
| d011-R7 | compiled -> T-47 |
| d011-R8 | compiled -> T-09 |
| d011-R9 | merged-duplicate -> T-09 (evidence-discipline kernel: no conclusion sentences an empty result set did not produce) |
| d011-R10 | compiled -> T-61 |
| d012-R1 | compiled -> T-49 |
| d012-R2 | merged-duplicate -> T-71 (as reconciled by later layer rulings: the ONE subprocess wiring spec runs mock-free; boundary mocks are sanctioned by T-70) |
| d012-R3 | compiled -> T-40 |
| d012-R4 | compiled -> T-39 |
| d012-R5 | compiled -> T-04 (v2: also listed under T-40 — it supplies the skip-marker half T-40's other source lacks) |
| d012-R6 | compiled -> T-15 |
| d012-R7 | compiled -> T-16 |
| d012-R8 | compiled -> T-77 |
| d012-R9 | merged-duplicate -> T-09 |
| d013-R2 | merged-duplicate -> T-77 |
| d014-R6 | compiled -> T-96 |
| d015-R1 | compiled -> T-96 |
| d015-R2 | compiled -> T-54 |
| d015-R3 | compiled -> T-76 |
| d015-R11 | merged-duplicate -> T-93 (one job per script) |
| d015-R13 | compiled -> T-08 |
| d016-R6 | merged-duplicate -> T-75 |
| d016-R7 | merged-duplicate -> T-54 (incidental-datum branch) |
| d016-R8 | compiled -> T-85 |
| d016-R9 | merged-duplicate -> T-17 |
| d017-R2 | merged-duplicate -> T-36 |
| d017-R3 | compiled -> T-38 (pending-only convention per ledger L-06) |
| d017-R4 | compiled -> T-22 |
| d017-R5 | merged-duplicate -> T-22 |
| d017-R13 | compiled -> T-07 |
| d017-R14 | merged-duplicate -> T-22 (v2: verification found the cited loc L1556 holds no author turn; the quoted "Focus on TDD discipline" opens the rename-scope turn at day-017:L1608, already T-22's — previously misfiled under T-10, whose re-run clause it alone supported) |
| d018-R1 | merged-duplicate -> T-04 |
| d018-R2 | merged-duplicate -> T-59 |
| d018-R3 | merged-duplicate -> T-59 |
| d018-R4 | compiled -> T-59 |
| d018-R5 | merged-duplicate -> T-50 |
| d018-R7 | merged-duplicate -> T-18 |
| d018-R8 | compiled -> T-94 |
| d019-R1 | compiled -> T-57 |
| d019-R2 | compiled -> T-12 |
| d019-R3 | compiled -> T-13 |
| d019-R4 | merged-duplicate -> T-15 |
| d019-R5 | merged-duplicate -> T-88 |
| d019-R6 | compiled -> T-18 |
| d019-R7 | merged-duplicate -> T-04 |
| d019-R8 | compiled -> T-03 |
| d019-R9 | compiled -> T-66 |
| d019-R10 | merged-duplicate -> T-52 (exact selected set at the integration layer) |
| d019-R11 | compiled -> T-81 |
| d019-R12 | compiled -> T-80 |
| d019-R13 | merged-duplicate -> T-41 |
| d020s1-R1 | merged-duplicate -> T-66 |
| d020s1-R2 | compiled -> T-71 |
| d020s1-R3 | compiled -> T-19 |
| d020s1-R4 | compiled -> T-43 |
| d020s1-R5 | compiled -> T-60 |
| d020s1-R6 | merged-duplicate -> T-60 |
| d020s1-R7 | merged-duplicate -> T-76 |
| d020s1-R8 | compiled -> T-84 |
| d020s1-R9 | compiled -> T-83 |
| d020s1-R10 | compiled -> T-70 |
| d020s1-R11 | compiled -> T-53 (per ledger L-01) |
| d020s1-R12 | compiled -> T-62 |
| d020s1-R13 | compiled -> T-20 |
| d020s1-R14 | merged-duplicate -> T-36 |
| d020s1-R15 | rejected (exception-variable naming — general code style, not spec discipline; belongs with code-style guidance) |
| d020s1-R25 | compiled -> T-32 |
| d020s2-R1 | merged-duplicate -> T-19 |
| d020s2-R2 | merged-duplicate -> T-43 |
| d020s2-R3 | merged-duplicate -> T-62 |
| d020s2-R4 | merged-duplicate -> T-84 |
| d020s2-R5 | merged-duplicate -> T-84 |
| d020s2-R6 | merged-duplicate -> T-83 |
| d020s2-R7 | merged-duplicate -> T-71 |
| d020s2-R8 | merged-duplicate -> T-36 |
| d020s2-R9 | merged-duplicate -> T-53 (per ledger L-01: no weakening, no hardcoded census — FIXME and route to owning layer) |
| d020s2-R10 | merged-duplicate -> T-38 |
| d020s2-R11 | compiled -> T-23 |
| d020s2-R12 | merged-duplicate -> T-22 |
| d020s3-R1 | merged-duplicate -> T-60 |
| d020s3-R2 | merged-duplicate -> T-60 |
| d020s3-R3 | merged-duplicate -> T-76 |
| d020s3-R4 | merged-duplicate -> T-70 |
| d020s3-R5 | merged-duplicate -> T-71 |
| d020s3-R6 | merged-duplicate -> T-47 |
| d020s3-R7 | merged-duplicate -> T-62 |
| d020s3-R8 | compiled -> T-24 |
| d020s3-R9 | merged-duplicate -> T-87 |
| d020s3-R19 | merged-duplicate -> T-21 |
| d020s4-R1 | merged-duplicate -> T-19 |
| d020s4-R2 | merged-duplicate -> T-43 |
| d020s4-R3 | merged-duplicate -> T-20 |
| d020s4-R4 | merged-duplicate -> T-23 |
| d020s4-R5 | merged-duplicate -> T-60 |
| d020s4-R6 | merged-duplicate -> T-71 |
| d020s4-R7 | merged-duplicate -> T-83 |
| d020s4-R8 | merged-duplicate -> T-70 |
| d020s4-R9 | merged-duplicate -> T-76 |
| d020s4-R11 | compiled -> T-79 |
| d020s4-R13 | merged-duplicate -> T-62 |
| d020s4-R14 | merged-duplicate -> T-38 |
| d020s4-R15 | merged-duplicate -> T-86 |
| d020s4-R19 | compiled -> T-95 |
| d020s5-R1 | compiled -> T-88 |
| d020s5-R2 | merged-duplicate -> T-87 |
| d020s5-R3 | merged-duplicate -> T-89 |
| d020s5-R4 | compiled -> T-56 |
| d020s5-R5 | rejected (v2: retracted on verification — the cited line sits inside a diff the author rejected for non-equivalence and unrecovered motivation, day-020:L32334-L32336; no turn in the window concerns message coupling; T-56 carries the episode's actual lesson) |
| d020s5-R6 | merged-duplicate -> T-32 |
| d020s5-R9 | merged-duplicate -> T-21 |
| d021-R1 | compiled -> T-48 |
| d021-R2 | merged-duplicate -> T-83 |
| d021-R3 | compiled -> T-26 |
| d021-R4 | merged-duplicate -> T-26 |
| d021-R5 | compiled -> T-90 |
| d021-R6 | compiled -> T-13 (also feeds T-90 demonstration clause) |
| d021-R7 | merged-duplicate -> T-63 |
| d021-R8 | compiled -> T-63 |
| d021-R9 | compiled -> T-82 |
| d021-R10 | merged-duplicate -> T-81 |
| d021-R11 | compiled -> T-99 |
| d021-R12 | compiled -> T-33 |
| d021-R21 | compiled -> T-78 |
| d021-R25 | rejected (general debugging technique — reduce-to-one-line diff iteration — outside the discipline's activation moments; candidate for a future debugging skill) |

Tallies: 194 entries — compiled 98, merged-duplicate 90, rejected 4, reroute:project-memory 2. (v2: d006-R3 merged→compiled as T-100; d017-R14 refiled T-10→T-22; d020s5-R5 merged→rejected.)

v2.1 retirement cascade note (2026-08-15): commit-after-RED retired per author ruling (threads.md "COMMIT-AFTER-RED RETIRED" + "RULING CONFIRMED"). No disposition rows change — the rule postdates the mined corpus (the miners recorded its absence explicitly), so T-14 never had a corpus source: it entered the skill via ledger L-14 and the then-current CLAUDE.md, and its rewrite to the surviving core (RED proven by the observed failing run, quoted) is recorded in rule-index-tdd-bdd.md and skill-v2-changelog-tdd-bdd.md. Recorded here so the tallies' silence is legible.
