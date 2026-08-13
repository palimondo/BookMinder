# Contradiction Ledger — Compile Phase

Scope: the 24 validated harvest files (.coordination/mining/v2/, schema v2.2), the 3 council-fidelity trial files (.coordination/mining/pairing/), and the live-session 2026-08 rulings recorded in .coordination/threads.md and .coordination/eval-design.md, checked against the repo's governing documents (CLAUDE.md, .coordination/bdd-style-canonical.md — unratified draft per threads.md:63, README.md) plus docs/ files the corpus flags pointed at. Method: sweep of miner-flagged `overlap:` tensions and contradiction signals, plus targeted topic sweeps (docstrings, council mechanics, coverage, commit rules, test seams, fixture-census assertions, repo-state claims); every present-tense repo claim below was verified against the working tree at branch claude/bookminder-recall-5ite2s (HEAD 60e9d3d).

Resolution rules applied (eval-design.md §Compile/reduce policy, author-approved): (1) user-verbatim > user-paraphrase > agent-synthesis; (2) among user statements, later date overrides earlier (day-file numbering = chronology; 2026-08 threads.md rulings latest of all); (3) agent-era artifacts never override an earlier user ruling; (4) every entry proposes, nothing resolves silently — both sides ship verbatim for the author to overrule.

Attribution note: quotes marked user-verbatim are reproduced character-exact from the mining YAMLs' `quote:` fields, which validate_mining.py checked verbatim against source transcripts; their fidelity is inherited from that gate. Quoted-looking text outside `quote:` fields is unaudited corpus-wide (known limitation, threads.md:4). threads.md and eval-design.md are coordinator-written records of user rulings — provenance user-paraphrase at best, and marked so.

Entries: 20 total — internal 10 (4 judgment-calls), corpus-vs-repo 10 (3 judgment-calls).

## Ratification record (2026-08-13, author rulings + coordinator triage)

- L-01 DISSOLVED by recovered source context (day-020:L13020-L13093, read in-session): the rejected count was `assert len(books) > 10` encoding the recent-vs-all limit contract via incidental fixture size — a different assertion kind than census identity sets. Author's independent recollection matched ("maybe from a different use case… guarding against future growth of examples in the fixture", user-verbatim 2026-08-13). Compile BOTH rules: (a) fixture-backed specs assert exact identity sets where membership IS the requirement; (b) behavioral contracts (e.g. limit properties) are never asserted via fixture cardinality — test them at the layer that controls volume.
- L-02 RULED by author (2026-08-13): "Skeleton phase exempt" — while the walking skeleton is being stood up, ceremony is relaxed generally. Compile as a phase-scoped exemption, day-007 quote as the WHY; the narrower plumbing-only scoping is rejected.
- L-03, L-04 WITHDRAWN as self-litigation (author correction, 2026-08-13): both sides were coordinator session records of rulings already made, not corpus contradictions. L-03: MIRROR always meant the author's self-verification moves as agent reflexes, never partner-claim-policing. L-04: already adjudicated by the council-modernization design (principle survives; ungrounded simulacra channeling = anti-pattern). Ledger briefs must treat threads.md as settled adjudications, not as a contradiction source.
- L-11, L-13 DEFERRED to gardening pass (author decision pending there; does not block skill extraction). L-12: hedged-until-reverified stands (no live DB in this environment).
- L-05..L-10, L-14..L-20 rule-mechanical: stand under the author-approved ranks; author may overrule any individually.

---

## Class A — INTERNAL (corpus vs corpus)

### Judgment-calls — author's eyes needed

### L-01 — Fixture assertions: exact known census vs no-hardcoded-counts

- class: internal
- side_a: canonical §2.3 (.coordination/bdd-style-canonical.md:55, agent-synthesis, unratified draft): "**Fixture-backed specs: exact sets of the known fixture census** — `assert sample_titles == expected_samples` — because the census is known, so anything weaker throws information away."
- side_b: user-verbatim, 2025-07-07 (v2/day-020-s2.yaml rule d020s2-R9, loc day-020:L13073): "you're right that this is always true, but this looks like something that shoudl be tested with a mock somewhere elese; but hardcoding 6 here is also wrong. Maybe just add a FIXME comment and we'll adress that later"
- proposed_resolution: reconcile, don't pick — compile the rule as: assert exact sets of fixture identities (titles) where membership IS the requirement; never assert bare cardinality (a count pins nothing the requirement names); when the only available assertion would couple to incidental fixture shape, mark FIXME and move the property to the layer that can own it. The reconciliation text is my synthesis — the two user-era practices genuinely differ in what they pin, and the author should ratify the boundary.
- confidence: judgment-call — side_a encodes earlier user practice via agent synthesis, side_b is later user-verbatim, but they may be about different assertion kinds (identity sets vs counts), so the ranks don't cleanly fire.
- consumers: tdd-bdd

### L-02 — Skeleton-phase ceremony relaxation vs always-acceptance-first

- class: internal
- side_a: user-verbatim, 2025-05-29 (v2/day-007.yaml rule d007-R3, loc day-007:L570-L573): "since we are just at the step of trying to get the Walking skeleton up and running, we don't have to be that constrained by strict adherenc yet! Can we make it even simpler?"
- side_b: CLAUDE.md:123 (current tree): "Always start with a failing BDD acceptance test based on requirements." — reinforced by the user's later commit-after-RED rationale, 2026-08-12 (threads.md:27, user-paraphrase): "rigorous process > one-shotting, that's the bet".
- proposed_resolution: keep the general rule; compile the day-007 relaxation as a scoped exception — changes with no user-visible behavior (CI plumbing, test infrastructure) may take the smallest change that restores the feedback loop, said explicitly when doing so. The scoping ("no user-visible behavior") is the miner's needs-rework narrowing (agent-synthesis), not the author's words.
- confidence: judgment-call — both sides trace to the user; the later statement is general and the earlier one specific, so date-rank does not obviously extinguish the exception. Author should ratify the exception's scope or kill it.
- consumers: tdd-bdd

### L-03 — Pairing must not fuse with verification vs MIRROR class in the pairing skill

- class: internal
- side_a: user correction, emphatic, 2026-08-10 (threads.md:23, user-paraphrase with verbatim fragments): pairing is "a partner to bounce ideas off … The discipline of dialogue. NOT about verifying the partner's claims — never fuse pairing with verification (a synthesizer did; user: \"totally off base\", \"essayist tying a bow on unrelated things\")".
- side_b: pairing-skill definition, coordinator-proposed, user approved trial 2026-08-13 (threads.md:91, agent-synthesis): "(1) MIRROR — author's verification moves as agent reflexes (pytest --spec not narration; prose dry-runs; rehearse-on-disposable-copy)".
- proposed_resolution: not a contradiction IF MIRROR means self-verification (verify your own claims and code before asserting) and never partner-claim-policing — but that boundary line is my reading, and side_b is a trial approval, not a ratified rule. Compile MIRROR with an explicit exclusion: verification moves target the agent's own output, never the partner's claims; ask the author to ratify this line before the pair-programming skill ships.
- confidence: judgment-call — both sides live in the 2026-08 layer; ranks tie, and the reconciliation is agent-synthesis.
- consumers: pair-programming

### L-04 — Expert-council as compile target vs simulacra-shallowness verdict

- class: internal
- side_a: eval-design.md:60 (draft, "LGTM" on the pipeline 2026-08-12; text is coordinator-written): the pair-programming skill covers "expert-council invocation (channeling pretrained BDD/TDD expert simulacra)". Root provenance: user-verbatim, 2025-06-26 (v2/day-010.yaml rule d010-R16, loc day-010:L2611): "create new slash-command `/expert-council` that invites our TDD/BDD/ATDD gurus to offer their perspective"
- side_b: user, 2026-08-13 (threads.md:25, user-paraphrase): "/expert-council's pretrained simulacra of TDD/BDD experts proved SHALLOW CARICATURES — skewed, non-actionable summaries of real positions." Corroborating measurement (agent-synthesis, threads.md:84, pairing trial): "~40% caricature/fabrication rate … zero book citations".
- proposed_resolution: compile council mechanics into pair-programming conditioned on grounding — the operable procedure (voices, disagreement, synthesis) ships, but ungrounded pretrained-simulacra channeling is compiled as the anti-pattern simulacra-shallowness, with book-grounded persona skills (council-modernization design, threads.md:102) as the sanctioned form. This makes eval-design.md:60's "channeling pretrained … simulacra" wording stale — it should be reworded at gardening.
- confidence: judgment-call — both sides are 2026-08 user positions recorded by the coordinator; the later shallowness verdict qualifies rather than revokes the earlier mechanism, and how much council survives ungrounded is the author's call.
- consumers: pair-programming, gardening (eval-design.md wording)

### Rule-mechanical

### L-05 — Walking-skeleton honest fake: does a fake that greens the acceptance test stay legitimate?

- class: internal
- side_a: canonical §3 (.coordination/bdd-style-canonical.md:109, agent-synthesis, unratified): "Fake data is a legitimate intermediate because the red acceptance test holds the target fixed while the implementation walks toward it."
- side_b: user-verbatim, 2025-06-23 (v2/day-009.yaml rule d009-R2, loc day-009:L7329-L7331): "It didn't tolerate failing acceptance test until we drove the implementation with unit tests, but first made the acceptance test pass by returning page data from implementation." — the user indicting a fake that made the acceptance test GREEN, which forced a meta-test later deleted.
- proposed_resolution: user-verbatim outranks the synthesis — compile as: a labeled hardcoded fake is permitted only while something red still pulls; a fake that turns the outermost RED green owes a unit-driven real implementation in the same sitting, stated in the commit body, and never a meta-test that detects the fake. (Reconciliation phrasing follows the miner's overlap note, v2/day-009.yaml:129 — agent-synthesis; the winning side is the user quote.)
- confidence: rule-mechanical (provenance rank decides the winner; the compiled rule text still gets author review since it is synthesis)
- consumers: tdd-bdd

### L-06 — Docstrings in specs: blanket ban vs pending-skip convention

- class: internal
- side_a: user-verbatim, 2025-04-13 (v2/day-002.yaml philosophy, loc day-002:L400): "Please don't write doctrings in specs, these are redundant with describe_/it_ functions -- remember we'll get a human readable description when we run `pytest --spec`"
- side_b: later convention, at HEAD in CLAUDE.md:100-101 ("Keep docstrings in skipped/pending tests as specifications to implement" / "Remove docstrings from implemented tests - the code IS the specification"), user-enforced by name — user-verbatim, 2025-07-07 (v2/day-020-s2.yaml rule d020s2-R10, loc day-020:L13202): "that docstring says literally the same thing as `it`... remember our `code_style`"; also the day-021 detector reserving docstrings for pending skipped specs only (v2/day-021.yaml:751-752).
- proposed_resolution: later overrides earlier — compile the pending-only convention (story when:/then: as docstring while @pytest.mark.skip; deleted in the same commit that implements the body); the compile step MUST NOT emit the day-002 blanket ban even though it is the highest-provenance single quote on the topic.
- confidence: rule-mechanical (rule 2: later user statements + user-enforced HEAD convention win)
- consumers: tdd-bdd

### L-07 — One canonical rules file vs three skills + thin CLAUDE.md

- class: internal
- side_a: user-verbatim, 2025-04-13 (v2/day-002.yaml philosophy, loc day-002:L742): "These are great, but doesn't this belong to CLAUDE.md?" — recorded there as: exactly one canonical rules file, parallel principles docs are duplication that drifts.
- side_b: user decision 2026-08-13 (eval-design.md:60, user-paraphrase): split into THREE skills (tdd-bdd / bookminder project-memory / pair-programming); plus user-validated memory architecture (threads.md:96, user-paraphrase): "CLAUDE.md stays thin (always-loaded tax)" with durable content graduating into the project-memory skill.
- proposed_resolution: later overrides earlier — compile to the three-skill architecture with a thin CLAUDE.md; the surviving kernel of side_a is single-ownership per rule (each rule lives in exactly one artifact, no duplicated copies that can drift), which the gardening pass should enforce when thinning CLAUDE.md.
- confidence: rule-mechanical (rule 2)
- consumers: all three skills, gardening

### L-08 — Council must run in-context (2025 ban) vs per-persona forks (2026 design)

- class: internal
- side_a: user-verbatim, 2025-07-06 (pairing/day-019.yaml rule p019-R4, loc day-019:L4466): "I think the experts ran a different kind of analysis, because you've used the task tool and there it was necessary to gather project context from scratch and nuance of my question got lost." — mined as: run councils in the current conversation, never delegate to a Task subagent.
- side_b: user design direction, 2026-08-13 (threads.md:102, user-paraphrase): "BOTH 2025 rules are era-conditioned workarounds, not principles. Modern design: per-persona FORKS inheriting full conversation (server cache ≈ free), parallel, mutually blind … Compile step must split council rules: timeless principle (individual voices before consensus, full context per voice, first-take skepticism, disagreement-as-signal) vs superseded implementation."
- proposed_resolution: later overrides earlier — compile the principles (full context per voice, individual voices before consensus, disagreement-as-signal, first-take skepticism) as timeless; compile "in-context only / never Task" as a superseded era-conditioned implementation note, replaced by full-context forks. The 2025 quote survives as the WHY of the full-context-per-voice principle.
- confidence: rule-mechanical (rule 2; side_b explicitly adjudicates side_a)
- consumers: pair-programming

### L-09 — Test seam: module-constant pattern vs fixtures through the front door

- class: internal
- side_a: user-verbatim, 2025-06-23 (v2/day-009.yaml rule d009-R11, loc day-009:L5037-L5038): "Why not follow the exact same pattern: BKLIBRARY_DB_FILE = Path(" — reuse the module-constant seam for new data sources.
- side_b: canonical §2.2 (.coordination/bdd-style-canonical.md:48, agent-synthesis encoding later user-driven practice): "The `monkeypatch` of `_books_plist` was deleted in its favor — \"No more monkeypatching needed\" — because patching a private name couples the spec to an implementation identifier *and bypasses the path-construction code you claim to test*." The miner's own overlap note (v2/day-009.yaml:218) records that the module-constant seam is unpatchable across a process boundary, discovered in the same day-009 session (L6043-L6061).
- proposed_resolution: later practice wins — compile the front-door seam (`--user` synthetic $HOME) as the rule; the module-constant pattern survives only with its stated limitation (in-process substitution only, resolved at import time), per the miner's needs-rework note.
- confidence: rule-mechanical (rule 2: the front-door practice postdates and was driven by the user; the same session already falsified the module-constant seam's generality)
- consumers: tdd-bdd, project-memory

### L-10 — threads.md doc-rot item vs the executed spec-tree restore

- class: internal
- side_a: threads.md:126 open thread 6 (coordinator synthesis, 2026-08-10 era): "Doc rot: README spec path, pre-commit-workflow.md (black/flake8 stale)"
- side_b: user directive executed 2026-08-12 (threads.md:77, user-paraphrase): "spec tree restored wholesale to pre-reorg checkpoint c851f95 via git rm + checkout; 53 tests green". Verified against tree: specs/apple_books/library_spec.py exists at HEAD, so README.md:98's `pytest specs/apple_books/library_spec.py --spec` is a valid command again.
- proposed_resolution: later ruling + verified tree win — drop "README spec path" from the gardening backlog (fixing it now would break a working doc); the pre-commit-workflow.md half of thread 6 remains true and is ledgered separately (L-19).
- confidence: rule-mechanical (repo state falsifies the stale half of the claim)
- consumers: gardening

---

## Class B — CORPUS-VS-REPO (gardening-pass work items)

### Judgment-calls — author's eyes needed

### L-11 — README documents the dead plist API as primary usage

- class: corpus-vs-repo
- side_a (repo): README.md:53-58 "Usage" opens with `from bookminder.apple_books.library import list_books, find_book_by_title` and calls `list_books()` / `find_book_by_title("…")`. Verified against tree: bookminder/apple_books/library.py:89 and :105 now require a `user_home: Path` argument, so the README sample raises TypeError as written; neither function has any caller in bookminder/cli.py or bookminder/__main__.py (grep verified).
- side_b (corpus): canonical §5.11 (.coordination/bdd-style-canonical.md:187, agent-synthesis): "Dead plist API: `list_books`/`find_book_by_title` are integration-tested with zero `cli.py` callers — deliberate seed of the EPUB path, or unreaped growth. Decide, then spec or delete."
- proposed_resolution: gardening cannot execute this without a ruling — the author must decide: (a) keep as deliberate EPUB-path seed → fix README signatures and mark the API as pre-release, or (b) unreaped growth → delete API + README section. Either way README's current sample is broken and must change.
- confidence: judgment-call — no user statement exists on which branch to take (canonical §5.11 itself says "Decide").
- consumers: gardening, project-memory

### L-12 — docs/apple_books.md contradicts itself on ZCONTENTTYPE confidence

- class: corpus-vs-repo
- side_a (repo, hedged): docs/apple_books.md:60 (verified): "- `ZCONTENTTYPE`: Integer indicating content type (likely: 1 = Book, 3 = PDF)"
- side_b (repo, flat — flagged by corpus): docs/apple_books.md:114-115 (verified): "- `ZCONTENTTYPE = 1`: Regular books (EPUB)" / "- `ZCONTENTTYPE = 3`: PDF documents". Corpus flag: v2/day-008.yaml:240,351 (2025-06-22, agent-era doc, flag itself agent-synthesis): "a document contradicting itself about its own confidence".
- proposed_resolution: no user ruling on the fact exists — propose the hedged form wins until re-verified against a live database (per the claims-verification design, eval-design.md:65, awaiting first-run go); project-memory compiles only mappings carrying a verification stamp, and gardening either re-verifies or re-hedges lines 114-115.
- confidence: judgment-call — the ranks don't decide data truth; only a re-run query can, and this environment has no Apple Books DB.
- consumers: project-memory, gardening

### L-13 — Story-status split-brain: done vs needing ATDD reimplementation

- class: corpus-vs-repo
- side_a (repo): TODO.md:7-14 lists "Validate Filter Values" and "Filter by Sample Flag" under "## Completed Features"; stories/discover/validate-filter-values.yaml:5 and stories/discover/filter-by-sample-flag.yaml:5 both read `status: done` (all verified at HEAD).
- side_b (repo + corpus): TODO.md:21-24 (verified) lists the same two stories (plus filter-by-reading-status.yaml) under "Stories that need proper ATDD reimplementation" with the user-era note "After commit 6f786cc, ATDD practice wasn't followed properly" (TODO.md:19-20); canonical §5.9 (.coordination/bdd-style-canonical.md:185, agent-synthesis): "a feature without process provenance is, by definition, not done"; PR #18, which corrected the cards to backlog, is unmerged (threads.md:122, thread 3).
- proposed_resolution: the needing-reimplementation side wins on the project's own provenance principle, but the REMEDY is contested and only the author can pick: (a) mark cards `reopened` (CLAUDE.md:227 defines exactly this state) and remove them from Completed Features, keeping the code; or (b) merge/replay PR #18's semantic revert and mark them `backlog`. Gardening executes whichever he ratifies. Related cleanup: CLAUDE.md:116 routes requirements to TODO.md while CLAUDE.md:192 makes stories/ cards the story ledger — the dual bookkeeping that produced this split-brain; propose declaring the story card the single source of status truth.
- confidence: judgment-call — which repair path (patch-forward vs revert-and-rederive) is an open author decision on record.
- consumers: gardening, project-memory

### Rule-mechanical

### L-14 — CLAUDE.md commit rules: "preserve working state (all tests passing)" vs commit-after-RED and red-acceptance-on-main

- class: corpus-vs-repo
- side_a (repo): CLAUDE.md:242 (verified): "Each commit should be small, focused, and preserve working state (all tests passing)." Also CLAUDE.md:29: "Commit frequently at stable points", and the stale ordinal CLAUDE.md:132: "**Commit After Refactor**: Make second commit if any refactoring was done." (it is the third commit of the restored three-commit cycle).
- side_b (corpus): commit-after-RED is the author's own rule, restored at his direction 2026-08-10 (threads.md:73) and rationalized by him 2026-08-12 (threads.md:27, user-paraphrase: rewindable project record; instruction-following pressure; "rigorous process > one-shotting, that's the bet"); CLAUDE.md itself now mandates it at :127 ("**Commit After RED**: Commit the failing spec before writing any implementation.") and :235-238 (three commits incl. "After RED phase (new failing spec, committed before implementation)"); outside-in ATDD keeps a red acceptance test on main by design (CLAUDE.md:124; canonical §3:109 "A red acceptance test on main means feature-in-progress by design").
- proposed_resolution: corpus ruling wins — gardening rewrites CLAUDE.md:242 to except RED-phase spec commits and in-progress red acceptance tests (e.g. "preserve working state — all tests passing except the RED commit's own new spec and any deliberately-red acceptance test"), harmonizes :29's "stable points" with the three-commit cycle, and fixes :132 "second" → "third". This is the surviving instance of open thread 5 (threads.md:124), whose original subject (missing commit-after-RED step) is already repaired.
- confidence: rule-mechanical (later user ruling; the contradiction is revert-collateral wording)
- consumers: gardening, tdd-bdd

### L-15 — CLAUDE.md still describes AGENTS.md/GEMINI.md as duplicated copies

- class: corpus-vs-repo
- side_a (repo): CLAUDE.md:254 (verified): "These instructions are duplicated in AGENTS.md and GEMINI.md for use with other agentic coding systems, therefore when updating these instructions, always ask the user if changes should be applied to CLAUDE.md, AGENTS.md, and GEMINI.md"
- side_b (corpus): user-directed conversion 2026-08-12 (threads.md:77, user-paraphrase): "AGENTS.md/GEMINI.md converted to symlinks → CLAUDE.md … — resolves the sync question." Verified at HEAD: both are symlinks to CLAUDE.md.
- proposed_resolution: later user ruling wins — gardening rewrites CLAUDE.md:254 to state the symlink arrangement (single source, no sync question), dropping the ask-before-syncing procedure.
- confidence: rule-mechanical
- consumers: gardening

### L-16 — "Type hints for all functions" vs the specs/ exclusion the user ordered

- class: corpus-vs-repo
- side_a (repo): CLAUDE.md:88 (verified): "**Types**: Use type hints for all functions and parameters"
- side_b (corpus): user-verbatim, 2025-05-25 (v2/day-005.yaml rule d005-R12, loc day-005:L1555): "could be exclude the specs from the type hint requirements? It doesn't add value there IMO" — and the exclusion is live at HEAD: .pre-commit-config.yaml:31 `exclude: ^(claude-dev-log-diary/|specs/)` (verified).
- proposed_resolution: user-verbatim + implemented tooling win — gardening amends CLAUDE.md:88 to carve out spec files (type hints mandatory in bookminder/, not required in specs/); tdd-bdd skill must not demand annotations on `it_` functions.
- confidence: rule-mechanical (rule 1 + rule 2; the miner flagged this exact tension as unresolved at v2/day-005.yaml:206)
- consumers: gardening, tdd-bdd

### L-17 — canonical guide's repo-state claims falsified by the 2026-08-12 restore

- class: corpus-vs-repo
- side_a (repo doc): .coordination/bdd-style-canonical.md (unratified draft, agent-synthesis) asserts present-tense repo state that predates the restore: §5.4:180 "The commit-after-RED rule is missing from the constitution. CLAUDE.md self-contradicts …"; §5.3:179 "The four-layer taxonomy stands as if decided."; §2.2:50 "The `specs/{unit,integration,acceptance,e2e}` split at HEAD"; §5.1:177 cites `specs/acceptance/cli_spec.py:67`; §5.5:181 cites `integration/library_containers_spec.py:147-161`; §5.10:186 "`README.md:98` documents `pytest specs/apple_books/library_spec.py --spec`, a path deleted in the reorg."; §5.7:183 cites e2e/ paths.
- side_b (corpus rulings + verified tree): user-directed restore to pre-reorg checkpoint c851f95 (threads.md:77, 2026-08-12) and commit-after-RED restoration (threads.md:73, 2026-08-10). Verified at HEAD: CLAUDE.md:127 and :235-238 contain the rule (§5.4 false); the spec tree is concern-based — specs/cli_spec.py, specs/cli_formatting_spec.py, specs/apple_books/library_spec.py, specs/apple_books/library_integration_spec.py — with four-layer directories surviving only as untracked __pycache__ residue (§5.3/§2.2/§5.5/§5.7 paths gone); the filter-validation patch now lives at specs/cli_spec.py:100 targeting `bookminder.cli.SUPPORTED_FILTERS` (§5.1's loc stale, its substance — the borrow `assert cli.SUPPORTED_FILTERS is library.SUPPORTED_FILTERS` still unwritten — remains TRUE, grep verified); README.md:98's path exists again (§5.10 false).
- proposed_resolution: later user rulings + tree win — gardening re-verifies every §2.2/§4/§5 present-tense claim against the current tree and rewrites or freshness-stamps them (the offered verified-residue sweep, eval-design.md:65, is exactly this instrument); the compile step must not import any canonical repo-state claim without a verified_against stamp. Surviving-true items spot-checked here: §5.1 borrow unspecified (specs/apple_books/library_spec.py:21 asserts set equality, not identity with the cli binding), §5.9 status split-brain (L-13), §2.1:30 README rot (L-18).
- confidence: rule-mechanical (repo state decides each claim; document is unratified draft, rank agent-synthesis)
- consumers: gardening

### L-18 — README advertises unbuilt features

- class: corpus-vs-repo
- side_a (repo): README.md:10-13 (verified): "- List books from Apple Books library / - Extract table of contents from EPUB files / - Extract highlighted passages with context / - Export in Markdown format for LLM consumption". Verified against tree: bookminder/ contains only cli.py and apple_books/library.py — no EPUB TOC, highlights, or export code exists.
- side_b (corpus): user-verbatim, 2025-04-13 (v2/day-002.yaml philosophy, loc day-002:L637): "we must codify all our assumptions in executable specification, so that we stay grounded" — prose that outruns the specs is the rot the method exists to prevent; canonical §2.1:30 names this instance: "this repo's own README still advertises unbuilt features".
- proposed_resolution: corpus wins on existence — gardening splits Features into built (list) vs vision/roadmap (TOC, highlights, export), or deletes the unbuilt lines; which presentation the author prefers is his pick, but the current unqualified claims cannot stand.
- confidence: rule-mechanical (the contradiction is verified fact; only the remedy's cosmetics are open)
- consumers: gardening

### L-19 — docs/pre-commit-workflow.md documents the pre-ruff toolchain

- class: corpus-vs-repo
- side_a (repo): docs/pre-commit-workflow.md:12-13 (verified): "- **Code Formatting**: trailing-whitespace, end-of-file-fixer, black / - **Code Quality**: flake8, mypy"; also :22 references flake8.
- side_b (corpus + repo constitution): CLAUDE.md:80 (verified): "**Formatting and Linting**: Use ruff (max line length 88)"; .pre-commit-config.yaml at HEAD carries ruff, not black/flake8; corpus records the doc-rot flag at threads.md:126 (thread 6).
- proposed_resolution: gardening updates docs/pre-commit-workflow.md to the ruff-based hook chain or deletes the doc if CLAUDE.md's build_commands section already covers it (per L-07's single-ownership principle).
- confidence: rule-mechanical
- consumers: gardening

### L-20 — docs/apple_books.md "Verified ZSTATE Mappings" vs the day-014 re-probed census

- class: corpus-vs-repo
- side_a (repo): docs/apple_books.md:337 (verified): "**Key Discovery**: This UI provides visual evidence that `ZSTATE = 5` in the database represents series entities and unowned books within a series." and :638 lists "ZSTATE = 5: **Series Entity / Unowned Series Book**" under "Verified ZSTATE Mappings" (:632). Era note: this layer of the doc was built during the Gemini research sessions incl. post-Flash-downgrade work (day-012/013, era_class model-artifact for the Flash portions).
- side_b (corpus): user-directed re-probe, 2025-07-03 (v2/day-014.yaml rule d014-R3, user-paraphrase, evidence day-014:L735-L764): ZSTATE census re-taken shows "5 appearing only as a *second* row for a title that already has a 3", with the miner's because-note: "Every earlier single-value story about ZSTATE (5 means cloud; 5 means series) was contradicted by the next batch of real rows." Same session, agent's own re-query (v2/day-014.yaml failure_modes, loc day-014:L486, agent quote): "The database query for \"What's Our Problem?\" returns ZISSAMPLE = 1. However, in the log from day-012, my query returned ZISSAMPLE = 0."
- proposed_resolution: rank decides — day-014's user-directed, later evidence (user-paraphrase) outranks the earlier agent-written doc, and agent-era artifacts cannot override it (rule 3); project-memory compiles ZSTATE as a re-take-the-census enum (1 local, 3 cloud, 6 cloud-sample verified; 5 demoted from "verified series entity" to open hypothesis with the duplicate-row observation attached), and gardening re-hedges docs/apple_books.md:337/:638 or re-verifies against a live DB. The ZISSAMPLE flip means per-title sample claims in the doc also need freshness stamps.
- confidence: rule-mechanical (ranks fire cleanly; underlying data truth still needs a live-DB re-run, which gardening should note rather than fabricate)
- consumers: project-memory, gardening

---

## Index

| id | one-line description | proposed winner | confidence |
|----|----------------------|-----------------|------------|
| L-01 | exact fixture census vs no-hardcoded-counts | reconciliation (identity sets yes, bare counts no) | judgment-call |
| L-02 | skeleton-phase ceremony relaxation vs always-acceptance-first | rule + scoped no-user-visible-behavior exception | judgment-call |
| L-03 | never fuse pairing with verification vs MIRROR class | MIRROR restricted to self-verification | judgment-call |
| L-04 | council in pair-programming skill vs simulacra-shallowness | council mechanics conditioned on book-grounding | judgment-call |
| L-05 | honest fake legitimacy vs fake-greened acceptance indictment | user quote: fake only while something red pulls | rule-mechanical |
| L-06 | blanket docstring ban vs pending-skip convention | later: pending-only convention | rule-mechanical |
| L-07 | one canonical rules file vs three skills + thin CLAUDE.md | later: three-skill split, single-ownership kernel kept | rule-mechanical |
| L-08 | council in-context-only ban vs per-persona forks | later: forks; principle/implementation split | rule-mechanical |
| L-09 | module-constant seam vs front-door fixtures | later: front door; constant carries in-process caveat | rule-mechanical |
| L-10 | threads.md "README spec path rot" vs executed spec restore | restore: drop the stale gardening item | rule-mechanical |
| L-11 | README's dead plist API usage section | author decides: spec the EPUB seed or delete | judgment-call |
| L-12 | ZCONTENTTYPE hedged vs flat in the same doc | hedge until re-verified | judgment-call |
| L-13 | stories done vs needing ATDD reimplementation | not-done side; remedy (reopened vs PR#18 revert) = author | judgment-call |
| L-14 | all-commits-passing vs commit-after-RED / red acceptance | commit-after-RED; rewrite CLAUDE.md:242/:29/:132 | rule-mechanical |
| L-15 | CLAUDE.md duplication rule vs AGENTS/GEMINI symlinks | symlinks; rewrite CLAUDE.md:254 | rule-mechanical |
| L-16 | type hints everywhere vs user-ordered specs/ exclusion | carve out specs/ in CLAUDE.md:88 | rule-mechanical |
| L-17 | canonical's stale repo-state claims vs restored tree | tree; re-verify/stamp every §5 claim | rule-mechanical |
| L-18 | README advertises unbuilt features | split built vs roadmap (or delete) | rule-mechanical |
| L-19 | pre-commit-workflow.md black/flake8 vs ruff | update or delete the doc | rule-mechanical |
| L-20 | "Verified" ZSTATE=5 series mapping vs day-014 re-probe | demote to hypothesis; re-verify on live DB | rule-mechanical |
