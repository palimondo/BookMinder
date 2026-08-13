# Delegation — tiers, tool routing, briefs, swarms

Load this page the moment you are about to launch, brief, steer, or stop a worker, swarm, or workflow; choose a model tier or Agent-vs-Workflow routing; or decide how any large input gets read.

## Tier routing

The author's original instruction: delegate actual work to workers, "Opus 5 primary, or in cases where the highest level of intelligence or our full accumulated context is needed a Fable worker or fork of this main thread," while you gather context for high-level decisions. That sentence encodes three tiers, and they are not interchangeable.

- **Opus, `effort: 'xhigh'` — the default worker.** Use for all bulk and parallel work: archaeology over git history, corpus mining, scouts, reconnaissance, investigations, per-file extraction, repair agents. This is where volume lives; ~45 of this engagement's ~50 worker launches were Opus.
- **Fable, `effort: 'xhigh'` — judgment, synthesis, and prose the author will personally read and grade.** Reserve it for: comparing and judging worker outputs, synthesizing multiple extractions into one canonical document, revising a document against his stated corrections, and any deliverable that is itself a test of whether you understood him. Six invocations in the engagement, all of that shape.
- **Fork of this thread (`Agent` with `subagent_type: "fork"`) — only when the *input* is the conversation itself.** Fork when the task requires his voice-stated goals, the corrections he made in dialogue, and the accumulated session judgment — things no file contains. The canonical style synthesis was forked for exactly this reason: "it needs our full conversation context… to pass your real test — whether *we* understood what you were going for." Do not fork for work that reads files; that is a fresh worker's job and forking only pollutes it.
- **Effort is `xhigh` by standing order** since 2026-08-11: "from now on… extra high is our default." The one legitimate exception is mechanically-specified work with a structured output schema (splitting a file on banner boundaries ran at `effort: 'low'`).
- **If he names a tier or mechanism for a deliverable ("let Fable fork draft it"), use it or say explicitly why not.** Silently substituting your own routing is a trust defect even when the output is fine.

## Tool routing — the trade-off that decides everything

- The **`Agent` tool** spawns an individually addressable worker. You can `SendMessage` to it mid-flight to expand its scope or correct its trajectory (this is how the meta-analyst's diary access was widened), and its task-id can notify more than once. It has **no effort knob** and no orchestration.
- The **`Workflow` tool** runs a deterministic script that fans out agents with `agent(prompt, { model, effort, label, phase, schema })`, `phase()`, and `parallel([...])`. It gives you per-agent model and effort control, concurrency management, structured output schemas, and a journal that caches completed agents so a dead run resumes via `resumeFromRunId` without re-paying for finished work. Its agents are **not addressable** — `SendMessage` to them is refused; they do not appear in `ListAgents`.
- Therefore: **need xhigh, parallelism, or resumability → Workflow. Need to steer mid-flight → Agent.** Steering a workflow means stop → edit script → resume, and any agent whose prompt changed re-runs from zero. State this cost honestly as cache economics, not as impossibility — the author caught the sloppy version ("this categorical refusal now?") and he was right.
- Give every workflow script a stable path under `.coordination/tools/` and version it (`v2.1`, `v2.2`); commit the script itself so the run is reproducible after reclamation.

## Briefing workers

- **Brief design beats model tier.** The controlled A/B/C experiment settled this: the first extraction's shallowness was primarily *brief-induced*, and a re-briefed Opus at xhigh matched Fable. Before blaming a model, re-run with a better brief.
- **Demand motivation, not observation.** The author's core complaint about the first extraction: it "did not at all make any reasoning effort about the motivation… why am I doing things the way I'm doing things?" Every rule a worker extracts must be stated as "X because Y," and where the rationale is unrecoverable the worker must say so rather than invent one.
- **Control contamination explicitly.** "Give it all the advantages you can from the… repo map, process evaluation… but keep it fresh. Do not contaminate it with giving it the BDD style." Orientation documents = allowed and named; prior attempts at the same deliverable = forbidden and named.
- **Restart early rather than patch late.** When a brief is wrong and the worker is minutes in, `TaskStop` and relaunch with the corrected lens; a clean restart beats reconciling a misaimed deliverable.
- Give every worker its exact deliverable path, the no-hard-wrap rule, and a bounded return format ("return a max-10-line summary"). Long worker returns land in your context and become the wall of text.
- Forbid workers from touching tracked files other than their deliverable.
- Push attribution discipline into every worker schema: `source: user-verbatim | user-paraphrase | agent-synthesis`, with verbatim requiring an exact quote plus a line reference, and enforce it with a validator, not with instructions.

## Swarm operations

- **Workers commit their own deliverables as they finish.** The author's directive: "The worker should definitely be committing their deliverables as they finish their workloads," and his experience: "I have been using the commit your own workload as you go technique without any issues in other projects — they have completely disjoined workloads." Bake a self-commit stage into the workflow script. Do not hold deliverables in scratchpad; scratchpad dies with the container.
- Concurrent commits do not race meaningfully — disjoint files means no merge conflicts, and git's `index.lock` fails loudly and retries cleanly. Do not use race fear as a reason to centralize commits; a coordinator batch-commit sweep is a *backstop* only (firing-time rules in `liveness.md`).
- **Use an uncommitted scratchpad file as the inter-agent coordination channel** when workers need to resolve something between themselves; the Write tool's stale-detection forces a re-read when another worker has modified it.
- **Slice for concurrency.** A single workflow's cap is `min(16, nproc - 2)`; on a 4-core container that is 2. Slicing 24 units across three workflows with an `args` array tripled effective concurrency. Take an arg-sliced variant of the swarm script as the normal shape for large runs.
- **Drain before kill.** Never `TaskStop` a run without first checking in-flight agents' progress; killing to re-slice burned ~357K tokens of nearly-complete work and the author noticed: "you should have not killed the workflow so aggressively, you wasted almost 400k tokens there." If in-flight agents are deep, let them finish and self-commit, then stop.
- **Pilot before swarm.** Two units first, inspect the raw output together, then scale. The pilot caught a parsing error (`^│  > ` with two spaces, only on two files) that would have silently broken the full run.
- **Enforce schemas with a script, not with prose.** "I think that's a best practice, to use scripts and tools to enforce basic rules. Of course, you have a flexible schema where the agents have the ability to extend it, but where you require the base set." Write a validator that checks required fields *and* greps every `quote:` against its source file so paraphrase-as-quote fails mechanically. Run it over the whole harvest and dispatch repair agents for violations.
- When a validator reports a wall of violations, check whether the *validator* is wrong first — 51 of 62 raw violations in this engagement were validator artifacts (enum drift, shard prefixes, box glyphs, elision handling), not miner errors.

## Context protection

- "It's imperative that you protect your context from pollution from large docs." Delegate the reading of large artifacts and take back only summaries — but when your opinion is what he wants, read the primary source yourself (see `claims.md`).
- Get a repo map with file sizes and land mines before touching anything, and keep it committed so workers can choose access strategies too.
- Grep large reference files; never read them whole.
- Cloud clones arrive **shallow**. Run `git fetch --unshallow` before any history archaeology, or the whole project history will be invisible.
