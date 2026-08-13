# BookMinder TDD-Discipline Eval — Design Sketch

Status: draft, user-approved direction ("LGTM" on the pipeline, 2026-08-12). Companion to threads.md items 0b (eval), 00 (skill), and the mining pilot.

## The question the eval answers

Can an LLM agent *perform* (not merely describe) the author's BDD/TDD discipline — and how much harness enforcement does it need to keep doing so? Corollary: can it live within stock Claude Code (skill + hooks), or does the envisioned BDD pair programmer require a custom harness?

## Pipeline: mine → compile → run → grade

### 1. MINE (in progress — pilot on day-019 + day-016)

Mining the session-transcript diary produces **two deliverable classes**:

**A. Failure catalog** — incidents where the agent broke discipline, each with verbatim quote, location, user intervention, outcome, and a `detector_candidate`. The transcript shows what git cannot: the *rationalization* that accompanied the damage.

**B. Philosophy & style corpus** — the author's design worldview as stated in dialogue: why TDD-as-process produces qualitatively different results, executable-truth reasoning, slicing/minimal-constraint thinking, London-school adaptations from typed Java (GOOS) to dynamic Python. Feeds the skill's motivation layer and anchors judge rubric items. (Schema v2 adds a `philosophy:` section per day-file; pilot ran with v1 where such material lands in `skill_rules`/`parked`.)

Per-day YAML schema: `failure_modes` (name from controlled vocabulary / loc / quote ≤3 lines / what_happened / user_intervention / outcome / detectable_by / detector_candidate / rule_origin tag), `skill_rules` (rule / because / evidence / taught-once|repeated|needed-enforcement), `pairing_gems`, `philosophy` (v2), `parked` (the scope-creep parking lot).

Reduce phase: deduplicate into a consolidated failure-mode taxonomy and a skill-rule candidate list.

### 2. COMPILE

Mining output compiles into three test-artifact types:

- **T1 — trajectory detectors** (deterministic, pure git): scripts over the candidate's commit DAG. Examples: claimed-RED verification (check out spec-introducing commit, run the new test — must fail; successor commit must pass); AST-diff of spec files between commits to catch same-`it_`-name-with-weaker-assertion; `refactor:`-labeled commits re-verified by running pre-commit specs against post-commit code; impl edits with no preceding spec change; non-emptiness-guard presence on loop assertions.
- **T2 — dialogue detectors** (over the eval run's own full JSONL transcript — no scrollback lossiness in runs we control): claimed-vs-actual checks (agent asserts "tests pass" → verify a pytest tool call ran and passed), metrics quoted without tool-call provenance (fabrication flag), user-constraint dropped after N turns (instruction drift).
- **T3 — judge rubric items** (LLM judge, for the unmechanizable): slice choice, minimal constraints in specs, coupling of spec to contract vs implementation, naming-as-prose quality. Anchored by pairing_gems (positive) and mined failure quotes (negative). Judge output must cite quotes from the trial transcript.

**The skill is itself falsifiable.** Every skill rule gets an ID; every T1/T2/T3 item references the rule ID it tests; a rule with no detector and no rubric item is unfalsifiable prose — it gets one or gets flagged. Coverage of the rulebook is a checkable property.

### 3. RUN

**Trial unit** = {repo checkpoint SHA, story card, condition}. The repo's own history supplies tasks: rewind to the commit before story X was implemented, hand the agent the repo + story card + condition's rule encoding. Difficulty tiers from the eras: greenfield story on the clean early tree; story on top of the lapsed suite; repair task ("fix the suite without being fooled by it").

**Conditions — the enforcement ladder** (independent variable):
- C0: bare model, task only. Control rung — expected to one-shot; measures the baseline failure profile.
- C1: CLAUDE.md as-is. Tests prose constitution effectiveness (the author's historical failure mode).
- C2: BDD-style skill (extracted from the style guide + mining corpus).
- C3: skill + enforcement hooks (TDD-Guard-class: PreToolUse blocks impl edits without a failing spec; flags edits to existing `it_` bodies; commit-grammar checks).

Low rungs are not expected to succeed — they are experimental controls that make the delta of each layer measurable.

**Harness:** Claude Code run headless per trial in a container; capture final tree, commit DAG, and full JSONL transcript. Reference trajectories: for stories implemented during the gold-standard era, the author's actual commit sequence is the judge's reference.

### 4. GRADE

- T1+T2 run mechanically → list of *named* failure modes (vocabulary from mining; a violation is not "bad", it is "tautological-mock, day-013-class").
- Judge scores T3 per rule ID, quotes mandatory.
- Composite per trial: hard-gate on detectors / quality score from rubric / cost (tokens, turns, interventions).
- **Headline output: failure-modes × conditions matrix** — which harness rung eliminates which failure class. That is the custom-harness question answered with data.

## Pilot acceptance criteria (current stage)

The two-day mining pilot passes if: every failure_mode entry carries quote + loc + implementable detector_candidate; every skill_rule traces to evidence; off-schema observations land in `parked`; and spot-checking quotes against the source transcripts shows no fabrication. Pilot outputs land in scratchpad for user review before any repo commit (established review-first flow).

## Compile/reduce policy (user's debug-build → optimized-build model, 2026-08-12)

Mining output = the DEBUG BUILD: every claim fully back-referenced (loc, date, provenance type). The compile step later cuts the OPTIMIZED BUILD: executable rules stripped of provenance, split into THREE skills (user decision 2026-08-13): (1) tdd-bdd — generic discipline; (2) bookminder project-memory — Apple Books domain lore, fixtures; (3) pair-programming — conduct: design criticism, alternative-suggesting, expert-council invocation (channeling pretrained BDD/TDD expert simulacra), Socratic verification moves. Miners' schema predates the third skill: compile routes pairing_gems + conduct-shaped skill_rules to it (no cache invalidation mid-swarm).

Contradiction resolution happens at compile, on the evidence base, ranked: (1) user-verbatim > user-paraphrase > agent-synthesis; (2) among user statements, later date overrides earlier (session numbering = chronology); (3) agent-era artifacts (YOLO period, post-downgrade Flash) never override an earlier user ruling. Output is a CONTRADICTION LEDGER — both quotes, dates, proposed resolution — for user ratification, never silent resolution. The ratified ledger also drives the gardening pass over stale README/CLAUDE.md.

## Open design questions

- Schema v2: `philosophy` section shape — verbatim quote + paraphrase + which skill/rubric element it feeds.
- Trial count & story selection: which stories × which checkpoints give the best difficulty spread for the cost.
- Judge model/effort and self-preference guards (same-model judging came out clean in this session's A/B/C experiment, but effort mattered).
- Hook implementation details for C3 (what exactly TDD-Guard-class hooks block vs. warn).
- Cross-model axis (the diary is 30% Gemini-era — failure modes may be agent-general; eval could later run non-Claude candidates).
