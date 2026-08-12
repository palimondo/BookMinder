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
- MINING PILOT (2026-08-12, user-directed): trial on day-019 (Claude, 43k, best corrective density) + day-016 (Gemini, 51k, hardest parse format, richest card refs) → .coordination/mining/day-NNN.yaml, fixed schema (failure_modes/skill_rules/pairing_gems/parked + controlled vocab). Evaluate outputs with user BEFORE full swarm. Picker corrected scout regex: Gemini marker "^│  > " (two spaces), only day-015/016. Runner-ups: day-018 (Claude), day-011/012 (Gemini)
- Diary access EXPANDED (2026-08-10, later): recon scout authorized inside claude-dev-log-diary incl. sampling raw transcripts; multi-agent swarm processing PRELIMINARILY authorized but NOT to launch until discussion. Key question: do full transcripts overlap the YAML-story-card era, or must user commit later JSONL backups first?
- .coordination/ committed to session branch `claude/bookminder-recall-5ite2s`; graduation to docs/ deferred to end of reevaluation
- Removed worker-added self-ignoring .gitignore (hid artifacts instead of preserving them)

## Review ledger (user's read state; NOTHING is repo rule until user approves wholesale)
- bdd-style-canonical.md: §1 reviewed in earlier form (gist approved, phrasing not); post-revision version NOT yet reviewed. NOT RATIFIED — not a rule of this repo
- claude-experiments.md: exec summary read via chat; doc itself skimmed at most
- process-evolution.md, repo-map.md, comparisons, bdd-style-fable/opus2: NOT read by user (reference only)

## Artifacts
- repo-map.md — sizes, land mines, access strategies
- bdd-style.md — gold-standard ATDD characterization + post-6f786cc lapse anatomy
- process-evolution.md — 7-era timeline, model history, failure modes, session-summary pass (714L)

## STABLE POINT (2026-08-10, user on break) — decisions & owed answers
APPROVED & DONE: CLAUDE.md commit-after-RED restored (git_workflow: 3 commits/cycle; tdd_discipline: Commit After RED step). NOT yet synced to AGENTS.md/GEMINI.md — project rule says ask user first. OWED: sync yes/no?
APPROVED, NOT YET EXECUTED: resurrect fixture-based sample acceptance specs killed in e5c7074.
RECOVERED: SPECS_REVIEW.md (325L) from dead branch b84f56e → .coordination/recovered/. User is reading it. The 2025 deep-research reports (ChatGPT/Claude/Perplexity on spec structure) NOT found in any branch's docs/ — OWED: where do they live?
STRUCTURE DECISION — EVIDENCE NOW COMPLETE, AWAITING USER GO/NO-GO: coordinator read recovered SPECS_REVIEW.md in full. Its verdict: original two-file structure was concern-based and correct; the taxonomy failed at CONCEPTION ("taxonomy is discovered, not imposed"); mixing levels within a concern-file is what describe/it is for; hijack risk is an ownership/naming problem (style rule + hook), not a directory problem. Three sources now align (post-reorg audit: nothing to port; SPECS_REVIEW; style guide rules) → checkpoint revert of specs/ to pre-9781be1 restores concern files + fixtures co-location + e5c7074-killed tests in one stroke. DIARY-SCOUT REPORT: moved out of repo to session scratchpad (verbatim transcript quotes; repo may be public) — OWED: commit / redact / keep local?
(Superseded framing below kept for history:) STRUCTURE DECISION — RESOLVED & EXECUTED (2026-08-12, user directive "restore by best available method"): spec tree restored wholesale to pre-reorg checkpoint c851f95 via git rm + checkout; 53 tests green; e5c7074-killed guarded fixture tests confirmed back (subsumes the approved resurrection). AGENTS.md/GEMINI.md converted to symlinks → CLAUDE.md (no model-specific content found worth preserving; both were stale restyled copies) — resolves the sync question. Whether structural steering is needed for current models: moved to evals, not assumed.
(superseded) STRUCTURE DECISION — CONTESTED, ON HOLD: user challenged coordinator's back-to-original recommendation. User's points: (1) 2025 all-model consensus was that MIXING test styles in one flat file caused wrong-style generation; (2) coordinator's "modern models don't need the taxonomy" = untested hypothesis, zero evidence — belongs in the EVAL; (3) why piecemeal instead of checkpoint revert? AUDIT ANSWER (new): only 3 commits touched bookminder/specs/conftest after e5c7074, ALL part of the same reorg day — nothing was built on top; wholesale spec-tree revert to pre-be394a0 loses nothing AND restores the e5c7074-killed tests for free. TENSION: revert also restores the mixed flat file the 2025 diagnosis blamed. Decision = user's, after break.
COORDINATOR FAILURE MODES logged this session: wall-of-text relapses (2x warned); overconfident assertion without evidence (structure/modern-models)
## Parked proposals (coordinator's, awaiting user go — resurface at the right moments)
P1. WALK-THE-WALK DEMO: one small repair story from the recovery plan, done live in-session in the style, user watching — converts "directionally correct" into pass/fail evidence. Cheapest first data point on whether Fable can perform (not just describe) the discipline. Parked: no code until user says go. Natural moment: right after structure decision.
P2. Delegation identity spec: `assert cli.SUPPORTED_FILTERS is library.SUPPORTED_FILTERS` — one-line falsifiable encoding of the CLI-borrows-library-vocabulary contract (user found the syntax reasonable). Fold into first repair story.
P3. Possible NEW STORY: `list all --filter cloud/!cloud` — currently validated but silently unimplemented (story predates the recent/all split; not a lapse-hole). Belongs in stories/ backlog only if user wants the behavior.
P4. Eval design draft as a document (Fable + full context) — user interested; explicitly AFTER more discussion.
P5. Hooks prototype (TDD-guard-style PreToolUse: block impl edits without a failing spec; flag edits to existing it_ blocks) — the enforcement rung of the eval ladder; also useful immediately if implementation resumes.

## Open threads
00. SKILL EXTRACTION (user-proposed): encode the BDD/TDD style as a Claude Code skill — user's London-school variation transposed from typed Java (GOOS) to dynamic Python, invented as he goes, outside pretraining; must be encoded to be followable. Style-guide SHAs = provenance noise in a rules doc; skill needs crisp imperative rules + motivation, evidence dossier stays separate. THE experiment's end-question: with skill in place, how much harness enforcement (hooks) is needed for discipline, how much customization for efficiency — can this live within Claude Code or does the envisioned BDD pair partner require a custom harness? Related learning: models talk the talk on TDD, walking the walk is the open question; in-context understanding ≠ correct actions.
0. A/B/C experiment RESOLVED (style-comparison.md + style-comparison-3way.md): rebriefed Opus (C) closed essentially the whole gap to Fable (B) — scores A 5/7/7.5/7, B 9/9/8.5/9, C 9/9/9.5/9. C found the fa0bc72 mutation at full depth; residual model gap ≈ zero on this task (single-run caveat); the doc-quality problem was the BRIEF (+effort), not the model. e5c7074 tautological-mock swap missed by all three extractors (judge-only find); HEAD still patches cli.SUPPORTED_FILTERS (specs/acceptance/cli_spec.py:67) → delegation property unspecified today. RECOMMENDED: canonical merge = C spine + B meta-insights + A HEAD-residue audit + judge findings. Merge not yet commissioned.
0b. Benchmark/eval design sketch (trajectory eval: deterministic commit-DAG checks + LLM-judge rubric; schema-drift maintenance axis) — user interested, Fable fork to draft AFTER more discussion. Design elements agreed in discussion: rewind-to-checkpoint trials (story card + repo state as task), enforcement ladder as independent variable (bare model → CLAUDE.md → skill → skill+TDD-guard-style hooks), deterministic failure-mode detectors from this session's catalog + judge rubric vs gold-standard reference trajectories that exist in history. TDD Guard (community CC plugin enforcing red-first) = rung 3 candidate, user was aware of it in 2025, never tested.
0c. TRANSCRIPT CORPUS (blocked on user): full JSONL session transcripts from 2025 exist as user's private backups, NOT in repo; the dialogue with the model is where full motivation lives — commits are the shadow, dialogue is the source. Proper reawakening requires reprocessing them: extract dialogue-level failure modes, define metrics/detectors from them for the eval. Waiting on user to supply/commit transcripts someday.
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
