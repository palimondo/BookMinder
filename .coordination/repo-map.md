# BookMinder Repo Map

Generated for coordinator/worker navigation. Sizes in bytes, `L` = line count.
Repo total **20M** (`.git` 4.3M, `claude-dev-log-diary/` 12M, `docs/` 2.6M, rest ~1M).
Python 3.13 / uv / pytest-describe BDD project: CLI over the macOS Apple Books SQLite+plist library.
No `.venv` present. Working tree clean; HEAD `0e28476`.

## Tree

```
/home/user/BookMinder
├── CLAUDE.md              13695  262L  Project dev guidelines (BDD/TDD, style, workflow) — authoritative
├── AGENTS.md              17675  247L  Same guidelines for other agents (keep in sync w/ CLAUDE.md)
├── GEMINI.md              14244  223L  Same guidelines for Gemini (keep in sync)
├── README.md               2643  122L  Install/usage/CI badge
├── TODO.md                 1828   37L  Backlog overview; "In Progress" = ATDD restoration of filters
├── vision.md               6140  132L  Current vision: AI product-dev benchmark + story-card format
├── ORIGINAL_VISION.md     11396  223L  Historical v1.0 "BookMind" spec (superseded)
├── LICENSE                 1071        MIT
├── pyproject.toml          2095   87L  Deps, entry point, pytest/mypy/ruff config
├── pytest.ini               104    5L  testpaths=specs, *_spec.py, describe_/it_ discovery
├── conftest.py              182    7L  Adds project root to sys.path
├── .gitignore               286   29L  venv, caches, egg-info, .claude/settings.local.json
├── .pre-commit-config.yaml  793   31L  ruff format/check + mypy; auto-stages only fixed files
├── xs -> claude-dev-log-diary/tools/explore_session.py  (symlink, RESOLVES — target exists)
│
├── bookminder/                    28K  Production package (only ~290 lines total)
│   ├── __init__.py           92    4L  Defines BookminderError base exception
│   ├── __main__.py          116    6L  `python -m bookminder` → cli.main
│   ├── cli.py              2797   96L  Click group: `list recent` / `list all`, --user/--filter, validate_filter, format
│   └── apple_books/
│       ├── __init__.py        0    0L  (intentionally empty)
│       └── library.py      5632  181L  CORE: BKLibrary sqlite + Books.plist reader; Book TypedDict,
│                                        list_recent_books/list_all_books/list_books/find_book_by_title,
│                                        SUPPORTED_FILTERS {cloud,!cloud,sample,!sample}, APPLE_EPOCH
│
├── specs/                        932K  Test suite (BDD, 4 layers, each __init__ documents its layer)
│   ├── __init__.py            0    0L
│   ├── unit/                        Pure logic, no I/O
│   │   ├── __init__.py      499   16L  Layer contract docstring
│   │   ├── cli_formatting_spec.py  2765  88L  format() output shaping
│   │   └── library_spec.py         3100  88L  Filter/parse logic w/ mocks
│   ├── integration/                 Real sqlite/plist fixtures
│   │   ├── __init__.py      622   16L  Layer contract docstring
│   │   ├── library_containers_spec.py  8200 207L  Edge cases: missing/corrupt DB, container variants
│   │   └── apple_books/
│   │       ├── __init__.py    0    0L
│   │       └── fixtures/          860K  ← see LAND MINES
│   │           ├── All_Books.swift          241255  4344L  Generated dump of real Books.plist (reference data)
│   │           ├── All_Books_20250627.swift 246960  4467L  Later snapshot of same
│   │           ├── Books.swift                4445    81L  Small readable sample of plist shape
│   │           ├── _common.sh                  283     7L  zsh path helper
│   │           ├── copy_book_to_fixture.sh    1932    53L  Copies a real book row into fixture DB
│   │           ├── create_fixture.sh          1288    42L  Creates empty fixture DB w/ correct schema
│   │           └── users/                     Synthetic $HOME trees per scenario:
│   │               ├── test_reader/           full: Books.plist 5910/150L + BKLibrary-fixture.sqlite 77824 (binary)
│   │               │                          + 401429854.epub (0 bytes, EMPTY placeholder)
│   │               ├── fresh_books_user/      Books.plist 369/15L + sqlite 8192 (binary, empty schema)
│   │               ├── legacy_books_user/     Books.plist 369/15L only (no iBooksX container)
│   │               ├── never_opened_user/     only .gitkeep in BKLibrary/
│   │               ├── corrupted_db_user/     0-byte plist + 0-byte sqlite (corruption case)
│   │               └── dummy_relative_user/   0-byte plist + 0-byte sqlite (relative-path case)
│   ├── acceptance/
│   │   ├── __init__.py      588   16L  Layer contract docstring
│   │   └── cli_spec.py     4987  130L  Click CliRunner, mocks library fns, asserts params/format calls
│   └── e2e/
│       ├── __init__.py      531   13L  Layer contract docstring
│       └── cli_wiring_spec.py 1462 49L  Single subprocess smoke test of full stack
│
├── stories/discover/              44K  9 YAML story cards (story/status/acceptance_criteria)
│   ├── list-recent-books.yaml            1033  24L  done (REOPENED: samples)
│   ├── list-recent-books-enhanced.yaml   1185  23L  backlog
│   ├── handle-user-environments.yaml     1521  30L  done
│   ├── filter-by-cloud-status.yaml        721  18L  done
│   ├── filter-by-sample-flag.yaml         903  25L  needs ATDD redo
│   ├── validate-filter-values.yaml        793  19L  needs ATDD redo
│   ├── filter-by-reading-status.yaml      917  24L  backlog
│   ├── filter-by-multiple-criteria.yaml   884  23L  backlog
│   └── pagination.yaml                    510  17L  backlog
│
├── docs/                         2.6M  (2.5M of it is docs/ui images)
│   ├── apple_books.md          26504  664L  ★ KEY REFERENCE: Apple Books data sources, DB schema, ZSTATE map
│   ├── modern_python_practices.md 10989 356L  General Python practice notes
│   ├── modern_python_distribution.md 4536 180L  Packaging/distribution guide
│   ├── python_best_practices.md  4957  107L  Setup-issue analysis
│   ├── test_fixtures.md          3737   83L  How fixtures/users trees are built and used
│   ├── project_structure.md      3269   82L  Config-file rationale
│   ├── uv_setup.md               2543  117L  uv venv setup (referenced by CLAUDE.md)
│   ├── pre-commit-workflow.md    1615   40L  Hook workflow
│   ├── github_setup.md           1609   53L  One-time GitHub remote setup (stale)
│   ├── yolo_mode_retrospective.md 6086 143L  Retrospective on autonomous-AI experiment
│   └── ui/apple/                 2.5M  15 JPEG/PNG screenshots of Apple Books UI (BINARY)
│
├── .claude/
│   ├── settings.json         502   25L  Registers PreCompact + PreToolUse hooks
│   ├── validate_git_commands.py 1102 36L  Blocks accidental staging of large files
│   ├── hooks/precompact_flag_hook.py        1069  36L  Sets post-compaction flag
│   ├── hooks/pretooluse_context_recovery_hook.py 2128 65L  Injects context recovery after compaction
│   ├── hooks/test_compaction_hooks.py       4158 124L  Manual test script for the two hooks
│   └── commands/{expert-council.md 1485/37L, hi.md 1038/36L}  Slash commands
│
├── .github/workflows/
│   ├── main.yml             1225   53L  CI: pytest + lint
│   ├── claude.yml           4914  136L  @claude mention bot
│   ├── claude-code-review.yml 3103  79L  Auto PR review
│   └── archive-claude-logs.yml 3873 115L  DISABLED (commit churn)
│
├── claude-dev-log-diary/         12M  83 files ← DO NOT READ (see LAND MINES)
└── .coordination/                     This map
```

## LAND MINES

| Hazard | Size | Rule |
|---|---|---|
| `claude-dev-log-diary/` | **12M**, 83 files | **DO NOT TOUCH.** Permission-gated transcripts; CLAUDE.md forbids access without explicit user consent. Measured with `du -sh` only. Contains `tools/` (the `xs` script), `tools/specs/`, `tools/docs/`. |
| `docs/ui/apple/*.jpg\|png` | 2.5M / 15 files | Binary screenshots. Largest: `Previous list p2.jpg` 488K, `Previous list.jpg` 398K, `Want to Read.jpg` 313K. Never Read/grep; reference by path only. |
| `specs/.../fixtures/All_Books_20250627.swift` | 247K / 4467L | Text but enormous, single-purpose generated data. |
| `specs/.../fixtures/All_Books.swift` | 241K / 4344L | Same. Grep with narrow patterns; never read whole. |
| `specs/.../test_reader/...BKLibrary-fixture.sqlite` | 78K | **Binary SQLite.** Query with `sqlite3`, never Read. |
| `docs/apple_books.md` | 26K / 664L | Largest doc. Read in excerpts (grep to section, then offset-Read). |
| `fresh_books_user/...sqlite` | 8192 | Binary SQLite (empty schema). |
| `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` | 14-18K each | Triplicated content — read ONE (CLAUDE.md), not all three. |
| Zero-byte traps | 0 bytes | `401429854.epub`, and all `corrupted_db_user` / `dummy_relative_user` plist+sqlite files are intentionally empty — that is the fixture's point, not corruption to fix. |
| `.git` | 4.3M | Normal; don't walk objects. |
| `xs` symlink | — | **NOT broken** — resolves to `claude-dev-log-diary/tools/explore_session.py`. But following it enters the forbidden dir: treat `./xs` as do-not-read (executing it per CLAUDE.md's documented usage is the sanctioned path). |
| `.venv` | absent | Environment not provisioned; `pytest` may need `uv venv && uv pip install -e ".[dev]"` first. |

## ACCESS STRATEGY

**safe-to-read-whole** (all <10K, cheap, high signal):
- `bookminder/**` (entire production package is ~290 lines — read it all, it's the cheapest way to ground any task)
- `specs/unit/*`, `specs/acceptance/*`, `specs/e2e/*`, `specs/integration/library_containers_spec.py`
- `stories/discover/*.yaml` (all 9 total ~7K), `TODO.md`, `pyproject.toml`, `pytest.ini`, `conftest.py`, `.pre-commit-config.yaml`, `.gitignore`
- `.claude/**`, `.github/workflows/*`, `README.md`, `vision.md`
- Fixture shell scripts and the small `Books.plist` / `Books.swift` files

**read-excerpts-only** (grep/offset first, never whole):
- `docs/apple_books.md` — the schema/ZSTATE reference; grep for the table or column name you need
- `CLAUDE.md` (262L) — read once per session, skip AGENTS.md/GEMINI.md duplicates
- `docs/modern_python_practices.md`, `ORIGINAL_VISION.md`, other docs — consult only if the task names them
- `All_Books*.swift` — `grep -n` for a specific key/title, then Read with `offset`/`limit`

**delegate-to-worker** (isolate the context burn in a subagent):
- Any question requiring a survey across both `All_Books*.swift` snapshots (e.g. "which fields changed?")
- Querying `BKLibrary-fixture.sqlite` contents (worker runs `sqlite3 ... ".schema"` / SELECTs and returns rows)
- Visual questions about `docs/ui/apple/` screenshots (worker Reads one image, returns a description)
- Full-suite `pytest` runs plus failure triage

**do-not-touch**:
- `claude-dev-log-diary/**` (permission-gated; ask the user first — CLAUDE.md is explicit)
- `./xs` as a file to read (invoke as documented tool instead)
- `.git/` internals, all files under `docs/ui/`
- Never `git add .` (CLAUDE.md rule; a hook actively blocks large-file staging)

## Orientation shortcuts
- Behavior spec of the whole system: `pytest --spec`.
- Feature entry point chain: `bookminder/cli.py` → `bookminder/apple_books/library.py`. Everything else is docs, fixtures, or process.
- Current work item per TODO.md: restore proper ATDD for `validate-filter-values`, `filter-by-sample-flag`, `filter-by-reading-status`.
