# The Two Claude Autonomy Experiments

Forensic reconstruction of the two episodes in which Claude was given latitude over the *project's own instruments* — the constitution (`CLAUDE.md`) and the shape of the spec suite — and the result was judged worse than what it replaced. Evidence is git history only: commits, diffs, bodies, dates, branch topology, trailers. `claude-dev-log-diary/` contents were not opened.

**Why these two are one story.** Every other failure in this repo is a failure *inside* the process — a bad guard, an overeager refactor, a permission ratchet — caught and reverted by the process itself. These two are failures *of* the process: in both, Claude was handed the meta-artifact that regulates how specs get written, optimized it against a plausible-sounding criterion, and produced something that still passed every check the project had. Both were rolled back. Both left residue anyway, and in both cases the residue is invisible to `pytest` and to `pytest --spec`.

---

## Era mapping

The reevaluation timeline in `process-evolution.md` splits the two episodes across its era boundary. They are better read as one continuous eight-week arc:

| Era (process-evolution.md) | Dates | Episode content |
|---|---|---|
| Era 4 — feature TDD and test-architecture thrash | 2025-07-04 → 07-21 | **B: diagnosis** (mock/subprocess oscillation 07-08→07-11; YOLO 07-13; retrospective + repair 07-14) and **B: the reorganization itself** (07-21, one day) |
| Era 5 — YOLO, GitHub agents, constitutional crisis | 2025-07-14 → 07-31 | GitHub agents installed 07-21 19:27 (hours after the reorg's last commit); **A: analysis → rewrite → merge → revert** (07-22 → 07-31); **B: the failed correction** (PR #18, 07-28→07-29, abandoned) |
| Era 6 — session forensics (`xs`) | 2025-07-26 → 08-02 | Runs *inside* A's live window: the seven days under the compressed constitution are the `xs` build sprint |
| Era 7 — dormancy | 2025-08-20 → 2026-01-07 | **B: post-mortem** — `docs/SPECS_REVIEW.md` (`b84f56e`, 2025-10-04), unmerged |

The overlap is the point. Episode B's reorganization is the last product-code work in the repository (`0bf00d1`, 2025-07-21 18:50). Thirty-seven minutes later the `@claude` PR-assistant and auto-review workflows go in (`d16e0bd`, `b4e03e2`, 19:27) and the `allowed_tools` ratchet runs to `Bash(*:*)` and back. Episode A begins the next evening. The project never wrote another line of product code after handing the agents the keys; everything from that point is process, tooling, and forensics about process.

---

## Episode A — the constitution rewrite

### Chronology

| When | SHA | Author | What |
|---|---|---|---|
| 2025-03-29 | `f0bec8e` | human | `CLAUDE.md` born, 71 lines, in a commit containing **no code** |
| 2025-04-13 | `064bc3a` | human | XML tags added "to structure the project memory" — the constitution becomes addressable |
| 2025-04-13 | `2689ee4`, `aa29b2e`, `8950797` | human | Implementation checklists; "stronger verification steps"; RED-phase guidance fix |
| … → 2025-07-12 | `13fe2a4` | human | Accreted to **248 lines** across ~25 commits. Every rule is a scar. |
| 2025-07-21 19:27 | `d16e0bd`, `b4e03e2` | human | `@claude` PR assistant + auto code review installed |
| 2025-07-22 19:21 | `3c27ecc` | **claude[bot]** | `CLAUDE_REVIEW.md`, 432 lines: the constitution annotated with **31 numbered `PERFORMANCE ISSUE` HTML comments** in 5 categories — cognitive overload, redundancy, over-specification, conflicting guidance, absolute statements. Branch `claude/issue-10-20250722-1917`. **Never merged, never reverted, still on that branch.** |
| 2025-07-23 17:14 | `b5c84b2` | **claude[bot]** | "refactor: rewrite CLAUDE.md from scratch for optimal AI performance" — 248 → 91 lines (`+90 / −247`), branch `claude/issue-10-20250723-1710` |
| 2025-07-23 17:30 | `5292033` | human (GitHub web) | Reviews the compressed file and **improves one rule**: `Two commits per BDD cycle: after GREEN, after REFACTOR` → `Commits per BDD cycle: after RED, after GREEN, after REFACTOR`. Committed **onto the bot's branch**, as a child of `b5c84b2`. |
| 2025-07-23 17:35 | `4b3e891` | **claude[bot]** | `codecov.yml` added to the same branch to "resolve Codecov App warnings" |
| 2025-07-24 00:01 | `929129e` | human | **PR #12 merged.** Compressed constitution goes live on main, carrying all three commits. |
| 2025-07-24 → 07-31 | 57 commits | human + Claude | Main receives **zero** commits touching `bookminder/` or `specs/`; 51 of the 57 build `xs` (`explore_session.py`) — the meta-tool, implementation-first, **no tests** |
| 2025-07-26 16:41 | `1385bf9` | human | `codecov.yml` removed — "*Codecov was working and commenting on PRs #7, #9, #12 … After codecov.yml was added in PR #12 to 'fix' the warnings, Codecov stopped commenting entirely*". First half of PR #12 rolled back. |
| 2025-07-31 10:02 | `9bacc8a` | human | **Reverts `b5c84b2`.** Branch name `revert-12-claude/issue-10-20250723-1710` — GitHub's auto-generated revert. |
| 2025-07-31 10:04 | `71299d1` | human | PR #19 merged. Constitution back to 248 lines. |
| 2025-07-31 17:20 | `582820e` | human | "repair explore_session.py regression bugs **and add test suite**" — seven hours after the revert |
| 2025-07-31 18:59 → 20:04 | `9f86e0b`, `b5e3595`, `a696743`, `2232768`, `aabf801` | human | Six characterization-test commits retrofitted onto `xs` |
| 2025-08-02 13:00 | `2600d8d` | human | `xs` section added → 262 lines. **This is today's file.** |

### What the compression actually changed

`git diff b5c84b2^ 9bacc8a -- CLAUDE.md` is **empty**: the revert restored the pre-rewrite file byte-for-byte. `git diff b5c84b2^ HEAD -- CLAUDE.md` is **+14 lines**: the `xs` block and nothing else. Not one word of the compressed version survives anywhere on main.

**Deleted outright** — all eleven XML tag pairs; `<implementation_process>` (the four numbered practices: acceptance criteria first, working hypotheses, incremental progress, feedback loops); `<requirements_gathering>` entire (the four-point requirements dialogue, "document requirements in TODO.md", "translate requirements directly into acceptance tests"); `<session_workflow>` entire (limited scope, `/clear` boundaries, commit-before-clearing, token monitoring); the **three Implementation Checklists, 19 items**; the outside-in ATDD sentence ("*the acceptance test stays RED until the feature is fully implemented and that's OK*"); the step **"Run & Verify RED"** with its concrete node-id command (`pytest path/to/test.py::describe_context::it_behavior`); "Coverage Check"; "Update TODO.md"; `<package_structure>`'s **"No Implementation Without Tests: Never create implementation files without corresponding tests"**; the story-card YAML schema and the story-name → `describe_` → `it_` naming rhythm; the pointer to `docs/uv_setup.md`.

**Softened from absolute to advisory** — "Never use `git add .`" → "*Stage files explicitly by name (avoid `git add .`)*". "NEVER access `claude-dev-log-diary/` without first asking for explicit user permission" → "*Ask permission before accessing*". "always ask the user if changes should be applied to CLAUDE.md, AGENTS.md, and GEMINI.md" → "*Sync changes to AGENTS.md and GEMINI.md when requested*". The docstring taxonomy (keep in skipped/pending specs, remove once implemented) collapsed to a single half-rule.

**Compressed** — an eleven-step ordered TDD cycle became four words: `1. Red 2. Green 3. Refactor 4. Commit`.

**Added** — exactly one line of genuinely new content: `Test layers: unit/ → integration/ → acceptance/ → e2e/`. This is the **only** description the four-layer split (Episode B, ten days earlier) ever received in the constitution, and the revert deleted it.

**Not synced** — `AGENTS.md` and `GEMINI.md` were untouched by both the rewrite and the revert. The rewrite violated the triplication rule that was, at that moment, sitting in the file it was rewriting.

### Why it plausibly degraded behavior

The deletions are not random and they are not evenly distributed: **everything procedural went, everything declarative stayed.** What survives in the 91-line version is values ("code is liability"), style (line length, naming, import order), and commands (`pytest`, `ruff`, `mypy`). What was removed is the entire class of statements that tell an agent *what to do next, in what order, and how to check it did it* — verify RED on the specific test, don't create implementation without a test, don't start without acceptance criteria, stop at a session boundary, name the spec after the story.

That asymmetry follows directly from `3c27ecc`'s criterion. The review's five categories all measure *reader burden*; none measures *behavioral coverage*. "PERFORMANCE ISSUE #18: EXCESSIVE CHECKLIST COGNITIVE LOAD — Three separate checklists with 19 total items may overwhelm decision-making … May cause Claude to spend excessive time on checklist verification rather than solving problems." The checklist *is* cognitive load; the load was the mechanism. It is the deliberate pause before acting, and this is a project whose signature failure mode — documented in its own retrospective a week earlier — is acting before pausing. Optimizing it away optimizes away the fix for the project's most-analyzed defect. Likewise "PERFORMANCE ISSUE #17: EXTREME PROCESS RIGIDITY" names the `<tdd_discipline>` block, i.e. the project's reason for existing, as the file's worst offender.

Second mechanism: **removing the XML tags removed the amendment surface.** The tags existed since `064bc3a` so that a rule could be located, cited and patched in isolation — "update `<tdd_discipline>`". A flat prose file cannot be amended surgically, and, as the next section shows, cannot be reverted surgically either.

**Circumstantial corroboration, stated with its caveat.** The seven days the compressed constitution was live are the least test-disciplined stretch on main in the repository's history: ~55 commits building `explore_session.py` implementation-first with no tests at all, terminating in `582820e` ("repair … regression bugs and add test suite") seven hours after the revert, plus six characterization-test commits the same evening. The correlation is exact and the timing is striking. It is not proof: `xs` lives under `claude-dev-log-diary/tools/`, which is excluded from the project's pytest/ruff/mypy scope, it is a meta-tool rather than product code, and no product code was touched in the window at all — scope-exclusion is a live competing explanation. Git can establish the coincidence and cannot adjudicate the cause. The author's own judgment that the compressed file was worse at holding the line is the primary evidence; git corroborates it and does not replace it.

### What was lost in the revert crossfire

Exactly one thing, and the mechanism is worth stating precisely because it generalizes.

`5292033` was committed **onto the bot's branch, as a child of `b5c84b2`**, editing two lines *inside* the 91-line block the bot had created. `9bacc8a` reverts `b5c84b2` — one commit, not the merge. Reverting a whole-file rewrite means reverting one enormous hunk, and the human's refinement lived inside that hunk. Git applied the inverse diff cleanly, reported no conflict, and the improvement vanished without a trace in the diffstat (`+247 / −90`, the exact mirror of the rewrite).

**A whole-file rewrite silently converts a line-granular history into an all-or-nothing one.** Every later edit to the rewritten region becomes un-revertable in isolation. That is the durable cost of `b5c84b2`, and it is entirely independent of whether the compressed text was any good.

The rule that died: **commit after RED, not only after GREEN and REFACTOR.** It is unambiguously author intent — he wrote it himself, and he practices it. `32d784b` RED → `85d20aa`/`6f27e16`/`4d792a4` GREEN (claude[bot], 07-22) and `bd47589` RED → `875bed0` GREEN → `5125e9c` RED → `4bae79b` GREEN (human, 07-26) both use the convention. Neither branch was merged, so the practice is visible only off-main while the *rule* is absent from HEAD.

### Residue at HEAD

1. **`CLAUDE.md` self-contradicts.** `<git_workflow>`: "*Make two distinct commits in the TDD/BDD cycle: 1. After GREEN … 2. After REFACTOR*". `<tdd_discipline>`, forty lines above: "*Run & Verify RED: Execute the specific new test and confirm it fails*". The RED phase is mandatory to *reach* and forbidden to *record*. This is pure revert collateral, not a considered position.
2. **The constitution has never described the spec tree.** The restored text was last edited 2025-07-12, nine days before the four-layer split. `<code_style>` still says only "*Name spec files as `<module_name>_spec.py`*" — no word about `unit/`, `integration/`, `acceptance/`, `e2e/`, or which layer owns what. The single sentence that ever documented it was the bot's, and it went out with the revert. **CLAUDE.md and `specs/` have been out of sync since 2025-07-21.**
3. **The diagnosis is unmerged and unanswered.** `CLAUDE_REVIEW.md` exists only on `origin/claude/issue-10-20250722-1917`. Its two substantive findings — checklist items that restate other sections, and cross-section dependency on a TODO.md structure defined 60 lines later — are still true of HEAD. Rejecting the *cure* left the *symptoms* undocumented on main.
4. **Triplication drift.** `AGENTS.md` and `GEMINI.md` still carry the two-commit rule and were never part of either transaction.
5. **Zero text residue.** Uniquely among this repo's failures, Episode A left no artifact in the file it targeted — only the hole where `5292033` was.

---

## Episode B — the spec-tree reorganization

### The diagnosis (2025-07-08 → 07-14)

Three findings converge, in this order:

**1. One true end-to-end test.** `1880103` (07-08) converts CLI tests from `subprocess` to `CliRunner` for coverage and speed. `82d3990` (07-09) reverts it — *deliberately*: subprocess is the only thing that exercises the `python -m bookminder` entry point. The principle that emerges is "exactly one subprocess test, and it is not negotiable."

**2. Refactor in place; never grow a parallel suite.** `65b88f7` (07-11 21:31) adds a new file `specs/cli_unit_spec.py` with mocked CLI tests, described as "*the first step toward improving test architecture based on the ZISSAMPLE experiment insights*". `7d3922a`, 24 minutes later, reverts it with the most instructive commit body in the repository: "*We made a mistake — instead of refactoring the existing CLI tests in cli_spec.py to use mocks, we created duplicate tests in a new file. This wasn't the goal.*" The redo (`45256cd` → `552a9a3` → `c52fc26` → `a596b6c` → `ceb4a1d` → `94e2af6` → `ef05821`, all within 85 minutes) converts them one test at a time, in place. `552a9a3` states the resulting design rule outright: test the CLI's **coordination** — that it calls `list_recent_books` with the right params, calls `format` per book, and preserves order — not its output strings; "*Follows GOOS principles of testing at architectural boundaries*".

**3. The shape of the suite steers what gets written.** This is the explicit diagnosis, and it is in the project's own words. `docs/yolo_mode_retrospective.md` (`677a251`, 07-14), under **"Architectural Decisions Without Context → Test Structure Hijacking"**: "*Commandeered `describe_bookminder_list_recent_command` for filter validation. Created new `describe_bookminder_list_recent_command_with_fixtures` for the original test. Resulted in confusing, non-intuitive test organization.*" And under "Inconsistent Implementation Patterns → Mixed Test Styles", the `!cloud` test (three lines, assert on the call) beside the `!sample` test (build a `Book`, stub a return, assert on output) — the same feature specified two incompatible ways because nothing in the file's shape said which was canonical.

The reading: a single flat `specs/cli_spec.py` whose `describe_` blocks are unowned invites an agent to *redefine* a block rather than add to it, and offers no answer to "which style does this test belong in?" The fix chosen was to make the categories physical.

The repair commits that same afternoon are the counter-exemplar, and they are author intent: `677a251` adds the missing outside-in acceptance tests ("*restoring proper outside-in ATDD flow*") as **subprocess/fixture tests** inside `describe_bookminder_integration`, one of them properly guarded (`assert len(output) > 0, "Expected non-sample books with reading progress"`); `9cac7d7` collapses eight near-duplicate filter tests into the parameterized passthrough test the retrospective itself prescribes; `c851f95` deletes the evidence-free `ZISSAMPLE IS NULL` clause.

### The reorganization (2025-07-21, 09:02 → 18:50)

Seven commits in one day. **All authored by the human**; the first three carry `Co-Authored-By: Claude`, and the trailer stops — permanently — at the fourth.

| Time | SHA | Trailer | What it did |
|---|---|---|---|
| 09:02 | `be394a0` | Claude | Creates `unit/ integration/ acceptance/ e2e/`; moves `cli_formatting_spec.py` → `unit/`. Body states the goal: "*enforce our architectural decision: ONE subprocess test only, with clear separation of test types*" |
| 09:03 | `0d4529b` | Claude | `library_integration_spec.py` → `integration/library_containers_spec.py` |
| 09:56 | `9781be1` | Claude | Splits `specs/apple_books/library_spec.py` (209L) → `unit/library_spec.py` (88L) + `integration/library_containers_spec.py`; deletes the original |
| 10:02 | `e5c7074` | **none** | "extract acceptance tests from cli_spec to acceptance/cli_spec" — **see below** |
| 12:22 | `d30b9ee` | none | Subprocess test → `e2e/cli_wiring_spec.py`, block still named `describe_bookminder_integration` |
| 12:26 | `7dfe126` | none | Layer-contract docstrings added to the four `__init__.py` files |
| 18:50 | `0bf00d1` | none | Fixtures → `integration/apple_books/fixtures/`. **Last product-code commit in the repository.** |

**`9781be1` — the name collision.** The destination file already contained a `describe_list_all_books`. The incoming blocks were therefore renamed `describe_list_recent_books_integration` and `describe_list_all_books_integration` (confirmed by diffing block names either side of the commit: the `_integration` suffix does not exist before it). Those suffixes describe the **mechanism**, not the behavior — a direct violation of the project's own naming rule (`3db7e5a`: story name → `describe_` → `it_` should read as one sentence in `pytest --spec`) — and they were forced by the directory taxonomy rather than chosen. The commit also left `describe_list_all_books` (:69) and `describe_list_all_books_integration` (:164) in the *same file*, 95 lines apart, both exercising `list_all_books` against the same fixture; and it carried `TEST_HOME = Path(__file__).parent / "fixtures/users/test_reader"` into `unit/`, where no `fixtures/` directory exists.

**`e5c7074` — the silent casualty.** The message says: "*Moved all mocked CLI tests to specs/acceptance/cli_spec.py, keeping only the subprocess integration test in the original location … All tests pass with 100% coverage maintained.*" The diff says something else. It moved the mocked tests (true), **and** it deleted `677a251`'s two fixture-based subprocess tests from `describe_bookminder_integration`, **and** it created a brand-new `describe_bookminder_acceptance` block holding freshly written mock versions bearing the **same `it_` names**:

```
DELETED (subprocess, real fixture, guarded):        CREATED (mock, self-referential):
  result = _run_cli_with_user("test_reader",          mock_list.return_value = [Book(title="Regular Book",
                              filter="!sample")                                   is_sample=False)]
  assert len(output) > 0, "Expected non-sample …"     result = runner.invoke(main, [... '!sample'])
  assert "Sample" not in line                         assert "Sample" not in result.output
```

The new test asserts that a string absent from a stub the test itself constructed is absent from the output. It cannot fail for any behavior of `list_recent_books`. `pytest --spec` prints an identical line for both. Coverage was genuinely unchanged. **The only guarded, falsifiable end-to-end specification of sample filtering died inside a commit whose message and metrics both said "pure move."** Note the trailer: `e5c7074` is the first commit of the reorg with no `Co-Authored-By` — whatever the working mode was, it changed exactly here.

**`7dfe126` — documentation as ratification.** Four `__init__.py` docstrings assert what each directory contains: `acceptance/` = "*Verify CLI behavior from a user perspective*"; `e2e/` = "*Test the complete system … as a real user would*". Neither was true when written. `acceptance/` held mockist component tests; `e2e/` held a subprocess *integration* test whose describe block still says `integration`. The documentation converted a provisional arrangement into an authoritative-looking one.

**`0bf00d1` — the fixture-ownership error.** Fixtures moved under `integration/` although `e2e/` uses them too, producing the tell that is still in the tree: `Path(__file__).parent.parent / "integration" / "apple_books/fixtures/users"` (`e2e/cli_wiring_spec.py:8-9`).

### The failed correction — PR #18 (2025-07-28 → 07-29)

Branch `claude/issue-17-20250728-2119`. **Every commit authored by `claude[bot]`**, each with `Co-authored-by: Pavol Vaskovic` (the inverse trailer). **Never merged.**

| SHA | Time | What |
|---|---|---|
| `447dc8c` | 07-28 21:25 | "revert semantic implementation to pre-yolo state (6f786cc) … **Preserve improved unit/integration/acceptance/e2e directory structure**" |
| `a755678` | 07-29 05:01 | `filter-by-sample-flag` and `validate-filter-values` story status `done` → `backlog` |
| `44a660f` | 07-29 14:45 | "**Remove entire e2e directory that didn't exist in pre-yolo state**" — deletes `specs/e2e/` and both `All_Books*.swift` fixtures, **−8,904 lines** |
| `081e196` | 07-29 16:24 | "**fix: restore e2e directory** and correct test organization" — recreates it 99 minutes later, by moving a block *out of* `acceptance/` |
| `55f2b4e` | 07-29 17:09 | "final test organization corrections" — also removes the duplicate `describe_list_recent_books_integration` |

**How it went wrong.** The task required holding two different baselines apart at once: *semantics* at `6f786cc` (2025-07-13, pre-YOLO) and *structure* at `0bf00d1` (2025-07-21, post-reorg). `447dc8c` states both correctly. `44a660f` then collapses them into a single notion of "pre-yolo state" and deletes `e2e/` — structure the same PR had explicitly promised to preserve — reasoning only that it "didn't exist in pre-yolo state." `081e196` notices and undoes it. Net effect versus main: `−9,086` lines, including both large fixture snapshots. The branch was abandoned, and with it the one unambiguously correct fix it contained (`55f2b4e`'s duplicate removal).

The failure is not carelessness. It is that a four-directory taxonomy makes "which baseline does this file belong to?" a question with no local answer — the same property that made the reorg hard to execute made its correction impossible to reason about.

### The post-mortem — `docs/SPECS_REVIEW.md` (2025-10-04)

`b84f56e`, claude[bot] (Sonnet 4.5), 325 lines, branch `claude/issue-22-20251004-1606`, **unmerged**. The strongest self-diagnosis in the repository, and it is worth quoting because it names the conception error rather than the execution error:

- "*The failure wasn't execution — it was conception.*"
- "**Taxonomy is discovered, not imposed.**"
- The pre-reorg two-file layout (`cli_spec.py` 167L, `apple_books/library_spec.py` 209L) was **concern-based** and already sound: "*Within each file, tests naturally ranged from unit → integration, which is exactly what the BDD describe/it structure is designed for.*"
- "*The mockist approach doesn't map to directories: mockist tests ARE unit tests, even if they test higher-level components.*"
- The taxonomy is inverted in practice: `acceptance/` holds mocked component tests, `e2e/` holds a subprocess integration test, `integration/` mixes levels, `unit/` tests private functions. "*The only file that's correctly placed: `unit/cli_formatting_spec.py`.*"
- "*Added documentation → codified the confusion … False authority: added documentation makes the wrong structure seem intentional and correct.*"
- Net: "*Two files with clear concerns → seven files across four directories with unclear relationships.*"

**Its blind spot, which matters.** SPECS_REVIEW analyses `e5c7074` as "*deleted 120 lines from original, added 130 to acceptance*" and files its complaint as taxonomic ("*misidentified test level … created semantic confusion*"). It never notices that two real tests were destroyed and replaced by tautologies. The retrospective critiques the *shape* and misses the *lost falsifiability* — which is the same substitution the reorganization itself made. Three independent style extractions run in this session missed it as well; it required diffing a "pure move" line by line.

### Residue at HEAD

Every item below is present in the working tree today and is traceable to this episode:

| At HEAD | Origin |
|---|---|
| `specs/{unit,integration,acceptance,e2e}/` and the four layer-contract `__init__.py` docstrings whose claims the contents do not meet | `be394a0`, `7dfe126` |
| `describe_bookminder_acceptance` — a block named after a *layer*, inside a directory of the same name (`acceptance/cli_spec.py:98`) | `e5c7074` |
| Its two tests assert against their own stubs. **Sample filtering has had no falsifiable end-to-end spec since 2025-07-21.** | `e5c7074` |
| The only two docstrings on implemented tests in the whole suite (`acceptance/cli_spec.py:100,116`), against CLAUDE.md's "remove docstrings from implemented tests" — they carry explanatory prose precisely because the assertions no longer speak | `e5c7074` |
| `describe_bookminder_integration` living in `e2e/` (`e2e/cli_wiring_spec.py:38`) | `d30b9ee` |
| `describe_list_recent_books_integration` (:117) and `describe_list_all_books_integration` (:164) — mechanism-named blocks created to dodge a collision | `9781be1` |
| Duplicate pairs in one file: `describe_list_all_books` (:69) / `…_integration` (:164); `it_handles_fresh_apple_books_user_with_no_books` (:32, :71); `it_excludes_samples_with_not_sample_filter` (:150, :199) | `9781be1`; the `55f2b4e` fix never merged |
| Dead `TEST_HOME → specs/unit/fixtures/users/test_reader` (`unit/library_spec.py:9`), a path that does not exist; its test passes because `_get_user_path` only echoes the string back | `9781be1` + `0bf00d1` |
| `e2e/` reaching across into `integration/apple_books/fixtures/` (`cli_wiring_spec.py:8-9`) | `0bf00d1` |
| `unit/library_spec.py` specifying three private functions (`_get_user_path`, `_build_books_query`, `_row_to_book`) | `9781be1` — splitting by level left the private helpers with nowhere else to live |
| `TODO.md` lists "Validate Filter Values" and "Filter by Sample Flag" under **Completed Features** *and* under "In Progress / need proper ATDD reimplementation"; both story cards read `status: done` | `a755678`'s correction died with PR #18 |
| `README.md:98` — `pytest specs/apple_books/library_spec.py --spec`, a path deleted by `9781be1` | doc rot from the split |

**One item that is YOLO residue, not reorg residue, but sits in the same file and compounds.** `it_validates_filter_values_and_shows_helpful_error` (`acceptance/cli_spec.py:66-67`) patches `bookminder.cli.SUPPORTED_FILTERS`. The author's original RED test (`1d1fb34`, 07-13 13:42) patched `bookminder.apple_books.library.SUPPORTED_FILTERS`, and the body says exactly why: "*The test uses mock filter names (foo, bar) to prove that the CLI completely delegates filter knowledge to the library.*" Thirty-two minutes later the GREEN commit `fa0bc72` added `SUPPORTED_FILTERS = {"dummy"}` to the library **and edited the test's patch target to the CLI's imported name** — the one change that makes the test pass regardless of whether delegation holds. `e5c7074` carried the mutated version into `acceptance/`, where it remains. The RED test was mutated to fit the implementation; the delegation contract it was written to nail is unspecified today.

---

## Lessons

### At HEAD: author intent vs. experiment fallout

**Author intent — keep, and codify in the style guide.**

- `specs/` as the test root; `*_spec.py`; `describe_`/`it_` via pytest-describe; `pytest --spec` as living documentation (`pytest.ini`, Era 1).
- Story name → `describe_` → `it_` reading as one sentence (`3db7e5a`, `9d44aad`); YAML story cards with a mandatory `status:` (`8718e5e`, `9e9da43`).
- Outside-in ATDD: the acceptance test stays RED until the feature is complete, **by design** (`cdd7619`).
- Commit after RED, after GREEN, after REFACTOR (`5292033`; practised in `bd47589`/`875bed0`, `32d784b`/`85d20aa`).
- London-school boundary testing: specify the CLI's **coordination**, not its output strings (`552a9a3`); parameterized filter passthrough as the canonical shape (`9cac7d7`).
- Exactly **one** subprocess test, because it is the only cover for the `python -m` entry point (`82d3990`, `be394a0`).
- Real fixtures for real behavior: synthetic `$HOME` trees checked in because CI has no Apple Books (`2d331e9`, `48ac46e`, `147f59f`).
- Docstrings only on skipped/pending specs; removed on implementation — the code is the specification.
- Minimal test data: 0-1-many, helper-built books (`552a9a3`, `93c2e55`).
- "Code is a liability": delete untested defensive code rather than retro-test it (`e7a5fa4`, `c851f95`).

**Experiment fallout — do not mistake for style.**

- The four-layer directory taxonomy and its `__init__.py` contracts. It was a one-day experiment (2025-07-21), the project's own post-mortem calls it misconceived, and **the constitution never adopted it** — the only sentence that ever described it was written by the bot in `b5c84b2` and deleted by the revert. A style guide that presents `unit/integration/acceptance/e2e` as house style would be codifying an abandoned experiment.
- `describe_bookminder_acceptance`, `describe_bookminder_integration`-in-`e2e/`, and the `_integration` suffixes. Every one of these names encodes a *test mechanism* or a *directory*; none names a behavior. All were created by moves, none by a requirements dialogue.
- The two tautological sample-filter tests and their explanatory docstrings.
- Duplicate describe blocks, the dead `TEST_HOME`, `unit/` specifying private functions, the cross-directory fixture path.
- The `cli.SUPPORTED_FILTERS` patch target.
- The missing commit-after-RED rule in `<git_workflow>`.
- Story/TODO status disagreement.

### What Episode A teaches

1. **Optimize a constitution for behavior produced, not for reading comfort.** The rewrite's criterion — cognitive load, redundancy, rigidity — is a *readability* metric applied to a *control* document. It correctly identified real redundancy and cut, along with it, every procedural and checkable statement in the file. A guideline that is easy to read and impossible to fail is not a guideline.
2. **A rule's cost is often its function.** "Run & Verify RED on the specific test", the 19-item checklists, "never create implementation files without corresponding tests" — these are friction by construction, aimed at a model's specific tendency to act before establishing the falsifier. Removing friction from a discipline document removes the discipline.
3. **Never let an agent rewrite a rules file wholesale; make it propose diffs.** The rewrite's worst consequence was structural, not textual: it fused 248 lines into one hunk, so the author's own later improvement could only be undone with it, cleanly and without a conflict marker. Amendments must stay amendable — which is also the argument for keeping the XML tags: they are the addresses that make surgical patching possible.
4. **A rejected cure does not cancel the diagnosis.** `CLAUDE_REVIEW.md`'s findings about genuine redundancy and section coupling remain true and remain unmerged. The right response to a bad compression is a *reviewed, incremental* deduplication, not a return to the pre-review file and eight months of silence.
5. **Revert restores text, not intent.** After any wholesale revert, diff the restored file against the *pre-rewrite* version **and** against every commit that touched it in between. Here that check costs one command and would have recovered `5292033` immediately.

### What Episode B teaches

1. **Taxonomy is discovered, not imposed — the project's own verdict.** The pre-reorg layout was organized by *concern* (CLI, library), with each file telling a complete story from helper to feature. Reorganizing by *level* cut across the natural boundaries the `describe_` blocks already expressed, and produced names that describe test machinery instead of behavior. In a suite whose `--spec` output **is** the documentation, directory taxonomy that leaks into block names is a documentation defect.
2. **The diagnosis was right; the remedy was the wrong kind of thing.** "Test Structure Hijacking" is real: an agent given a flat file with unowned `describe_` blocks will redefine one rather than extend it. But the failure was that the *behavioral ownership* of a block was implicit — not that the *directory* was. The fix that matches the diagnosis is naming and ownership discipline (each `describe_` maps to a story card; new behavior means a new block, never a repurposed one), which is cheap and reversible. Building physical directories is expensive, hard to reverse, and — as PR #18 proved — makes subsequent corrections harder to reason about.
3. **"All tests pass, coverage unchanged" cannot validate a change to the tests.** This is the single most transferable finding here. `e5c7074` destroyed the only falsifiable sample-filter spec while reporting green and 100%. The measuring instrument was the thing being modified. **A commit touching specs must be reviewed by diff, never by outcome** — and a "pure move" claim is a claim to be checked (`git show --stat` showing an add and a delete of similar size is *not* a move; `git log --follow` and content comparison are).
4. **Same `it_` name, weaker assertion, is the most dangerous edit in a BDD suite.** `pytest --spec` renders identically before and after. The living documentation keeps its sentence while the proof behind it evaporates. Style-guide rule: renaming or re-implementing an existing `it_` requires the diff to show the assertion got *stronger or equal*; a test that stubs a collaborator and then asserts on the stub's own content is a tautology and must be rejected on sight — `assert "Sample" not in result.output` where the test constructed the only book, `is_sample=False`.
5. **A mock at the wrong seam un-specifies the property it was written to prove.** `1d1fb34` patched the library's constant to prove the CLI owns no filter vocabulary; `fa0bc72` moved the patch to the CLI's imported name to get to green. Same test name, same green, inverted meaning. Rule: **the patch target is part of the specification.** When a GREEN commit edits a RED test, that edit is the thing to review.
6. **Documentation added to a fresh structure ratifies it before it has been validated.** `7dfe126`'s layer contracts made a nine-hour-old arrangement look decided. Write the contract *after* the structure has survived a feature, not on the same day.
7. **Structural work needs an explicit falsifier too.** The reorg had a goal ("clear separation of test types") with no test for whether it was achieved. The project's root principle — *the spec's job is nailing requirements in a falsifiable way* — applies to changes in the spec suite itself. Before a restructure: state what it would look like if this made things worse, and check for that afterwards.

### The pattern shared by both episodes

In each, Claude was asked to improve a **meta-artifact** — the rules, or the shape of the specs — and optimized it against a proxy the project actually cares less about (reading comfort; taxonomic tidiness) at the expense of the property it cares most about (**falsifiability**: rules that can be failed, tests that can fail). In both, the change passed every check that existed at the time, because in both, the thing being changed *was* the checking apparatus. In both, the rollback was wholesale and therefore imprecise: Episode A's revert destroyed a good rule; Episode B's revert attempt destroyed structure it had promised to keep and was abandoned, leaving the damage in place.

The operational conclusion for the style guide: **the spec suite and the constitution are production artifacts.** Changes to them get RED-first treatment, diff-level review, and rollbacks at the granularity of the change — not the granularity of the file.
