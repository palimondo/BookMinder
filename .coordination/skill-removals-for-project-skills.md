# Fragments removed from the project-coordinator skill during generalization — awaiting absorption into the bookminder project skill

## From SKILL.md

- Frontmatter/page-map trigger routing the pipeline through claims discipline: "Making or relaying any operational claim — done, running, broken, fixed, live at HEAD; running or judging the mining/compile pipeline → `references/claims.md`"

## From references/claims.md

- Page trigger: "or run, design, or judge the mining/compile evidence pipeline."
- "A miner reading a 2025 transcript writes "this bug shipped into the committed scripts" and means 2025." … "The `USERNAME` zsh bug was reported as live and had been fixed a year earlier."
- "Know your validators' blind spots and record them. The mining validator checked `quote:` fields only, so a fabricated user quote in a `user_intervention:` field passed unflagged and was caught by a repair agent by luck."
- "When the author challenged the mining yield, the honest move was reading both YAMLs end to end rather than relaying miner summaries — and it produced a verdict that partially disagreed with him, which is what he wanted."
- "Read the code yourself when it is small enough to read (the production package is ~290 lines)."
- Entire section:

> ## Evidence-base architecture (the debug/optimized build model)
>
> His model, adopted verbatim: mining produces the **debug build** — every claim fully back-referenced with location, date, and provenance type. Compilation later cuts the **optimized build** — executable rules stripped of provenance, split by target.
>
> - Never resolve contradictions in the mining phase; a day-level miner cannot see other days. Reconciliation is the compiler's job.
> - **Contradiction resolution is ranked, not merely recent:** user-verbatim beats paraphrase beats agent-synthesis; among his own statements later overrides earlier; but an agent-era "decision" (a YOLO-period commit, a post-downgrade Gemini session) never overrides an earlier user ruling. Some of what looks like him changing his mind is an agent drifting while he was not looking.
> - Output a **contradiction ledger**, not a silent resolution: both quotes, both dates, a proposed resolution, and his ratification.
> - Record absences explicitly in a `gaps:` field so a missing rule is distinguishable from an oversight.
> - Sort rules by `skill_target` at mine time so the compile step can split them mechanically.

## From references/authorization.md

- Named-consumer examples: ""Philosophy extraction: not scope creep — it has a named consumer" is the test. Failure catalogue → detectors; philosophy corpus → skill's WHY layer and judge rubric anchors."
- "Provenance archaeology is **a tag, not a task**: attach `rule_origin:` in passing, never run a dedicated pass for it."
- Parked-proposal resurfacing example: "(e.g. a restoration creating the demo target P1 was waiting for)"
- Over-fencing incident: "When you proposed splitting council-fidelity work out of the miners' schema as "creep," he pushed back — "You think documenting and diagnosing expert council failure is a scope creep for the mining agents? 🤔 really?" — and he was right; the split was over-optimization defending a cache that did not exist."
- Acceptance-criteria example for the mining swarm: "the swarm passes if every failure mode carries a quote plus a detector candidate, and every rule candidate traces to an incident."
- Stop-hook specifics: "The repo's stop-hook encodes a *single-agent* invariant ("no uncommitted work at turn end") that misfires in a multi-agent regime where a freshly-written file is healthy pipeline state. Diagnose the sensor, tell him, and let him decide — he did: "It's time to disable this hook because the harness environment has evolved.""

## From references/delegation.md

- "corpus mining" as a named Opus-tier workload.
- Fork rationale for the style synthesis: "The canonical style synthesis was forked for exactly this reason: "it needs our full conversation context… to pass your real test — whether *we* understood what you were going for.""
- Brief-vs-tier evidence: "The controlled A/B/C experiment settled this: the first extraction's shallowness was primarily *brief-induced*, and a re-briefed Opus at xhigh matched Fable."
- Motivation complaint about the first extraction: it "did not at all make any reasoning effort about the motivation… why am I doing things the way I'm doing things?"
- Contamination directive for extraction briefs: "Give it all the advantages you can from the… repo map, process evaluation… but keep it fresh. Do not contaminate it with giving it the BDD style."
- Pilot finding: "The pilot caught a parsing error (`^│  > ` with two spaces, only on two files) that would have silently broken the full run."
- Validator-artifact evidence: "51 of 62 raw violations in this engagement were validator artifacts (enum drift, shard prefixes, box glyphs, elision handling), not miner errors."

## From references/persistence.md

- Substrate map, project-specific entries: "`mining/` (extracted-knowledge corpus: v2 = current schema, pairing/ = council-fidelity trial, v1 = superseded pilots) · `eval-design.md` (pipeline + compile policy + claims-verification design) · `verified-residue.md` (the stamped current repair backlog — the work queue, not the narrative docs) · `recovered/` (artifacts restored from dead branches)"
- "design documents (`eval-design.md`) that carry policy the compile phase must inherit"
- "This is the project's own stickiness law applied to yourself: corrections shipped as automation stick; as prose they only partly stick."

## From references/register.md

- Bow-tying incident: "it produced the single worst deliverable of the engagement (a fused pairing/verification motivation that was "totally off base")."

## Second-pass removals (specificity audit)
- Mining schema attribution enum verbatim: `source: user-verbatim | user-paraphrase | agent-synthesis` + exact-quote-plus-line-reference requirement (validate_mining.py enforces).
- Mining validator mechanics: grep every `quote:` field against its source transcript file.
