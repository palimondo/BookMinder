# Persistence — the substrate and the sweep

Load this page the moment you run a persistence sweep, commit or push, record a decision, correction, or proposal, or touch `.coordination/threads.md`.

The author will not be your reminder trigger: persistently record everything that exists only in session state and would not survive container restart or compaction, without being prompted.

**`.coordination/` is the durable substrate, and it is committed.** In this environment the git repo is the *only* cross-session memory — there is no auto-memory, no user-global CLAUDE.md, nothing that carries knowledge to the next cloud session. Verify this rather than assume it, then act accordingly.

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

## Git and commit conventions

- Stage files explicitly by name. Never `git add .`.
- Use `git mv` for moves.
- Commit messages explain **why**, referencing the decision or directive that motivated the change.
- Every commit carries the project's `Co-Authored-By` and `Claude-Session` trailers.
- Commit and push after each meaningful state change; the container is ephemeral and pushing is the only durability. If the classifier blocks a combined `commit && push`, run them as separate commands rather than abandoning the push.
- Work on the session branch; never push to `main`.
- When a repo file must be reconstructed from history, prefer a checkpoint restore (`git rm -r` + `git checkout <sha> -- path`) over piecemeal patching, and verify the restoration by running the suite and grepping for the specific artifacts that were supposed to return.
