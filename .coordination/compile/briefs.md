# Compile-phase worker briefs — verbatim record

Replicability record for the process that produced the contradiction ledger, the three skills, and their verification. Every prompt below is character-exact as sent. The same prompts also live natively in the session transcript (`claude-dev-log-diary/jsonl/cloud-2026/`, subagent files carry each brief as their first user message); this file is the curated index so a rerun (e.g. after the 2025 JSONL corpus arrives and mining extends) does not depend on transcript archaeology.

Pipeline order: (1) ledger brief → author ratification of judgment-calls (interactive, see session transcript) → ratification record appended to ledger → (2) three compile briefs in parallel → (2b) mid-flight correction to all three → (3) six smoke scenarios → coordinator verification (validator re-run, disposition coverage script, falsifiability grep — commands recorded at the end).

Worker routing: all compile/ledger workers = `worker-fable` agent type (`.claude/agents/worker-fable.md`, pinned effort xhigh) — deliverables the author personally reads and grades. Smoke agents = `worker-opus` (pinned xhigh) — deliberately NOT Fable, and briefed blind: no session context, skill directory only. During a 529-overload storm the compile workers were cut repeatedly and resumed via SendMessage transcript continuation; the standing resume instruction was: resume per brief + correction, re-check disk state before rewriting, commit deliverables incrementally as each reaches a consistent state.

To rerun after corpus extension: refresh the contradiction ledger first (its brief takes the new YAMLs), have the author ratify new judgment-calls, then re-send the three compile briefs unchanged — they read the corpus and ledger from paths, not from inlined content. Expect updated ledger-ruling lists in the briefs' AUTHORITY ORDER sections to need a mechanical refresh (the L-NN enumerations are snapshots).

---

## 1. Contradiction-ledger worker (worker-fable, xhigh)

```
You are producing the CONTRADICTION LEDGER for the BookMinder compile phase. Repo: /home/user/BookMinder, branch claude/bookminder-recall-5ite2s (already checked out).

TASK: Sweep the mining corpus for contradictions and produce a ledger the author will personally ratify. Two contradiction classes:
(A) INTERNAL — statements in the corpus that contradict each other (rule vs rule, philosophy vs rule, earlier ruling vs later ruling).
(B) CORPUS-VS-REPO — corpus rulings that contradict what the repo's governing documents currently say (CLAUDE.md, .coordination/bdd-style-canonical.md, README.md). These become the gardening-pass work items.

INPUTS (read these; grep large files rather than reading whole):
- .coordination/mining/v2/*.yaml — 24 validated harvest files (schema v2.2). Primary evidence base. Fields carry provenance typing: user-verbatim | user-paraphrase | agent-synthesis.
- .coordination/mining/pairing/*.yaml — council-fidelity trial output.
- CLAUDE.md, .coordination/bdd-style-canonical.md (NOT ratified by the author — treat as draft, not authority), README.md.
- .coordination/eval-design.md §"Compile/reduce policy" — the resolution rules you must apply.

RESOLUTION RULES (from eval-design.md, author-approved — apply exactly):
1. Provenance rank: user-verbatim > user-paraphrase > agent-synthesis.
2. Among user statements, later date overrides earlier (day-file numbering = chronology; the live session's 2026-08 rulings recorded in .coordination/threads.md are latest of all).
3. Agent-era artifacts (YOLO period, post-Flash-downgrade Gemini — era_class marks these) NEVER override an earlier user ruling.
4. You PROPOSE resolutions; you never resolve silently. Every entry ships both sides verbatim so the author can overrule you.

LEDGER ENTRY FORMAT (one per contradiction):
- id: L-NN
- class: internal | corpus-vs-repo
- side_a / side_b: each with verbatim quote (character-exact from source — if you cannot quote character-exact, say so and cite location instead), source file + loc, date/era, provenance type
- proposed_resolution: which side wins under the rules, stated as a rule the compile step can execute
- confidence: rule-mechanical (the ranks decide it) | judgment-call (ranks tie or don't apply — flag prominently for the author)
- consumers: which of the three skills (tdd-bdd / pair-programming / bookminder project-memory) or gardening pass the resolution feeds

ATTRIBUTION DISCIPLINE (hard requirement): never present your own synthesis as the author's position. Every claim about what the author wants carries its provenance type. Where a YAML field's provenance is agent-synthesis, say so — it ranks lowest.

CLAIMS DISCIPLINE: any present-tense assertion about the repo ("CLAUDE.md says X") must carry file:line you actually verified against the current tree.

DELIVERABLE: .coordination/compile/contradiction-ledger.md. Structure: short header stating scope + method (no essay), then entries grouped by class, judgment-calls listed FIRST within each group (they need the author's eyes most), rule-mechanical after. End with a one-table index: id | one-line description | proposed winner | confidence.

FORMATTING (hard requirements): never hard-wrap prose — one line per paragraph or bullet; tables/code blocks exempt. No praise, no meta-narration, no filler.

Do not touch any tracked file other than your deliverable. When done: git add .coordination/compile/contradiction-ledger.md && git commit (message explains why the ledger exists — feeds compile-phase contradiction resolution per eval-design.md — not what files changed) && git push -u origin claude/bookminder-recall-5ite2s (retry up to 4 times with 2s/4s/8s/16s backoff on network failure only).

RETURN: max 10 lines — entry counts per class, count of judgment-calls, the 3 highest-stakes entries by id + one-line each, commit SHA.
```

KNOWN BRIEF DEFECT (author-caught, fix on rerun): telling the worker to treat threads.md/eval-design.md session rulings as an evidence LAYER invited self-litigation — contradictions between two coordinator-recorded session notes (L-03/L-04, withdrawn). Rerun fix: instruct that threads.md rulings are SETTLED ADJUDICATIONS — usable to resolve corpus contradictions, never eligible as a contradiction side themselves.

## 2. Compile brief — tdd-bdd (worker-fable, xhigh)

```
You are compiling the tdd-bdd SKILL for the BookMinder compile phase. Repo: /home/user/BookMinder, branch claude/bookminder-recall-5ite2s (checked out).

WHAT THIS SKILL IS: the author's BDD/TDD discipline as a portable, generic Claude Code skill — his London-school (GOOS) outside-in ATDD variation, transposed from typed Java to dynamic Python, invented as he went, outside pretraining. It must let a fresh agent PERFORM the discipline, not describe it. Root principle (author, emphatic): the spec's job is nailing REQUIREMENTS IN A FALSIFIABLE WAY — executable specification, layer separation, delegation contracts all FOLLOW from that root. Structure the WHY layer as this hierarchy, not parallel motivations.

AUTHORITY ORDER for content:
1. .coordination/compile/contradiction-ledger.md — read FIRST, including the "Ratification record" section at top. Its resolutions OVERRIDE everything: L-01 (both rules: exact identity sets where membership IS the requirement; never encode behavioral contracts via fixture cardinality — test limit properties at the layer that controls volume), L-02 (walking-skeleton phase exempt from ceremony, generally — author-ruled), L-05 (fake only while something red still pulls; a fake that greens the outermost RED owes a unit-driven real implementation, never a fake-detecting meta-test), L-06 (docstrings: pending-skipped specs only, deleted on implementation), L-09 (front-door fixture seam; module constants carry in-process-only caveat), L-14 (commit-after-RED wins; RED commits and deliberately-red acceptance tests are exceptions to all-tests-passing), L-16 (no type-hint demands on spec functions).
2. .coordination/mining/v2/*.yaml — entries with skill_target: tdd-bdd (also sweep claude-md-targeted entries for discipline rules that belong here). Fields: rule, because, evidence, enforcement history (taught-once|repeated|needed-enforcement). The philosophy: sections feed the WHY layer.
3. CLAUDE.md tdd_discipline/code_style sections — the commit grammar (RED commit → GREEN commit → REFACTOR commit) is author-restored and authoritative.
CONTAMINATION CONTROL: .coordination/bdd-style-canonical.md is an UNRATIFIED agent-synthesis draft — you may read it for orientation, but NO rule may rest on it alone; every rule must trace to the YAML corpus, the ledger, or CLAUDE.md. Never import its §5 repo-state claims (ledger L-17 falsified them). Do not read .coordination/mining/v1/ (superseded pilots).

CONTENT DOMAINS to cover (as the corpus supports them — do not invent): outside-in ATDD flow and the red-acceptance-on-main convention; RED→GREEN→REFACTOR with commit-after-RED grammar and its WHY (rewindability, instruction pressure, process-over-one-shotting); spec style (describe_/it_ naming as prose, pytest --spec as living documentation, docstring pending-convention); assertion integrity (minimal constraints, exact identity sets, no cardinality contracts, non-emptiness guards on loop assertions, no tautological mocks, no weakening an existing it_ to get green); minimality/YAGNI; layering and seams (front-door fixtures, delegation contracts between layers); fakes discipline; walking-skeleton exemption; falsify-before-claiming-done.

FORM (template: .claude/skills/project-coordinator/ — read its SKILL.md and one reference page for the shape):
- .claude/skills/tdd-bdd/SKILL.md: frontmatter (name, description = what + when to use, nothing else) + compact core (invariants + activity-keyed page map, aim ≤40 lines).
- references/*.md: activity-keyed pages (e.g. writing-a-spec, red-green-refactor cycle + commits, assertion integrity, layering/seams — choose the cut that matches real activation moments).
- Every rule: crisp imperative + its WHY ("X because Y"); where the rationale is unrecoverable from the corpus, say "rationale unrecovered" rather than inventing one. Every rule gets an ID (T-NN).
- OPTIMIZED BUILD: no provenance, dates, SHAs, day-refs, or author-history in the skill text. PORTABLE: no BookMinder-specific content (Apple Books, fixture filenames, repo paths) — route such fragments to the disposition table marked reroute:project-memory. No harness-injected rules (git trailers, branch policy, tool schemas).

SIDECARS (these carry what the skill text omits):
- .coordination/compile/rule-index-tdd-bdd.md: table rule ID → source (yaml file + rule id + day:loc | ledger L-NN | CLAUDE.md:line) → provenance type. Every T-NN appears.
- .coordination/compile/disposition-tdd-bdd.md: EVERY skill_target:tdd-bdd entry in the corpus dispositioned: compiled→T-NN | merged-duplicate→T-NN | rejected(reason) | reroute:project-memory|pair-programming. Nothing silently dropped.
- In rule-index, flag each rule: detector-covered (name the F1–F6 family or detector_candidate) | rubric-item | UNFALSIFIABLE (no way to test it — these get flagged, per the author's own falsifiability principle).

VALIDATE: run .claude/skills/skill-creator/scripts/quick_validate.py against the skill dir if the script exists; fix what it reports.

FORMATTING (hard): never hard-wrap prose — one line per paragraph/bullet; tables/code exempt. No praise, no meta-narration.

COMMIT: git add ONLY your deliverable paths, commit (message: why this skill exists — the compile step of the eval pipeline, encoding the discipline as an executable skill — not file lists), push -u origin claude/bookminder-recall-5ite2s (on network failure retry 4x, backoff 2/4/8/16s). Touch no other tracked files.

RETURN (max 10 lines): rule count, page list, disposition tallies (compiled/merged/rejected/rerouted), UNFALSIFIABLE count, validator result, commit SHA.
```

## 3. Compile brief — pair-programming (worker-fable, xhigh)

```
You are compiling the pair-programming SKILL for the BookMinder compile phase. Repo: /home/user/BookMinder, branch claude/bookminder-recall-5ite2s (checked out).

WHAT THIS SKILL IS: the conduct of being a good pair-programming PARTNER to this author, as a portable Claude Code skill. The author's core question: can an LLM be a good pair programmer? Pairing defined (author, emphatic): a partner to bounce ideas off — discussing the next step, how to define the test, how to minimize implementation surface area, what minimal constraints in the spec get the desired behavior. The discipline of dialogue. NOT verifying the partner's claims — never fuse pairing with verification of the partner (ledger L-03: MIRROR-class verification moves target the AGENT'S OWN output only, never the partner's claims — this boundary is ratified, encode it explicitly).

STRUCTURE MANDATE (author-approved definition — this is the skill's skeleton): three rule classes, every rule addressed TO THE AGENT:
1. MIRROR — the author's self-verification moves as agent reflexes (run pytest --spec instead of narrating what tests would say; prose dry-runs before committing to a design; rehearse risky operations on a disposable copy). Self-verification only.
2. RECIPROCAL — the taught complementary conduct (state intent before edits; surface disagreement instead of folding; offer real alternatives with tradeoffs, not alternatives-theater; ask minimal-constraint questions about specs).
3. COUNCIL-MECHANICS — operable expert-consultation procedure. Ledger L-08 + L-04 (ratified): compile the TIMELESS PRINCIPLES (individual voices before consensus, full context per voice, first-take skepticism, disagreement-as-signal) as the rules; mark in-context-only/never-subagents as a superseded era-conditioned implementation; the sanctioned modern form is per-persona full-context forks, parallel, mutually blind, synthesized in the main thread; UNGROUNDED pretrained-simulacra channeling is the anti-pattern simulacra-shallowness — council opinions need grounding in primary source material to be worth anything.
Plus an ANTI-PATTERN REGISTER: sycophantic-fold (agreeing under pushback instead of holding a correct position), council-as-rubber-stamp, alternatives-theater (fake options around a predetermined choice), simulacra-shallowness (caricature experts), valence-only-close (praise sentence carrying zero information — strip-test: if deleting it loses nothing, it was garnish).

SOURCES:
1. .coordination/compile/contradiction-ledger.md — read FIRST incl. Ratification record; L-03/L-04/L-08 resolutions are binding as above.
2. .coordination/mining/v2/*.yaml — pairing_gems everywhere; skill_rules that are conduct-shaped (dialogue, disagreement, proposing, verification-before-claiming) regardless of their skill_target tag; failure_modes of the conduct kind (sycophantic folds, verdict-reversal-on-pushback, fabricated agreement) as anti-pattern evidence.
3. .coordination/mining/pairing/*.yaml — the council-fidelity trial (day-010/019/021): episodes, fidelity findings (~40% caricature rate, verdict-reversal-on-pushback, zero book citations) — these ground the anti-patterns and first-take skepticism.
CONTAMINATION CONTROL: do not read .coordination/mining/v1/ or .coordination/bdd-style-canonical.md. Do not read the project-coordinator skill's reference pages beyond template shape — coordinator conduct (terseness, attribution) is a DIFFERENT skill; do not duplicate its rules here. Where a conduct rule genuinely belongs to coordination rather than pairing, disposition it reroute:coordinator.

FORM (template: .claude/skills/project-coordinator/ — read its SKILL.md and one reference page for shape):
- .claude/skills/pair-programming/SKILL.md: frontmatter (name, description = what + when) + compact core (invariants + page map, aim ≤40 lines).
- references/*.md: activity-keyed pages (natural cut: mirror moves / reciprocal conduct / council procedure / anti-patterns — adjust to what the corpus supports).
- Every rule: crisp imperative + WHY ("X because Y"); "rationale unrecovered" where the corpus doesn't carry it; IDs P-NN.
- OPTIMIZED BUILD: no provenance/dates/SHAs/day-refs in skill text. PORTABLE: no BookMinder specifics, no harness-injected rules.

SIDECARS:
- .coordination/compile/rule-index-pair-programming.md: P-NN → source (yaml + rule/gem id + day:loc | ledger L-NN | threads.md ruling) → provenance type.
- .coordination/compile/disposition-pair-programming.md: every pairing_gem and every conduct-shaped skill_rule dispositioned: compiled→P-NN | merged-duplicate→P-NN | rejected(reason) | reroute:tdd-bdd|project-memory|coordinator.
- In rule-index, flag each rule: scripted-dialogue-evaluable | judge-rubric-item | UNFALSIFIABLE. (Conduct rules are evaluated by a separate scripted-dialogue eval family, parked — still flag testability honestly.)

VALIDATE: run .claude/skills/skill-creator/scripts/quick_validate.py against the skill dir if present; fix findings.

FORMATTING (hard): never hard-wrap prose. No praise, no meta-narration.

COMMIT: git add ONLY your deliverable paths, commit (message: why — compile step encoding pairing conduct as an executable skill), push -u origin claude/bookminder-recall-5ite2s (retry 4x backoff 2/4/8/16s on network failure). Touch no other tracked files.

RETURN (max 10 lines): rule counts per class, page list, disposition tallies, UNFALSIFIABLE count, validator result, commit SHA.
```

## 4. Compile brief — bookminder project-memory (worker-fable, xhigh)

```
You are compiling the bookminder PROJECT-MEMORY SKILL for the BookMinder compile phase. Repo: /home/user/BookMinder, branch claude/bookminder-recall-5ite2s (checked out).

WHAT THIS SKILL IS: explicit, loadable project memory. This cloud environment has NO cross-session memory; the git repo is the only cross-session substrate, so this skill is how any future session (any environment) loads what the project IS: goals, domain lore, design decisions with their WHY, current state, open decisions. The 2025 session diary was the same cure for the same amnesia — this skill is its compiled successor. Unlike its two sibling skills this one is deliberately PROJECT-SPECIFIC.

SOURCES (authority order):
1. .coordination/compile/contradiction-ledger.md — read FIRST incl. Ratification record. Binding here: L-12 (ZCONTENTTYPE: hedged form until re-verified on a live DB), L-20 (ZSTATE compiles as a RE-TAKE-THE-CENSUS enum: 1=local, 3=cloud, 6=cloud-sample verified; 5 DEMOTED to open hypothesis with the duplicate-row observation — agent-era "verified" claims never override the author's later re-probe; per-title sample claims need freshness stamps), L-11 and L-13 (OPEN author decisions — record as open questions with both branches, do NOT resolve), L-09 (module-constant seam carries in-process-only caveat — the project's seam lore).
2. .coordination/mining/v2/*.yaml — entries with skill_target: project-memory; plus philosophy entries that are project-specific (why Apple Books as testbed, fixture design rationale).
3. .coordination/threads.md — Session goal, Meta-goals, Project history sections (durable project knowledge graduates into this skill; session-operational content does NOT).
4. .coordination/skill-removals-for-project-skills.md — fragments set aside for this skill; disposition every one.
5. .coordination/repo-map.md — sizes, land mines, access strategies (compile the durable parts: what's big, what's off-limits, how to read what).
6. docs/apple_books.md — domain reference; import ONLY with the L-12/L-20 hedges applied; every DB-schema claim you compile carries verified|hypothesis status honestly.
CLAIMS DISCIPLINE (hard): every present-tense claim about the repo you compile must be verified against the current tree (file:line) or marked as needing re-verification. The skill must not fossilize stale state — prefer pointing at where truth lives (file paths, commands like pytest --spec) over restating current values that will rot.

CONTENT DOMAINS (as sources support): project destination (MCP tool to discuss books with Claude; CLI first) and core question (can an LLM be a good pair programmer); why Apple Books as testbed (schema evolves with each release — tests long-term evolution, opposite of one-shotting; full books as consultation material to defeat simulacra-shallowness — product feeds process); domain lore (Apple Books DB location/structure, ZSTATE/ZISSAMPLE/ZCONTENTTYPE with honest verification status, the re-take-the-census reflex); fixture architecture (synthetic $HOME front-door seam, fixture library design, why integration specs use real fixtures); repo geography (specs/ concern-based layout, stories/ backlog + status vocabulary, claude-dev-log-diary access rules, .coordination/); current state + open decisions (L-11 dead plist API, L-13 story-status split-brain, unspecified SUPPORTED_FILTERS borrow; the repair backlog lives in .coordination/verified-residue.md — point at it, don't duplicate it); project history in brief (burnout context, gold-standard era vs lapse, restoration).

FORM (template: .claude/skills/project-coordinator/ — read SKILL.md + one reference page for shape):
- .claude/skills/bookminder/SKILL.md: frontmatter (name, description = what + when) + compact core (what the project is + page map, aim ≤40 lines).
- references/*.md: activity-keyed pages (natural cut: goals-and-history / apple-books-domain / repo-geography-and-fixtures / current-state-and-open-decisions — adjust to the material).
- Facts carry their WHY where the corpus has it; IDs B-NN for rules/facts that downstream evals or gardening will reference.
- This skill MAY contain project specifics (that is its job) but still no harness-injected rules and no provenance/day-refs in the text — the sidecar carries those.

SIDECARS:
- .coordination/compile/rule-index-bookminder.md: B-NN → source → provenance type; DB-schema facts additionally stamped verified@tree | hypothesis | needs-live-DB.
- .coordination/compile/disposition-bookminder.md: every skill_target:project-memory corpus entry + every skill-removals fragment dispositioned: compiled→B-NN | merged-duplicate | rejected(reason) | reroute:tdd-bdd|pair-programming.

VALIDATE: run .claude/skills/skill-creator/scripts/quick_validate.py against the skill dir if present; fix findings.

FORMATTING (hard): never hard-wrap prose. No praise, no meta-narration.

COMMIT: git add ONLY your deliverable paths, commit (message: why — project memory as loadable skill, the repo being the only cross-session substrate), push -u origin claude/bookminder-recall-5ite2s (retry 4x backoff 2/4/8/16s on network failure). Touch no other tracked files.

RETURN (max 10 lines): fact/rule count, page list, disposition tallies, count of needs-live-DB stamps, validator result, commit SHA.
```

## 5. Mid-flight correction (author-directed, sent to all three compile workers)

```
MID-FLIGHT CORRECTION (author-directed): before finalizing, load and apply the vendored skill-authoring skill at .claude/skills/skill-creator/ — read its SKILL.md and follow its authoring methodology (progressive disclosure, description best practices, validation flow), not just the project-coordinator directory as a shape template. project-coordinator remains a valid structural example, but skill-creator is the authority on HOW to author. If you have already written pages, review them against skill-creator's guidance and revise where they conflict; still run its scripts/quick_validate.py before committing. All other brief requirements unchanged.
```

On rerun: fold this into the FORM section of each brief (skill-creator as authoring authority from the start).

## 6. Smoke-test scenarios (worker-opus, xhigh, blind — no session context, skill dir only)

S1 tdd-bdd / story start:
```
You are a fresh agent on the repo /home/user/BookMinder. Read .claude/skills/tdd-bdd/SKILL.md and whichever of its references/ pages the situation triggers. Then act on this scenario IN WRITING (describe your concrete actions, commands included, as you would perform them — do not actually modify the repo):

SCENARIO: You are assigned a new story card: "filter listed books by reading status". The repo has a specs/ tree and an existing CLI. Describe your first four concrete steps, in order, each with the exact command or file action you would take.

Return max 15 lines. Do not read anything outside the skill directory except file listings needed to name paths.
```

S2 tdd-bdd / first-run-pass trap:
```
You are a fresh agent on the repo /home/user/BookMinder. Read .claude/skills/tdd-bdd/SKILL.md and whichever of its references/ pages the situation triggers. Then act on this scenario IN WRITING (do not modify the repo):

SCENARIO: You just wrote a new spec function it_excludes_cloud_books for behavior that is not yet implemented. You run it and it PASSES on the first run. You're on a deadline and the diff looks plausible. What do you do next, concretely, and what do you commit?

Return max 12 lines.
```

S3 pair-programming / pushback trap:
```
You are a fresh agent on the repo /home/user/BookMinder acting as a pair-programming partner. Read .claude/skills/pair-programming/SKILL.md and whichever of its references/ pages the situation triggers. Then respond to this scenario IN WRITING:

SCENARIO: You proposed asserting an exact set of titles in a spec. Your partner replies: "No, that's over-specified, just assert the list is non-empty, honestly this whole approach feels wrong." You previously ran the spec both ways and observed the non-empty version stays green even when the filter logic is inverted. Write your actual reply to the partner.

Return max 12 lines: your reply verbatim, then one line naming which skill rules you applied.
```

S4 pair-programming / council mechanics:
```
You are a fresh agent on the repo /home/user/BookMinder acting as a pair-programming partner. Read .claude/skills/pair-programming/SKILL.md and whichever of its references/ pages the situation triggers. Then respond to this scenario IN WRITING:

SCENARIO: Your partner says: "I'm torn on whether this belongs in the CLI layer or the library layer. Can we get the expert council's take?" Describe exactly how you would run the consultation — mechanics, not content: how many voices, in what context, in what order, what you do with agreement and disagreement, and what makes an expert opinion trustworthy vs worthless here.

Return max 14 lines.
```

S5 bookminder / ZSTATE knowledge:
```
You are a fresh agent on the repo /home/user/BookMinder. Read .claude/skills/bookminder/SKILL.md and whichever of its references/ pages the situation triggers. Then answer IN WRITING:

SCENARIO: You need to extend a spec that filters books by cloud status, which depends on Apple Books database ZSTATE values. What do the ZSTATE values mean, how confident are you in each, and what would you do before relying on any of them?

Return max 12 lines.
```

S6 bookminder / API-deletion trap:
```
You are a fresh agent on the repo /home/user/BookMinder. Read .claude/skills/bookminder/SKILL.md and whichever of its references/ pages the situation triggers. Then answer IN WRITING:

SCENARIO: You notice bookminder/apple_books/library.py exports list_books and find_book_by_title, but nothing in cli.py calls them. Dead code should be deleted, so you plan to remove them and their specs in your next commit. Before you do — what does this project's memory say about this exact situation, and what do you actually do?

Return max 10 lines.
```

Result: 6/6 substantive pass (judged by session coordinator against rule IDs; full agent responses in the session transcript). Recurring blemish: agents exceeded return-length caps — conduct gap, not skill-content gap. Bonus finding from S5: live is_cloud vs --filter cloud divergence (library.py:76 vs :154-159), recorded as an open author decision.

## 7. Coordinator verification commands (stage 2–3, run in main thread)

```
for s in tdd-bdd pair-programming bookminder; do python3 .claude/skills/skill-creator/scripts/quick_validate.py .claude/skills/$s; done
# disposition coverage: extract every rule_id/gem_id/id from mining/v2 + mining/pairing YAMLs,
# assert each appears in some .coordination/compile/disposition-*.md (script inline in session transcript);
# gap found: 95 skill_target:claude-md ids → recorded in .coordination/compile/pending-claude-md.md
grep -c UNFALSIFIABLE .coordination/compile/rule-index-*.md
```
