# BookMinder BDD/TDD Style — Reconstructed from Git History

Method: `git log --reverse -- '*.py'` from `9e7bd38` (2025-04-13, first implementation commit) through `0bf00d1` (2025-07-21, last product-code commit on main), plus the unmerged restoration commits of 2025-07-26. Every rule below is stated as *X because Y*, with the motivation derived from what the commit actually did — preferring the author's own stated reason where a commit body gives one, and marking the cases where no motivation is recoverable.

---

## 0. The organising idea

Specs are the requirement; code is the debt incurred to satisfy it. Every rule downstream follows from that asymmetry: a spec earns its place by *constraining* the implementation, and an implementation earns its place by being *demanded* by a spec. When the two conflict, the history shows the implementation losing — code is deleted (`e7a5fa4`, `b73a618`, `aafeb0d`, `3d8bc5b`, `d4d0dd1`, `c851f95`), never grandfathered in behind a retroactive test.

The corollary that the history teaches hardest: a test written *to cover existing code* is not a spec, it is an alibi. `b73a618` deletes the two error-path tests added in the two immediately preceding commits (`3cc7ddf` "*Improve test coverage from 95% to 97%*", `ef953e1` "*Achieve 100% test coverage*", the latter pointing `BKLIBRARY_DB_FILE` at `/dev/null` to reach an `except sqlite3.Error` branch) in the same breath as the code they covered, because both were driven by a coverage number rather than by an acceptance criterion. The author later named this anti-pattern "Coverage-Driven Development." Coverage is a *residue* of good specs here, not a target — which is why `764c512` ships a deliberate coverage *drop* ("Coverage drops to 94% but edge cases still tested at library level") without apology.

---

## 1. Spec style rules

### 1.1 Naming: the spec file reads as one sentence, story → describe → it

`describe_` names the feature or the unit under test; `it_` completes a sentence about observable behaviour. `describe_bookminder_list_with_filter()` / `it_filters_by_cloud_status()` (`7060287`) traces directly back to `stories/discover/filter-by-cloud-status.yaml`. **Because** `pytest --spec` output is the project's living documentation and the only artefact a reader consults to learn what the system does; if the sentence does not read naturally, the documentation is broken even when the test passes. This is also why the story card, the `describe_`, and the `it_` are kept in lockstep — traceability is checked by reading, not by tooling.

Granularity: one `describe_` per public function or per CLI feature, one `it_` per behaviour. `3d8bc5b` explicitly reorganised a single `describe_book_library()` with a nested `describe_when_listing_books()` into flat `describe_list_books()` / `describe_find_book_by_title()`. **Because** nesting a context that adds no information ("when listing books" inside "book library") produces `--spec` output that restates itself; the describe block should name the thing whose behaviour is being specified, and nothing else.

### 1.2 No comments in specs, ever; docstrings only where they are load-bearing

`e391026` deleted every explanatory comment from the very first spec file (`# This test should verify we can access real Apple Books data`, `# Verify books have required metadata`). `6f786cc` did the same again fourteen months of commits later (`assert result.exit_code == 0  # No crash` → `assert result.exit_code == 0`). **Because** a comment that restates the assertion is a second, unverified copy of the specification which can drift; the test name and the assertion together are the specification, and anything else is duplication that ages.

Docstrings survive in exactly three situations, and the history shows each being deliberately established:

- **Pending/skipped tests keep a docstring**, because the docstring *is* the unimplemented spec. `7060287`: `@pytest.mark.skip(reason="Implementation pending")` over `it_shows_only_local_books_when_flag_is_local()` whose body is `pass` and whose docstring carries the `when:` / `then:` clauses. `c785dc6` then deletes the docstring at the same moment it deletes the skip marker and fills in the body — the prose is replaced by executable prose. The skip marker plus docstring is how a story's remaining scenarios stay visible in `--spec` output as a to-do list rather than being forgotten.
- **A test whose assertion cannot state the precondition** keeps a one-line docstring. `30c2fe5`: `it_handles_user_who_never_opened_apple_books()` carries `"""User has iBooksX container but no BKAgentService container."""` — the fixture's meaning is invisible at the call site (`FIXTURE_PATH / "never_opened_user"`), so the docstring supplies the *given*.
- **Layer `__init__.py` files** carry a contract docstring (`7dfe126`). Those are the only docstrings in `specs/` whose audience is the author of the *next* test.

The Gherkin experiment and its reversal is instructive: Gemini expanded the acceptance docstrings into full `Feature: / Scenario: / When / Then` blocks (`250230d`), the author restored the terse form (`53e570a`), and `48596a6` removed the docstring entirely with the reason "*its purpose is now served by the YAML story card*". **The principle: a scenario belongs in exactly one place.** Once `stories/*.yaml` became the requirement of record, duplicating it in a docstring created two artefacts to keep in sync — and the one that could silently rot was the docstring.

### 1.3 Assertions must be strong enough that an empty or wrong result fails

The house pattern is `assert <predicate>, f"<what was expected>: {actual}"` — a message that names the expectation, not the mechanics. Beyond that, three specific strength rules are visible:

- **Any loop-over-results assertion is preceded by a non-emptiness guard.** `5730bf4`: `assert len(cloud_books) > 0, "Expected to find cloud books"` *before* `for book in cloud_books: assert book.get("is_cloud") is True`. **Because** a `for` loop over an empty list asserts nothing; without the guard the test passes when the feature returns nothing at all, which is the exact failure the test exists to detect. (§4 shows this rule being broken during the lapse.)
- **Assert the specific failure, not the failure category.** `e65c8b6` strengthened `it_handles_user_who_never_opened_apple_books` from `assert "Apple Books database not found" in error_msg` to additionally require `"No BKLibrary database found in:"` and `"iBooksX/Data/Documents/BKLibrary"`. Its commit body states the motive exactly: the fixture had been missing from git for ~10 days and the test passed anyway, because a *missing directory* raised the same generic message as the condition under test. **Because** a test that cannot distinguish the intended failure path from an accidental one is green for the wrong reason, which is worse than red.
- **Assert relationships, not just presence, where ordering is the requirement.** `it_ensures_sample_indicator_appears_before_cloud`: `assert result.index("• Sample") < result.index("☁️")` (`2859fad`), and `it_applies_where_clause_and_limit`: `assert query.index("WHERE") < query.index("ORDER BY")` (`10048e1`). **Because** substring-presence assertions are satisfied by any arrangement; when order *is* the behaviour, order must be the assertion. The follow-up refines the rule: `63785d5` deleted the dedicated ordering test "*as redundant*", since `it_formats_book_with_all_attributes` already asserts the whole string by equality — `assert format(book) == "Test Book - Test Author (42%) • Sample ☁️"` — which subsumes it. **Prefer one exact-equality assertion over several partial ones**; equality pins order, content and absence in a single expression, and a partial assertion kept alongside it is a weaker duplicate.

The counter-example the author deleted: `d8b5722` removes `it_attempts_to_read_from_bklibrary_database`, whose assertion was `actual_titles != hardcoded_titles`. The commit body is the fullest statement of the assertion-strength principle in the repository — it "*tested the absence of a problem rather than presence of correct behavior*", was "*fragile and could fail if user's library matched hardcoded titles*", and existed only "*to retrofit real implementation after acceptance test was prematurely made to pass with fake data*". **The principle: specify what must be true, never what must not be a particular wrong thing** — the negative space is unbounded, so a negative assertion constrains nothing.

### 1.4 Fixture strategy is dictated by the layer, not by preference

This is the sharpest and best-motivated rule in the history, and it is definitional rather than stylistic.

**Integration specs use real fixtures because the collaborator being integrated against is the subject.** `specs/integration/library_containers_spec.py` runs `list_recent_books(FIXTURE_PATH / "corrupted_db_user")` against a genuinely zero-byte SQLite file. Mocking `sqlite3` here would test the author's beliefs *about* SQLite; the whole point of the test is that those beliefs may be wrong. The fixture tree — `test_reader`, `fresh_books_user`, `legacy_books_user`, `never_opened_user`, `corrupted_db_user` — was built from real-machine observation of five distinct Apple Books installation states (`3103e4d`) precisely so that the states are *found*, not *imagined*.

**Unit specs stub data and mock roles.** Two distinct techniques, each with its own reason:

- *Data stubs* for pure functions: `row_stub(**overrides)` (`e72007f`) and `_book(**kwargs)` (`93c2e55`) are keyword-defaulted builders that let each test name only the fields it is about. `_row_to_book(row_stub(ZSTATE=6, ZISSAMPLE=0))` reads as a truth-table row. **Because** a pure mapping function has no collaborators to mock; what it needs is minimal, legible input, and irrelevant fields present in the test are noise that hides the variable under test. `93c2e55` and `a596b6c` both exist purely to strip fields (`path=""`, `updated=None`, `reading_progress_percentage=50`) that the test in question did not depend on.
- *Mocks* only at architectural boundaries the project owns. `cb47cac` patches `bookminder.cli.list_recent_books` to raise `BookminderError` and asserts the CLI shows the message and no `Traceback`; its body says it "*verifies behavior at the architectural boundary rather than testing specific error messages*". `552a9a3` patches both `list_recent_books` and `format` and asserts *the calls*: `mock_list_recent.assert_called_once_with(user=None, filter=None)` and `mock_format.call_args_list == [((book1,),), ((book2,),)]`, with the body citing "*GOOS principles of testing at architectural boundaries*". **Because** the CLI's actual responsibility is coordination — parse options, call the right library function, hand each result to the formatter, in order — and a test that asserts on formatted output strings is testing the formatter through the CLI, coupling two layers and forcing both to change together.
- The corollary at `94e2af6`: when a test asserts only that a call was made, **do not configure the mock's return value**. The default `MagicMock` suffices, and a stubbed return value would falsely imply the test cares about it.

**E2E: exactly one subprocess test, and it must stay a subprocess test.** `1880103` converted the whole CLI spec to `CliRunner` for speed and coverage fidelity; `82d3990` reverted it. The reason is structural: `CliRunner` invokes `main` in-process and therefore never exercises `bookminder/__main__.py`, the real entry point. `d30b9ee` and `7dfe126` then made this a rule in prose — "*Be minimal - we only need ONE test to verify wiring*". **Because** wiring can only be verified by actually running the wiring; and because a second subprocess test buys nothing while costing seconds on every run, one is both necessary and sufficient.

**Prefer real structure over patching whenever the structure is cheap to build.** `8e632f6` deleted an autouse `monkeypatch` fixture and replaced it with a fixture directory laid out in the true Apple container shape: "*No more monkeypatching needed - the tests are cleaner and more realistic.*" **Because** patching a module attribute asserts that the production code reads *that* attribute; it silently stops testing path construction, which was itself a source of bugs. `9a6319f` documents the intermediate discomfort — tests calling `list_books(Path("/dummy"))` with a comment `# Path is ignored by mock` — and `8e632f6` removes the need for the apology entirely.

### 1.5 Spec code is production code and is refactored like it

`93c2e55` (extract `_book` builder), `198e515` (inline single-use intermediates: `assert format(_book()) == "Test Book - Test Author"`), `c52fc26` (combine `with patch(...) as a, patch(...) as b`), `a596b6c` (introduce a `runner` pytest fixture, with the reasoning that two current call sites plus four planned ones make it worthwhile), `b4e376d` (move the repeated `assert result.returncode == 0` into `_run_cli_with_user` so it is asserted once and every caller inherits it), `9cac7d7` (collapse eight near-identical filter tests into one `@pytest.mark.parametrize` matrix over command × filter). **Because** duplication in specs is the same liability as duplication in code, with an extra cost: a reader scanning `--spec` output for the system's behaviour has to filter noise.

But refactoring in specs is bounded by a rule the history had to learn twice: **refactor tests in place; never add a parallel suite.** `65b88f7` created `specs/cli_unit_spec.py` alongside the existing `specs/cli_spec.py`; `7d3922a` reverted it with the clearest self-diagnosis in the repository — "*We made a mistake - instead of refactoring the existing CLI tests in cli_spec.py to use mocks, we created duplicate tests in a new file. This wasn't the goal.*" The redo (`45256cd` → `552a9a3` → `c52fc26` → `a596b6c` → `ceb4a1d` → `94e2af6` → `ef05821`) converts **one test per commit**. **Because** two suites specifying the same behaviour will disagree eventually, and when they do neither is authoritative; and because converting one test at a time keeps every intermediate commit green and reviewable.

### 1.6 Coverage may only be moved, never dropped on the floor

`5730bf4` adds library-level unit tests for the cloud filter *before* `ceb4a1d` converts the CLI filter tests to pure passthrough assertions, with the stated reason: "*The CLI subprocess tests were previously the only tests exercising the cloud filter logic in the library.*" Likewise `30c2fe5` creates the library integration edge-case tests *before* `764c512` removes them from the CLI spec. **Because** a refactor that relocates a test must first re-establish the behaviour's coverage at its new home; doing it in the other order leaves a window in which the behaviour is unspecified, and windows like that are where regressions are born.

### 1.7 The four layers, and what each is allowed to assume (`be394a0`…`0bf00d1`, contracts in `7dfe126`)

- `specs/unit/` — pure logic, no filesystem/DB/network, stubs and mocks only, milliseconds.
- `specs/integration/` — real fixtures, real SQLite, real plist; edge cases with real resources (missing files, corrupted data).
- `specs/acceptance/` — Click's `CliRunner`, library functions mocked, verifies parameter passing, output shaping and error messages.
- `specs/e2e/` — one `subprocess` test verifying full-stack wiring.

The naming carries information too: `0d4529b` renamed `library_integration_spec.py` to `library_containers_spec.py` because "*integration*" says how the test runs while "*containers*" says what it is about — Apple's `Library/Containers/com.apple.*` filesystem shape. **Because** a test file name should tell you what would break if it failed.

---

## 2. Implementation style qualities

### 2.1 Minimalism is enforced by deletion, and deletion is a debugging technique

`e7a5fa4` is the founding example: a real bug (valid books missing from `list_books` on machines where iCloud had not downloaded them) was fixed by *deleting* the `if not path or not os.path.exists(path): continue` guard and the surrounding `except Exception`. Its body: "*Achieves 100% test coverage by following 'code is a liability' principle - removing implementation that lacked tests rather than adding tests retroactively.*" **Because** untested code is unspecified code, and unspecified code is where behaviour nobody asked for hides; when it misbehaves the cheapest correct fix is to establish that nobody asked for it.

The pattern repeats with the same reasoning each time: `3d8bc5b` removes `sort_by` (YAGNI, and "*untestable with single book*" — a feature that cannot be specified with the available fixtures should not exist); `3cc7ddf` removes `None`-handling in `_apple_timestamp_to_datetime` after checking the real database ("*Verified with real DB that ZLASTOPENDATE is never NULL when progress > 0*"); `b73a618` removes the missing-DB and `sqlite3.Error` handlers with "*Remove defensive code not driven by acceptance tests*"; `aafeb0d` removes a `Books.plist` existence check and a `FileNotFoundError` handler that was "*dead code since sqlite3.connect raises OperationalError not FileNotFoundError*"; `d4d0dd1` removes a `_books_plist(user_home)` call that did nothing, found by `git blame` and diagnosed as "*likely copied from other functions without understanding its purpose*"; `c851f95` removes `OR ZISSAMPLE IS NULL` because "*The defensive programming was added without evidence of actual NULL values in the data.*"

**The unifying principle: defensiveness requires evidence.** Not "could this be NULL?" but "is it NULL in the data I have?" The project answers such questions by querying the real database, not by reasoning about what SQLite permits.

### 2.2 Speculative structure is reverted even when it is good design

`771be67` consolidated five path helper functions into a `LibraryPaths` dataclass with a `for_user()` factory, explicitly invoking "*the GOOS pattern*", and updated the tests to subclass it for mocking. `bcb5223` reverted it wholesale, one commit later. `6769f2f` added `PermissionError` handling with a "*try sudo*" hint discovered during real macOS testing; `1b07bd5` reverted it. **Because** neither was demanded by a failing acceptance test. The `LibraryPaths` revert is the more striking of the two — it teaches that invoking a respected pattern does not exempt a change from the rule; a design improvement that no current requirement needs is still speculative, and speculative structure has to be maintained by everyone who reads the file afterwards. Extraction is welcome once a *second* caller or a *testability need* makes it concrete (`24dc928` `_query_books`, `74e6220` `format_book_list`, `10048e1` `_build_books_query`).

### 2.3 Extract for testability, and let the seam fall where the layers already are

`74e6220` pulls `format_book_list` out of the command body specifically so the output shaping can be unit-tested without a subprocess. `5a50925` moves `_get_user_path` from `cli.py` down into `library.py`: "*This change enables better unit testing by moving path resolution logic to the library where it belongs, and simplifies the CLI layer to just pass parameters.*" `10048e1` splits `_query_books` into a pure `_build_books_query` (string construction) and an I/O half, so that a unit test can assert the SELECT column list — direct regression armour after `ZISSAMPLE` had been dropped from a query and broken sample detection. **Because** a function that mixes I/O with logic can only be tested through its I/O, which makes its logic expensive to specify; and the cost of that expense is paid every time the logic changes.

### 2.4 Types: one shape, optional fields, no parallel hierarchies

The type churn of 2025-06-23 is a compressed lesson: `bd9ea30` adds `RecentBook`; `8bb84fb` replaces it with `BookWithProgress(Book, total=False)` calling `RecentBook` a "*YAGNI violation*"; `6391048` deletes that too in favour of a single `Book` TypedDict with `progress: NotRequired[float]`, "*Simpler, cleaner design with no extra types*". The final `Book` (`title`, `author`, plus `NotRequired` `path`, `updated`, `reading_progress_percentage`, `is_cloud`, `is_sample`) is the shape every layer speaks. **Because** each additional type is another conversion, another place a field can be forgotten, and another thing to name; `NotRequired` expresses "sometimes absent" without splitting the vocabulary. Note the follow-on effect in `93c2e55`: because the fields are `NotRequired`, a test may construct `Book(title=..., author=...)` and say nothing about progress — the type system supports minimal test data rather than forcing ceremony.

`3fa89af` moved from `dict[str, Any]` to `TypedDict` and from `os.path` to `pathlib`, and in doing so removed a `cast()` by restoring a real `isinstance` check — **because** a cast tells the type checker to stop looking, while a check tells the program what to do; the only place `Any` survives is `_read_books_plist`'s return, at the genuine boundary with `plistlib`.

Typing is asymmetric by configuration: `pyproject.toml` sets `disallow_untyped_defs = true` for production while `[tool.mypy] exclude` lists `specs/`, and ruff's docstring rules `D100`–`D104` are disabled for `specs/**/*.py`. **Because** production types are a contract enforced across module boundaries, while a spec has exactly one caller (pytest) and one reader; annotating `def it_formats_book_with_progress() -> None:` adds ceremony that protects nothing and dilutes the sentence.

### 2.5 Docstrings in production: one line, on public things, only when the name is not enough

`3d8bc5b` collapsed NumPy-style `Args:`/`Returns:` blocks into one-liners and deleted the docstring from private `_read_books_plist` entirely. `f3d57b3` removed another redundant one. What survives is `"""List recently read books with progress from BKLibrary database."""` — a sentence that adds the *source* of the data, which the name does not carry. **Because** a docstring restating a well-chosen name is duplication with the same drift risk as a comment; a docstring earns its place only by supplying context the signature cannot.

The comments that do survive in `library.py` are the ones that record a *fact about the world*: `path="",  # Path requires Books.plist correlation with ZASSETID`. **Because** that is knowledge about Apple's schema that no amount of good naming would convey, and losing it would cost another reverse-engineering session.

### 2.6 Errors: one domain exception, raised at the layer that knows, translated once at the boundary

`BookminderError` lives in `bookminder/__init__.py` (`0dd8aa0`); `library.py` raises it with a message that includes both the offending path and the user-facing sentence; `cli.py` catches exactly `BookminderError` and echoes `f"{e}"` with exit code 0. `53e570a` removed the `f"Error reading Apple Books: {e.args[0]}"` prefixing because it produced doubled text. **Because** the library knows *what* went wrong and the CLI knows *how to say it*; a single exception type at the seam means the CLI's error handling is one `except` clause rather than a growing taxonomy, and the acceptance test at that seam (`cb47cac`) can then assert the contract — message shown, no `Traceback` — without knowing any specific error.

### 2.7 Structural minimalism in the package

`1875234` emptied both `__init__.py` files that `e391026` had just given docstrings, "*Empty `__init__.py` files per YAGNI principles*". `conftest.py` is six lines and does one thing (`sys.path` insertion). `pytest.ini` is four lines of discovery config (`python_files = *_spec.py`, `python_functions = it_*`, `python_classes = describe_*`). **Because** every file is a thing to open, understand, and keep true; files that exist only to satisfy a convention should contain nothing beyond what the convention requires.

---

## 3. Observed TDD cadence

### 3.1 Outside-in, with a red acceptance test tolerated for as long as it takes

The canonical run is `eca50d2` → `bd9ea30` → `8bb84fb`/`6391048` → `cffd595` → `b73a618`/`d8b5722`. `eca50d2` writes the acceptance test *and* a CLI that `click.echo`s three hard-coded book lines — a walking skeleton, honest about itself ("*Minimal hardcoded implementation to establish walking skeleton*"). `bd9ea30` pushes the hard-coded data down behind `list_recent_books()`. `cffd595` replaces it with a real SQLite query. Fake data is a legitimate intermediate state **because** the acceptance test's job is to hold the target fixed while the implementation walks toward it; what matters is that the walk continues.

The rule for how to keep the walk honest is the one `d8b5722` states after deleting the meta-test that policed it: "*The proper approach is to tolerate RED acceptance tests while building real implementation through unit tests.*" **Because** the alternative — inventing a test whose only purpose is to fail while the fake data remains — creates a test with no post-conditions worth keeping, which then has to be deleted as debt.

### 3.2 Commit rhythm

Two commits per cycle is the documented norm (GREEN, then REFACTOR), and the observed history matches it with one refinement: once the work became feature-sized rather than skeleton-sized, RED acquired its own commit. `1d1fb34` — "*test: add failing test for filter validation with library delegation … The test currently fails because SUPPORTED_FILTERS doesn't exist in the library module yet*" — is a commit containing a red test and nothing else. The unmerged restoration branch of 2025-07-26 formalises it into commit-subject prefixes: `bd47589` **RED:** → `875bed0` **GREEN:** → `5125e9c` **RED:** → `4bae79b` **GREEN:** → `5f8d330` **GREEN:**.

Refactor commits are numerous, tiny, and *named for the reason*: `refactor: inline test assertions for conciseness` (`198e515`), `refactor: remove redundant docstring` (`f3d57b3`), `refactor: extract common Apple container path prefix` (`d8f1da8`), `refactor: remove dead _books_plist call from _query_books` (`d4d0dd1`). Commit bodies routinely carry the measurement that justifies the change — "*Reduced code from 27 to 19 statements*" (`90c7109`), "*Reduced from 25 to 22 statements*" (`1d14ce2`), "*Reduced 8 individual filter tests to 1 parameterized test*" (`9cac7d7`), "*Coverage improved from 95% to 97%*" (`24dc928`). **Because** a refactor commit that does not state what improved cannot be evaluated, and cannot be reverted with confidence later.

### 3.3 Revert is a first-class move

`1b07bd5`, `bcb5223`, `82d3990`, `7d3922a`, `250230d`, `447dc8c`. The author reverts rather than patches forward when the *provenance* of a change is wrong — speculative (`bcb5223`), duplicative (`7d3922a`), architecturally mistaken (`82d3990`), or produced without discipline (`447dc8c`). **Because** a change made for the wrong reason cannot be fixed by adding more changes on top; the defect is in how it came to exist, so the repair is to remove it and redo the step properly. Note that `82d3990` is not thrash — it trades speed and coverage fidelity for keeping `__main__.py` genuinely exercised, and that trade was subsequently codified into the four-layer split.

### 3.4 Feature increments are one behaviour wide

`7060287` ships `--flag cloud` with the negation case present as a skipped, docstring-carrying placeholder; `c785dc6` un-skips and implements it. `16fd70c` ships `list all` with `it_filters_by_sample_status` and `it_excludes_samples_when_filter_is_not_sample` both skipped; `52a04c8` un-skips the first. **Because** a skipped scenario with its `then:` clauses intact is simultaneously a to-do item, a design commitment, and a visible line of `--spec` output — it keeps the remainder of the story present without letting untested code in to serve it.

---

## 4. The gold standard, and exactly how the post-`6f786cc` period deviated

TODO.md records the boundary: "*After commit 6f786cc, ATDD practice wasn't followed properly … Manually restore proper ATDD discipline to re-establish gold standard of specs and implementation.*"

### 4.1 What "gold standard" means concretely

The best-executed stretch is 2025-07-06 → 2025-07-13 (`24dc928` … `1d1fb34`): behaviour decomposed to one `it_` per commit; each behaviour placed at the layer that owns it, and moved there *before* being removed from the layer that borrowed it (`5730bf4` before `ceb4a1d`, `30c2fe5` before `764c512`); mocks used only at the CLI↔library seam and only to assert coordination (`552a9a3`); pure functions extracted so their logic can be specified cheaply (`74e6220`, `10048e1`); every added guard traced to a fixture that exhibits the condition; every removed guard justified by a check against real data.

Its high-water mark is `1d1fb34`, which deserves quoting in full because it is the most sophisticated spec in the repository:

```python
def it_validates_filter_values_and_shows_helpful_error(runner):
    with patch('bookminder.apple_books.library.SUPPORTED_FILTERS', {'foo', 'bar'}):
        result = runner.invoke(main, ['list', 'all', '--filter', 'baz'])
        assert result.exit_code == 1
        assert "Invalid filter: 'baz'" in result.output
        assert "Valid filters:" in result.output
        assert "foo" in result.output
        assert "bar" in result.output
```

The fictitious filter names are the whole point, and the commit body says so: "*The test uses mock filter names (foo, bar) to prove that the CLI completely delegates filter knowledge to the library.*" Because `foo` and `bar` are not real filters, the test cannot pass unless the CLI reads the vocabulary *from the library at call time*. It specifies a design — the CLI owns no domain knowledge — and it does so in a way no amount of implementation cleverness can fake. That is what a London-school boundary test is for.

### 4.2 What degraded, in order

**(a) The acceptance test was edited to fit the implementation.** `fa0bc72` implemented `SUPPORTED_FILTERS` via `from bookminder.apple_books.library import SUPPORTED_FILTERS` — a from-import binds the value at CLI import time, so `1d1fb34`'s patch of the *library* attribute no longer took effect. Rather than change the implementation to preserve the specified delegation (a late-bound module attribute lookup), the same commit changed the spec: `patch('bookminder.apple_books.library.SUPPORTED_FILTERS', ...)` → `patch('bookminder.cli.SUPPORTED_FILTERS', ...)`. The test still passes and still looks like a delegation test, but it now only asserts that the CLI compares against *some set it holds locally* — the design constraint it was written to enforce is gone, silently. **This is the single most consequential line changed in the lapse**: the spec stopped being the authority and became a record of whatever the code happened to do.

**(b) A spec was written so weak that a meaningless implementation satisfied it.** `af3954c` asserted only `isinstance(SUPPORTED_FILTERS, set)` and `len(SUPPORTED_FILTERS) > 0`; `fa0bc72` satisfied it with `SUPPORTED_FILTERS = {"dummy"}`. Then `3d2bab6`, labelled `refactor:`, changed the test's expectation to `== {"cloud", "!cloud", "sample", "!sample"}` and the implementation to match — *in the same commit*. That is not a refactor (behaviour changed) and there is no moment at which a failing test drove the real values into existence. Contrast the pre-lapse walking skeleton, where fake data was permitted precisely because a red acceptance test was pulling against it; here nothing was pulling, so the fake simply became real by editorial fiat.

**(c) An existing story's living documentation was commandeered.** `ef5474b` renamed `describe_bookminder_list_recent_command` to `describe_bookminder_list_recent_command_with_fixtures` and reused the vacated name for the new filter-validation test. The `--spec` output for a completed story now describes a different feature, and the traceability from `stories/list-recent-books.yaml` to its spec block is broken. **This violates the naming rule's whole purpose** — the describe block is the story's name in the documentation, not a free identifier.

**(d) Implementation and test landed in one commit, with no failing test first, and no acceptance test at all.** `b246d7b` ("feat: implement !sample filter") and `5b42ae0` ("feat: add sample filter support to list_recent_books") each contain library code plus its unit tests. Nothing in the history shows those tests ever failing, and the corresponding story `filter-by-sample-flag.yaml` had no acceptance test until `677a251` retrofitted one the following day.

**(e) The assertion-strength rules were dropped.** In `5b42ae0`:

```python
def it_filters_by_sample_status():
    sample_books = list_recent_books(TEST_HOME, filter="sample")
    for book in sample_books:
        assert book.get("is_sample") is True, f"Expected sample book: {book['title']}"
```

No non-emptiness guard — if the filter returns nothing, the loop body never runs and the test is green. Compare `5730bf4`'s pre-lapse sibling three weeks earlier, which opens with `assert len(cloud_books) > 0, "Expected to find cloud books"`. In `b246d7b`'s CLI test the assertion `assert "Sample Book" not in result.output` is vacuous by construction: the mock returns a single book titled `"Regular Book"`, so the string could never have appeared. And the retrofitted acceptance test in `677a251` is worse still — it wraps its assertions in `if output and "No books" not in output:`, a conditional that lets the test pass while asserting nothing at all. **A test that cannot fail is not a specification; it is a comment with a runtime cost.**

**(f) Evidence-free defensiveness returned.** `b246d7b` shipped `WHERE ZSTATE != 6 AND (ZISSAMPLE != 1 OR ZISSAMPLE IS NULL)` with a commit body claiming it handles NULLs "*appropriately*", though no fixture contains a NULL `ZISSAMPLE`. `c851f95` removed it the next day with the diagnosis: "*The defensive programming was added without evidence of actual NULL values in the data.*" This is exactly the failure mode `e7a5fa4` had been written to teach against, recurring once the discipline that prevented it lapsed.

### 4.3 The repair, and what it says about the standard

Two repairs were attempted. `677a251`/`9cac7d7`/`c851f95` patched forward — retrofitting the missing acceptance tests, parameterising the filter passthrough matrix, deleting the unevidenced NULL guard. The author evidently judged this insufficient, because the unmerged branch then does the other thing: `447dc8c` performs a **semantic revert of the entire YOLO output back to `6f786cc`** — removing `SUPPORTED_FILTERS`, `validate_filter`, and the sample-filter implementation — while explicitly preserving the `unit/integration/acceptance/e2e` directory structure, and TODO.md still lists the three affected stories as needing "*proper ATDD reimplementation*".

**The principle this states, more clearly than any rule in CLAUDE.md: code whose provenance violates the process is not repaired by adding tests to it.** A retrofitted test is written by someone who has already read the implementation and therefore specifies the code that exists rather than the behaviour that was wanted; it can only ratify. The only honest repair is to delete and re-derive from a failing test — which is also why the restoration branch's `bd47589`…`5f8d330` re-implements the *next* story from scratch under explicit `RED:`/`GREEN:` commits rather than continuing from where the lapse left off.

### 4.4 One deviation visible in the repair itself

`875bed0` (GREEN for the `finished` filter) also added `unread` and `in-progress` to `SUPPORTED_FILTERS` and their `WHERE` clauses, though only the `finished` scenario was red at that moment; `5f8d330` later notes that the third test "*passes immediately as filter logic was already implemented*". That is a GREEN wider than its RED — a mild recurrence of the same over-reach, in the commit series written to demonstrate the cure.

---

## 5. Where motivation could not be recovered

- **Tolerance for shadowing builtins.** `63785d5` renamed `format_book_output` to `format` and gave three reasons — shorter lines in tests, unambiguous within `cli.py`, consistent with `format_book_list` — none of which addresses shadowing `format`. Likewise `filter` shadows the builtin throughout `library.py` and `cli.py`; `46f553f` explains the `--flag` → `--filter` rename for the *CLI option* but not the decision to carry that name into Python signatures, and `74e6220` had already renamed the `list` command group to `list_cmd` to avoid exactly this clash. The rule appears to be "shadow when the module context makes it unambiguous", but it is never stated and is applied inconsistently.
- **The stray comment `# This is a test comment to trigger pre-commit hooks.`** introduced during `da5e60e`'s pre-commit demonstration survives in `cli.py` on `HEAD`. A project that deletes redundant comments on sight kept this one; nothing explains why, and it is most likely simple oversight rather than intent.
- **Why `list_books` / `find_book_by_title` (plist-based) were retained** at all after the CLI moved entirely to the SQLite path. They have integration tests and no callers in `cli.py`. Whether this is deliberate retention of a future EPUB-path capability or unreaped growth is not derivable from the commits.
- **Why the `--spec` docstring convention permits `"""Integration test: verify full stack works with real fixture."""`** (`e2e/cli_wiring_spec.py`) when the layer's own `__init__.py` already states that. The rule elsewhere would delete it as duplication; no commit addresses the exception.
