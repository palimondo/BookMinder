# BookMinder BDD/TDD Style — extracted from git history

Method: `git log --reverse --oneline -- '*.py' ':!claude-dev-log-diary'` → 117 commits,
2025-04-13 (`9e7bd38`) … 2025-08-02. Note the working clone was shallow (grafted at
`5a57aa2`); `git fetch --unshallow` is required or the entire BookMinder history is invisible
and only the `xs` sidequest shows up.

Era map:

| # | range | character |
|---|---|---|
| 1–14 | `9e7bd38`…`1d14ce2` (Apr–May) | pre-discipline: docstring-heavy, `try/except` swallowing, YAGNI features |
| 15–26 | `eca50d2`…`d8b5722` (Jun 23) | walking skeleton; ATDD discipline *discovered* and retro-applied |
| 27–59 | `af3b75a`…`086fbea` (Jun 26–27) | refactor storm + 3 reverts; spec conventions settle |
| 60–96 | `14ef3da`…`10048e1` (Jul 4–12) | **gold standard**: story-card-driven ATDD, mock-at-boundary |
| 97–98 | `1d1fb34`, `6f786cc` (Jul 13) | last clean RED-first cycle; boundary |
| 99–107 | `af3954c`…`c851f95` (Jul 13–14) | **the lapse** ("YOLO mode"), retro at `677a251` |
| 108–114 | `be394a0`…`0bf00d1` (Jul 21) | test-pyramid reorg into `specs/{unit,integration,acceptance,e2e}` |

---

## 1. Spec style rules

### 1.1 Layout and naming

`specs/<...>/<module>_spec.py`. Config (`pyproject.toml` `[tool.pytest.ini_options]`,
duplicated in `pytest.ini`):

```
python_files = "*_spec.py"   python_functions = "it_*"   python_classes = "describe_*"
```

**Two levels, not three.** `9e7bd38` opened with three
(`describe_book_library` → `describe_when_listing_books` → `it_finds_books…`); everything
after `eca50d2` is flat `describe_X()` / `it_Y()`.

**`describe_` names the feature or command; `it_` names the story.** Codified in `3db7e5a`
and CLAUDE.md: story `stories/discover/filter-by-cloud-status.yaml` →
`describe_bookminder_list_with_filter()` + `it_filters_by_cloud_status()`. The `describe_`
is the *command surface*, never a test category — that is what makes `pytest --spec` read as
prose.

### 1.2 Acceptance criteria live in YAML, not docstrings

The convention was fought out in three commits. `ca8284d` (Gemini) *restored* Gherkin
docstrings as "living documentation"; `b4e376d` left a `# FIXME: Now that this gherkin
scenarion is in stories, code is enough - remove!`; `48596a6` removed them for good:

> removes the redundant Gherkin docstring … as its purpose is now served by the YAML story card

Final rule (also CLAUDE.md `<code_style>`): **implemented tests carry no docstring**;
the spec is the story card + the test name + the assertions. `6f786cc` is the terminal
application of this to inline comments:

```python
-        assert result.exit_code == 0  # No crash
+        assert result.exit_code == 0
-        assert "Traceback" not in result.output  # No stack trace leaked
+        assert "Traceback" not in result.output
```

### 1.3 Pending specs keep their docstring, and are skipped — not stubbed silently

`7060287` is the canonical shape — one implemented `it_`, one pending `it_` carrying the
story's `when:`/`then:` verbatim:

```python
def describe_bookminder_list_with_flag_filter():
    def it_shows_only_cloud_books_when_flag_is_cloud():
        """List cloud books
        when: I run "bookminder list recent --flag cloud"
        then:
          - I see only books stored in iCloud (not downloaded locally)
          - Cloud status is indicated by "☁️"
        """
        result = _run_cli_with_user("test_reader", subcommand="recent", flag="cloud")
        assert "Lao Tzu: Tao Te Ching" in result.stdout
        assert "☁️" in result.stdout
        assert "The Pragmatic Programmer" not in result.stdout

    @pytest.mark.skip(reason="Implementation pending")
    def it_shows_only_local_books_when_flag_is_local():
        """List local books
        when: I run "bookminder list recent --filter !local" ...
        """
        pass
```

`c785dc6` then implements it: deletes the `@skip` **and** the docstring in the same commit
that adds the body. `20b03dc` does the same for `@pytest.mark.skip(reason="Need to update
fixture to include database")`. Skip reasons are always *concrete blockers*, never "TODO".

### 1.4 Assertions: positive **and** negative, with the actual value in the message

Every filter spec asserts both what appears and what must not:

```python
assert "Lao Tzu: Tao Te Ching" in result.stdout          # c785dc6
assert "☁️" in result.stdout
assert "Extreme Programming Explained" not in result.stdout
assert "The Left Hand of Darkness" not in result.stdout
```

Message style is `assert <cond>, f"Expected …, got: {actual}"` — see
`e2e/cli_wiring_spec.py:47` and `integration/library_containers_spec.py:134`. Set-equality
over membership where the full expected result is knowable (`b246d7b`'s sibling in
`library_containers_spec.py:191`):

```python
assert sample_titles == expected_samples, f"Expected {expected_samples}, got {sample_titles}"
```

**Loop assertions must be guarded by a non-emptiness assertion**, or they pass vacuously.
Gold-standard example (`library_containers_spec.py:129`):

```python
cloud_books = list_recent_books(FIXTURE_PATH / "test_reader", filter="cloud")
assert len(cloud_books) > 0, "Expected to find cloud books"
for book in cloud_books:
    assert book.get("is_cloud") is True, f"Expected cloud book: {book['title']}"
```

This guard is exactly what the lapse dropped (§4).

### 1.5 Fixtures: real directory trees over monkeypatch

`3103e4d` introduced four **persona-named** fixture users under
`specs/integration/apple_books/fixtures/users/` — `never_opened_user`, `fresh_books_user`,
`legacy_books_user`, `test_reader` (later `corrupted_db_user`, `dummy_relative_user`) — each
a real Apple container tree. `8e632f6` then removed mocking outright:

> Instead of mocking `_books_plist`, moved Books.plist to a test_home directory with the
> proper Apple directory structure. … No more monkeypatching needed — the tests are cleaner
> and more realistic.

Progression is explicit and one-directional: `monkeypatch.setattr` (`3103e4d`) → dummy paths
(`9a6319f`) → real fixture tree (`8e632f6`) → fixtures colocated with the tests that use
them (`0bf00d1`).

`pytest.fixture` is introduced only once a second consumer justifies it — `a596b6c` adds the
`runner` fixture and says so: *"We already have 2 tests using CliRunner … and will convert 4
more, making the fixture worthwhile."*

### 1.6 Mock at the architectural boundary; assert coordination, not strings

`552a9a3` is the clearest statement of intent (explicitly GOOS-flavoured):

```python
def it_shows_recently_read_books_with_progress(runner):
    book1 = Book(title="B1", author="A1")
    book2 = Book(title="B2", author="A2")
    with patch('bookminder.cli.list_recent_books') as mock_list_recent, \
         patch('bookminder.cli.format') as mock_format:
        mock_list_recent.return_value = [book1, book2]
        runner.invoke(main, ['list', 'recent'])
    mock_list_recent.assert_called_once_with(user=None, filter=None)
    assert mock_format.call_args_list == [((book1,),), ((book2,),)]
```

> Tests the CLI's actual responsibility (coordination) … Follows GOOS principles of testing
> at architectural boundaries. Changes to format strings only require updating format tests.

Test data is deliberately degenerate (`"B1"`/`"A1"`) — the CLI spec must not know formatting.
`a596b6c` even strips `reading_progress_percentage` from the stubs because `format` is mocked.
**0-1-many** sizing is named in `552a9a3` and `2859fad` (2 books is "enough to verify
ordering"; formatter tested at 0, 1 and n).

Mocks may name *fictional* collaborator values to prove delegation — `1d1fb34`:

```python
with patch('bookminder.apple_books.library.SUPPORTED_FILTERS', {'foo', 'bar'}):
    result = runner.invoke(main, ['list', 'all', '--filter', 'baz'])
```

> uses mock filter names (foo, bar) to prove that the CLI completely delegates filter
> knowledge to the library.

### 1.7 One subprocess test, ever

`d30b9ee` / `specs/e2e/__init__.py`: *"Be minimal — we only need ONE test to verify wiring."*
The four `__init__.py` files added in `7dfe126` are the placement contract:
`unit/` pure logic, no I/O · `integration/` real filesystem + SQLite fixtures ·
`acceptance/` CliRunner + mocked library · `e2e/` the single subprocess test.

### 1.8 Duplication in specs is removed by helper or parameterize

Helper with the invariant assertion hoisted inside it (`b4e376d`, still at
`e2e/cli_wiring_spec.py:31`):

```python
    assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}: {result.stderr}"
    return result
```

Parameterize once the matrix appears (`9cac7d7`, "reduced 8 individual filter tests to 1"):

```python
@pytest.mark.parametrize("command,library_function", [("recent","list_recent_books"),("all","list_all_books")])
@pytest.mark.parametrize("filter_value", ["cloud", "!cloud", "sample", "!sample"])
def it_passes_filters_to_library_function(command, library_function, filter_value, runner):
```

---

## 2. Implementation style

- **Minimal to the point of fake.** `eca50d2` ships three hardcoded `click.echo` lines to
  turn the acceptance test green as a walking skeleton; `bd9ea30` moves the fake behind a
  function; `cffd595` finally hits SQLite. `fa0bc72` does the same at unit granularity —
  `SUPPORTED_FILTERS = {"dummy"}` — then `3d2bab6` triangulates to the real set.
- **Defensive code is deleted unless a test demanded it.** `b73a618` removes the missing-DB
  guard *and its passing tests* — "Remove error handling code that was added without
  corresponding acceptance criteria, restoring ATDD discipline" — replacing a
  `try/except sqlite3.Error: return []` with a bare `assert`. `c851f95` removes
  `OR ZISSAMPLE IS NULL` after checking the fixture data: "defensive programming was added
  without evidence of actual NULL values."
- **Types collapse toward one type.** `RecentBook` (`bd9ea30`) → `BookWithProgress(Book,
  total=False)` (`8bb84fb`, "YAGNI violation") → `progress: NotRequired[float]` on `Book`
  itself (`6391048`). Final `Book` is one `TypedDict` with `NotRequired` optionals
  (`library.py:42`). Modern syntax throughout: `X | None`, `list[Book]`, `dict[str, Any]`
  (`2f77667`), full annotations on production code, mypy `disallow_untyped_defs = true`
  with `specs/` excluded.
- **Private by default, promoted only when tested directly.** `ef953e1` *re*-privatises
  `apple_timestamp_to_datetime` → `_apple_timestamp_to_datetime` because nothing needed it
  public. Module is a flat set of `_`-prefixed helpers + 4 public functions; no classes.
- **Pure functions extracted for testability.** `74e6220` pulls `format_book_list` out of the
  command; `63785d5` renames `format_book_output` → `format`; `10048e1` splits
  `_build_books_query` out of `_query_books`.
- **Errors: one domain exception at the layer boundary.** `0dd8aa0` adds `BookminderError`;
  library wraps `FileNotFoundError`/`sqlite3.Error`, CLI catches it and echoes the message
  with exit code 0 and no traceback (`cli.py:82`). Messages carry the offending path
  (`library.py:27`).
- **Docstrings on production code only where they carry meaning** — one line per public
  function; `3cc2e39`, `f3d57b3` strip the rest. Ruff `select = ["E","F","I","B","W","UP",
  "N","D"]`, line length 88, with `D1xx` ignored under `specs/`.

---

## 3. Observed TDD cadence

The rhythm, when honoured, is visible in the commit *subjects* themselves:

```
1d1fb34  test: add failing test for filter validation …      ← RED (states "currently fails")
af3954c  test: add failing unit test for SUPPORTED_FILTERS   ← RED ("failed before implementation")
fa0bc72  feat: implement minimal SUPPORTED_FILTERS …         ← GREEN ("just enough")
3d2bab6  refactor: update SUPPORTED_FILTERS with real values ← triangulate
ef5474b  refactor: extract validate_filter function …        ← REFACTOR
```

Properties:

- **Two commits per cycle** (CLAUDE.md `<git_workflow>`): GREEN, then REFACTOR. In practice
  refactor commits dominate — 45 of 117 subjects start `refactor:`, vs 14 `feat:`.
- **Refactors are one idea each.** `af3b75a` … `9a6319f` is a chain of ~14 single-concept
  commits ("Extract common Apple container path prefix", "Inline fixtures_path variable",
  "Remove redundant docstring").
- **The acceptance test is allowed to stay RED.** `d8b5722` deletes a meta-test written to
  force real implementation and states the rule: *"The proper approach is to tolerate RED
  acceptance tests while building real implementation through unit tests"* — the test was
  *"created to retrofit real implementation after acceptance test was prematurely made to
  pass with fake data."*
- **Revert rather than patch forward.** Four true reverts: `1b07bd5` (unrequested error
  handling), `bcb5223` (a `LibraryPaths` dataclass consolidation), `82d3990` (subprocess →
  CliRunner, reverted so it could be redone incrementally), `7d3922a` — the most instructive:

  > We made a mistake — instead of refactoring the existing CLI tests in cli_spec.py to use
  > mocks, we created duplicate tests in a new file. This wasn't the goal.

  The redo is `45256cd` → `552a9a3` → `c52fc26` → `a596b6c`: four commits converting **one**
  test, each commit's message naming the next step ("The next commit will show a better
  approach that tests the CLI's coordination role rather than output strings").
- **Coverage is a check, not a goal** — `ef953e1` reaches 100%, `b73a618` then *deletes* two
  of those tests; `aafeb0d` restores 100% by "removing untested defensive code" rather than
  adding tests.

---

## 4. Gold standard vs. the post-`6f786cc` lapse

**"Gold standard"** = the loop running story-card-first, outside-in, in this order:

1. Story YAML exists in `stories/…` with `status:` and `acceptance_criteria: when/then`.
2. An **acceptance spec** is written from it — implemented, or `@skip`ped carrying the
   Gherkin as its docstring (`7060287`).
3. It is run and confirmed RED; the commit message says so (`1d1fb34`, `af3954c`).
4. A **unit spec** for the collaborator the acceptance test revealed is written and confirmed
   RED.
5. Minimum implementation to green, possibly a literal dummy (`fa0bc72`).
6. Triangulate to the real value (`3d2bab6`), then refactor in separate one-idea commits
   (`ef5474b`), deleting anything not demanded by a test (`b73a618`, `c851f95`).

`6f786cc` is not itself a fault — it is a pure comment-strip. It is the **last commit on the
gold-standard side**; the very next commit begins working bottom-up.

### What specifically degraded

**(a) The order inverted — unit-first instead of outside-in.** From `af3954c` onward the
sequence is library unit spec → library impl → CLI, with no story-level acceptance test
leading. `5b42ae0` ("add sample filter support to list_recent_books") touches **only**
`library.py` and `library_spec.py` — zero acceptance coverage for a user-visible filter whose
story card (`stories/discover/filter-by-sample-flag.yaml`) explicitly specifies
`bookminder list [any] --filter sample`.

**(b) Non-emptiness guards dropped → vacuously passing specs.** `5b42ae0` added, and
`specs/integration/library_containers_spec.py:147-161` still contains:

```python
def it_filters_by_sample_status():
    sample_books = list_recent_books(FIXTURE_PATH / "test_reader", filter="sample")
    for book in sample_books:                      # ← passes if the list is EMPTY
        assert book.get("is_sample") is True, f"Expected sample book: {book['title']}"

def it_excludes_samples_with_not_sample_filter():
    non_sample_books = list_recent_books(FIXTURE_PATH / "test_reader", filter="!sample")
    for book in non_sample_books:                  # ← same
        assert book.get("is_sample") is False, …
```

Compare the cloud pair immediately above them (lines 129–145, gold-standard era), which open
with `assert len(cloud_books) > 0, "Expected to find cloud books"`. Same file, same shape,
guard present before `6f786cc` and absent after.

**(c) Tautological CLI tests — asserting the mock, not the behaviour.** `b246d7b` un-skipped
`it_excludes_samples_when_filter_is_not_sample` with a body that cannot fail; the same defect
survives at `specs/acceptance/cli_spec.py:115-130`:

```python
regular_book = Book(title="Regular Book", author="Regular Author",
                    reading_progress_percentage=50, is_sample=False)
with patch('bookminder.cli.list_recent_books') as mock_list:
    mock_list.return_value = [regular_book]
    result = runner.invoke(main, ['list', 'recent', '--filter', '!sample'])
    assert "Regular Book - Regular Author (50%)" in result.output
    assert "Sample" not in result.output      # ← no sample was ever in the mock
```

The `not in` assertion verifies nothing about filtering: it is guaranteed by the stub. In the
gold-standard version (`c785dc6`) the negative assertion named books that genuinely existed in
the fixture DB and had to be excluded by real SQL.

**(d) Impl and spec landed in one commit, with no RED step.** `b246d7b` and `5b42ae0` each
modify `library.py` and its spec together. Contrast `af3954c`→`fa0bc72`, two commits apart,
one hour earlier.

**(e) The retro-fix was itself weak, then deleted.** `677a251` ("YOLO mode retrospective")
added the missing acceptance tests — but with a vacuity guard *inverted into a conditional*:

```python
    output = result.stdout.strip()
    # Sample books may not have reading progress, resulting in empty list
    if output and "No books" not in output:      # ← whole assertion body is optional
        for line in output.split("\n"):
```

`9cac7d7` (the next Python commit) then deleted the entire
`describe_bookminder_list_recent_integration` block containing them rather than strengthening
them. Net effect: the recent-command sample filter has never had a non-vacuous end-to-end test.

**(f) Naming convention broken.** `677a251` introduced `describe_bookminder_acceptance()` —
still at `specs/acceptance/cli_spec.py:98`. It names a *test category*, not a command,
violating the `3db7e5a` rule that `describe_` names the feature/command; in `pytest --spec`
it reads "bookminder acceptance / filters recent books by sample status". `ef5474b` also left
`describe_bookminder_list_recent_command_with_fixtures` — a describe named after its
*mechanism*.

**(g) Residue still at HEAD, all traceable to the lapse + the reorg that followed it:**

- `specs/acceptance/cli_spec.py:59` and `:66` — `it_validates_filter_values` and
  `it_validates_filter_values_and_shows_helpful_error` are near-duplicates (`ef5474b` added
  the first without noticing `1d1fb34` had already covered it).
- `specs/integration/library_containers_spec.py` carries two `describe_list_all_books`-family
  blocks (`:69` and `:164`) and duplicate `it_handles_fresh_apple_books_user_with_no_books`
  (`:31`, `:70`) — merge residue from `9781be1`.
- `specs/unit/library_spec.py:9` — `TEST_HOME = Path(__file__).parent /
  "fixtures/users/test_reader"` points at `specs/unit/fixtures/`, **which does not exist**;
  dead since `9781be1`/`0bf00d1` moved the fixtures. It is still referenced at `:43`, where
  it happens not to matter because `_get_user_path` only string-round-trips it.
- `bookminder/cli.py:48` — `# This is a test comment to trigger pre-commit hooks.`, from
  `da5e60e`, survives despite the CLAUDE.md ban on redundant comments and `6f786cc`'s cleanup.
- **Behavioural asymmetry**: `list_recent_books` wraps `sqlite3.Error` in `BookminderError`
  (`library.py:167`); `list_all_books` (`:171`) does not — added during the lapse without a
  spec to demand parity.

**(h) One pre-boundary crack worth naming.** `10048e1` (#96) extracted `_build_books_query`
and specced it by asserting on the SQL *string* — `assert "ZTITLE" in query`,
`assert query.index("WHERE") < query.index("ORDER BY")` (`specs/unit/library_spec.py:48-69`).
That is testing implementation, the exact smell `d8b5722` removed a month earlier. It is the
first place the discipline slipped, two commits before `6f786cc`.

### Restoration checklist implied by the evidence

For each of `validate-filter-values.yaml`, `filter-by-sample-flag.yaml`,
`filter-by-reading-status.yaml` (TODO.md lines 19–25): write the acceptance spec from the
story card first and confirm RED; assert against real fixture book titles, not stub echoes;
guard every loop assertion with `assert len(...) > 0`; rename
`describe_bookminder_acceptance` to the command it exercises; delete the duplicate validation
and `list_all_books` describes; fix or delete the dead `TEST_HOME`.
