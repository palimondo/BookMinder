# Rule Index — pair-programming skill

Maps every compiled rule (P-NN) and register entry (AP-NN) to its corpus sources and provenance. Primary source carries the rule's WHY; merged sources are duplicate/adjacent rules folded in (full per-source dispositions in disposition-pair-programming.md). Provenance rank: user-verbatim > user-paraphrase > agent-synthesis; ledger-ratification = author ruling recorded in the contradiction ledger's Ratification record; brief-mandate = author-approved skill definition relayed in the compile brief. Testability flag per the parked scripted-dialogue eval family: scripted-dialogue-evaluable (violation detectable from a scripted transcript), judge-rubric-item (needs an LLM judge's qualitative rating), UNFALSIFIABLE (no observable violation).

UNFALSIFIABLE count: 0 — every compiled rule names an observable violation (a command not run, an edit in a question turn, a consensus block emitted, a reversal without cited evidence). No rule had to be compiled as pure stance.

## MIRROR (references/mirror.md)

| id | primary source | merged sources | provenance | testability |
|----|----------------|----------------|------------|-------------|
| P-01 | pairing/day-019.yaml p019-R10 @ day-019:L2613 ("Really?!? !pytest --spec") | v2 p019-R2, p002-R2, p002-R11, p003-R5, p004-R5, p004-R6, p005-R12, p006-R2, p009-R2, p009-R10, p009-R11, p015-R2, p015-R10, p016-R5, p018-R1, p018-R11, p020s1-R17, p020s2-R4, p020s5-R2; trial p010-R1, p019t-R30; skill_rules d002-R21, d016-R5 | user-verbatim | scripted-dialogue-evaluable |
| P-02 | pairing/day-010.yaml p010-R8 @ day-010:L5782 | v2 p010-R2, p005-R3, p007-R14, p018-R8 | user-verbatim | scripted-dialogue-evaluable |
| P-03 | pairing/day-021.yaml p021-R7 @ day-021:L4171 | v2 p021-R3, p019-R3, p020s4-R1; trial p019t-R27 (record deliberate breakage), p021t-R6 | user-verbatim | scripted-dialogue-evaluable |
| P-04 | v2/day-020-s1.yaml p020s1-R9 @ day-020:L5153 | trial p010-R11 @ day-010:L6173; v2 p002-R8, p010-R10, p011-R2, p012-R4, p012-R11(gem), p015-R7, p018-R7, p020s2-R10, p020s3-R10, p020s4-R11, p021-R15; trial p010-R2 | user-verbatim | judge-rubric-item |
| P-05 | v2/day-016.yaml p016-R2 @ day-016:L3212 (rehearse on disposable copy) | v2 p003-R9, p004-R3, p004-R4, p008-R6, p009-R6, p012-R1, p013-R2, p013-R5, p015-R6, p016-R1, p016-R3, p016-R4, p018-R6, p020s1-R13, p020s1-R14, p020s3-R8, p020s3-R11, p020s4-R4; trial p019t-R1; skill_rules d004-R11, d009-R28, d016-R18, d020s3-R14 | user-verbatim | scripted-dialogue-evaluable |
| P-06 | pairing/day-010.yaml p010-R4 @ day-010:L2908 | pairing/day-019.yaml p019t-R28 @ day-019:L2586; v2 p010-R3, p010-R4(v2), p007-R6, p007-R7, p021-R1; trial p021t-R3 | user-verbatim | scripted-dialogue-evaluable |
| P-07 | pairing/day-021.yaml p021t-R4 @ day-021:L3576 | trial p021t-R32 @ day-021:L598 | user-verbatim | scripted-dialogue-evaluable |
| P-08 | pairing/day-010.yaml p010-R3 @ day-010:L2881 ("I wouldn't celebrate!") | v2 p010-R8, p005-R11, p006-R12 | user-verbatim | scripted-dialogue-evaluable |
| P-09 | v2/day-003.yaml p003-R14 @ day-003:L775-L783 | v2 p002-R1, p003-R15, p006-R1, p006-R13, p010-R9, p011-R6, p015-R9, p019-R7, p020s1-R10, p020s3-R9, p020s4-R7, p021-R4; skill_rules d002-R20, d003-R17 | user-verbatim | judge-rubric-item |
| P-10 | v2/day-008.yaml p008-R3 @ day-008:L478 | v2 p003-R6, p005-R8, p011-R10, p012-R3, p012-R6, p013-R6, p014-R3, p016-R6, p016-R10, p019-R1, p020s3-R2, p020s4-R6, p021-R9; trial p019t-R16, p021t-R17; skill_rules d008-R6, d013-R4, d019-R24 | user-verbatim | scripted-dialogue-evaluable |
| P-11 | pairing/day-019.yaml p019t-R17 @ day-019:L2000 | v2 p005-R10, p006-R11, p007-R11, p017-R1, p020s1-R11 | user-verbatim | scripted-dialogue-evaluable |
| P-12 | v2/day-002.yaml p002-R3 @ day-002:L1131 | v2 p004-R11, p018-R9; trial p021t-R2 (no parallel copies) | user-verbatim | scripted-dialogue-evaluable |
| P-13 | pairing/day-010.yaml p010-R5 @ day-010:L4447 ("nah, this ended up to be more LOC. revert") | v2 p010-R1, p003-R17; trial p021t-R14; skill_rules d010-R10 | user-verbatim | scripted-dialogue-evaluable |
| P-14 | v2/day-002.yaml p002-R4 @ day-002:L1191 | v2 p002-R7, p002-R10, p003-R7, p003-R13(part), p005-R5, p006-R3, p011-R11, p012-R7, p013-R7, p014-R5, p018-R3, p021-R8; skill_rules d006-R15 | user-verbatim | judge-rubric-item |

## RECIPROCAL (references/reciprocal.md)

| id | primary source | merged sources | provenance | testability |
|----|----------------|----------------|------------|-------------|
| P-15 | v2/day-020-s1.yaml p020s1-R1 @ day-020:L2897 | pairing/day-019.yaml p019t-R2 @ day-019:L1129; v2 p002-R6, p008-R2, p008-R7, p008-R14, p009-R1, p011-R12, p013-R1, p013-R10, p014-R4, p017-R3, p019-R5, p020s1-R2, p020s1-R15, p020s2-R1, p020s2-R5, p020s2-R9, p020s3-R7, p020s4-R3, p018-R10; trial p019t-R32; skill_rules d006-R12, d007-R2, d009-R27, d013-R1, d019-R25, d020s5-R14 | user-verbatim | scripted-dialogue-evaluable |
| P-16 | v2/day-003.yaml p003-R3 @ day-003:L955-L1461 | trial p021t-R15 @ day-021:L2463; v2 p004-R1, p004-R12, p006-R8, p007-R1, p007-R12, p011-R5, p014-R1, p014-R7, p020s2-R6; skill_rules d003-R12, d007-R1, d013-R3, d014-R1 | user-verbatim | scripted-dialogue-evaluable |
| P-17 | pairing/day-010.yaml p010-R14 @ day-010:L186 | pairing/day-019.yaml p019t-R19 @ day-019:L1674 ("2 is clearly useless!"); v2 p020s2-R7 @ day-020:L8798, p003-R12, p004-R2, p004-R10, p004-R13, p008-R4, p019-R10; skill_rules d008-R2 | user-verbatim | judge-rubric-item |
| P-18 | v2/day-021.yaml p021-R6 @ day-021:L2348 ("maybe you'll talk me out of it") | pairing/day-010.yaml p010-R17 @ day-010:L3686; v2 p003-R1, p004-R7, p016-R8, p017-R2 | user-verbatim | scripted-dialogue-evaluable |
| P-19 | v2/day-020-s1.yaml p020s1-R16 @ day-020:L2036 | v2 p006-R4, p009-R4, p013-R3, p017-R5, p018-R13 | agent-synthesis (grounded in user-verbatim day-013:L1647, day-009:L4139) | judge-rubric-item |
| P-20 | v2/day-003.yaml p003-R2 @ day-003:L334 et al. | v2 p005-R7, p006-R5, p015-R5, p020s5-R4 | agent-synthesis (pattern count user-corroborated: "You're absolutely right" 14x day-010, 30x day-019) | scripted-dialogue-evaluable |
| P-21 | pairing/day-019.yaml p019t-R18 @ day-019:L3745 ("Ah, OK, that's worse.") | pairing/day-010.yaml p010-R15 @ day-010:L3627; v2 p010-R11, p009-R5(gem L5191), p020s2-R2, p020s2-R3; skill_rules d018-R22c | user-verbatim | judge-rubric-item |
| P-22 | pairing/day-021.yaml p021t-R10 @ day-021:L1601 (0/1/many) | trial p021t-R1, p021t-R11, p021t-R12, p019t-R24; v2 p011-R9, p012-R5, p021-R2, p020s5-R5; gem day-018:L578 (assertion-strength ladder) | user-verbatim | judge-rubric-item |
| P-23 | pairing/day-019.yaml p019t-R9 @ day-019:L791 | pairing/day-019.yaml p019t-R35 @ day-019:L2818; v2 p003-R10, p007-R15, p008-R8, p008-R9, p015-R4, p015-R11, p017-R6, p018-R2, p020s2-R8, p020s4-R2, p020s5-R1, p020s5-R3, p020s5-R6, p020s5-R7, p021-R14; trial p021t-R19; skill_rules d008-R14 | user-verbatim | scripted-dialogue-evaluable |
| P-24 | pairing/day-019.yaml p019t-R29 @ day-019:L2433 ("No, you're not!") | v2 p010-R7 @ day-010:L6124, p002-R14, p008-R5, p009-R5, p013-R4, p014-R2, p017-R7, p017-R8, p020s5-R9; trial p010-R13; skill_rules d008-R7, d020s5-R8, d020s5-R11 | user-verbatim | scripted-dialogue-evaluable |
| P-25 | v2/day-021.yaml p021-R5 @ day-021:L3851 | v2 p005-R6; gem day-015:L3615 ("I'm spitballing") | user-verbatim | judge-rubric-item |
| P-26 | pairing/day-019.yaml p019t-R34 @ day-019:L1247 | trial p021t-R8 @ day-021:L1722 (inferior-then-superior commits); gem day-009:L6672 | user-verbatim | scripted-dialogue-evaluable |
| P-27 | v2/day-020-s4.yaml p020s4-R5 @ day-020:L27794 ("STOP! GET SOME HELP!") | v2 p002-R12, p003-R11, p004-R9, p005-R4, p011-R3, p015-R1, p015-R3, p015-R8, p016-R7, p020s3-R1, p020s3-R13 | user-verbatim | scripted-dialogue-evaluable |
| P-28 | v2/day-019.yaml p019-R8 @ day-019:L2818/L2872 | v2 p002-R9, p003-R13, p004-R8, p005-R2, p012-R7(gem L1073), p021-R7; skill_rules d018-R22b | user-verbatim | judge-rubric-item |

## COUNCIL-MECHANICS (references/council.md)

| id | primary source | merged sources | provenance | testability |
|----|----------------|----------------|------------|-------------|
| P-29 | pairing/day-010.yaml p010-R18 @ day-010:L2668 | pairing/day-021.yaml p021t-R25 @ day-021:L4998; v2 p010-R5, p012-R8, p018-R14 | user-verbatim | judge-rubric-item |
| P-30 | pairing/day-019.yaml p019t-R5 @ day-019:L4414 ("let me hear their individual voices") | v2 p019-R12, p019-R6 (no after-the-fact voices) | user-verbatim | scripted-dialogue-evaluable |
| P-31 | pairing/day-019.yaml p019t-R4 @ day-019:L4466 (the WHY of full context per voice) + ledger L-08 (principle/implementation split) | — | user-verbatim + ledger-ratification | scripted-dialogue-evaluable |
| P-32 | ledger L-08 (author design, 2026-08-13: per-persona full-context forks, parallel, mutually blind, main-thread synthesis; in-context-only ban marked superseded era-conditioned implementation) | pairing/day-010.yaml p010-R19 @ day-010:L3474 (isolation protocol origin); v2 p019-R11 (superseded in-context form, recorded as such) | ledger-ratification (root user-verbatim day-010:L3474) | scripted-dialogue-evaluable |
| P-33 | ledger L-04 (council conditioned on grounding; ungrounded simulacra channeling = anti-pattern) | pairing/day-019.yaml p019t-R7 @ day-019:L788 (persona-fabricated fact), p019t-R8 @ L856 (history in front of voices), p019t-R14; trial p010-R21, p010-R23 @ day-010:L3232 ("But, Kent: should we Tidy First?"); v2 p012-R10, p017-R9, p020s1-R8, p020s2-R11(part), p020s2-R13, p020s4-R12, p020s5-R10, p021-R13, p009-R13; day-010 gaps (zero book citations across six episodes) | ledger-ratification (root user-verbatim day-019:L709, L788) | judge-rubric-item |
| P-34 | pairing/day-019.yaml p019t-R6 @ day-019:L546 ("some AI splot adjacent first takes... ultrathink") | v2 p019-R13, p008-R12 | user-verbatim | scripted-dialogue-evaluable |
| P-35 | pairing/day-010.yaml p010-R20 @ day-010:L3625 | pairing/day-021.yaml p021t-R29 @ day-021:L4154; v2 p012-R9, p017-R10, p020s2-R12, p020s2-R14 | agent-synthesis (grounded in user-verbatim day-019:L4414, day-021:L4169) | scripted-dialogue-evaluable |
| P-36 | pairing/day-021.yaml p021t-R27 @ day-021:L4020 | v2 p008-R13; gem day-021:L4169 | user-verbatim | judge-rubric-item |
| P-37 | pairing/day-010.yaml p010-R22 @ day-010:L3220 | v2 p010-R6 | agent-synthesis (user-corroborated: rejected-as-slop verdicts day-010:L3627) | judge-rubric-item |
| P-38 | pairing/day-021.yaml p021t-R26 @ day-021:L4924 ("Did you all think hardest about how _query_books is implemented") | trial p021t-R30 @ day-021:L5958 (point at own last turn); v2 p021-R12, p020s2-R11; day-019 philosophy @ L5022 (fidelity degrades with abstraction) | user-verbatim | scripted-dialogue-evaluable |
| P-39 | v2/day-017.yaml p017-R11 @ day-017:L1209 | pairing/day-010.yaml p010-R25 @ day-010:L3628 (record when the council lost); v2 p010-R12, p018-R12, p020s3-R12; gem day-010:L3627 | agent-synthesis (grounded in user-verbatim day-010:L3627, day-020:L21708) | judge-rubric-item |

## ANTI-PATTERN REGISTER (references/anti-patterns.md)

| id | primary source | corroborating evidence | provenance | testability |
|----|----------------|------------------------|------------|-------------|
| AP-01 | brief-mandate (ratified register) | pairing/day-010.yaml anti_patterns sycophantic-fold @ L5893 (14x/day); day-019 @ L3740 (30x/day); day-021 @ L4154 (council mass-flip) | brief-mandate + agent-synthesis counts | scripted-dialogue-evaluable |
| AP-02 | brief-mandate (ratified register) | day-019 anti_patterns @ L538; day-021 @ L4011; day-010 @ L3222 | brief-mandate + user-verbatim verdicts (rejected-as-slop) | judge-rubric-item |
| AP-03 | brief-mandate (ratified register) | day-021 anti_patterns alternatives-theater @ L912; day-010 p010-R14 evidence @ L186; gem day-020:L8798 | brief-mandate + user-verbatim (day-019:L1674) | judge-rubric-item |
| AP-04 | brief-mandate (ratified register) + ledger L-04 | day-019 fidelity findings (~40% caricature/fabrication rate, threads.md:84 via ledger; zero book citations, day-019 gaps); day-021 @ L4884 (invented North position); day-019 @ L765 (fabricated 2022 provenance) | brief-mandate + ledger-ratification | judge-rubric-item |
| AP-05 | brief-mandate (ratified register, incl. strip-test) | day-010 anti_patterns premature-celebration @ L2872; p010-R3 @ L2881 | brief-mandate (strip-test), user-verbatim (L2881) | scripted-dialogue-evaluable |
| AP-06 | pairing/day-019.yaml anti_patterns false-process-claim @ L2431 | v2 p019-R29 evidence | user-verbatim ("No, you're not!") | scripted-dialogue-evaluable |
| AP-07 | pairing/day-021.yaml anti_patterns edit-instead-of-answer @ L2458 | recurrences @ L2427, L3608, L3432 | user-verbatim | scripted-dialogue-evaluable |
| AP-08 | pairing/day-021.yaml anti_patterns authority-laundering @ L477 | day-019 anti_patterns confabulated-individual-voices @ L4419 | agent-synthesis (user-corroborated day-019:L4424) | scripted-dialogue-evaluable |

## Boundary invariant

| id | source | provenance | testability |
|----|--------|------------|-------------|
| INV-B (MIRROR targets own output only, never partner claims) | ledger L-03 ratification (author correction 2026-08-13: MIRROR always meant the author's self-verification moves as agent reflexes, never partner-claim-policing) | ledger-ratification | judge-rubric-item |
