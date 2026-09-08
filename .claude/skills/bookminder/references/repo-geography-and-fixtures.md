# Repo geography, backlog, and fixture architecture

How to work in this tree: what is in it and how to read it without flooding the context, where specs and stories go, the design decisions already made, the fixture system, and the toolchain. Record a new decision here as the decision and its why; the record holds how it was reached.

## What is in the tree

One line per item that needs explaining; the tree listing shows the rest.

- `bookminder/`: the production package, `cli.py` and `apple_books/library.py`. Small; read it whole.
- `specs/`: the executable specification, laid out by concern (B-22), with the fixture home directories under `specs/apple_books/fixtures/users/` ("Fixture architecture" below).
- `specs/apple_books/fixtures/All_Books*.swift`: a real plist rendered as Swift literals, large and deliberately untracked pending curation. Grep them; never Read, gitignore, or stage them.
- Fixture `.sqlite` files: binary. Query them with `sqlite3`; never Read them.
- Zero-byte fixture files (`401429854.epub`, corrupted_db_user's plist and database): deliberate; the emptiness is the fixture's point.
- `stories/`: story cards, one YAML file per story, in story-map columns (B-23).
- `docs/`: project documentation. `docs/ui/apple/` holds screenshots, binary: reference them by path, never Read them. `docs/apple_books.md` is the research spike's map of Apple Books storage; the domain page compresses it and maps its sections.
- `claude-dev-log-diary/`: the session transcripts, permission-gated (B-21). `./xs` is a symlink into it: run it as the documented tool, never read it as a file.
- `.coordination/`: the meta-project's substrate, evidence and history, never instruction (current-state B-65).
- `.venv/`: vendored in-tree, as in BookMind. Exclude it, caches, and the diary from every listing and metric; a raw count is almost entirely site-packages.

## Orientation

- **B-20 — Orient from a size-aware tree listing before reading anything, then read the package whole.** Run `tree -h -I '__pycache__|claude-dev-log-diary|Library' .` once at the start of a session; if `tree` is missing, install it first (`apt-get install -y tree` on the cloud container). The listing is the census of what exists and how big it is, and every read is decided from it: a small text file is read whole, a large text file by grep or a line range, a binary never; the section above says which files are which. Then read `bookminder/cli.py` and `bookminder/apple_books/library.py` whole, because they are small and guessing about them costs more than reading them, and read what the system does from `pytest --spec` when starting a story or whenever the question is behavior. Never re-derive the tree with `find`, `ls -R`, or repo-wide line counts, because a large file read whole fills the context with nothing you needed, and a second census pays for information already in front of you.
- **B-21 — Never enter `claude-dev-log-diary/` without the author's explicit, scoped permission.** That includes reaching it indirectly through `git diff`, `git show`, or `git log -p`. A grant covers exactly the excerpt and manner it names: range-read the named lines rather than the whole file, in the foreground, because a background subagent's reads cannot be seen or stopped. A day-file holds several sessions, `^claude` marking each start, and only the session-end cost figure is trustworthy.
- **B-22 — Place specs by concern, not by test layer.** `specs/cli_spec.py`, `specs/cli_formatting_spec.py`, `specs/apple_books/library_spec.py`, `specs/apple_books/library_integration_spec.py`, with fixtures co-located under `specs/apple_books/fixtures/`. Ignore any `unit/integration/acceptance/e2e` directory you find: the four-layer split was reverted, and such directories can only be untracked `__pycache__` residue, never tracked structure (confirm with `git ls-files specs/`). Never read a coverage gap in subprocess-exercised code as evidence it is untested: `specs/cli_spec.py` drives the CLI via `subprocess`, and pytest-cov does not follow child processes.

## Session-transcript preservation

- **B-32 — Snapshot the native transcript into the diary when the container is ephemeral.** `claude-dev-log-diary/jsonl/` preserves full session transcripts in the agentic system's native format, the machine-readable source the day-files only shadow; its README holds the layout and copy commands. When working in an ephemeral container, snapshot the session's `.jsonl` file and directory from the harness's transcript store into `jsonl/cloud-<year>/` and commit it, because the container's transcript dies with it. Snapshot (1) always toward session end, when the final branch push is being prepared, and (2) incrementally at natural stable points, after a major phase of work lands or when resuming after a long pause, so that the pause's tail is on disk. Re-snapshot freely, since copies are append-only extensions, and batch the snapshot into an adjacent commit rather than making high-frequency snapshot-only commits. Expect the true tail of a session to arrive with the next session's first snapshot; a transcript cannot contain its own final minutes. Skip all of this in local sessions: the harness store persists there, and the author owns backup timing.

## Backlog and stories

- **B-23 — Take the next story from TODO.md's Discover Column in order, and write its card before its spec.** The column is a bare list of story paths in implementation order: the order is the plan, so never offer a menu, and keep the list free of emoji, numbering, and per-item rationale. The story-map columns are `discover` (listing, filtering, admin access, error handling), `access` (controlling the Apple Books app), `review` (highlights and notes), and `export` (text extraction). A card carries the mandatory `status` and nothing else: no priority or assignee metadata (YAGNI). Treat Completed Features as an immutable record of the journey: never reorder or remove entries, annotate a reopened story in place (`[REOPENED: ...]`), list user-visible stories only and no refactorings, and give a doc deletion a one-line breadcrumb with its commit hash. Write a parked backlog item with enough of the HOW (mechanism, trigger, expected behavior) that a fresh session can execute it without asking.

## Settled design decisions in the code

- **B-24 — Keep the CLI one Click group with one `--filter` option shared by `recent` and `all`, and give it no domain knowledge.** Keep `main` a Click group and `list` a subgroup on a function named `list_cmd`, never `list`: the builtin's name breaks `list[Book]` annotations at import time, and a name collision is fixed at the source, never with deprecated typing aliases. Share `--user` and `--filter` between the `recent` and `all` subcommands through one decorator, because Click does not inherit group options. Keep the filter vocabulary to one `--filter` option whose values are attribute names with `!` negation: `cloud`/`!cloud` and `sample`/`!sample` implemented, reading status (`finished`, `unread`, `in-progress`) assigned to the same option by the approved plan, and a single value per run, with combined filters their own backlog story. Do not add `--flag`, `--status`, or `--type`; the one-option vocabulary is settled. Negate with `!` rather than `-` because Click parses a leading `-` as an option, and keep filters orthogonal to list commands because nothing in Apple Books' UI makes them command-specific. Keep `list recent` a deliberate replica of Apple's Continue section, so that an agent consuming the future MCP surface and the human looking at the app share one frame of reference. Keep `--user` as both a real admin feature (examine another user's books) and the test seam; the admin use case is what licenses it in production. The CLI passes the raw `--user` string and filter through to the library and delegates path resolution and querying there.
- **B-25 — Keep one `Book` TypedDict, and never add a variant type for an extra field.** Use `NotRequired` for optional fields instead. Require only `title` and `author`; `path` and `updated` are `NotRequired` because the type guarantees only what every code path can honestly supply, and the database path leaves `path` empty (current-state B-70). Expect a plain dict from it: TypedDict is a static annotation only, with no attribute access and no runtime key enforcement.

## Fixture architecture

Integration fixtures are synthetic home directories under `specs/apple_books/fixtures/users/<persona>/`, each replicating Apple's container layout path-for-path.

### Personas

Each persona encodes one state a real machine can be in:

- `test_reader`: a populated library; extend it rather than adding a persona unless a spec needs isolation.
- `fresh_books_user`: both containers, a plist with no books, a database with the schema and no rows.
- `legacy_books_user`: the `BKAgentService` container with its plist, and no `BKLibrary` directory.
- `never_opened_user`: only the OS-created `com.apple.iBooksX` container, holding an empty `BKLibrary` directory and nothing else; the empty directory is load-bearing and stays tracked by its leaf `.gitkeep`.
- `corrupted_db_user`: the full container layout with a zero-byte plist and a zero-byte database.

Keep `legacy_books_user` and `never_opened_user` distinct: a missing `BKLibrary` directory and an empty one are two error paths in `library.py`, and each persona exercises one.

### The `--user` seam

Enter a fixture through the product's own `--user` parameter: an absolute path is used verbatim as the home directory, a bare name resolves to `/Users/<name>`, and no value means the current user's home, exactly three cases. Pass fixture paths absolute; a relative path is treated as a username and silently rewritten. The front door exercises the real path construction and crosses the subprocess boundary the CLI spec runs through, which a patched module constant, substituted in-process at import time, cannot.

### Populating a fixture

Create a fixture database with `create_fixture.sh`, which dumps the schema from a live library; never hand-write a schema. Populate it only with `copy_book_to_fixture.sh`, which copies a whole real row, so that every row is a real, complete book record; never hand-write or hand-edit SQL, because an invented or edited row encodes the agent's beliefs exactly where the spec is supposed to be falsifiable. When a needed state does not exist, leave it to the author: he adjusts a real book in his library and it gets copied. When a script fails, debug the script. Never make a script delete; cleanup is a deliberate human act. In the scripts, name the parameter variable `FIXTURE_USER`, never `USERNAME`, a zsh special parameter that silently shadows the argument; SQL-escape titles by doubling quotes; locate the fixture database by the same `BKLibrary-*.sqlite` glob production uses; root every path at `PROJECT_ROOT` and check the resolved path before the first write, because the scripts hold the real library's path beside the fixture's, and a wrong one writes into the real library. Document how each fixture was derived in `docs/test_fixtures.md` in the same commit. Preserve an intentionally empty directory with a single `.gitkeep` at the leaf. After any fixture change, verify through the product: `python -m bookminder list recent --user <absolute fixture path>`.

### What `test_reader` holds

Query it rather than recalling it: `sqlite3 "specs/apple_books/fixtures/users/test_reader/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary-fixture.sqlite" "SELECT ZTITLE, ZSTATE, ZISSAMPLE, ZREADINGPROGRESS FROM ZBKLIBRARYASSET"`. Its plist holds one book, "Growing Object-Oriented Software, Guided by Tests", the project's canonical known book named in ORIGINAL_VISION.md; the zero-byte `401429854.epub` stands in for its file.

### Fixtures and a real library

Explore Apple Books behavior read-only against a real library, because fixtures can only confirm what was built into them; when reality shows a new case worth capturing, copy it into the fixture. Specify any recency-window behavior with controlled time: fixtures freeze time, and a snapshot otherwise silently ages out of the window.

## Toolchain and maintenance

- **B-30 — Keep Python pinned `==3.13.*` and run every tool from the venv.** Never a permissive floor, because reproducibility across machines depends on one interpreter; the toolchain is uv + ruff + mypy on the setuptools backend, and ruff `target-version = "py312"` stays until the pinned ruff accepts py313. Run tests with `source .venv/bin/activate && pytest`; `uvx bookminder` fails because the package is unpublished, and bare `uv run` re-downloads CPython. Provision a fresh checkout, which has no `.venv`, with `uv venv && uv pip install -e ".[dev]"`. When ruff disagrees between shell and hook, compare `.pre-commit-config.yaml`'s pinned `rev:` against `ruff --version` in the venv. Keep `check-toml` in pre-commit, so that an invalid `pyproject.toml` fails on the committing machine rather than on the next machine's install.
- **B-31 — Keep one source of truth per concern, and prove a doc claim before writing it.** Make a migration delete the superseded file inside itself. Never invent identity metadata: the author is Pavol Vaskovic (pali@pali.sk); ask or leave blank. If you assert X is required, remove X and show the failure first, and never document a command until you have run it and shown it working. Judge any document by whether it is referred back to and changes behavior on this project; retrospective meta-analysis docs fail both tests. Write README bash snippets without inline comments, because readers copy-paste them, and put the explanation in the prose above.
