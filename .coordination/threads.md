# Session Coordination Log

Persistent record for the reevaluation session (started 2026-08-10, first CC cloud-infra test drive). Survives compaction and container loss. Maintained by coordinator; updated as threads open/close.

## Session goal
Reevaluate dormant project (~1yr) with fresh perspective. No new feature code. Coordinator (Fable) delegates to workers (Opus 5 primary; Fable/fork when full context or max capability needed).

## Meta-goals (user's own framing, voice, 2026-08-10)
- Destination: MCP tool to discuss books with Claude; CLI first (user knows CLI design + TDD/BDD; MCP was unfamiliar)
- Core question: can an LLM be a good PAIR PROGRAMMER? (user had no colleagues to pair with)
- PAIRING DEFINED (user correction, emphatic): a partner to bounce ideas off — discussing the next step, how to define the test, how to minimize implementation surface area, what minimal constraints in the spec get the desired behavior. The discipline of dialogue. NOT about verifying the partner's claims — never fuse pairing with verification (a synthesizer did; user: "totally off base", "essayist tying a bow on unrelated things")
- Testbed deliberately chosen: Apple Books DB schema evolves with each release → tests long-term software evolution, opposite of one-shotting pretraining-known problems
- Method is the point: executable specs nail verifiable invariants; art = slicing the problem + designing specs with minimal coupling to implementation. London school (GOOS)
- ROOT PRINCIPLE (user, emphatic): the spec's job is nailing REQUIREMENTS IN A FALSIFIABLE WAY — that's the basis of the whole philosophy. Executable specification, GOOS layers, enforced layer separation, delegation contracts (library constants imported into CLI; mocks demonstrating inter-module delegation) all FOLLOW from it. Not parallel motivations — a hierarchy with falsifiability at the root
- Analyst reports = reference material, not agenda; keep session at high level

## Project history (user's account, voice, 2026-08-10)
- Summer 2025 intensity → BURNOUT. Models then knew the process but couldn't perform it (knowing vs. performing TDD — the key distinction)
- CC hooks = most valuable CC innovation (enforcement via automation, not prose)
- CC 1.x→2.x backwards-incompatible break soured user on interface stability; persists today. Still rates CC most mature CLI (> Codex, Gemini)
- Session-summary practice origin: copy-pasted console transcripts to Gemini for summaries → discovered JSONL transcripts → built xs → format churn kept breaking it
- User's view: dedicated transcript tool still better than ad-hoc scripts, but ecosystem churn ("move fast break things") makes maintaining one thankless

## Working style (user preferences)
- TERSE console replies — user reads incrementally, fires feedback mid-read; avoid wall-of-text spiral
- User quotes my text as a cursor showing where they are in reading
- Voice input: expect mistranscriptions
- NEVER attribute coordinator/worker words or findings to the user
- Protect main-thread context: delegate doc-heavy reads; use repo-map access strategies
- User approves commits/plans before execution (approval granted for this branch: coordinator may manage branch contents at own judgment; cleanup later)
- Worker default: effort XHIGH from 2026-08-10 onward (original three Opus workers ran at inherited session default)
- Markdown for user: never hard-wrap prose — iOS viewer breaks on every newline

## Decisions
- Diary access: transcript SUMMARIES + xs-generated summaries OK; raw transcripts off-limits
- .coordination/ committed to session branch `claude/bookminder-recall-5ite2s`; graduation to docs/ deferred to end of reevaluation
- Removed worker-added self-ignoring .gitignore (hid artifacts instead of preserving them)

## Artifacts
- repo-map.md — sizes, land mines, access strategies
- bdd-style.md — gold-standard ATDD characterization + post-6f786cc lapse anatomy
- process-evolution.md — 7-era timeline, model history, failure modes, session-summary pass (714L)

## Open threads
0. A/B/C experiment RESOLVED (style-comparison.md + style-comparison-3way.md): rebriefed Opus (C) closed essentially the whole gap to Fable (B) — scores A 5/7/7.5/7, B 9/9/8.5/9, C 9/9/9.5/9. C found the fa0bc72 mutation at full depth; residual model gap ≈ zero on this task (single-run caveat); the doc-quality problem was the BRIEF (+effort), not the model. e5c7074 tautological-mock swap missed by all three extractors (judge-only find); HEAD still patches cli.SUPPORTED_FILTERS (specs/acceptance/cli_spec.py:67) → delegation property unspecified today. RECOMMENDED: canonical merge = C spine + B meta-insights + A HEAD-residue audit + judge findings. Merge not yet commissioned.
0b. Benchmark/eval design sketch (trajectory eval: deterministic commit-DAG checks + LLM-judge rubric; schema-drift maintenance axis) — user interested, Fable fork to draft AFTER more discussion
1. Reevaluation discussion: meta-level project character (in progress, voice)
2. What graduates from .coordination/ → docs/ or new stories (end of session)
3. Dormant TODO: ATDD restoration; PR #18 unmerged (pre-YOLO restoration) — surfaced by analysis
4. Residue at HEAD (from bdd-style.md): dead TEST_HOME, duplicate describes, missing sqlite3.Error in list_all_books
5. CLAUDE.md self-contradiction: git_workflow vs tdd_discipline (commit-after-RED rule lost in revert)
6. Doc rot: README spec path, pre-commit-workflow.md (black/flake8 stale)
7. Cloud-infra quirks log: shallow clone (unshallowed), no tree cmd, no .venv, hook nags on untracked files

## Failure modes observed THIS session (meta-lab data)
- Coordinator misattributed analyst finding to user ("your own finding") — user flagged; standing guard
- Wall-of-text spiral risk from incremental reading + long replies
- Worker self-resolved hook nag via .gitignore * (silenced symptom, preempted pending decision)
