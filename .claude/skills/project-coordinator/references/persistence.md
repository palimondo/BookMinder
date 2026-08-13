# Persistence — the substrate and the sweep


The author will not be your reminder trigger: persistently record everything that exists only in session state and would not survive container restart or compaction, without being prompted.

**`.coordination/` is the durable substrate, and it is committed.** How urgent its durability is depends on the environment — see the split below.

The substrate's fixed core: `threads.md` (the standing record, structure below) · `tools/` (committed runnable scripts: validators, scanners, versioned swarm scripts). Project-specific corpora, design documents, and work queues live alongside these; keep their map current in `threads.md`. Graduation into docs/ or skills is the author's call.

## threads.md — the single standing record

Keep these sections live:

- **HANDOFF — READ FIRST AFTER COMPACTION** at the very top: current phase state, where artifacts live, how to verify them, what must not be started without his go, and what inputs are pending from him.
- **Session goal and meta-goals**, in his framing, attributed.
- **Working style rules** — every conduct correction he has made, with his short verbatim phrase attached so the rule keeps its teeth.
- **Decisions and authorizations**, dated, including scope grants (what a worker may read) and standing authorizations.
- **Open threads**, numbered, each with its blocking condition.
- **Parked proposals** — *your* ideas awaiting his go, each with the moment it should resurface, so none is lost in the flood of a long session.
- **Review ledger** — his read state per artifact and its ratification status.
- **Operations ledger** — live state: what is running, what is stopped, what awaits which decision, with run IDs and script paths.
- **Failure modes observed** — your own errors, with root cause, as meta-lab data.

## The sweep

**The persistence sweep is machinery, not discipline.** At every watchdog firing, every task-notification, and before ending any substantial turn: diff "what exists only in conversation context" against "what is committed," and commit the delta. Embed this instruction in the watchdog trigger's own prompt so it fires by machinery. This is the stickiness law applied to yourself: corrections shipped as automation stick; as prose they only partly stick.

Also persist: scripts you wrote (validators, scanners, workflow scripts) into `.coordination/tools/`, and design documents that carry policy later phases must inherit.

## Git and commit conventions — evergreen (every environment)

- Stage files explicitly by name. Never `git add .`.
- Use `git mv` for moves.
- Commit messages explain **why**, referencing the decision or directive that motivated the change.
- Follow the environment's mandated git conventions — commit trailers and branch targets arrive with the harness or per-session directives; honor them, do not restate them here.
- Commit after each meaningful state change — commit cadence is evergreen; PUSH cadence is environment-conditional (below).
- When a repo file must be reconstructed from history, prefer a checkpoint restore (`git rm -r` + `git checkout <sha> -- path`) over piecemeal patching, and verify the restoration by running the suite and grepping for the specific artifacts that were supposed to return.

## Environment-conditional: push policy and memory

- **Ephemeral infra (remote cloud container; CI such as GitHub Actions): push after each meaningful state change.** The workspace can be wiped at any time; pushing is the only durability, and the pushed repo is the only cross-session memory (remote containers have no auto-memory and no user-global CLAUDE.md — verify rather than assume). If a permission layer blocks a combined `commit && push`, run them as separate commands rather than abandoning the push.
- **Local machine: commit per the evergreen conventions, but PUSHING IS THE AUTHOR'S DECISION — do not push without his word.** The workspace persists; there is no wipe pressure, and he reserves the push call for himself.
- Determine which regime you are in at session start, before adopting a push cadence.
