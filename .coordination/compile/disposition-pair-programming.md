# Disposition — pair-programming compile

Every pairing-shaped item in the mining corpus, dispositioned. Corpora covered: all v2 `pairing_rules` (314), all v2 `pairing_gems` (155, keyed by loc), all v2 `skill_rules` with `skill_target: pair-programming` (45), and all council-fidelity trial `pairing_rules` (92). Vocabulary: compiled→P-NN (primary source of the compiled rule), merged-duplicate→P-NN (folded into that rule), rejected(reason), reroute:tdd-bdd|project-memory|coordinator (conduct belongs to that skill, not to pairing). For gems, merged-duplicate→P-NN means the exemplary episode grounds that rule; gems carry no separate rule text.

Tallies (v2, 2026-08-14): 606 items — compiled 39, merged-duplicate 424, reroute 132 (tdd-bdd 75, coordinator 41, project-memory 16), rejected 11. Two further rules have non-corpus primaries: P-32 and P-33 compile ledger ratifications L-08 and L-04. v2 changes: p013-R7 and p003-R13 promoted merged→compiled (P-40, P-41); p006-R4 merged→rejected on transcript verification; eight sources re-dispositioned between rules — all itemized in skill-v2-changelog-pair-programming.md.

## v2 pairing_rules

| id | disposition |
|----|-------------|
| p002-R1 | merged-duplicate→P-09 |
| p002-R2 | merged-duplicate→P-01 |
| p002-R3 | compiled→P-12 |
| p002-R4 | compiled→P-14 |
| p002-R5 | reroute:tdd-bdd (requirements-dialogue-before-structure) |
| p002-R6 | merged-duplicate→P-15 |
| p002-R7 | merged-duplicate→P-14 |
| p002-R8 | merged-duplicate→P-04 |
| p002-R9 | merged-duplicate→P-28 |
| p002-R10 | merged-duplicate→P-14 |
| p002-R11 | merged-duplicate→P-01 |
| p002-R12 | merged-duplicate→P-27 |
| p002-R13 | reroute:coordinator (cost/meta-work accounting) |
| p002-R14 | merged-duplicate→P-24 |
| p003-R1 | merged-duplicate→P-18 |
| p003-R2 | compiled→P-20 |
| p003-R3 | compiled→P-16 |
| p003-R4 | merged-duplicate→P-16 |
| p003-R5 | merged-duplicate→P-01 |
| p003-R6 | merged-duplicate→P-10 |
| p003-R7 | merged-duplicate→P-14 |
| p003-R8 | reroute:tdd-bdd (gate/suppression discipline) |
| p003-R9 | merged-duplicate→P-05 |
| p003-R10 | merged-duplicate→P-23 |
| p003-R11 | merged-duplicate→P-27 |
| p003-R12 | merged-duplicate→P-17 |
| p003-R13 | compiled→P-41 (was merged-duplicate→P-28; standalone expression per pilot P-12/P-14 program — expressed by neither P-28 nor P-14) |
| p003-R14 | compiled→P-09 |
| p003-R15 | merged-duplicate→P-09 |
| p003-R16 | reroute:coordinator (delegated-investigation failure reporting) |
| p003-R17 | merged-duplicate→P-13 |
| p004-R1 | merged-duplicate→P-16 |
| p004-R2 | merged-duplicate→P-17 |
| p004-R3 | merged-duplicate→P-05 |
| p004-R4 | merged-duplicate→P-05 |
| p004-R5 | merged-duplicate→P-01 |
| p004-R6 | merged-duplicate→P-01 |
| p004-R7 | merged-duplicate→P-18 |
| p004-R8 | merged-duplicate→P-28 |
| p004-R9 | merged-duplicate→P-27 |
| p004-R10 | merged-duplicate→P-17 |
| p004-R11 | merged-duplicate→P-12 |
| p004-R12 | merged-duplicate→P-16 |
| p004-R13 | merged-duplicate→P-17 |
| p004-R14 | reroute:coordinator (outside-repo writes / authorization) |
| p005-R1 | merged-duplicate→P-16 |
| p005-R2 | merged-duplicate→P-28 |
| p005-R3 | merged-duplicate→P-02 |
| p005-R4 | merged-duplicate→P-27 |
| p005-R5 | merged-duplicate→P-14 |
| p005-R6 | merged-duplicate→P-25 |
| p005-R7 | merged-duplicate→P-20 |
| p005-R8 | merged-duplicate→P-10 |
| p005-R9 | reroute:tdd-bdd (staged-diff commit hygiene) |
| p005-R10 | merged-duplicate→P-11 |
| p005-R11 | merged-duplicate→P-08 |
| p005-R12 | merged-duplicate→P-01 |
| p005-R13 | reroute:project-memory (additive ledger convention) |
| p005-R14 | reroute:tdd-bdd (product-state-vs-mock question) |
| p006-R1 | merged-duplicate→P-09 |
| p006-R2 | merged-duplicate→P-01 |
| p006-R3 | merged-duplicate→P-14 |
| p006-R4 | rejected(verification 2026-08-14: cited turn day-006:L3455 is an evidence-backed reversal after a demanded evidence pass — the behaviour P-19 endorses, not a pressure flip) |
| p006-R5 | merged-duplicate→P-20 |
| p006-R6 | merged-duplicate→P-15 |
| p006-R7 | merged-duplicate→P-15 |
| p006-R8 | merged-duplicate→P-16 |
| p006-R9 | reroute:coordinator (permission batching) |
| p006-R10 | reroute:tdd-bdd (commit review + explicit staging) |
| p006-R11 | merged-duplicate→P-11 |
| p006-R12 | merged-duplicate→P-08 |
| p006-R13 | merged-duplicate→P-09 |
| p006-R14 | reroute:project-memory (append-only records) |
| p007-R1 | merged-duplicate→P-16 |
| p007-R2 | merged-duplicate→P-15 |
| p007-R3 | merged-duplicate→P-21 |
| p007-R4 | reroute:tdd-bdd (seam-took-effect proof) |
| p007-R5 | reroute:tdd-bdd (characterization-test naming) |
| p007-R6 | merged-duplicate→P-06 |
| p007-R7 | merged-duplicate→P-06 |
| p007-R8 | reroute:tdd-bdd (git staging hygiene) |
| p007-R9 | reroute:tdd-bdd (commit-message claims vs diff) |
| p007-R10 | reroute:tdd-bdd (sweep dead scaffolding in same commit) |
| p007-R11 | merged-duplicate→P-11 |
| p007-R12 | merged-duplicate→P-16 |
| p007-R13 | reroute:tdd-bdd (checker-silencing as design signal) |
| p007-R14 | merged-duplicate→P-02 |
| p007-R15 | merged-duplicate→P-23 |
| p008-R1 | reroute:project-memory (rationale provenance in rules files) |
| p008-R2 | merged-duplicate→P-15 |
| p008-R3 | compiled→P-10 |
| p008-R4 | merged-duplicate→P-17 |
| p008-R5 | merged-duplicate→P-24 |
| p008-R6 | merged-duplicate→P-05 |
| p008-R7 | merged-duplicate→P-15 |
| p008-R8 | merged-duplicate→P-23 |
| p008-R9 | merged-duplicate→P-23 |
| p008-R10 | reroute:project-memory (observed-once = variable) |
| p008-R11 | reroute:project-memory (discovery-doc hedging) |
| p008-R12 | merged-duplicate→P-34 |
| p008-R13 | merged-duplicate→P-36 |
| p008-R14 | merged-duplicate→P-15 |
| p008-R15 | rejected(era-specific model-attribution mechanics) |
| p009-R1 | merged-duplicate→P-15 |
| p009-R2 | merged-duplicate→P-01 |
| p009-R3 | reroute:tdd-bdd (red-at-wrong-layer signal) |
| p009-R4 | merged-duplicate→P-19 |
| p009-R5 | merged-duplicate→P-24 |
| p009-R6 | merged-duplicate→P-05 |
| p009-R7 | reroute:tdd-bdd (commit read-back) |
| p009-R8 | merged-duplicate→P-10 |
| p009-R9 | reroute:tdd-bdd (copy the existing seam) |
| p009-R10 | merged-duplicate→P-01 |
| p009-R11 | merged-duplicate→P-01 |
| p009-R12 | reroute:tdd-bdd (guard deletion + honest checker satisfaction) |
| p009-R13 | merged-duplicate→P-33 |
| p010-R1 | merged-duplicate→P-13 |
| p010-R2 | merged-duplicate→P-02 |
| p010-R3 | merged-duplicate→P-06 |
| p010-R4 | merged-duplicate→P-06 |
| p010-R5 | merged-duplicate→P-29 |
| p010-R6 | merged-duplicate→P-37 |
| p010-R7 | merged-duplicate→P-24 |
| p010-R8 | merged-duplicate→P-08 |
| p010-R9 | merged-duplicate→P-09 |
| p010-R10 | merged-duplicate→P-04 |
| p010-R11 | merged-duplicate→P-21 |
| p010-R12 | merged-duplicate→P-39 |
| p011-R1 | reroute:tdd-bdd (red test vs production change) |
| p011-R2 | merged-duplicate→P-04 |
| p011-R3 | merged-duplicate→P-27 |
| p011-R4 | reroute:tdd-bdd (never weaken project checks) |
| p011-R5 | merged-duplicate→P-16 |
| p011-R6 | merged-duplicate→P-09 |
| p011-R7 | rejected(harness mechanics: tool payloads vs calls) |
| p011-R8 | rejected(harness whole-file edit mechanics) |
| p011-R9 | merged-duplicate→P-22 |
| p011-R10 | merged-duplicate→P-10 |
| p011-R11 | merged-duplicate→P-14 |
| p011-R12 | merged-duplicate→P-15 |
| p012-R1 | merged-duplicate→P-05 |
| p012-R2 | reroute:tdd-bdd (fixture-bent-to-test) |
| p012-R3 | merged-duplicate→P-10 |
| p012-R4 | merged-duplicate→P-04 |
| p012-R5 | merged-duplicate→P-23 (was →P-22; an underspecified card is a question to ask, not a minimal-constraint lesson) |
| p012-R6 | merged-duplicate→P-10 |
| p012-R7 | merged-duplicate→P-14 |
| p012-R8 | merged-duplicate→P-29 |
| p012-R9 | merged-duplicate→P-35 |
| p012-R10 | merged-duplicate→P-33 |
| p012-R11 | merged-duplicate→P-24 |
| p013-R1 | merged-duplicate→P-15 |
| p013-R2 | merged-duplicate→P-05 |
| p013-R3 | merged-duplicate→P-19 |
| p013-R4 | merged-duplicate→P-24 |
| p013-R5 | merged-duplicate→P-05 |
| p013-R6 | merged-duplicate→P-10 |
| p013-R7 | compiled→P-40 (was merged-duplicate→P-14; standalone expression per pilot P-12/P-14 program) |
| p013-R8 | rejected(harness identity mechanics) |
| p013-R9 | rejected(era-specific slash-command file mechanics) |
| p013-R10 | merged-duplicate→P-15 |
| p014-R1 | merged-duplicate→P-16 |
| p014-R2 | merged-duplicate→P-24 |
| p014-R3 | merged-duplicate→P-10 |
| p014-R4 | merged-duplicate→P-15 |
| p014-R5 | merged-duplicate→P-14 |
| p014-R6 | reroute:coordinator (probe batching efficiency) |
| p014-R7 | merged-duplicate→P-16 |
| p014-R8 | reroute:coordinator (persistence of findings) |
| p015-R1 | merged-duplicate→P-27 |
| p015-R2 | merged-duplicate→P-01 |
| p015-R3 | merged-duplicate→P-27 |
| p015-R4 | merged-duplicate→P-23 |
| p015-R5 | merged-duplicate→P-20 |
| p015-R6 | merged-duplicate→P-05 |
| p015-R7 | merged-duplicate→P-04 |
| p015-R8 | merged-duplicate→P-27 |
| p015-R9 | merged-duplicate→P-09 |
| p015-R10 | merged-duplicate→P-01 |
| p015-R11 | merged-duplicate→P-23 |
| p016-R1 | merged-duplicate→P-05 |
| p016-R2 | compiled→P-05 |
| p016-R3 | merged-duplicate→P-05 |
| p016-R4 | merged-duplicate→P-05 |
| p016-R5 | merged-duplicate→P-01 |
| p016-R6 | merged-duplicate→P-10 |
| p016-R7 | merged-duplicate→P-27 |
| p016-R8 | merged-duplicate→P-18 |
| p016-R9 | reroute:tdd-bdd (tool design from story cards) |
| p016-R10 | merged-duplicate→P-10 |
| p016-R11 | reroute:project-memory (DB exploration conventions) |
| p017-R1 | merged-duplicate→P-11 |
| p017-R2 | merged-duplicate→P-18 |
| p017-R3 | merged-duplicate→P-15 |
| p017-R4 | reroute:tdd-bdd (plan ordering from discipline) |
| p017-R5 | merged-duplicate→P-19 |
| p017-R6 | merged-duplicate→P-15 (was →P-23; substance is change-only-what-was-named, per pairing-2) |
| p017-R7 | merged-duplicate→P-24 |
| p017-R8 | merged-duplicate→P-24 |
| p017-R9 | merged-duplicate→P-33 |
| p017-R10 | merged-duplicate→P-35 |
| p017-R11 | compiled→P-39 |
| p017-R12 | rejected(project-specific restricted-path mechanics) |
| p018-R1 | merged-duplicate→P-01 |
| p018-R2 | merged-duplicate→P-15 (was →P-23; sources P-15's fix-must-not-disable-built-behaviour clause) |
| p018-R3 | merged-duplicate→P-14 |
| p018-R4 | reroute:coordinator (read-freely/ask-before-writes authorization) |
| p018-R5 | merged-duplicate→P-10 |
| p018-R6 | merged-duplicate→P-05 |
| p018-R7 | merged-duplicate→P-04 |
| p018-R8 | merged-duplicate→P-02 |
| p018-R9 | merged-duplicate→P-12 |
| p018-R10 | merged-duplicate→P-15 |
| p018-R11 | merged-duplicate→P-01 |
| p018-R12 | merged-duplicate→P-39 |
| p018-R13 | merged-duplicate→P-19 |
| p018-R14 | merged-duplicate→P-29 |
| p018-R15 | reroute:project-memory (project-script preference) |
| p019-R1 | merged-duplicate→P-10 |
| p019-R2 | merged-duplicate→P-01 |
| p019-R3 | merged-duplicate→P-03 |
| p019-R4 | reroute:tdd-bdd (which layer can falsify) |
| p019-R5 | merged-duplicate→P-15 |
| p019-R6 | merged-duplicate→P-30 |
| p019-R7 | merged-duplicate→P-09 |
| p019-R8 | compiled→P-28 |
| p019-R9 | merged-duplicate→P-05 |
| p019-R10 | merged-duplicate→P-17 |
| p019-R11 | merged-duplicate→P-32 (superseded in-context-only form, recorded as such per L-08) |
| p019-R12 | merged-duplicate→P-30 |
| p019-R13 | merged-duplicate→P-34 |
| p019-R14 | merged-duplicate→P-33 |
| p020s1-R1 | compiled→P-15 |
| p020s1-R2 | merged-duplicate→P-15 |
| p020s1-R3 | reroute:coordinator (verbatim subagent output) |
| p020s1-R4 | reroute:coordinator (show prompt before sending) |
| p020s1-R5 | reroute:coordinator (tool calibration) |
| p020s1-R6 | reroute:coordinator (task batching for subagents) |
| p020s1-R7 | reroute:coordinator (cheapest evidence source first) |
| p020s1-R8 | merged-duplicate→P-33 |
| p020s1-R9 | compiled→P-04 |
| p020s1-R10 | merged-duplicate→P-09 |
| p020s1-R11 | merged-duplicate→P-11 |
| p020s1-R12 | reroute:tdd-bdd (test-migration diffing) |
| p020s1-R13 | merged-duplicate→P-05 |
| p020s1-R14 | merged-duplicate→P-05 |
| p020s1-R15 | merged-duplicate→P-15 |
| p020s1-R16 | compiled→P-19 |
| p020s1-R17 | merged-duplicate→P-01 |
| p020s2-R1 | merged-duplicate→P-15 |
| p020s2-R2 | merged-duplicate→P-28 (was →P-21; sources P-28's explain-the-name-you-chose clause) |
| p020s2-R3 | merged-duplicate→P-21 |
| p020s2-R4 | merged-duplicate→P-01 |
| p020s2-R5 | merged-duplicate→P-15 |
| p020s2-R6 | merged-duplicate→P-16 |
| p020s2-R7 | merged-duplicate→P-17 (falsifiability criterion for options) |
| p020s2-R8 | merged-duplicate→P-23 |
| p020s2-R9 | merged-duplicate→P-15 |
| p020s2-R10 | merged-duplicate→P-04 |
| p020s2-R11 | merged-duplicate→P-38 |
| p020s2-R12 | merged-duplicate→P-35 |
| p020s2-R13 | merged-duplicate→P-33 |
| p020s2-R14 | merged-duplicate→P-35 |
| p020s3-R1 | merged-duplicate→P-27 |
| p020s3-R2 | merged-duplicate→P-10 |
| p020s3-R3 | reroute:coordinator (verbatim delegated output) |
| p020s3-R4 | reroute:coordinator (subagent calibration) |
| p020s3-R5 | reroute:coordinator (subagent prompt batching) |
| p020s3-R6 | reroute:coordinator (evidence ladder) |
| p020s3-R7 | merged-duplicate→P-15 |
| p020s3-R8 | merged-duplicate→P-05 |
| p020s3-R9 | merged-duplicate→P-09 |
| p020s3-R10 | merged-duplicate→P-04 |
| p020s3-R11 | merged-duplicate→P-05 |
| p020s3-R12 | merged-duplicate→P-39 |
| p020s3-R13 | merged-duplicate→P-27 |
| p020s4-R1 | merged-duplicate→P-03 |
| p020s4-R2 | merged-duplicate→P-23 |
| p020s4-R3 | merged-duplicate→P-15 |
| p020s4-R4 | merged-duplicate→P-05 |
| p020s4-R5 | compiled→P-27 |
| p020s4-R6 | merged-duplicate→P-10 |
| p020s4-R7 | merged-duplicate→P-09 |
| p020s4-R8 | reroute:coordinator (verbatim subagent output) |
| p020s4-R9 | reroute:coordinator (show prompt before sending) |
| p020s4-R10 | reroute:coordinator (cheap source first, one day at a time) |
| p020s4-R11 | merged-duplicate→P-04 |
| p020s4-R12 | merged-duplicate→P-33 |
| p020s4-R13 | reroute:coordinator (plain-tool preference) |
| p020s5-R1 | merged-duplicate→P-23 |
| p020s5-R2 | merged-duplicate→P-01 |
| p020s5-R3 | merged-duplicate→P-23 |
| p020s5-R4 | merged-duplicate→P-20 |
| p020s5-R5 | merged-duplicate→P-22 |
| p020s5-R6 | merged-duplicate→P-23 |
| p020s5-R7 | merged-duplicate→P-23 |
| p020s5-R8 | reroute:coordinator (permission scope) |
| p020s5-R9 | merged-duplicate→P-24 |
| p020s5-R10 | merged-duplicate→P-33 |
| p021-R1 | merged-duplicate→P-06 |
| p021-R2 | merged-duplicate→P-22 |
| p021-R3 | merged-duplicate→P-03 |
| p021-R4 | merged-duplicate→P-09 |
| p021-R5 | compiled→P-25 |
| p021-R6 | compiled→P-18 |
| p021-R7 | merged-duplicate→P-13 (was →P-28; the lesson is count-before-arguing, same author turn as trial p021t-R14) |
| p021-R8 | merged-duplicate→P-14 |
| p021-R9 | merged-duplicate→P-10 |
| p021-R10 | reroute:coordinator (delegation briefing) |
| p021-R11 | reroute:coordinator (subagent report = lead) |
| p021-R12 | merged-duplicate→P-38 |
| p021-R13 | merged-duplicate→P-33 |
| p021-R14 | merged-duplicate→P-23 |
| p021-R15 | merged-duplicate→P-04 |

## Council-fidelity trial pairing_rules (.coordination/mining/pairing/)

| id | disposition |
|----|-------------|
| day-010 p010-R1 | merged-duplicate→P-01 (partner-run commands variant) |
| day-010 p010-R2 | merged-duplicate→P-04 |
| day-010 p010-R3 | compiled→P-08 |
| day-010 p010-R4 | compiled→P-06 |
| day-010 p010-R5 | compiled→P-13 |
| day-010 p010-R6 | reroute:tdd-bdd (commit message shorter than diff) |
| day-010 p010-R7 | reroute:tdd-bdd (comment/docstring deletion) |
| day-010 p010-R8 | compiled→P-02 |
| day-010 p010-R9 | reroute:tdd-bdd (fix the seam, not the label) |
| day-010 p010-R10 | reroute:tdd-bdd (dead defensive branch) |
| day-010 p010-R11 | merged-duplicate→P-04 |
| day-010 p010-R12 | reroute:tdd-bdd (git mv hygiene) |
| day-010 p010-R13 | merged-duplicate→P-24 (skipped instruction named, not buried) |
| day-010 p010-R14 | compiled→P-17 |
| day-010 p010-R15 | merged-duplicate→P-21 |
| day-010 p010-R16 | reroute:tdd-bdd (no self-skipping tests) |
| day-010 p010-R17 | merged-duplicate→P-18 |
| day-010 p010-R18 | compiled→P-29 |
| day-010 p010-R19 | merged-duplicate→P-32 (fork-isolation protocol origin) |
| day-010 p010-R20 | compiled→P-35 |
| day-010 p010-R21 | merged-duplicate→P-33 (traceable attribution) |
| day-010 p010-R22 | compiled→P-37 |
| day-010 p010-R23 | merged-duplicate→P-33 (apply the namesake's own method) |
| day-010 p010-R24 | reroute:tdd-bdd (no test-awareness in production) |
| day-010 p010-R25 | merged-duplicate→P-39 (simplest-idea check) |
| day-019 p019-R1 | merged-duplicate→P-05 (fixture mutation halt) |
| day-019 p019-R2 | merged-duplicate→P-15 (whole edit sequence first) |
| day-019 p019-R3 | reroute:project-memory (docs record data as-is) |
| day-019 p019-R4 | compiled→P-31 (WHY of full context per voice; ban half superseded per L-08) |
| day-019 p019-R5 | compiled→P-30 |
| day-019 p019-R6 | compiled→P-34 |
| day-019 p019-R7 | merged-duplicate→P-33 (personas never assert project facts) |
| day-019 p019-R8 | merged-duplicate→P-33 (history in front of the voices) |
| day-019 p019-R9 | compiled→P-23 |
| day-019 p019-R10 | compiled→P-01 |
| day-019 p019-R11 | reroute:tdd-bdd (refactor question after every GREEN) |
| day-019 p019-R12 | reroute:tdd-bdd (commit at phase boundaries) |
| day-019 p019-R13 | reroute:tdd-bdd (delete untested code) |
| day-019 p019-R14 | reroute:tdd-bdd (implement exactly the failing assertion) |
| day-019 p019-R15 | reroute:tdd-bdd (one scenario at a time) |
| day-019 p019-R16 | merged-duplicate→P-10 |
| day-019 p019-R17 | compiled→P-11 |
| day-019 p019-R18 | compiled→P-21 |
| day-019 p019-R19 | merged-duplicate→P-17 |
| day-019 p019-R20 | reroute:tdd-bdd (missing lower-level test) |
| day-019 p019-R21 | reroute:tdd-bdd (layer knowledge boundaries) |
| day-019 p019-R22 | reroute:tdd-bdd (integration-boundary assertions) |
| day-019 p019-R23 | reroute:tdd-bdd (simplest double) |
| day-019 p019-R24 | merged-duplicate→P-22 (double carries only fields under test) |
| day-019 p019-R25 | reroute:tdd-bdd (assertion failure messages) |
| day-019 p019-R26 | reroute:tdd-bdd (redundant comments) |
| day-019 p019-R27 | merged-duplicate→P-03 (record deliberate breakage) |
| day-019 p019-R28 | merged-duplicate→P-06 |
| day-019 p019-R29 | compiled→P-24 |
| day-019 p019-R30 | merged-duplicate→P-01 |
| day-019 p019-R31 | rejected(harness cwd mechanics) |
| day-019 p019-R32 | merged-duplicate→P-15 (approval-gated edit pacing) |
| day-019 p019-R33 | reroute:coordinator (todo ledger discipline) |
| day-019 p019-R34 | compiled→P-26 |
| day-019 p019-R35 | merged-duplicate→P-23 (declare the knowledge gap) |
| day-021 p021-R1 | merged-duplicate→P-22 (what unique thing does this test add) |
| day-021 p021-R2 | merged-duplicate→P-12 (no parallel spec file) |
| day-021 p021-R3 | merged-duplicate→P-06 (regroup: restate goal in flight) |
| day-021 p021-R4 | compiled→P-07 |
| day-021 p021-R5 | reroute:tdd-bdd (coverage held elsewhere before removal) |
| day-021 p021-R6 | merged-duplicate→P-03 (coverage is not a necessity oracle) |
| day-021 p021-R7 | compiled→P-03 |
| day-021 p021-R8 | merged-duplicate→P-26 (inferior-then-superior commits) |
| day-021 p021-R9 | reroute:tdd-bdd (requirements commit separate from code) |
| day-021 p021-R10 | compiled→P-22 |
| day-021 p021-R11 | merged-duplicate→P-22 |
| day-021 p021-R12 | merged-duplicate→P-22 (stronger assertion subsumes weaker) |
| day-021 p021-R13 | reroute:tdd-bdd (mock naming) |
| day-021 p021-R14 | merged-duplicate→P-13 (count before arguing) |
| day-021 p021-R15 | merged-duplicate→P-16 |
| day-021 p021-R16 | reroute:project-memory (real DB for exploration) |
| day-021 p021-R17 | merged-duplicate→P-10 (no circular evidence) |
| day-021 p021-R18 | reroute:project-memory (single authoritative place) |
| day-021 p021-R19 | merged-duplicate→P-23 (search the record before inventing vocabulary) |
| day-021 p021-R20 | reroute:tdd-bdd (dead-code removal in own commit) |
| day-021 p021-R21 | reroute:coordinator (delegation briefing) |
| day-021 p021-R22 | reroute:tdd-bdd (contract gap parks the feature) |
| day-021 p021-R23 | reroute:tdd-bdd (story before acceptance test) |
| day-021 p021-R24 | reroute:tdd-bdd (no speculative acceptance criteria) |
| day-021 p021-R25 | merged-duplicate→P-29 |
| day-021 p021-R26 | compiled→P-38 |
| day-021 p021-R27 | compiled→P-36 |
| day-021 p021-R28 | merged-duplicate→P-33 (reject misrepresenting output) |
| day-021 p021-R29 | merged-duplicate→P-35 (no "experts agree" close) |
| day-021 p021-R30 | merged-duplicate→P-38 (point at own last turn) |
| day-021 p021-R31 | reroute:project-memory (append-only completed list) |
| day-021 p021-R32 | merged-duplicate→P-07 |

## v2 skill_rules with skill_target: pair-programming

| id | disposition |
|----|-------------|
| d002-R20 | merged-duplicate→P-09 |
| d002-R21 | merged-duplicate→P-01 |
| d003-R12 | merged-duplicate→P-16 |
| d003-R17 | merged-duplicate→P-09 |
| d004-R11 | merged-duplicate→P-05 (restore then redo properly) |
| d004-R19 | reroute:coordinator (outside-repo writes) |
| d006-R12 | merged-duplicate→P-15 |
| d006-R13 | reroute:coordinator (permission batching) |
| d006-R14 | reroute:tdd-bdd (commit message review, explicit staging) |
| d006-R15 | merged-duplicate→P-14 |
| d007-R1 | merged-duplicate→P-16 |
| d007-R2 | merged-duplicate→P-15 |
| d008-R1 | reroute:tdd-bdd (no git add -A) |
| d008-R2 | merged-duplicate→P-17 (price the safety step) |
| d008-R6 | merged-duplicate→P-10 |
| d008-R7 | merged-duplicate→P-24 |
| d008-R14 | merged-duplicate→P-23 |
| d008-R18 | reroute:coordinator (document-commit-clear workflow) |
| d009-R27 | merged-duplicate→P-15 |
| d009-R28 | merged-duplicate→P-05 |
| d010-R10 | merged-duplicate→P-13 |
| d010-R12 | reroute:tdd-bdd (commit message vs diff ratio) |
| d010-R24 | reroute:coordinator (parallel audit subagents) |
| d013-R1 | merged-duplicate→P-15 (resume: report reconstructed state first) |
| d013-R3 | merged-duplicate→P-16 (planning phase = zero modifications) |
| d013-R4 | merged-duplicate→P-10 |
| d013-R7 | rejected(harness identity mechanics) |
| d014-R1 | merged-duplicate→P-16 |
| d014-R8 | reroute:coordinator (query batching) |
| d015-R15 | rejected(project-specific /hi opener) |
| d016-R5 | merged-duplicate→P-01 |
| d016-R13 | reroute:tdd-bdd (git add --patch) |
| d016-R18 | merged-duplicate→P-05 |
| d018-R22b | merged-duplicate→P-28 |
| d018-R22c | merged-duplicate→P-21 |
| d019-R24 | merged-duplicate→P-10 |
| d019-R25 | merged-duplicate→P-15 |
| d020s3-R13 | reroute:tdd-bdd (git revert over reconstruction) |
| d020s3-R14 | merged-duplicate→P-05 |
| d020s3-R15 | reroute:coordinator (rg over subagent for literal lookup) |
| d020s3-R16 | reroute:coordinator (cheap digest first) |
| d020s3-R17 | reroute:coordinator (tool calibration) |
| d020s5-R8 | merged-duplicate→P-24 (standing instruction stays in force) |
| d020s5-R11 | merged-duplicate→P-24 |
| d020s5-R14 | merged-duplicate→P-15 |

## v2 pairing_gems (by loc)

| loc | disposition |
|-----|-------------|
| day-002:L1768-L1827 | merged-duplicate→P-14 (revert the wrong rule; RED-semantics content itself reroutes to tdd-bdd via L-01/L-02 lineage) |
| day-002:L2820-L2865 | merged-duplicate→P-04 |
| day-002:L1516-L1518 | merged-duplicate→P-24 |
| day-002:L3052 and L3080-L3086 | merged-duplicate→P-24 (explicit exception asked and granted) |
| day-002:L1131 and L1842 | merged-duplicate→P-12 |
| day-003:L792 | merged-duplicate→P-18 |
| day-003:L1784 | merged-duplicate→P-14 |
| day-003:L1095 | reroute:tdd-bdd (comment-minimalism rationale) |
| day-003:L1276 | merged-duplicate→P-01 |
| day-003:L500 | merged-duplicate→P-10 |
| day-003:L887 | merged-duplicate→P-09 (disclose own constraints) |
| day-003:L1693 | merged-duplicate→P-28 |
| day-003:L2229 | reroute:tdd-bdd (commit-log signal-to-noise) |
| day-004:L1094-L1112 | merged-duplicate→P-05 |
| day-004:L5310-L5405 | merged-duplicate→P-01 |
| day-004:L5652-L5730 | merged-duplicate→P-02 |
| day-004:L3467-L3537 | reroute:tdd-bdd (git mv redo) |
| day-004:L2287-L2328 | merged-duplicate→P-10 |
| day-004:L4337-L4360 | merged-duplicate→P-01 |
| day-005:L1755 | merged-duplicate→P-27 |
| day-005:L1653 | merged-duplicate→P-02 |
| day-005:L2673 | merged-duplicate→P-14 |
| day-005:L2812 | merged-duplicate→P-11 |
| day-005:L1201-L1303 | reroute:tdd-bdd (concern-scoped commit mechanics) |
| day-005:L2147 | reroute:tdd-bdd (product question vs mock) |
| day-005:L118 | merged-duplicate→P-28 |
| day-005:L2379 | reroute:project-memory (backlog order as content) |
| day-006:L1735 | merged-duplicate→P-11 |
| day-006:L2996 | merged-duplicate→P-23 |
| day-006:L3277 | merged-duplicate→P-01 |
| day-006:L1512 | merged-duplicate→P-10 |
| day-006:L1793 | merged-duplicate→P-19 |
| day-006:L1039 | reroute:coordinator (front-load permission requests) |
| day-007:L1799 | reroute:tdd-bdd (coverage as spec-drift signal) |
| day-007:L2707 | merged-duplicate→P-22 |
| day-007:L7660 | merged-duplicate→P-10 |
| day-007:L7731 | merged-duplicate→P-01 |
| day-007:L570 | reroute:tdd-bdd (skeleton-phase exemption, L-02) |
| day-007:L2996 | merged-duplicate→P-01 |
| day-007:L1454 | merged-duplicate→P-23 (ask which reading was meant) |
| day-007:L88 | merged-duplicate→P-16 |
| day-008:L457 | merged-duplicate→P-15 |
| day-008:L478 | merged-duplicate→P-10 |
| day-008:L1200 | merged-duplicate→P-17 |
| day-008:L1008 | merged-duplicate→P-24 |
| day-008:L3610 | merged-duplicate→P-15 |
| day-008:L3713 | merged-duplicate→P-23 |
| day-008:L3902 | merged-duplicate→P-28 |
| day-008:L1707 | reroute:project-memory (falsifiable documentation) |
| day-009:L4436 | merged-duplicate→P-19 |
| day-009:L4440 | reroute:project-memory (docs are not revelations) |
| day-009:L5564 | merged-duplicate→P-01 |
| day-009:L4645 | merged-duplicate→P-10 |
| day-009:L7328 | reroute:tdd-bdd (fake-greened acceptance diagnosis, L-05) |
| day-009:L6672 | merged-duplicate→P-26 |
| day-009:L5191 | merged-duplicate→P-21 (don't generalize the literal hint) |
| day-009:L9145 | merged-duplicate→P-05 |
| day-009:L8037 | merged-duplicate→P-13 (self-skepticism toward own accumulated output) |
| day-009:L4139 | merged-duplicate→P-19 (no manufactured severity) |
| day-010:L1083 | merged-duplicate→P-04 |
| day-010:L2235 | reroute:coordinator (parallel cheap audit agents) |
| day-010:L2881 | merged-duplicate→P-08 |
| day-010:L3627 | merged-duplicate→P-39 |
| day-010:L5782 | merged-duplicate→P-02 |
| day-010:L6173 | merged-duplicate→P-04 |
| day-011:L9088 | reroute:tdd-bdd (incremental slicing plan) |
| day-011:L6943 | merged-duplicate→P-09 |
| day-011:L10704 | merged-duplicate→P-23 |
| day-011:L11634 | merged-duplicate→P-22 |
| day-011:L4598 | merged-duplicate→P-04 |
| day-012:L946 | reroute:tdd-bdd (spec inviolability rationale) |
| day-012:L1073 | merged-duplicate→P-15 (was →P-28; an author decomposing one edit into a reviewable sequence) |
| day-012:L2465 | merged-duplicate→P-10 |
| day-012:L2628 | merged-duplicate→P-04 |
| day-013:L1445-L1448 | merged-duplicate→P-15 (pre-flight read-back) |
| day-013:L1603 | merged-duplicate→P-40 (was →P-14; comprehension check after correction, now standalone) |
| day-013:L2820-L2822 | rejected(era-specific model-switch diagnosis) |
| day-013:L996-L1000 | reroute:project-memory (screenshots-in-repo policy) |
| day-013:L740-L741 | merged-duplicate→P-15 (context reacquisition named as goal) |
| day-013:L1709-L1710 | reroute:tdd-bdd (rules change before governed work) |
| day-014:L338-L343 | merged-duplicate→P-16 |
| day-014:L366-L415 | merged-duplicate→P-16 (research response shape) |
| day-014:L322-L333 | merged-duplicate→P-10 |
| day-014:L483-L492 | merged-duplicate→P-14 |
| day-015:L440-L446 | merged-duplicate→P-27 ("Use me, human") |
| day-015:L604 | merged-duplicate→P-01 |
| day-015:L1314-L1318 | reroute:project-memory (fixture authority) |
| day-015:L1642-L1645 | merged-duplicate→P-04 |
| day-015:L2423 | merged-duplicate→P-01 |
| day-015:L2084-L2085 | merged-duplicate→P-04 |
| day-015:L3615-L3616 | merged-duplicate→P-25 |
| day-016:L958 | merged-duplicate→P-05 |
| day-016:L1085 | merged-duplicate→P-05 (destructive acts stay human) |
| day-016:L1263 | merged-duplicate→P-01 |
| day-016:L3209 | merged-duplicate→P-05 |
| day-016:L4835 | reroute:tdd-bdd (commit taxonomy as narrative) |
| day-016:L6551 | merged-duplicate→P-24 |
| day-017:L1556 | reroute:tdd-bdd (RED verified twice) |
| day-017:L2208 | merged-duplicate→P-24 |
| day-017:L2129 | merged-duplicate→P-18 (licence to demolish) |
| day-017:L1876 | reroute:tdd-bdd (bug as natural falsifier) |
| day-017:L1212 | merged-duplicate→P-33 |
| day-018:L578 | merged-duplicate→P-22 (assertion-strength ladder) |
| day-018:L641 | reroute:tdd-bdd (skip-removal convention) |
| day-018:L1125 | merged-duplicate→P-06 |
| day-018:L1869 | merged-duplicate→P-04 |
| day-018:L3255 | reroute:project-memory (escape-hatch design documentation) |
| day-018:L7081 | merged-duplicate→P-39 (commission evidence, resist verdict) |
| day-019:L1247 | merged-duplicate→P-26 |
| day-019:L3806 | merged-duplicate→P-03 |
| day-019:L2613 | merged-duplicate→P-01 |
| day-019:L4650-L4702 | reroute:tdd-bdd (Mock vs Stub vs Fake teaching) |
| day-019:L5011 | reroute:tdd-bdd (integration-boundary catch) |
| day-019:L1720-L1773 | merged-duplicate→P-17 |
| day-019:L4355 | reroute:tdd-bdd (assertion failure message) |
| day-019:L794-L983 | merged-duplicate→P-33 (grounding via the full primary record) |
| day-020:L899 | merged-duplicate→P-15 |
| day-020:L2372 | merged-duplicate→P-15 (destination stated before executing) |
| day-020:L4249 | merged-duplicate→P-10 (distrust inherited context) |
| day-020:L4419 | merged-duplicate→P-23 (bisect by provenance) |
| day-020:L6763 | merged-duplicate→P-14 |
| day-020:L5153 | merged-duplicate→P-04 |
| day-020:L3643 | merged-duplicate→AP-04 (author out-applies the persona; register evidence) |
| day-020:L8145 | merged-duplicate→P-03 |
| day-020:L10111 | merged-duplicate→P-28 (derive from the named rule) |
| day-020:L10134 | reroute:tdd-bdd (duplication as design signal) |
| day-020:L12438 | merged-duplicate→P-15 |
| day-020:L13572 | merged-duplicate→P-24 (regression shipped with justification) |
| day-020:L11173 | merged-duplicate→P-06 (discipline binds both partners) |
| day-020:L17391 | merged-duplicate→P-15 (ground-rules read-back) |
| day-020:L18203 | reroute:coordinator (subagent calibration) |
| day-020:L21047 | merged-duplicate→P-14 |
| day-020:L21412 | merged-duplicate→P-05 |
| day-020:L16895 | reroute:tdd-bdd (general fix over per-site patch) |
| day-020:L22380 | merged-duplicate→P-03 |
| day-020:L23689 | merged-duplicate→P-23 (motivation recovered before change) |
| day-020:L27220 | reroute:tdd-bdd (coverage signal not target) |
| day-020:L27794 | merged-duplicate→P-27 |
| day-020:L28428 | merged-duplicate→P-05 (silent mutation destroyed evidence) |
| day-020:L30678 | merged-duplicate→P-14 |
| day-020:L29593 | reroute:coordinator (verbatim subagent output rationale) |
| day-020:L31933 | merged-duplicate→P-01 |
| day-020:L31219 | merged-duplicate→P-19 (refuse the comfortable conclusion) |
| day-020:L32244 | merged-duplicate→P-11 |
| day-020:L32334 | merged-duplicate→P-22 (itemized properties before rejection) |
| day-020:L31828 | reroute:tdd-bdd (coverage as search instrument) |
| day-021:L1722 | merged-duplicate→P-26 (inferior-then-superior commits) |
| day-021:L1529 | merged-duplicate→P-22 (reusable questions handed over) |
| day-021:L4169 | merged-duplicate→P-36 |
| day-021:L2348 | merged-duplicate→P-18 |
| day-021:L6321 | reroute:project-memory (real-DB exploration) |
| day-021:L6455 | merged-duplicate→P-10 (circular evidence named) |
| day-021:L9030 | reroute:tdd-bdd (path dependency in criteria) |
| day-021:L8745 | reroute:project-memory (immutable completion order) |
| day-021:L7810 | reroute:coordinator (delegation coaching) |
