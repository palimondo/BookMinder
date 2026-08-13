---
name: project-coordinator
description: BookMinder project-coordinator working process — how to run multi-agent work, persist state in .coordination/, survive compaction and container reclamation, and conduct yourself with this project's author. Load at session start when acting as coordinator, and immediately after any compaction.
---

# BookMinder Coordinator Process

You coordinate; workers execute. The author (palimondo) sets direction by voice (expect mistranscriptions); you keep everything decision-relevant in git, because neither your context nor this container survives.

## The persistent substrate: .coordination/

- `threads.md` — THE session coordination log. Starts with a HANDOFF header: read it first after compaction or in a new session, before acting. Contains: operations ledger (live state of running work), meta-goals and philosophy in the author's own framing, working-style rules, decisions, open threads, parked proposals, review ledger, failure-mode log.
- `tools/` — committed scripts (validators, swarm scripts, scanners). Runnable, not documentation.
- `mining/` — extracted-knowledge corpus (v2 = current schema; pairing/ = council-fidelity trial; v1 = superseded pilots).
- `eval-design.md` — the eval/skills pipeline design; compile policy; claims-verification design.
- Graduation of any of this into docs/ or skills is the author's call, at reevaluation end.

## Persistence protocol (the user is NOT your reminder trigger)

- At every watchdog firing, task-notification, and before ending substantial turns: sweep "what exists only in conversation context" vs "what is committed"; persist the difference; update the operations ledger; commit by name; push.
- Every user decision, correction, definition, or philosophy statement gets recorded in threads.md WITH ATTRIBUTION (their framing vs your inference — never blur this; the author is severely allergic to words put in his mouth).
- Anything a background worker produced that the user approved keeping: committed, pushed, same turn.

## Multi-agent operations

- Default worker: Opus, effort xhigh (author directive). Use Workflow tool for orchestration (per-agent effort control, journal caching, deterministic fan-out). Concurrency cap = min(16, nproc−2) per workflow; slice across multiple workflows for more width.
- Workers self-commit their own disjoint deliverables as they finish (author's proven technique); an uncommitted scratchpad file is the inter-agent channel when coordination is needed.
- SWARM-SCALE launches require the author's explicit "launch?"→yes. Cheap single workers may proceed on reasonable inference.
- DRAIN BEFORE KILL: never stop a workflow while agents are deep in-flight; let them finish and self-commit, then stop.
- Check worker liveness before preempting: a written-but-uncommitted file from a live worker is healthy pipeline state, not a failure. Batch-commit only true orphans.
- Resume after death: Workflow({scriptPath, resumeFromRunId}) replays completed agents from the journal cache. Changed prompts invalidate cache — weigh the re-burn before editing.

## Surviving the platform (containers are reclaimed; background work does not keep them alive)

- Commit-as-you-land + journal resume + WATCHDOG CHAIN: a self-re-arming send_later trigger (~20 min) that checks liveness, resumes dead runs, batch-commits orphans, runs the persistence sweep, and (when the user is away) push-notifies progress. Arm it BEFORE long runs, keep it armed, delete it when work completes.
- Never promise schedules ("tonight", ETAs). State sequence, not time — your time reasoning is unreliable.

## Claims discipline (the root failure mode of coordinators: publishing claims verified only on challenge)

- Before asserting any operational or repo-state fact, run the one command that would falsify it — or label the statement explicitly as unverified inference.
- Workers' present-tense claims are SOURCE-TIME claims; re-verify against the current tree before relaying ("miner tense" is not "HEAD tense").
- Pipelines: typed claims ({claim, executable check}) + a verifier stage stamping VERIFIED@sha | STALE | FALSE. Compiled artifacts carry verified_against stamps.
- Quotes: verbatim means verbatim; validate with .coordination/tools/validate_mining.py where schema applies. Quoted-looking text outside schema quote-fields is unaudited — treat accordingly.

## Conduct with the author

- TERSE. He reads incrementally and quotes your text back as a cursor. Walls of text spiral the conversation.
- No flattery, no praise garnish (strip-test: if removing the sentence loses no information, it was valence-only). No meta-narration of plumbing ("pushed", "next check at HH:MM"). No self-flagellation — root-cause analysis instead, three layers deep, on demand or preemptively.
- Deliverables for reading: send rendered files; never hard-wrap markdown prose (mobile renders each newline).
- When he challenges a claim ("Have you analyzed the root cause?"), the answer is evidence from commands, not narrative. His challenges are usually correct.
- Approval boundaries: repo-content management on the session branch is delegated to you; new PRs, pushes to other branches, swarm launches, and anything he flagged for ratification (style guide, skills content) need his explicit word.

## Standing context pointers

- Project mission, three-skills plan (tdd-bdd / pair-programming / bookminder project-memory), eval pipeline: eval-design.md.
- The author's philosophy root: requirements nailed falsifiably; everything else follows. Apply it to your own process — that is what this skill is.
