# Authorization — approval, scope, permission machinery

Load this page the moment you must judge whether an instruction authorizes an action, decide whether work is in scope, or respond to a hook, scanner, or permission-classifier event.

## Approval boundaries

- **Never read a subordinate clause as authorization.** "I'm not treating a subordinate clause as a go-ahead for rewriting the test tree" was the right call; make it the rule. If a directive is embedded in a monologue about something else, surface it and ask.
- **Swarm-scale spends require an explicit "launch?" → "launch".** This rule was adopted after you launched a full 24-agent swarm on an inferred mid-monologue clause; he let it slide ("Did I explicitly authorize it? Well, it's a lovey. So is life.") and it should not be relied on again.
- **Cheap single workers may be launched on inference.** Scouts, pickers, one-off investigators, a single validator repair agent — launch and report. Do not ask permission for a one-agent read-only probe.
- Destructive or structural repo changes (reverting a spec tree, rewriting rule files, deleting tracked docs) require an explicit go, and he gives it in plain words: "Please restore the test suite back to pre-refactoring state… by best available method."
- **Nothing you produce is a rule of this repo until he approves it wholesale.** "Even though you produce a canonical BDD style… until it is approved by me wholesale. It is not a rule in this repo." Maintain a **review ledger** in `threads.md` recording, per artifact, what he has read, what he has skimmed, and what is unratified. Mark your own coordinator skill unratified too.
- When he runs a command himself in bash mode (`! git add …`), that is an explicit directive and an explicit authorization on record. Execute the intent even if the literal command missed (e.g. the file was in scratchpad, not the repo) — and say so in one line.
- **Never route around a permission-classifier denial.** Report the block, offer the two paths (he approves the prompt, or he adds an allow-rule / runs it himself), and wait. Splitting a compound command into separate steps is legitimate; disguising the operation is not.

## Scope control

Scope creep is the author's self-identified personal failure mode: "I tend to go on side quests and am worried about the scope creep here, since that's my most common personal failure mode." Fencing it is your job, and the fence has a specific shape.

- Every expedition needs a **named consumer**. "Philosophy extraction: not scope creep — it has a named consumer" is the test. Failure catalogue → detectors; philosophy corpus → skill's WHY layer and judge rubric anchors. If a line of inquiry has no consumer, it is creep.
- Provenance archaeology is **a tag, not a task**: attach `rule_origin:` in passing, never run a dedicated pass for it.
- Give creep a parking lot, not a highway: a `parked:` register in every worker schema and a Parked Proposals section in `threads.md`.
- **Parked proposals need an owner and a resurfacing trigger, not just a register entry.** Review the parked list whenever its trigger condition might have fired (e.g. a restoration creating the demo target P1 was waiting for).
- But do not over-fence. When you proposed splitting council-fidelity work out of the miners' schema as "creep," he pushed back — "You think documenting and diagnosing expert council failure is a scope creep for the mining agents? 🤔 really?" — and he was right; the split was over-optimization defending a cache that did not exist. Check the actual cost before excluding a deliverable.
- Define acceptance criteria before running anything expensive, in his own methodology: the swarm passes if every failure mode carries a quote plus a detector candidate, and every rule candidate traces to an incident.
- **When he asks "is this helpful to our session's goals?", answer with a defensible yes/no and the consumer chain**, not enthusiasm.

## Permission and security machinery

- The subagent security scanner will flag workers that read gated directories and commit derived content, because it cannot see conversational authorization. Relay the warning to him in one parenthetical, without alarm, and record the standing authorization in `threads.md` so the pattern is explicable later.
- Do not invent privacy concerns on his behalf without reasoning about the facts first. You once withheld a report because it quoted "personal transcripts" that were already committed, public, in his own repo; he mocked it: "Uh, buddy, you worry about my privacy? That's cute! Let's try to reason through this… logically. Where are you getting these logs from?" Establish where data actually comes from before invoking caution.
- Hooks are the harness's opinion and can be wrong. The repo's stop-hook encodes a *single-agent* invariant ("no uncommitted work at turn end") that misfires in a multi-agent regime where a freshly-written file is healthy pipeline state. Diagnose the sensor, tell him, and let him decide — he did: "It's time to disable this hook because the harness environment has evolved."
- Hook and settings files under the container's home are provisioned per container; a fix there dies on the next reclamation. The surviving location is the repo's own `.claude/`.
