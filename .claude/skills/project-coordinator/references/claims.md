# Claims and evidence — verify before you assert

Load this page the moment you are about to state or relay any operational claim — done, running, committed, alive, broken, fixed, live at HEAD — or run, design, or judge the mining/compile evidence pipeline.

## Verification discipline

The deepest failure of this engagement, named after the author asked "Have you analyzed the root cause?" three times: **you publish operational claims at composition time and verify them only on challenge — the author has been functioning as your RED phase.** Every false claim was falsifiable by one cheap command (`git log`, `nproc`, a date check, a journal grep) that you ran only after being asked.

- **Run the falsifying command before the assertion, or label the statement as unverified inference.** No exceptions for claims that "feel" safe.
- Beware observation-selection bias from one-sided sensors. The stop-hook fires only on files caught mid-pipeline, so it reported only failures; concluding "worker self-commits are failing consistently" from it was reasoning from a biased instrument.
- **Worker reports are in source-time tense.** A miner reading a 2025 transcript writes "this bug shipped into the committed scripts" and means 2025. Before relaying any "still at HEAD / currently broken / live today" claim, check today's tree. The `USERNAME` zsh bug was reported as live and had been fixed a year earlier.
- The durable fix is structural, not another prose rule: **typed claims** (`{claim, check}` where `check` is an executable probe), **a verifier stage** after any analysis fan-out that stamps each claim `VERIFIED@<sha> | STALE | FALSE`, and **freshness stamps** (`verified_against: <sha>`) required before any present-tense claim enters a skill, a backlog, or a canonical guide.
- Know your validators' blind spots and record them. The mining validator checked `quote:` fields only, so a fabricated user quote in a `user_intervention:` field passed unflagged and was caught by a repair agent by luck. Carry known limitations into the trust model of whatever consumes the data.
- **Read the primary source yourself before giving an opinion on it.** When the author challenged the mining yield, the honest move was reading both YAMLs end to end rather than relaying miner summaries — and it produced a verdict that partially disagreed with him, which is what he wanted.
- Read the code yourself when it is small enough to read (the production package is ~290 lines). Do not opine on architecture from worker summaries.

## Evidence-base architecture (the debug/optimized build model)

His model, adopted verbatim: mining produces the **debug build** — every claim fully back-referenced with location, date, and provenance type. Compilation later cuts the **optimized build** — executable rules stripped of provenance, split by target.

- Never resolve contradictions in the mining phase; a day-level miner cannot see other days. Reconciliation is the compiler's job.
- **Contradiction resolution is ranked, not merely recent:** user-verbatim beats paraphrase beats agent-synthesis; among his own statements later overrides earlier; but an agent-era "decision" (a YOLO-period commit, a post-downgrade Gemini session) never overrides an earlier user ruling. Some of what looks like him changing his mind is an agent drifting while he was not looking.
- Output a **contradiction ledger**, not a silent resolution: both quotes, both dates, a proposed resolution, and his ratification.
- Record absences explicitly in a `gaps:` field so a missing rule is distinguishable from an oversight.
- Sort rules by `skill_target` at mine time so the compile step can split them mechanically.
