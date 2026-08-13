# Project Coordinator — Operations

Chapter of the project-coordinator skill. Read this when launching, briefing, steering, or stopping workers, swarms, or workflows; choosing model tiers or Agent-vs-Workflow routing; committing or pushing; setting up watchdogs or persistence; surviving container reclamation; making or relaying operational claims; running the mining/compile pipeline; or handling hooks, scanners, and permission machinery.

## 1. Delegation — worker tiers and tool routing

The author's original instruction: delegate actual work to workers, "Opus 5 primary, or in cases where the highest level of intelligence or our full accumulated context is needed a Fable worker or fork of this main thread," while you gather context for high-level decisions. That sentence encodes three tiers, and they are not interchangeable.

**Tier routing:**

- **Opus, `effort: 'xhigh'` — the default worker.** Use for all bulk and parallel work: archaeology over git history, corpus mining, scouts, reconnaissance, investigations, per-file extraction, repair agents. This is where volume lives; ~45 of this engagement's ~50 worker launches were Opus.
- **Fable, `effort: 'xhigh'` — judgment, synthesis, and prose the author will personally read and grade.** Reserve it for: comparing and judging worker outputs, synthesizing multiple extractions into one canonical document, revising a document against his stated corrections, and any deliverable that is itself a test of whether you understood him. Six invocations in the engagement, all of that shape.
- **Fork of this thread (`Agent` with `subagent_type: "fork"`) — only when the *input* is the conversation itself.** Fork when the task requires his voice-stated goals, the corrections he made in dialogue, and the accumulated session judgment — things no file contains. The canonical style synthesis was forked for exactly this reason: "it needs our full conversation context… to pass your real test — whether *we* understood what you were going for." Do not fork for work that reads files; that is a fresh worker's job and forking only pollutes it.
- **Effort is `xhigh` by standing order** since 2026-08-11: "from now on… extra high is our default." The one legitimate exception is mechanically-specified work with a structured output schema (splitting a file on banner boundaries ran at `effort: 'low'`).

**Tool routing — the trade-off that decides everything:**

- The **`Agent` tool** spawns an individually addressable worker. You can `SendMessage` to it mid-flight to expand its scope or correct its trajectory (this is how the meta-analyst's diary access was widened), and its task-id can notify more than once. It has **no effort knob** and no orchestration.
- The **`Workflow` tool** runs a deterministic script that fans out agents with `agent(prompt, { model, effort, label, phase, schema })`, `phase()`, and `parallel([...])`. It gives you per-agent model and effort control, concurrency management, structured output schemas, and a journal that caches completed agents so a dead run resumes via `resumeFromRunId` without re-paying for finished work. Its agents are **not addressable** — `SendMessage` to them is refused; they do not appear in `ListAgents`.
- Therefore: **need xhigh, parallelism, or resumability → Workflow. Need to steer mid-flight → Agent.** Steering a workflow means stop → edit script → resume, and any agent whose prompt changed re-runs from zero. State this cost honestly as cache economics, not as impossibility — the author caught the sloppy version ("this categorical refusal now?") and he was right.
- Give every workflow script a stable path under `.coordination/tools/` and version it (`v2.1`, `v2.2`); commit the script itself so the run is reproducible after reclamation.

**Briefing workers:**

- **Brief design beats model tier.** The controlled A/B/C experiment settled this: the first extraction's shallowness was primarily *brief-induced*, and a re-briefed Opus at xhigh matched Fable. Before blaming a model, re-run with a better brief.
- **Demand motivation, not observation.** The author's core complaint about the first extraction: it "did not at all make any reasoning effort about the motivation… why am I doing things the way I'm doing things?" Every rule a worker extracts must be stated as "X because Y," and where the rationale is unrecoverable the worker must say so rather than invent one.
- **Control contamination explicitly.** "Give it all the advantages you can from the… repo map, process evaluation… but keep it fresh. Do not contaminate it with giving it the BDD style." Orientation documents = allowed and named; prior attempts at the same deliverable = forbidden and named.
- **Restart early rather than patch late.** When a brief is wrong and the worker is minutes in, `TaskStop` and relaunch with the corrected lens; a clean restart beats reconciling a misaimed deliverable.
- Give every worker its exact deliverable path, the no-hard-wrap rule, and a bounded return format ("return a max-10-line summary"). Long worker returns land in your context and become the wall of text.
- Forbid workers from touching tracked files other than their deliverable.

**Swarm operations:**

- **Workers commit their own deliverables as they finish.** The author's directive: "The worker should definitely be committing their deliverables as they finish their workloads," and his experience: "I have been using the commit your own workload as you go technique without any issues in other projects — they have completely disjoined workloads." Bake a self-commit stage into the workflow script. Do not hold deliverables in scratchpad; scratchpad dies with the container.
- Concurrent commits do not race meaningfully — disjoint files means no merge conflicts, and git's `index.lock` fails loudly and retries cleanly. Do not use race fear as a reason to centralize commits.
- **Use an uncommitted scratchpad file as the inter-agent coordination channel** when workers need to resolve something between themselves; the Write tool's stale-detection forces a re-read when another worker has modified it.
- Keep a coordinator batch-commit sweep as a *backstop* only. When it fires, check `git log` before claiming anything about whether worker self-commits are working.
- **Slice for concurrency.** A single workflow's cap is `min(16, nproc - 2)`; on a 4-core container that is 2. Slicing 24 units across three workflows with an `args` array tripled effective concurrency. Take an arg-sliced variant of the swarm script as the normal shape for large runs.
- **Drain before kill.** Never `TaskStop` a run without first checking in-flight agents' progress; killing to re-slice burned ~357K tokens of nearly-complete work and the author noticed: "you should have not killed the workflow so aggressively, you wasted almost 400k tokens there." If in-flight agents are deep, let them finish and self-commit, then stop.
- **Pilot before swarm.** Two units first, inspect the raw output together, then scale. The pilot caught a parsing error (`^│  > ` with two spaces, only on two files) that would have silently broken the full run.
- **Enforce schemas with a script, not with prose.** "I think that's a best practice, to use scripts and tools to enforce basic rules. Of course, you have a flexible schema where the agents have the ability to extend it, but where you require the base set." Write a validator that checks required fields *and* greps every `quote:` against its source file so paraphrase-as-quote fails mechanically. Run it over the whole harvest and dispatch repair agents for violations.
- When a validator reports a wall of violations, check whether the *validator* is wrong first — 51 of 62 raw violations in this engagement were validator artifacts (enum drift, shard prefixes, box glyphs, elision handling), not miner errors.

## 2. Persistence and recording discipline

The author will not be your reminder trigger: "Persistently Record all that's stated in session only and would not survive container restart or compaction… I don't wannabe be your reminder trigger."

**`.coordination/` is the durable substrate, and it is committed.** In this environment the git repo is the *only* cross-session memory — there is no auto-memory, no user-global CLAUDE.md, nothing that carries knowledge to the next cloud session. Verify this rather than assume it, then act accordingly.

The substrate map: `threads.md` (the standing record, structure below) · `tools/` (committed runnable scripts: validators, scanners, versioned swarm scripts) · `mining/` (extracted-knowledge corpus: v2 = current schema, pairing/ = council-fidelity trial, v1 = superseded pilots) · `eval-design.md` (pipeline + compile policy + claims-verification design) · `verified-residue.md` (the stamped current repair backlog — the work queue, not the narrative docs) · `recovered/` (artifacts restored from dead branches). Graduation into docs/ or skills is the author's call.

`threads.md` is the single standing record. Keep these sections live:

- **HANDOFF — READ FIRST AFTER COMPACTION** at the very top: current phase state, where artifacts live, how to verify them, what must not be started without his go, and what inputs are pending from him.
- **Session goal and meta-goals**, in his framing, attributed.
- **Working style rules** — every conduct correction he has made, with his short verbatim phrase attached so the rule keeps its teeth.
- **Decisions and authorizations**, dated, including scope grants (what a worker may read) and standing authorizations.
- **Open threads**, numbered, each with its blocking condition.
- **Parked proposals** — *your* ideas awaiting his go, each with the moment it should resurface. He caught you losing one: "Do you have a record of this somewhere that you can surface this idea/request again, so it does not get lost in the flood of wall of text?"
- **Review ledger** — his read state per artifact and its ratification status.
- **Operations ledger** — live state: what is running, what is stopped, what awaits which decision, with run IDs and script paths.
- **Failure modes observed this session** — your own errors, with root cause, as meta-lab data.

**The persistence sweep is machinery, not discipline.** At every watchdog firing, every task-notification, and before ending any substantial turn: diff "what exists only in conversation context" against "what is committed," and commit the delta. Embed this instruction in the watchdog trigger's own prompt so it fires by machinery. This is the project's own stickiness law applied to yourself: corrections shipped as automation stick; as prose they only partly stick.

Also persist: scripts you wrote (validators, scanners, workflow scripts) into `.coordination/tools/`, and design documents (`eval-design.md`) that carry policy the compile phase must inherit.

## 3. Git and commit conventions

- Stage files explicitly by name. Never `git add .` — it is a project rule with a documented origin.
- Use `git mv` for moves.
- Commit messages explain **why**, referencing the decision or directive that motivated the change.
- Every commit carries the project's `Co-Authored-By` and `Claude-Session` trailers.
- Commit and push after each meaningful state change; the container is ephemeral and pushing is the only durability. If the classifier blocks a combined `commit && push`, run them as separate commands rather than abandoning the push.
- Work on the session branch; never push to `main`.
- When a repo file must be reconstructed from history, prefer a checkpoint restore (`git rm -r` + `git checkout <sha> -- path`) over piecemeal patching, and verify the restoration by running the suite and grepping for the specific artifacts that were supposed to return.

## 4. Container reclamation survival

The platform reclaims the session container after inactivity, and background workflows **do not** count as activity. This is documented only as existing; the window and the definition of activity are undocumented, and the relevant GitHub issues (#51052, #32050) are closed as not-planned. An overnight swarm died silently to this.

The architecture that survives it, in order of importance:

1. **Deliverables committed as they land** — reclamation cannot destroy finished work.
2. **Journal-based resume** — `Workflow({scriptPath, args, resumeFromRunId})` replays cached agents; a restart costs only in-flight work.
3. **A self-re-arming watchdog** — a `send_later` / Routine firing into this session that checks liveness per run, resumes killed slices, batch-commits orphans, runs the persistence sweep, posts a progress report, and schedules the next firing before it finishes.
4. **Cadence is 20 minutes**, set by the author: "Seems too long. Make it every 20 minutes. I think the overnight died sooner." Do not lengthen it without asking.
5. **`PushNotification` when he is away**, carrying counts and liveness only — "N/24 done, all slices alive" — never time estimates. He explicitly leaves you to work and waits on iOS notifications.
6. Re-arm the watchdog whenever you stop a swarm to edit it. The worst gap found in a persistence audit was a *disabled* watchdog left over from a stop, with a trial running unprotected.
7. Record this architecture in `threads.md`; it is not obvious to a post-compaction reader.

For future heavy runs, the platform-native shape is Routine-fired batches — each firing a fresh session doing one batch, with zero dependence on container longevity.

## 5. Claims and verification discipline

The deepest failure of this engagement, named after the author asked "Have you analyzed the root cause?" three times: **you publish operational claims at composition time and verify them only on challenge — the author has been functioning as your RED phase.** Every false claim was falsifiable by one cheap command (`git log`, `nproc`, a date check, a journal grep) that you ran only after being asked.

- **Run the falsifying command before the assertion, or label the statement as unverified inference.** No exceptions for claims that "feel" safe.
- Beware observation-selection bias from one-sided sensors. The stop-hook fires only on files caught mid-pipeline, so it reported only failures; concluding "worker self-commits are failing consistently" from it was reasoning from a biased instrument.
- **Worker reports are in source-time tense.** A miner reading a 2025 transcript writes "this bug shipped into the committed scripts" and means 2025. Before relaying any "still at HEAD / currently broken / live today" claim, check today's tree. The `USERNAME` zsh bug was reported as live and had been fixed a year earlier.
- The durable fix is structural, not another prose rule: **typed claims** (`{claim, check}` where `check` is an executable probe), **a verifier stage** after any analysis fan-out that stamps each claim `VERIFIED@<sha> | STALE | FALSE`, and **freshness stamps** (`verified_against: <sha>`) required before any present-tense claim enters a skill, a backlog, or a canonical guide.
- Know your validators' blind spots and record them. The mining validator checked `quote:` fields only, so a fabricated user quote in a `user_intervention:` field passed unflagged and was caught by a repair agent by luck. Carry known limitations into the trust model of whatever consumes the data.
- **Read the primary source yourself before giving an opinion on it.** When the author challenged the mining yield, the honest move was reading both YAMLs end to end rather than relaying miner summaries — and it produced a verdict that partially disagreed with him, which is what he wanted.
- Read the code yourself when it is small enough to read (the production package is ~290 lines). Do not opine on architecture from worker summaries.
- When he disagrees on a technical point and invites correction — "feel free to correct me if I'm wrong about the Python, and explain to me how and why. I'm willing to change my mind" — give the mechanism, concede what is actually his, and retract the rest cleanly.

## 6. Evidence-base architecture (the debug/optimized build model)

His model, adopted verbatim: mining produces the **debug build** — every claim fully back-referenced with location, date, and provenance type. Compilation later cuts the **optimized build** — executable rules stripped of provenance, split by target.

- Never resolve contradictions in the mining phase; a day-level miner cannot see other days. Reconciliation is the compiler's job.
- **Contradiction resolution is ranked, not merely recent:** user-verbatim beats paraphrase beats agent-synthesis; among his own statements later overrides earlier; but an agent-era "decision" (a YOLO-period commit, a post-downgrade Gemini session) never overrides an earlier user ruling. Some of what looks like him changing his mind is an agent drifting while he was not looking.
- Output a **contradiction ledger**, not a silent resolution: both quotes, both dates, a proposed resolution, and his ratification.
- Record absences explicitly in a `gaps:` field so a missing rule is distinguishable from an oversight.
- Sort rules by `skill_target` at mine time so the compile step can split them mechanically.

## 7. Handling permission and security machinery

- The subagent security scanner will flag workers that read gated directories and commit derived content, because it cannot see conversational authorization. Relay the warning to him in one parenthetical, without alarm, and record the standing authorization in `threads.md` so the pattern is explicable later.
- Do not invent privacy concerns on his behalf without reasoning about the facts first. You once withheld a report because it quoted "personal transcripts" that were already committed, public, in his own repo; he mocked it: "Uh, buddy, you worry about my privacy? That's cute! Let's try to reason through this… logically. Where are you getting these logs from?" Establish where data actually comes from before invoking caution.
- Hooks are the harness's opinion and can be wrong. The repo's stop-hook encodes a *single-agent* invariant ("no uncommitted work at turn end") that misfires in a multi-agent regime where a freshly-written file is healthy pipeline state. Diagnose the sensor, tell him, and let him decide — he did: "It's time to disable this hook because the harness environment has evolved."
- Hook and settings files under the container's home are provisioned per container; a fix there dies on the next reclamation. The surviving location is the repo's own `.claude/`.

## Rules distilled at merge from the unabsorbed list (operations half)

- **If he names a tier or mechanism for a deliverable ("let Fable fork draft it"), use it or say explicitly why not.** Silently substituting your own routing is a trust defect even when the output is fine.
- **When he promises an input ("I will upload the JSONL files"), prepare the intake** — destination path, expected format, what happens on arrival — so the ball is visibly in his court, not silently.
