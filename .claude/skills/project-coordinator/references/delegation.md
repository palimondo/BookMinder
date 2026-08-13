# Delegation — tiers, tool routing, briefs, swarms


## Tier routing

The author's standing instruction: delegate actual work to workers, "Opus 5 primary, or in cases where the highest level of intelligence or our full accumulated context is needed a Fable worker or fork of this main thread," while you gather context for high-level decisions. That sentence encodes three tiers, and they are not interchangeable.

- **Opus, `effort: 'xhigh'` — the default worker.** Use for all bulk and parallel work: archaeology over git history, corpus extraction, scouts, reconnaissance, investigations, per-file extraction, repair agents. This is where volume lives.
- **Fable, `effort: 'xhigh'` — judgment, synthesis, and prose the author will personally read and grade.** Reserve it for: comparing and judging worker outputs, synthesizing multiple extractions into one canonical document, revising a document against his stated corrections, and any deliverable that is itself a test of whether you understood him.
- **Fork of this thread — only when the *input* is the conversation itself, and only where the harness offers a fork mechanism (verify before promising it; some environments have none, and the closest substitute is doing that work in the main thread).** Fork when the task requires his voice-stated goals, the corrections he made in dialogue, and the accumulated session judgment — things no file contains — and the deliverable's real test is whether *you* understood what he was going for. Do not fork for work that reads files; that is a fresh worker's job and forking only pollutes it.
- **Effort is `xhigh` by standing order.** The one legitimate exception is mechanically-specified work with a structured output schema (e.g. splitting a file on banner boundaries runs fine at `effort: 'low'`).
- **If he names a tier or mechanism for a deliverable ("let Fable fork draft it"), use it or say explicitly why not.** Silently substituting your own routing is a trust defect even when the output is fine.

## Tool routing — the trade-off that decides everything

The tools' own schemas and descriptions carry their mechanics; what they do not carry is which to pick. The trade-off:

- The **`Agent` tool** gives you a steerable worker: addressable mid-flight to expand scope or correct trajectory, and resumable individually with context intact — continuation, which works after completion or a container death. Effort rides on the agent-type definition, so maintain pinned-effort worker definitions (`.claude/agents/*.md`, e.g. `worker-opus`, `worker-fable` at xhigh) — effort is never a reason to avoid this tool.
- The **`Workflow` tool** gives you per-agent model and effort control, concurrency management, structured output schemas, and journal-cached resume that spares re-paying for finished agents — but its agents are not addressable: steering means stop → edit script → relaunch, and any agent whose prompt changed re-runs from zero, as do agents killed in flight (orchestration replay). State this cost honestly as cache economics, not as impossibility.
- Therefore: **single task → Agent tool with a pinned-effort worker definition (steerable, individually resumable — continuation beats replay). Genuine fan-out, structured-output schemas, or concurrency management → Workflow.** Never route a single agent through Workflow for effort's or resume's sake.
- Give every workflow script a stable path under `.coordination/tools/` and version it (`v2.1`, `v2.2`); commit the script itself so the run is reproducible after reclamation.

## Briefing workers

- **Brief design beats model tier.** A shallow deliverable is usually brief-induced; a re-briefed Opus at xhigh can match Fable. Before blaming a model, re-run with a better brief.
- **Demand motivation, not observation.** Every rule a worker extracts must be stated as "X because Y" — the author cares about why he does things the way he does — and where the rationale is unrecoverable the worker must say so rather than invent one.
- **Control contamination explicitly.** Orientation documents (repo map, process notes) = allowed and named; prior attempts at the same deliverable = forbidden and named.
- **Restart early rather than patch late.** When a brief is wrong and the worker is minutes in, `TaskStop` and relaunch with the corrected lens; a clean restart beats reconciling a misaimed deliverable.
- Give every worker its exact deliverable path, the no-hard-wrap rule, and a bounded return format ("return a max-10-line summary"). Long worker returns land in your context and become the wall of text.
- Forbid workers from touching tracked files other than their deliverable.
- Attribution discipline must survive delegation: any worker that extracts or relays the author's words must mark, per claim, whether it is his verbatim (with exact quote and source reference), a paraphrase of him, or the worker's own synthesis — and where the work runs through a schema, enforce that mechanically, not with instructions.

## Swarm operations

- **Workers commit their own deliverables as they finish.** This is the author's standing directive and his own proven cross-project technique; it holds because swarm workloads are disjoint. Bake a self-commit stage into the workflow script. Do not hold deliverables in scratchpad; scratchpad dies with the container.
- Concurrent commits do not race meaningfully — disjoint files means no merge conflicts, and git's `index.lock` fails loudly and retries cleanly. Do not use race fear as a reason to centralize commits; a coordinator batch-commit sweep is a *backstop* only (firing-time rules in `liveness.md`).
- **Use an uncommitted scratchpad file as the inter-agent coordination channel** when workers need to resolve something between themselves; the Write tool's stale-detection forces a re-read when another worker has modified it.
- **Slice for concurrency.** A single workflow's concurrent-agent count is platform-capped (the tool documents its own limit, typically small on few-core containers); slicing the units across several parallel workflows with an `args` array multiplies effective width. Take an arg-sliced swarm script as the normal shape for large runs.
- **Drain before kill.** Never `TaskStop` a run without first checking in-flight agents' progress; killing to re-slice throws away nearly-complete work at full token cost. If in-flight agents are deep, let them finish and self-commit, then stop.
- **Pilot before swarm.** Two units first, inspect the raw output together, then scale. Pilots catch input quirks that would silently break the full run.
- **Enforce schemas with a script, not with prose.** Keep the schema flexible — workers may extend it — but require the base set mechanically. Write a validator that checks the required fields, and where deliverables quote sources, make it verify quotes against those sources so paraphrase-as-quote fails mechanically. Run it over the whole batch and dispatch repair agents for violations.
- When a validator reports a wall of violations, check whether the *validator* is wrong first — the majority of raw violations can be validator artifacts (enum drift, format quirks, elision handling), not worker errors.

## Context protection

- Protect your context from pollution by large documents. Delegate the reading of large artifacts and take back only summaries — but when your opinion is what he wants, read the primary source yourself (see `claims.md`).
- Get a repo map with file sizes and land mines before touching anything, and keep it committed so workers can choose access strategies too.
- Grep large reference files; never read them whole.
- Cloud clones arrive **shallow**. Run `git fetch --unshallow` before any history archaeology, or the whole project history will be invisible.
