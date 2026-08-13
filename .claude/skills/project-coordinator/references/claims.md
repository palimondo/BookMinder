# Claims and evidence — verify before you assert


## Verification discipline

The failure mode this page exists to kill: publishing operational claims at composition time and verifying them only on challenge, which makes the author function as your RED phase. A false operational claim is almost always falsifiable by one cheap command (`git log`, `nproc`, a date check, a journal grep) — the command belongs before the assertion, not after the challenge.

- **Run the falsifying command before the assertion, or label the statement as unverified inference.** No exceptions for claims that "feel" safe.
- Beware observation-selection bias from one-sided sensors. A sensor that fires only on failure states reports only failures; concluding "X is failing consistently" from such an instrument is reasoning from a biased sample.
- **Worker reports are in source-time tense.** A worker reading an old transcript writes "this bug shipped" and means the transcript's date, not today. Before relaying any "still at HEAD / currently broken / live today" claim, check today's tree.
- The durable fix is structural, not another prose rule: **typed claims** (`{claim, check}` where `check` is an executable probe), **a verifier stage** after any analysis fan-out that stamps each claim `VERIFIED@<sha> | STALE | FALSE`, and **freshness stamps** (`verified_against: <sha>`) required before any present-tense claim enters a skill, a backlog, or a canonical guide.
- Know your validators' blind spots and record them. A validator that checks only some fields lets fabrications in the unchecked fields pass unflagged. Carry known limitations into the trust model of whatever consumes the data.
- **Read the primary source yourself before giving an opinion on it.** When he challenges a result, the honest move is reading the underlying artifacts end to end rather than relaying worker summaries — even when the resulting verdict partially disagrees with him; that is what he wants.
- Read the code yourself when it is small enough to read. Do not opine on architecture from worker summaries.
