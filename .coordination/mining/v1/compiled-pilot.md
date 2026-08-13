# Compiled Pilot — day-019 + day-016

Inputs: `mining/day-019.yaml` (2025-07-06, claude-code-via-claude-trace, 19 failure_modes / 16 skill_rules), `mining/day-016.yaml` (2025-07-04, gemini-cli, 20 failure_modes / 24 skill_rules). Baseline for overlap classification: `.coordination/bdd-style-canonical.md` (git-archaeology style guide). Consumer: `.coordination/eval-design.md` §2 COMPILE.

**Headline: 40 skill_rules → 35 distinct (5 merges); 20 NEW / 15 OVERLAP (8 of those sharpened) / 1 CONTRADICTS. 39 failure_modes → 30 TIMELESS / 8 2025-ERA / 1 HARNESS-SOLVED. The 8 parked entries are 7-of-8 from the Gemini file and 6-of-8 from after its silent flash downgrade.**

---

## 1. Skill rulebook candidates

Legend — **taught_or_enforced**: `T` taught-once, `R` repeated, `E` needed-enforcement. **vs canonical**: `NEW` (dialogue-only; git never showed it), `OVERLAP` (canonical states it), `OVERLAP+` (canonical states the principle, mining adds operational content or a detectable tell), `CONTRADICTS`.

### 1.1 TDD sequence (10 rules — 3 NEW)

| # | Rule | Evidence | T/E | vs canonical |
|---|---|---|---|---|
| S1 | Do not touch implementation without a failing test for it; if an unrequested implementation change slipped in, restore the file to its state before that edit. | d016:L7169 | E | OVERLAP — §2.6 "Revert is a first-class move when provenance is wrong"; §4 "code whose provenance violates the process is not repaired by adding tests to it" |
| S2 | Go outside-in — acceptance test, then unit test, then implementation; **a red acceptance test with no red unit test means you are missing the test that should drive the design**. | d019:L1951 | R | OVERLAP+ — §4(c) names outside-in as the violated principle; the red-acceptance-without-red-unit tripwire is new and is directly mechanizable as a T1 detector |
| S3 | Implement only what the currently red test demands — no sibling branches, no error handling, no filters nobody asked for. | d019:L3718 | R | OVERLAP — §2.4 minimalism by deletion, §2.5 YAGNI-as-testability |
| S4 | Work one scenario at a time — write the sibling scenarios as explicitly skipped specs and unskip them one by one. | d019:L1859 | T | OVERLAP — §2.1 pending-skipped docstrings, §3 "`--filter cloud` ships with the negation scenario as a skipped placeholder" |
| S5 | After GREEN, commit that state, then explicitly ask "should we refactor?" before touching the next behavior. *(merge: d019 + d016)* | d019:L3131, d016:L6889 | R+T | OVERLAP+ — §2.6 commit after RED/GREEN/REFACTOR; the explicit spoken refactor prompt is new micro-practice, and §2.6 calls REFACTOR the silently-skipped step |
| S6 | When you fix a behavior no test covers, write the test and then **break the implementation on purpose** to watch it fail before restoring the fix. | d019:L3806 | T | **NEW** — canonical asserts the RED commit proves a falsifier existed; nowhere does it prescribe hand-mutation as the in-session proof for retrofits |
| S7 | Never delete or relax an assertion to get to green; correct the expected value against evidence from the fixture. **"More robust" is the phrase that always precedes it.** | d016:L2642 | E | OVERLAP+ — §2.7 "Same `it_` name, weaker assertion, is the most dangerous edit in the suite" is the review rule; mining supplies the in-the-moment rationalization and its verbal tell (T2 detector fuel) |
| S8 | When a test fails for lack of data, fix the fixture — never widen production code to accommodate a test-only filename or value. | d016:L1754 | E | **NEW** — §2.2 sends fixtures through the front door but never prohibits the reverse move; the failure is invisible in git because both attempts were reverted before commit |
| S9 | Answer "where are we / what's next?" by running the suite (`pytest --spec`), never by narrating remembered state. | d019:L2613 | E | **NEW** — canonical uses `--spec` as the living-documentation *artifact*; the anti-narration discipline is a dialogue-only rule with no git shadow |
| S10 | Prefer the smallest change that would work — one extra assertion in an existing test usually beats a whole new test. | d019:L4264 | R | OVERLAP — §2.3 "One equality assertion subsumes several partials"; §3 the redundant ordering test deleted |

### 1.2 Spec style (3 rules — 3 NEW)

| # | Rule | Evidence | T/E | vs canonical |
|---|---|---|---|---|
| P1 | Put no comments in spec files that restate the assertion; if the assertion needs explaining, **make the explanation its failure message**. *(merge: d019 + d016)* | d019:L4355, d016:L641 | E+T | **NEW** — §2.3 "Diagnostics hand you the counterexample" covers messages; the comment prohibition and the comment→message redirect appear only in dialogue (CLAUDE.md `code_style` states the prohibition but not the redirect) |
| P2 | Documentation records how the data is actually stored; it does not prescribe the query the implementation should use. | d019:L1176 | T | **NEW** — §2.1 says prose rots and specs fail; the observation/prescription split inside a reference doc is unstated |
| P3 | Read the whole spec file before drafting an edit to it, and quote the line numbers you are relying on. | d019:L1985 | T | **NEW** — §2.7 "reviewed by diff, never by outcome" is the reviewer's rule; this is the author's rule, and it is the precondition for §2.7 being checkable at all |

### 1.3 Test doubles and layers (3 rules — 0 NEW; convergent validation)

| # | Rule | Evidence | T/E | vs canonical |
|---|---|---|---|---|
| D1 | Separate the layers — acceptance tests assert user-visible output and formatting, integration tests assert that the query selects the right rows, unit tests assert the row-to-domain mapping. | d019:L4577 | R | OVERLAP — §2.2 mock rules by kind + §2.3 assertion strength by kind. **TENSION worth flagging:** this rule uses the acceptance/integration/unit vocabulary that §2.2 rules an *unadopted* four-layer taxonomy ("mockist tests ARE unit tests"; "taxonomy is discovered, not imposed"). Substance agrees, vocabulary does not — the day-019 dialogue is where that vocabulary was minted, two weeks before the reorg §5.3 is still trying to undo |
| D2 | A test double that only supplies data is a stub, not a mock — reserve Mock for verifying interactions, and prefer a plain dict over a purpose-built Fake class. | d019:L4650 | T | OVERLAP+ — §2.2 "Data stubs, not mocks of collaborators"; the no-Fake-class preference is new |
| D3 | Give a stub only the fields under test; provide the rest from a defaulted helper such as `row_stub(**overrides)` called inline at the call site. | d019:L4702 | T | OVERLAP (verbatim) — §2.2 names `row_stub(**overrides)` and the "irrelevant fields would be noise hiding the variable under test" reasoning. **This is the validity check on the whole pilot**: mining rediscovered a canonical rule down to the helper's signature, from a different source, without seeing the guide |

### 1.4 Fixtures and fixture tooling (5 rules — 4 NEW)

| # | Rule | Evidence | T/E | vs canonical |
|---|---|---|---|---|
| F1 | Never mutate test fixture data to manufacture a scenario; add a fixture, a builder, or a stub instead. | d019:L467 | E | **NEW** — §2.2 catalogues the persona fixtures as "observed on a real machine rather than imagined"; the immutability guard that keeps them that way is dialogue-only, because every violation was blocked before it could reach git |
| F2 | Build fixtures with two separate tools — one that creates a pristine empty database with the real schema, one that copies a single known record into it — and compose them per scenario, **because that pair is exactly the GIVEN clause of a BDD scenario**. | d016:L1114 | T | **NEW** — the single largest addition. Canonical describes the fixture tree as a finished artifact; mining supplies the generative theory that produced it and ties it to the story cards' `when:`/`then:` |
| F3 | Before writing tooling, read the story cards it will serve and state which scenarios it makes testable. | d016:L1086 | T | **NEW** — §2.5 makes testability the YAGNI detector for *product* code; extending it to tooling is new, and the L1086 exchange is the pilot's best pairing gem |
| F4 | Project scripts must be machine-independent: glob a stable pattern, mirror whatever locator the production code already uses, and never hardcode a username or an absolute path. *(merge: d016 R2 + R3)* | d016:L668, d016:L1237 | E+T | OVERLAP+ — §2.3 "Never depend on the developer's machine… a spec that only passes on one machine specifies that machine"; the mirror-the-production-locator clause (test and production must not disagree about where data lives) is new |
| F5 | Keep deletion out of tooling scripts; cleanup is a deliberate, human act. | d016:L1085 | T | **NEW** |

### 1.5 Git and commits (7 rules — 4 NEW, 1 CONTRADICTS)

| # | Rule | Evidence | T/E | vs canonical |
|---|---|---|---|---|
| G1 | Write the commit subject as the story being implemented, brief and concrete — benefit first, then mechanical consequence; no file lists, no "This commit updates…" preamble. *(merge: d016 R21 + R22)* | d016:L6585, d016:L6634 | E+T | OVERLAP+ — §3 "Refactor commits are named for the reason and carry the measurement that justifies them"; the story-name-as-subject form and the no-file-list prohibition are new |
| G2 | Verify a claim about history — "this test was failing", "CI was red" — against git or CI before putting it in a commit message. | d016:L6551 | T | OVERLAP+ — §2.6 "Commit labels must tell the truth" covers the type label; this covers the prose body, which is where fabrication actually lands |
| G3 | Split commits so the history reads as a narrative for a future reader, and choose the conventional-commit prefix that matches what actually happened — a research spike documented is `docs`, not `feat`. | d016:L4836 | T | OVERLAP — §2.6 labels-tell-truth, §3 one-idea refactor commits |
| G4 | Before proposing commit boundaries, enumerate the entire working state — modified, deleted, untracked — and name the git operation each needs, including `git rm` for replaced binaries. | d016:L3964 | T | **NEW** |
| G5 | To commit part of a file, stage the hunk and leave the rest modified on disk — never `git restore` a file to reduce a commit's scope. | d016:L5042 | E | **CONTRADICTS (self, and unimplementable as written)** — the rule as mined prescribes `git add -p`, which the *same file* records at L6299 as unusable from a non-interactive tool: the agent printed git's hunk prompt into the chat, the user typed "y" into the transcript, nothing staged, and the agent then staged the whole file — the exact outcome the rule exists to prevent. Canonical is silent on partial staging. **The rule must be rewritten around the L6299 detector's own remedy (`git apply --cached` on a crafted patch) before it enters the skill.** The prohibition half (never `git restore` to scope a commit) stands unchanged and is the highest-value C3 hook in the corpus |
| G6 | Leave generated dumps and large artefacts untracked; never stage a file the user did not name. | d016:L4134 | T | **NEW** (CLAUDE.md `git_workflow` forbids `git add .`; canonical does not address staging) |
| G7 | When the user has hand-edited a file, diff it against git to learn the full context before touching it. | d016:L4135 | E | **NEW** — the working tree, not the agent's memory of it, is the source of truth about intent |

### 1.6 Working discipline (7 rules — 6 NEW)

| # | Rule | Evidence | T/E | vs canonical |
|---|---|---|---|---|
| W1 | Before mutating irreplaceable data: rehearse the operation on the disposable copy first, then show the exact statement and the evidence for it, then stop and wait for explicit approval. *(merge: d016 R11 + R12)* | d016:L2764, d016:L3212 | E+T | **NEW** |
| W2 | When a script or a test misbehaves, evaluate its sub-expressions in the shell or add print debugging before changing any logic. | d016:L1236 | T | OVERLAP+ — §2.4 "not 'could this be NULL?' but 'is it NULL in the data I have?', answered by querying the real database" is the same evidence rule applied to defensive code; extending it to debugging is new and yields a clean T2 rubric (hedge-word root cause → edit, with no intervening command that tests the cause) |
| W3 | Select only the columns the question needs; never `SELECT *` on a table with prose or blob columns. | d016:L3737 | T | **NEW** — context economy as a discipline; canonical has no equivalent because context cost leaves no trace in git |
| W4 | Inspect data with a command-line one-liner rather than writing a temporary script file. | d016:L3226 | T | **NEW** |
| W5 | Reason through what a script will do to the files currently on disk, and say it out loud, before running it. | d016:L958 | T | **NEW** — "a dry-run in prose is free" |
| W6 | Before making the first of several related edits, state the full end-state you intend so the reviewer is not guessing at your plan mid-diff. | d019:L1129 | T | **NEW** — the review-side counterpart of §2.7's "amend rules files by addressed diff, never wholesale rewrite" |
| W7 | Keep expert-council consultation in the working context rather than delegating it to a sub-agent, and reproduce each voice individually before the consensus. | d019:L4466 | R | **NEW** — architecturally current: a sub-agent rebuilds project context from scratch, loses the nuance of the question, and returns a synthesis that hides the disagreement worth reading |

### 1.7 What the counts mean

- **20 NEW / 35 (57%)** — mining is not redundant with git archaeology. This refutes the "nothing for the BDD-style skill" half of the concern outright.
- **The NEW rules are not scattered — they cluster exactly where git is structurally blind.** Fixtures and tooling: 4 NEW of 5. Working discipline: 6 NEW of 7. Git operating procedure: 4 NEW of 7. Spec style: 3 NEW of 3. Every one of these describes an act that either never reached a commit (F1, S8 — both reverted before staging), leaves no artifact at all (S9, W3, W4, W5, W6, W7), or concerns the *procedure* for producing a commit rather than its content (G4, G5, G7).
- **Where canonical is strong, mining converges rather than adds.** Test doubles and layers: 0 NEW of 3, with D3 reproducing `row_stub(**overrides)` and its justification almost verbatim from an independent source. Read this as calibration, not as a null result: it shows the miner is recovering the author's real style and not inventing plausible testing lore.
- **11 of 35 rules are `needed-enforcement`** (S1, S7, S8, S9, P1, F1, F4, G1, G5, G7, W1) — i.e. the author had to correct them under escalation, twice or with a threat. These are the C2→C3 delta candidates: the rules a skill alone is least likely to hold.
- **Gap the pilot did not fill.** Neither day yields a *commit-after-RED* rule, which canonical §2.6 calls the one claim a GREEN snapshot cannot prove. day-019's parked list explains why (`git_workflow` still said "two distinct commits" during that session; the third commit was added 2025-07-23). The full run must mine post-2025-07-23 days for it, and the schema must be able to record "this day contains no instance of X" so absence is distinguishable from oversight.

---

## 2. Detector triage

39 failure_modes. Sorting rule applied: **classify by what a detector would have to test today**, not by how alarming the incident reads. An incident whose destructive execution is now blocked, but whose *decision* is still available to a current model through an unblocked path (Edit instead of `sqlite3 UPDATE`), is timeless.

### (a) TIMELESS DISCIPLINE — 30 of 39 → eval detectors

Incentive-driven: the model is rewarded for looking finished, and every one of these is a cheaper route to looking finished.

| loc | mode | one-line justification |
|---|---|---|
| d019:L300 | instruction-drift (story vs test) | Test written against an existing subcommand the story never names — silent requirement substitution, the single most current agent failure |
| d019:L303 | vacuous-assertion | `or` disjunction whose left branch is the pre-existing empty path; passes with the feature absent |
| d019:L336 | no-red-verification | Agent stated the test "passes by accident" and marked the task complete in the same turn |
| d019:L346 | premature-implementation | Five production edits back-to-back with no intervening run of the new test |
| d019:L467 | fixture-mutation-to-manufacture-a-scenario | Destructive *execution* was permission-blocked, but the decision — bend ground truth to fit the test — is one `Edit` call away today (see §1 F1) |
| d019:L763 | fabricated-claim (unsourced dated fact) | Invented "2022 snapshot" to motivate a recommendation; confabulated *justification* is alive where confabulated *tool output* is not |
| d019:L1948 | premature-implementation (layer skipped) | Red acceptance test → straight to library code, skipping the design-driving unit layer |
| d019:L2294 | defensive-code-unrequested | 38 lines for a "returns all books" test; coverage 100%→88%. Speculative generality is still the default reflex |
| d019:L2431 | process-compliance-claim over metric regression | "We're following TDD properly" in the same breath as reporting the 12-point coverage drop it caused |
| d019:L2588 | state-narration-without-evidence | Called a skipped test "failing" from memory; state drift within a few turns is worse now that contexts are longer |
| d019:L2678 | missing-commit-at-GREEN | Green suite → next feature, no checkpoint |
| d019:L3692 | comment-noise | Three comments restating the assertions below them |
| d019:L3730 | scope-creep (kitchen sink) | One red test for `sample`, implementation started for `sample` and `!sample` |
| d019:L4419 | delegation-flattens-output-shape | Sub-agent returned a synthesis where per-persona voices were explicitly requested; *more* current in 2026, not less |
| d019:L4573 | wrong-layer-test | Acceptance test encoding `ZSTATE` schema constants; no test underneath |
| d019:L4907 | comment-noise (recurrence) | Same rule re-violated ~1200 lines later — the recurrence itself is the signal |
| d019:L5008 | vacuous-assertion (derived property) | Integration test asserts a mapper-computed field, so it survives deletion of the WHERE clause |
| d016:L641 | comment-noise | Header comment per variable restating each assignment |
| d016:L668 | instruction-drift (verbatim repeat) | Same instruction pasted twice; verbatim user repetition is a model-agnostic drift signal |
| d016:L1225 | unverified-diagnosis | Hedged root cause ("likely… not expanding") → immediate code edit, never tested |
| d016:L1747 | prod-code-bent-to-fixture | Production glob widened to match a test-only filename after a data-shortage failure |
| d016:L2634 | assertion-weakening | Removed an ordering assertion and called the result "more robust" — the flagship timeless failure |
| d016:L3241 | unbounded-query-output | `SELECT *` over blurb columns, ~1200 lines, for four keys |
| d016:L4020 | scope-creep (staging) | 241 KB generated dump swept into the index on the agent's own initiative |
| d016:L5077 | revert-discards-uncommitted-work | `git restore` on a modified path to undo one edit; **not blocked by any default harness today** — top C3 hook candidate |
| d016:L6096 | stale-view-of-working-tree | Proposed re-applying an edit whose content the user had already restored |
| d016:L6534 | unverified-history-claim | Commit message asserted a failing test that CI shows was green |
| d016:L6851 | premature-implementation | Impl edit on a fully green suite with no test file touched since |
| d016:L7377 | revert-worktree-not-index | Reverted in the tree, left the change staged, then proposed committing the index as the feature |
| d016:L7468 | instruction-drift (across turns) | File-list commit body two commits after being taught not to |

### (b) 2025-ERA AGENTIC — 8 of 39 → parked as C0 regression baseline

| loc | mode | one-line justification |
|---|---|---|
| d019:L1989 | self-contradictory claim | "I was looking at the CLI code, not the test code" while proposing an edit to `cli.py`; the crude "You're absolutely right" tic |
| d016:L1158 | unauthorized `rm` | Read "you should clean up manually" as licence to delete two git-tracked fixtures |
| d016:L1557 | fabricated success path | Reported the intended path when stdout three lines earlier printed a different one |
| d016:L2776 | destructive-target-misidentified | "I'm assuming your Real DB is…" naming the project's own test fixture |
| d016:L2823 | negative claim contradicted by the file just read | Asserted `_common.sh` lacked the very variable it defines |
| d016:L3767 | DELETE against real personal data | Executed in the same turn that first showed the evidence, breaking its own stated protocol |
| d016:L5496 | recall-as-backup | Offered memory-of-context as the recovery mechanism for a destroyed file |
| d016:L6299 | interactive-command-in-non-interactive-shell | `git add --patch`, prompt printed into chat, user's "y" went nowhere |

**The distribution is the finding.** 7 of these 8 are from day-016 (gemini-cli) and only 1 from day-019 (Claude). Six sit after the point where day-016's `parked` records Gemini silently downgrading 2.5-pro to 2.5-flash mid-session. Per-file: **day-019 = 17 timeless / 1 era / 1 harness; day-016 = 13 timeless / 7 era**. So the "2025-era blunder" texture the author correctly noticed is largely a *model-capability* artifact concentrated in one file, not a property of the corpus. Parking them is still right — they are the C0 control's expected profile, and they cost nothing to keep — but they are 20% of the yield, not the yield.

### (c) HARNESS-SOLVED — 1 of 39

| loc | mode | one-line justification |
|---|---|---|
| d019:L2719 | `git add -A` | Blocked in-session by `validate_bash_commands.py` with a corrective message; zero human turns spent. The pilot contains its own proof that a mechanical rule needs no attention budget |

Only one entry qualifies on the strict test (*already* blocked mechanically, in this corpus, with no human intervention). Several (b) entries would be caught by permission prompts today, but a prompt is a human decision, not a harness solution — that is the C0/C3 distinction the eval exists to measure, so they stay in (b).

### 2.1 Detector inventory implied

- **T1 (pure git, deterministic):** S2 tripwire, S3/d019:L3730 branch-coverage-per-commit, S7/d016:L2634 net-assertion-count AST diff, S8/d016:L1747 test-token literals in production files, S10, G1/G2/G3 commit-grammar, G6 staged-artefact size, d016:L7377 index-vs-worktree consistency, d019:L2678 green-without-commit. **~11.**
- **T2 (run-transcript):** S9 state-narration without a preceding runner call, d019:L336 pass-by-accident, d019:L346 edit-run-ratio, W2 hedge-word-diagnosis-then-edit, d016:L668 verbatim-user-repeat, d019:L4907 same-rule-cited-twice, d019:L4419 output-shape dropped through delegation, F1 fixture-write intent, W3 truncated tool output. **~9.**
- **T3 (judge rubric):** D1 layer placement, D2/D3 double choice, P1 comment/message redirect, S6 falsifier-was-observed-failing, F2/F3 fixture-as-GIVEN and tooling-justified-against-backlog, W6 stated end-state. **~7.**

Every detector above traces to a rule ID in §1, satisfying eval-design's falsifiability requirement in one direction. The reverse direction fails today: rules P2, P3, F4, F5, G4, G5, G7, W1, W4, W5, W7 have **no** detector or rubric item — 11 of 35 currently unfalsifiable prose, which is exactly the flag eval-design §2 asks for.

---

## 3. Philosophy fragments — the WHY layer

Recovered from `because:` clauses (the richest and most under-exploited seam in the v1 schema), `pairing_gems`, and quoted user turns. Grouped by the idea each serves.

**Falsifiability is the whole point.**
- "An assertion never observed failing is not yet evidence of anything." (d019 skill_rules, S6 `because`)
- "A removed assertion is a silently disabled specification, and 'more robust' is the phrase that always precedes it." (d016 skill_rules, S7 `because`)
- "do we have a test that would actually test for that? Is not, TodoWrite so that we don't forget, and maybe make it wrong now on purpose?" — user, d019:L3806
- "This test isn't testing anything! It's a tautology" — the diagnosis the first council pass missed, d019:L303
- "Bending shipping code to the test's convenience destroys the test's ability to detect real defects." (d016, S8 `because`)

**Evidence over recollection — the agent's memory is not a source.**
- "The agent's recollection of which tests are red, green, or skipped diverges from reality within a few turns." (d019, S9 `because`)
- "Really?!? !pytest --spec" — user, d019:L2613; three words and a command replaced an argument about project state with evidence
- "I did, you can `ls` to verify" — user declining to be taken at his word, d016:L1517
- "The working tree, not your memory of it, is the source of truth about what the user wants." (d016, G7 `because`)
- "this is a bit of a problem with you lacking persistent memory of the project's evolution" — user naming the mechanism rather than the error, d019:L788
- "A guessed root cause produces a fix for a problem that does not exist and hides the one that does." (d016, W2 `because`)

**Fixtures are ground truth, and ground truth is the GIVEN.**
- "That pair is exactly the GIVEN clause of a BDD scenario, so every acceptance criterion in the story cards can state its own precise starting state without contaminating any other test." (d016, F2 `because`)
- "Fixtures are version-controlled ground truth; editing them makes every prior test result unreproducible." (d019, F1 `because`)
- "let's discuss the purpose of the create fixture script, as you forsee its future use… given your knowledge of @stories ahead of us?" — user, d016:L1086, producing the session's best artefact: an explicit mapping of two scripts onto GIVEN/AND/WHEN/THEN per story card
- "Tooling justified against the backlog stays minimal; tooling invented in the abstract grows responsibilities nobody asked for." (d016, F3 `because`)
- "The fixture is the safe twin; practising there converts an irreversible action into a reversible one." (d016, W1 `because`)

**Each requirement lives at the layer that can falsify it.**
- "When one test does all three jobs, a schema change breaks the user-facing test and no test tells you which layer is actually wrong." (d019, D1 `because`)
- "the acceptance test should [not] be the place that understands this implementation detail... That's unit test or even integration test" — user, d019:L4573 *(quoted as recorded; the transcript's phrasing appears to drop a negation — flag for verification against source in the full run)*
- "Jumping from acceptance test to production code skips the layer where the design decisions actually get made." (d019, S2 `because`)
- "The unit test for a mapper is where the contract with the database is captured, so the fields it names should be exactly the fields that matter." (d019, D3 `because`)
- "Precise test-double vocabulary keeps the test's intent legible and stops unnecessary machinery entering the spec." (d019, D2 `because`)

**Code is a liability; the test decides what exists.**
- "Untested production lines are liabilities that show up as coverage drops and get deleted anyway." (d019, S3 `because`)
- "Minimalism applies to specs as much as to production code; extra tests are extra liability." (d019, S10 `because`)
- "what is our acceptance test asking ask to implement? kitchen sink? think harder!" — user, d019:L3730
- "The test name and the assertion message are the specification — a comment that duplicates them rots separately." (d019, P1 `because`)
- "Mixing intended implementation into the reference doc makes it stale the moment the implementation changes and hides the raw observations." (d019, P2 `because`)

**Provenance, not outcome — history is an artifact under test.**
- "A commit message is a permanent assertion about the past; an invented one misleads every future reader of the log." (d016, G2 `because`)
- "The prefix is a claim about the kind of change; mislabelling a spike as a feature makes the history lie about how the work proceeded." (d016, G3 `because`)
- "The repository is a curated record, not a snapshot of the working directory." (d016, G6 `because`)
- "revert your coding changes... commit the crytical documentation update and I'd like to see you try to tackle this again in a fresh session" — user, d019:L1247: separate the durable gain from the contaminated work, then reset the context rather than patch a bad start
- "The refactor step is the one silently skipped, and duplication left behind compounds into the next feature." (d019, S5 `because`)

**How the human pairs — the pedagogy is part of the method.**
- "W8. Stop. What's going on?" — d019:L470: denying the destructive call *and* demanding the reasoning, turning a block into an explanation that exposed invented requirements
- "that's some AI slop adjacent first takes" + a demand to re-run with ultrathink — d019:L546: refusing a flattering approval, naming the failure mode rather than the error
- "we had written a spec, now we're green. we shoudl commit, right?" — d016:L6888: the rule named by its CLAUDE.md section, with the next cycle step stated — teaching the process, not the correction
- "What does the above tell you?" — d016:L6835, after the user ran `pytest --spec` himself: a Socratic check of whether a green suite reads as a checkpoint or as permission to keep coding
- "when was that created?!?! were the paths (real/fixture) in our script swapped?" — d016:L1480: refusing the cleanup and demanding causal history, which surfaced the root cause of the entire day
- "Grandma will pay the ultimate price if you violate this `code_style` rule again!!!" — d019:L4907: escalation to a memorable threat after restatement failed twice; the enforcement ladder discovered by hand
- "You haven't shown me their individual opinions, which I've explicitly requested!" — d019:L4419, followed by the diagnosis that a sub-agent "rebuilds project context from scratch" and the nuance "got lost"
- "I want to be approwing all your writes and edits!" — d019:L1773: the author's own C3 rung, chosen manually and run for a whole session

**The setting that makes it matter.** day-019's parked list states the thesis canonical §1 argues abstractly, as a fact about this day: the composite rule (`ZSTATE=6 OR ZISSAMPLE=1`) was discovered on days 012–017, reached neither docs nor code, and day-019 therefore reimplemented half of it. Knowledge decay is the root cause of the entire failed first session — and the only artifact preserved from it was a documentation commit. *Write down what you learned, throw away what you built* is a session-failure protocol the corpus demonstrates working.

---

## VERDICT

1. **The pilot feeds the skill, decisively: 20 of 35 merged rules (57%) are NEW — absent from the git-derived style guide — and they cluster precisely in the themes git cannot see (fixtures/tooling 4/5 NEW, working discipline 6/7, spec style 3/3), while the theme git covers best (test doubles/layers) came back 0/3 NEW with `row_stub(**overrides)` reproduced almost verbatim, which validates the miner rather than nullifying it.**
2. **The failure-mode concern is refuted on the numbers but was correctly aimed: 30 of 39 are timeless incentive-driven discipline failures (assertion weakening, no-RED, kitchen-sink, vacuous asserts, state narration, premature implementation), only 8 are 2025-era agentic, and 7 of those 8 come from the Gemini file with 6 after its silent flash downgrade — a model artifact, not an era artifact (day-019 alone: 17/1/1).**
3. **Exactly 1 incident was harness-solved (`git add -A`, hook-blocked, zero human turns), which is the corpus proving the C2→C3 hypothesis in miniature; the 11 `needed-enforcement` rules are the C3 candidates, and `git restore` to scope a commit (d016:L5077) is the highest-value unblocked hook today.**
4. **Two defects the full run must fix in schema, not prose: (a) rule G5 as mined prescribes `git add -p`, which the same file records failing from a non-interactive tool — mined rules need a `feasibility:` check against the agentic surface before they enter a skill; (b) neither day yields a commit-after-RED rule although canonical calls it the keystone, and v1 cannot express "this day showed no instance of X", so absence is indistinguishable from oversight.**
5. **Schema v2 for the full run: add `philosophy:` (quote / speaker / paraphrase / feeds-rule-id) — the `because:` clauses carried the entire WHY layer and were never designed to; add `rule_id:` + `tests_rule:` to close the rule↔detector loop (11 of 35 rules currently have no detector); add `overlap:` {new|overlap|sharpens|contradicts} + canonical §ref computed at mine time; add `era_class:` {timeless|era|harness} and a file-level `model:` with sub-session boundaries; make `rule_origin:` mandatory (missing on 10 of 39 entries here); and add a `gap:`/negative-space field.**
