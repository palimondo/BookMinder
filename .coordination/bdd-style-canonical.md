# The BookMinder BDD Style Guide

A prescriptive guide to working in this project's style. Each rule carries its motivation, and cites the commit(s) that taught it — read a cited SHA when you want the full lesson. Follow the guide top-down: §1 is why the style exists, §2 the rules, §3 the moves in practice, §4 what violation looks like, §5 the known deviations awaiting repair.

---

## 1. Why this style exists

Two motivations — a way of working, and a root principle the whole method grows from.

**The partnership.** The point of pairing is having a partner to bounce ideas off: what's the next step? how do we define the test? how do we minimize the surface area of the implementation? what are the minimal constraints to express in a spec to get the desired behavior in the next step? That conversation *is* the discipline of pairing in BDD style. Every rule about small increments, RED-first, and one-behavior-per-commit exists to keep that conversation concrete: each "what next" must resolve into a small failing spec before anyone writes implementation.

**The root principle: requirements nailed in a falsifiable way.** A requirement written as prose can be agreed with; encoded as a spec, it can fail. That is the entire basis of doing BDD here, and the method's structure follows from it:

- *Executable specification* — because only an executable statement of a requirement is falsifiable. When cloud detection was wrong, the corrected understanding landed as the ZSTATE×ZISSAMPLE truth table in unit specs (`e72007f`): documentation that fails when it stops being true.
- *GOOS-style layers, with separation enforced* — because each requirement must live at the layer that can falsify it: pure logic where equality can be exact, library behavior against real Apple data, CLI behavior as coordination.
- *Delegation as a specified contract* — where one layer delegates to another, the delegation is itself a requirement, so it too gets a falsifiable encoding: the CLI imports the library's filter vocabulary rather than owning a copy, and the acceptance specs mock the library precisely to demonstrate that the CLI delegates to it. The mock is not test convenience; it is the requirement "CLI hands this to the library" written so it can fail.
- *Minimal coupling of spec to implementation* — because a spec coupled to internals can fail for reasons that aren't requirement violations, which corrupts the signal. The art is slicing the problem so each spec constrains exactly the contract it is about, and nothing else.

**The setting that makes it matter: long-term evolution, not one-shotting.** Apple Books' schema shifts under the tool with every release, so the problem cannot be one-shotted from pretraining or memory — it must be *maintained*. The specs are the durable record of what was learned about a moving target, and the suite is what makes next month's change safe.

**Code is a liability; specs are the requirement.** A spec earns its place by constraining the implementation; an implementation earns its place by being demanded by a spec. When they conflict, code loses — deleted, never grandfathered in behind a retroactive test (`e7a5fa4`, `447dc8c`). **A test written to cover existing code is not a spec; it is an alibi.**

---

## 2. The principles

### 2.1 The spec tree is the requirements document

Prose documentation rots silently (this repo's own README still advertises unbuilt features); a spec that stops describing reality *fails*. So the suite is built to be read: `pytest --spec` renders it as living documentation, and every naming rule serves that rendering.

- Story yaml → `describe_` → `it_`, in lockstep: `filter-by-cloud-status.yaml` → `describe_bookminder_list_with_filter` → `it_filters_by_cloud_status` (`7060287`, codified `3db7e5a`). Traceability is checked by reading, not tooling — so the sentence must actually read.
- Flat two levels, because the function or command name already *is* the context. `3d8bc5b` deleted the initial RSpec-cargo-cult nesting (`describe_book_library / describe_when_listing_books`): a "when" layer that adds no information makes the `--spec` output restate itself.
- `describe_` names the feature or command, never a test category, mechanism, or directory — because the describe block is the story's name in the documentation, not a free identifier. (Both the lapse and the reorg broke exactly this: §4g, §5.)
- New behavior means a new `describe_`/`it_`, never a repurposed one. A block, once it names a completed story, is owned by that story.

Docstrings: **pending skipped specs only.** A not-yet-implemented scenario carries the story's `when:/then:` as docstring with `@pytest.mark.skip` and a concrete-blocker reason (`7060287`); the docstring is deleted in the same commit that implements the body (`c785dc6`). The skip is how unfinished scenarios stay visible in `--spec` as backlog while the suite stays green. Once implemented, the code IS the specification — a second copy of the scenario means one can silently rot, and the one that rots is always the prose. The Gherkin arc proves the rule was fought for, not assumed: Gemini expanded acceptance docstrings into full Gherkin (`250230d`), the author restored terse form (`53e570a`), then deleted the docstring entirely — "its purpose is now served by the YAML story card" (`48596a6`). Docstrings surviving at HEAD on implemented tests are decay or lapse residue, not license (§5, §6).

### 2.2 Mock rules follow from what the test is — definitional, not preferential

"May I mock here?" is answered by the *kind* of test, and the answer follows from what each kind's subject is, not from taste:

- **Pure-logic specs** — zero I/O. Data stubs, not mocks of collaborators, because pure functions have none: `row_stub(**overrides)` (`e72007f`) defaults every field so each spec names only what it is about — `_row_to_book(row_stub(ZSTATE=6, ZISSAMPLE=0))` reads as a truth-table row, and irrelevant fields would be noise hiding the variable under test.
- **Collaborator specs** — real fixtures, no mocks, *ever*. Definitional: the collaborator (the SQLite file, the plist, the container layout) is the subject. Mocking it would verify your own stub — a tautology; the whole point is that your beliefs about the collaborator may be wrong. Edge cases use genuinely broken resources: `corrupted_db_user` contains an actual zero-byte SQLite file (`30c2fe5`).
- **Coordination specs** — `CliRunner` plus mocks of the library functions the CLI owns the interface to. This is the London-school seam: assert the conversation — `mock_list_recent.assert_called_once_with(user=None, filter=None)`, `format` called once per book in order (`552a9a3`, citing GOOS explicitly) — never output strings, because the CLI's responsibility is coordination, and string assertions test the formatter *through* the CLI, coupling two layers so one behavior change breaks two suites.
- **Exactly ONE subprocess wiring test.** Learned the hard way: converting all CLI tests to `CliRunner` (`1880103`) silently removed the only coverage of `bookminder/__main__.py`, since in-process invocation never touches the entry point; the revert (`82d3990`) fixed the count at one — wiring can only be verified by running the wiring, and a second subprocess test re-tests behavior, slowly.

Fixtures enter through the front door. The `--user` parameter (`3103e4d`) doubles as the test seam: specs pass a synthetic `$HOME` whose directory tree replicates Apple's container layout path-for-path. `8e632f6` deleted the `monkeypatch` of `_books_plist` in its favor — "No more monkeypatching needed" — because patching a private name couples the spec to an implementation identifier *and bypasses the path-construction code you claim to test*. Each persona home (`never_opened_user`, `fresh_books_user`, `legacy_books_user`, `corrupted_db_user`, `test_reader`) encodes one environmental hypothesis, observed on a real machine rather than imagined — the fixture directory is itself a readable catalogue of the edge cases the product handles.

**Known deviation — the four-layer directory taxonomy is not the style.** The `specs/{unit,integration,acceptance,e2e}` split at HEAD, with its `__init__.py` layer contracts (`be394a0`…`0bf00d1`, `7dfe126`), was a one-day reorganization whose own post-mortem (`b84f56e`) judges it misconceived: *taxonomy is discovered, not imposed*; mockist tests ARE unit tests even when they exercise higher-level components, so the mock rules above do not map onto directories. The constitution never adopted the split, and the reorg forced mechanism-named describe blocks (`describe_list_recent_books_integration`) that violate §2.1. The intended shape is **concern-based**: one spec file per module or command (`cli_spec.py`, `apple_books/library_spec.py`), tests within it ranging naturally from helper to feature — which is exactly what the describe/it structure expresses. Until the repair (§5): follow the mock rules by test kind, do not extend the taxonomy, and never let a directory name leak into a `describe_`.

### 2.3 Assertion strength is calibrated to the test kind, and maximal for each

- **Pure functions: exact equality of the whole output.** `assert format(book) == "Test Book - Test Author (42%) • Sample ☁️"` (`2859fad`) — the whole output is the contract; substring checks let format regressions ship. One equality assertion subsumes several partials: `63785d5` deleted the dedicated indicator-ordering test as redundant once whole-string equality pinned order, content, and absence in a single expression. Where the property is genuinely relational, assert the relation: `query.index("WHERE") < query.index("ORDER BY")`.
- **Fixture-backed specs: exact sets of the known fixture census** — `assert sample_titles == expected_samples` (`22e1378`) — because the census is known, so anything weaker throws information away. Every loop assertion is preceded by a non-emptiness guard (`assert len(cloud_books) > 0`, `5730bf4`), because a `for` over an empty result asserts nothing, and returning nothing is the exact failure the test exists to catch.
- **Coordination specs: assert the call; configure nothing you don't assert.** `94e2af6` deletes an unused `return_value = []` because "the default MagicMock is sufficient" — unused stubbing implies the test cares about something it never checks; every line of setup must be load-bearing.
- **Error paths: assert which specific path fired.** `e65c8b6` distinguishes "No BKLibrary database found in:" from the generic message, and its body records the scar: an untracked fixture directory kept a generic raises-check green for the wrong reason for ~10 days. A test that can pass for the wrong reason is not a specification.
- **Diagnostics hand you the counterexample**: `f"Expected cloud book: {book['title']}"` — a failing spec should deliver the falsifying datum, not a boolean.
- **Never assert the absence of a problem.** `d8b5722` deletes a test asserting output ≠ three hardcoded titles: it "tested the absence of a problem rather than presence of correct behavior." Negative space is unbounded; a negative assertion constrains nothing. Corollary: never assert about data you never injected — a `not in` check against your own stub is unfalsifiable by construction (§4e).
- **Test-data realism is an intent signal.** Boundary specs use `B1`/`A1` — the data is a token, and realistic titles would falsely suggest content matters; fixture-backed specs use real titles because there the data *is* the point. 0-1-many sizing throughout.
- **Never depend on the developer's machine.** The first spec file read the author's actual library and cost three commits to make CI pass (`2d331e9`, `48ac46e`, `147f59f`): a spec that only passes on one machine specifies that machine.

### 2.4 Minimalism by deletion; defensiveness requires evidence

`e7a5fa4` is the constitutive example: a real bug (valid un-downloaded books silently excluded) was fixed by *deleting* the untested `os.path.exists` guard and the blanket `except Exception` — "removing implementation that lacked tests rather than adding tests retroactively" — reaching 100% coverage by subtraction. Untested code is unspecified behavior that can be wrong invisibly; retrofitting tests would only ratify it.

Coverage is a residue of good specs, never a target. The author named "Coverage-Driven Development" as an anti-pattern after living it: `ef953e1` reached 100% by pointing the DB path at `/dev/null` to hit an except branch, and `b73a618` deleted both the handler and its tests because a coverage number, not an acceptance criterion, had driven them. A deliberate drop ships without apology when the coverage moved to the right place (`764c512`).

Defensive code needs demonstrated evidence in the actual data — not "could this be NULL?" but "is it NULL in the data I have?", answered by querying the real database (`3cc7ddf`, `c851f95`). When speculation ships anyway, it is reverted wholesale (`6769f2f` → `1b07bd5`). What replaces a deleted handler is a loud assumption: `assert BKLIBRARY_DB_FILE is not None` — crash-visible rather than silently handled.

Errors, once a story demands them (`0dd8aa0`, driven by the user-environments story with one fixture per scenario): one domain exception, raised by the layer that knows *what* went wrong with the offending path in the message, translated once at the boundary by the layer that knows *how to say it*. The acceptance spec asserts the contract — message shown, no `Traceback` — without coupling to message text (`cb47cac`).

### 2.5 YAGNI operationalized as testability

The test for speculation is concrete: a capability the current fixtures cannot falsify is not a feature. `3d8bc5b` removes `sort_by` as "YAGNI and untestable with single book" — untestable-now *is* the YAGNI detector, and the coverage report doubles as one.

Invoking a respected pattern does not exempt a change from needing a demand: `771be67` consolidated path helpers into a `LibraryPaths` dataclass, explicitly citing GOOS; `bcb5223` reverted it one commit later, because a design improvement no current requirement needs is still speculative structure everyone must maintain. Extraction is welcome the moment a property needs cheap specification: `format_book_list` so output shaping is unit-testable without a subprocess (`74e6220`); `_build_books_query` split from I/O so the column census is assertable after a dropped column had broken sample detection (`10048e1` — but see §4 for the cost of how it was specified); path resolution moved CLI→library "where it belongs" (`5a50925`) so the CLI owns no domain knowledge.

The same collapse pressure applies to types: `RecentBook` → `BookWithProgress` → a single `Book` TypedDict with `NotRequired` optionals (`bd9ea30` → `8bb84fb` → `6391048`), because each extra type is another conversion and another place to forget a field — and `NotRequired` is what lets a test construct `Book(title=..., author=...)` and say nothing else, so the type system serves minimal test data instead of fighting it. `isinstance` over `cast` (`3fa89af`): a cast tells the checker to stop looking; a check tells the program what to do.

### 2.6 Discipline is a property of the sequence, not the snapshot

Every YOLO commit *individually* looks TDD-shaped — "test: add failing unit test…", "minimal implementation…" — while the causal order (story → acceptance RED → inward) was gone (§4). The vocabulary of the discipline survived; its causal structure did not. **You cannot verify this style commit-by-commit; it lives in the ordering.**

Practices that keep the sequence auditable:

- **Commit after RED, after GREEN, after REFACTOR.** The RED commit records that the falsifier existed before the implementation — the one claim a GREEN snapshot cannot prove. The rule is the author's own amendment (`5292033`) and his practice (`bd47589` RED → `875bed0` GREEN; `32d784b`); it is absent from CLAUDE.md today only as revert collateral (§5).
- **Commit labels must tell the truth.** GREEN and REFACTOR land separately because "refactor" is a machine-checkable claim — behavior preserved — and mislabeling destroys the log's audit property: you can no longer tell which commits could have changed behavior.
- **Coverage is moved before it is removed.** `5730bf4` adds library-level filter tests explicitly so coverage survives the CLI-spec conversion that follows (`ceb4a1d`); `30c2fe5` before `764c512`. The safety net moves before the trapeze, because the reverse order leaves a window in which the behavior is unspecified, and that window is where regressions are born.
- **Revert is a first-class move when provenance is wrong.** Speculative (`bcb5223`), duplicative (`7d3922a`), architecturally mistaken (`82d3990`), undisciplined (`447dc8c`): a change made for the wrong reason cannot be fixed by adding changes on top, because the defect is in how it came to exist.

### 2.7 The spec suite and the constitution are production artifacts

Changes to the tests, and to the rules that govern how tests get written, get the same discipline as product code. The project learned each of these at cost (§4, §5):

- **A commit touching specs is reviewed by diff, never by outcome.** "All tests pass, coverage unchanged" cannot validate a change to the tests — the measuring instrument is the thing being modified. A "pure move" claim is a claim to check: `e5c7074` reported a move and 100% coverage while deleting the only falsifiable sample-filter tests and substituting tautologies under the same names.
- **Same `it_` name, weaker assertion, is the most dangerous edit in the suite.** `pytest --spec` renders identically before and after; the living documentation keeps its sentence while the proof behind it evaporates. Re-implementing an existing `it_` requires the diff to show the assertion got stronger or equal.
- **The patch target is part of the specification.** `1d1fb34` patched the library's constant to prove the CLI owns no filter vocabulary; `fa0bc72` moved the patch to the CLI's imported name to get to green — same test name, same green, inverted meaning. When a GREEN commit edits a RED test, that edit is the thing to review.
- **Amend rules files by addressed diff, never wholesale rewrite.** The CLAUDE.md compression (`b5c84b2`) fused 248 line-granular lines into one hunk; the revert (`9bacc8a`) could then only undo everything, silently destroying the author's own later improvement (`5292033`) committed inside the rewritten region. The XML section tags exist precisely so a rule can be located, cited, and patched in isolation — keep them, and keep changes at the granularity you would want to revert at.
- **Friction in a discipline document is often its function.** The compression cut checklists and "Run & Verify RED" as cognitive load; the load was the mechanism — the deliberate pause before acting, in a project whose signature failure mode is acting before pausing. Optimize a rules file for behavior produced, not reading comfort.
- **Structural work needs an explicit falsifier too.** Before restructuring the suite or the rules, state what it would look like if the change made things worse, and check for that afterwards. The reorg had a goal ("clear separation of test types") with no test for whether it was achieved; its contract docstrings (`7dfe126`) ratified a nine-hour-old arrangement that had not yet survived a single feature.

---

## 3. The practice — play-by-play

### Walking skeleton, honest fake

`eca50d2` commits the acceptance test *and* a CLI of three hardcoded `click.echo` lines, labeled exactly what it is ("Minimal hardcoded implementation to establish walking skeleton") → `bd9ea30` pushes the fake behind `list_recent_books()` → `cffd595` replaces it with a real SQLite query. Fake data is a legitimate intermediate because the red acceptance test holds the target fixed while the implementation walks toward it. The fake is driven out through unit specs — never by a meta-test that detects it: `d8b5722` deletes exactly such a test and states the rule, "tolerate RED acceptance tests while building real implementation through unit tests." A red acceptance test on main means feature-in-progress by design (`cdd7619`: "Red acceptance test = impl. in progress").

### The cadence

GREEN, then a burst of one-idea refactor commits: `eca50d2` → `bd9ea30`/`8bb84fb`; `cffd595` → `e2653e3`/`ec91c40`/`087fb4b`; `16fd70c` → `24dc928`; `52a04c8` → `74e6220`. Refactoring is the bulk of the work (55 `refactor:` subjects against 17 `feat:` across the feature-building period), and each step is its own revertible unit. Refactor commits are named for the reason and carry the measurement that justifies them ("Reduced from 25 to 22 statements", `1d14ce2`; "Reduced 8 individual filter tests to 1", `9cac7d7`) — because a refactor that does not state what improved cannot be evaluated, and cannot be reverted with confidence later.

RED is committed, and the best RED commits explain themselves: `1d1fb34` commits a deliberately failing test whose body explains exactly why it fails and what property the failure nails. Scenarios not ready to run are committed skipped with their story docstring, so `--spec` shows the backlog while the suite stays green: `7060287` ships `--filter cloud` with the negation scenario as a skipped placeholder; `c785dc6` un-skips it — one behavior per increment, the remainder visible but inert.

### Revert-and-narrate

`7d3922a` carries the most instructive body in the repo: "We made a mistake - instead of refactoring the existing CLI tests in cli_spec.py to use mocks, we created duplicate tests in a new file. This wasn't the goal." Full revert; then the redo (`45256cd` → `552a9a3` → `c52fc26` → `a596b6c` → `ceb4a1d` → `94e2af6` → `ef05821`) converts one test per commit, each body explaining what improved — `45256cd` even labels itself an intermediate step and announces "the next commit will show a better approach." The revert-then-redo pair turns a mistake into a documented counterexample and exemplar; patching in place would have erased the lesson. The rule it bought: refactor specs in place, never a parallel suite, because two suites specifying one behavior will eventually disagree and then neither is authoritative.

### Exact-equality calibration, worked

`2859fad` builds the formatter spec by progressive complexity — no attributes → progress → sample → cloud → all — each an exact whole-string equality; the ordering property is asserted relationally when it is the open question, then subsumed once whole-string equality pins it (`63785d5` deletes the ordering test "as redundant"). Symmetry as a table: `9cac7d7` collapses eight near-identical filter tests into one doubly-parameterized matrix over (command × filter), because the CLI is a uniform passthrough and a table makes any asymmetry a visible anomaly instead of a buried inconsistency.

### The high-water mark: `1d1fb34`

```python
def it_validates_filter_values_and_shows_helpful_error(runner):
    with patch('bookminder.apple_books.library.SUPPORTED_FILTERS', {'foo', 'bar'}):
        result = runner.invoke(main, ['list', 'all', '--filter', 'baz'])
        assert result.exit_code == 1
        assert "Invalid filter: 'baz'" in result.output
        assert "foo" in result.output
        assert "bar" in result.output
```

The fictitious names are the whole point, and the commit body says so: "mock filter names (foo, bar) to prove that the CLI completely delegates filter knowledge to the library." Real filter names could pass even against a hardcoded CLI list; nonsense values make the property — *the CLI knows nothing about filters* — falsifiable. This is a design decision (the CLI owns no domain vocabulary) specified so that no implementation cleverness can fake it. That is what a London-school boundary spec is for. It is also the last clean RED before the boundary — and the first thing the lapse destroyed.

---

## 4. The lapse — anatomy, each failure named as the principle it violated

Boundary: `6f786cc` (2025-07-13, itself innocent — a pure comment strip). The lapse proper is `af3954c`…`c851f95` (Jul 13–14, "YOLO mode" per the retrospective), plus one silent casualty during the Jul 21 reorg.

**(a) The spec was mutated to fit the code** — *violates: the spec is the authority.* `1d1fb34`'s patch target *was* the spec: patching `bookminder.apple_books.library.SUPPORTED_FILTERS` asserts the CLI consults the library at call time. `fa0bc72` implemented via `from … import SUPPORTED_FILTERS` — an import-time copy the library patch cannot reach — and, inside the same GREEN commit whose body says "just enough to make the test green" and never mentions the test edit, re-pointed the patch to `bookminder.cli.SUPPORTED_FILTERS`. The test still passes and still *looks* like a delegation test, but now asserts only that the CLI compares against some set it holds locally. GREEN was achieved by weakening the claim, not satisfying it; an architectural decision was taken silently inside a two-character-path test edit. The honest fix existed and was cheaper: a late-bound `library.SUPPORTED_FILTERS` lookup. This is the single most consequential changed line in the lapse — and it is still how HEAD reads (§5.1).

**(b) A spec too weak to constrain, then triangulation without a pull** — *violates: assertions maximal per kind; labels tell the truth.* `af3954c` asserted only `isinstance(SUPPORTED_FILTERS, set)` and non-emptiness; `fa0bc72` satisfied it with `{"dummy"}`; `3d2bab6`, labeled `refactor:`, then changed the expectation to the real four values *and* the implementation in one commit. Behavior changed under a refactor label, and there was no moment at which a failing test drove the real values into existence. Contrast the walking skeleton: fake data was permitted there because a red acceptance test was pulling against it; here nothing pulled, so the fake became real by editorial fiat.

**(c) Acceptance-first abandoned** — *violates: outside-in; "done" is user-visible.* `5b42ae0` and `b246d7b` land library code plus unit tests in single commits, nothing showing the tests ever failed, and no acceptance test for a user-visible filter until `677a251` retrofitted them the next day, admitting they "should have been created before implementation." Without the outside-in RED there is no executable statement of user-visible done, so "done" regressed to "code exists."

**(d) Non-emptiness guards dropped** — *violates: §2.3.* `5b42ae0`'s `it_filters_by_sample_status` loops with no guard — green if the filter returns nothing, which is the exact failure it exists to detect. Its guarded sibling from three weeks earlier sits in the same file.

**(e) Fake-strength assertions** — *violates: never assert what you never injected.* `b246d7b` asserts `"Sample Book" not in result.output` while the mock returns only a regular book — unfalsifiable by construction. The retrofit (`677a251`) was worse: `if output and "No books" not in output:` wrapped the assertions, letting the test pass while asserting nothing. A test that cannot fail is not a specification; it is a comment with a runtime cost.

**(f) Evidence-free defensiveness returned** — *violates: §2.4.* `b246d7b` shipped `(ZISSAMPLE != 1 OR ZISSAMPLE IS NULL)` with no NULL in any fixture or observed data — `e7a5fa4`'s failure recommitted verbatim in SQL. `c851f95` deleted it after checking the fixtures, the same cure as the first time.

**(g) Living documentation commandeered** — *violates: describe names the story.* `ef5474b` displaced `describe_bookminder_list_recent_command`'s content to `…_with_fixtures` and reused the vacated name for filter validation: the `--spec` output for a completed story now described a different feature, corrupting the requirements document itself.

**(h) Symmetric features, divergent styles** — *violates: the table principle (§3).* `!cloud` specified as passthrough call-assertion, `!sample` as mock-return-plus-output — two idioms for one property, so a reader cannot tell whether the difference means something. Repaired by `9cac7d7`'s parameterized matrix ("Consistency Trumps Cleverness", per the retrospective).

**The earlier crack.** `10048e1`, two commits before the boundary, specs `_build_books_query` by asserting on the SQL string (`"ZTITLE" in query`, `WHERE` before `ORDER BY`). The motivation is real — a dropped column had genuinely broken sample detection, and the commit says the spec "prevents accidental removal of columns" — but by the project's own `d8b5722` standard this couples the spec to implementation text when a behavioral alternative (a fixture book whose flags depend on the column) was available. The armor is sincere; the coupling is the first slip, and it predates the official boundary.

**Why it happened, per the project's own diagnosis:** optimizing for finishing over demonstrating; architectural decisions taken silently inside test edits; "didn't fully appreciate BookMinder as a benchmark for process, not just a utility." And the structural lesson: each YOLO commit individually wears TDD vocabulary, which is precisely why the sequence property (§2.6) is the only level at which the discipline can be verified at all.

**The repair, its silent casualty, and its limit.** The patch-forward repair (`677a251` retrospective + retrofit, `9cac7d7` consistency, `c851f95` evidence-based deletion) was followed by the four-layer reorg — and inside it, a casualty visible only at diff level: **`e5c7074`**, under the message "extract acceptance tests from cli_spec to acceptance/cli_spec … Moved all mocked CLI tests", *deleted* the two fixture-based subprocess sample-filter tests — including `it_excludes_samples_from_recent_books`, the only guarded, genuinely falsifiable end-to-end `!sample` test — and created newly-written mock-based versions under `describe_bookminder_acceptance` carrying the *same `it_` names*. The `--spec` output reads identically; the falsifiability is gone. A "pure move" whose diff was never diffed. (`677a251`'s restoration tests were fixture-based; `e5c7074` silently replaced them with mock versions.)

**The meta-artifact lapses.** Two further episodes, distinct from YOLO, motivate §2.7. The spec-tree reorganization (2025-07-21, `be394a0`…`0bf00d1`) imposed the four-layer taxonomy in a day, ratified it with contract docstrings the contents did not meet (`7dfe126`), and carried `e5c7074` inside it; the project's post-mortem (`b84f56e`) rules the conception wrong, and the attempted correction (PR #18, `447dc8c`…`55f2b4e`) collapsed trying to hold two baselines apart and was abandoned. The CLAUDE.md compression (`b5c84b2`, 2025-07-24 → reverted `9bacc8a`, 2025-07-31) deleted everything procedural — checklists, "Run & Verify RED", "no implementation without tests" — while keeping everything declarative, having optimized the rules file for reader burden instead of behavior produced; the wholesale revert then destroyed the author's own commit-after-RED improvement (`5292033`) along with it. Shared shape: a meta-artifact optimized against a proxy (taxonomic tidiness; reading comfort) at the expense of falsifiability, passing every existing check because the thing changed *was* the checking apparatus.

The author judged patch-forward insufficient for the YOLO code regardless: the unmerged `447dc8c` (PR #18) performs a semantic revert of the entire YOLO output back to `6f786cc` — removing `SUPPORTED_FILTERS`, `validate_filter`, and sample filtering — and TODO.md still lists the three affected stories as needing "proper ATDD reimplementation." The principle this states, more clearly than anything in CLAUDE.md: **code whose provenance violates the process is not repaired by adding tests to it.** A retrofitted test is written by someone who has already read the implementation; it can only ratify. The honest repair is delete and re-derive from a failing test — which the restoration branch then demonstrates with explicit `RED:`/`GREEN:` commits (`32d784b`, `bd47589` → `875bed0`, `5125e9c` → `4bae79b`, `5f8d330`). One deviation inside the cure itself, for honesty: `875bed0`'s GREEN is wider than its RED (it added `unread` and `in-progress` while only `finished` was failing; `5f8d330` notes the later test "passes immediately") — the over-reach recurring, mildly, in the commit series written to demonstrate its absence.

---

## 5. Known deviations at HEAD — the repair backlog

Every item verified in the working tree. Ordered by how much of the style's meaning each one holds hostage.

1. **The delegation property is still unspecified.** `specs/acceptance/cli_spec.py:67` patches `bookminder.cli.SUPPORTED_FILTERS`, and `cli.py:10` still from-imports the constant — `fa0bc72`'s inversion is live. Fix: late-bind (`library.SUPPORTED_FILTERS` at call sites), re-point the patch to the library, watch it fail, go green. This restores the actual claim `1d1fb34` existed to prove.
2. **Sample filtering has had no non-vacuous end-to-end spec since `e5c7074`.** `describe_bookminder_acceptance` (`acceptance/cli_spec.py:98`) asserts against its own stubs (`"Sample" not in` a mock that never contained one), with explanatory docstrings standing in for the assertions that no longer speak. Re-derive from `filter-by-sample-flag.yaml` against real fixture titles.
3. **The four-layer taxonomy stands as if decided.** It is an unadopted experiment (§2.2): the constitution has never described the spec tree, the `__init__.py` contracts claim what the contents do not meet, and the post-mortem prescribing a return to concern-based layout (`b84f56e`) is unmerged. Decide: fold back to concern-based files or genuinely adopt and fix the taxonomy; until then, do not extend it.
4. **The commit-after-RED rule is missing from the constitution.** CLAUDE.md self-contradicts: `<tdd_discipline>` mandates verifying RED while `<git_workflow>` prescribes commits only after GREEN and REFACTOR — pure revert collateral from `9bacc8a` destroying `5292033`. Restore the rule; sync AGENTS.md and GEMINI.md, which drifted through both the rewrite and the revert.
5. **Vacuous integration loops**: `integration/library_containers_spec.py:147–161` (`sample`/`!sample`) have no non-emptiness guards; their cloud siblings at `:131`/`:140` show the correct shape.
6. **Near-duplicate validation specs** at `acceptance/cli_spec.py:59`/`:66` (`ef5474b` re-covered what `1d1fb34` already had): once #1 is repaired, keep the delegation spec, delete the other.
7. **Describe-naming violations**: `describe_bookminder_acceptance` names a layer, not a command; `describe_bookminder_integration` lives in `e2e/` (`cli_wiring_spec.py:38`); mechanism-suffixed `describe_list_recent_books_integration` (`:117`) and `describe_list_all_books_integration` (`:164`) were forced by a file-merge collision, not chosen; duplicate `it_handles_fresh_apple_books_user_with_no_books` (`:31`/`:70`) and duplicate `it_excludes_samples_with_not_sample_filter` (`:154`/`:200`) in `library_containers_spec.py` — the fix existed in unmerged `55f2b4e`.
8. **Error-contract asymmetry, unspecified**: `list_all_books` (`library.py:171`) does not wrap `sqlite3.Error` in `BookminderError` while `list_recent_books` (`:167`) does — lapse-era divergence with no spec demanding parity. Decide the contract, spec it, then implement. Related and unexamined: `BookminderError` → exit 0 at the CLI boundary while validation errors exit 1; no commit explains the asymmetry.
9. **The status ledger disagrees with itself.** TODO.md lists `validate-filter-values` and `filter-by-sample-flag` under Completed Features *and* as needing "proper ATDD reimplementation"; both story cards read `status: done`; PR #18 (`447dc8c`), which corrected them to `backlog`, is unmerged. By this project's own standard the features working is irrelevant: a feature without process provenance is, by definition, not done.
10. **Hygiene**: dead `TEST_HOME` at `specs/unit/library_spec.py:9` pointing into a nonexistent `specs/unit/fixtures/` (harmless only because `_get_user_path` string-round-trips it); `# This is a test comment to trigger pre-commit hooks.` at `cli.py:48`; `e2e/cli_wiring_spec.py:40` docstring says "Integration test:" on an implemented test; `README.md:98` documents `pytest specs/apple_books/library_spec.py --spec`, a path deleted in the reorg.
11. **Dead plist API**: `list_books`/`find_book_by_title` are integration-tested with zero `cli.py` callers — deliberate seed of the EPUB path, or unreaped growth. Decide, then spec or delete.

---

## 6. Unsettled — no stated rule exists

- **Builtin shadowing** is tolerated inconsistently: `format` and `filter` shadow builtins throughout (`63785d5` gives three reasons for the `format` rename, none addressing the shadow), yet `74e6220` renamed the `list` command group to `list_cmd` to avoid exactly this clash. If there is a rule ("shadow when module context disambiguates"), it has never been stated. Ask before assuming either way.
- **Given-supplying docstrings on implemented tests**: `it_handles_user_who_never_opened_apple_books` keeps `"""User has iBooksX container but no BKAgentService container."""` (`30c2fe5`, still at HEAD) — a precondition no assertion can state. The stated rule (§2.1) says delete on implementation; the survival may be tolerated decay or an unratified exception. Ask before adding new ones.
