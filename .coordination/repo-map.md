# BookMinder Repo Map

Generated for coordinator/worker navigation. Sizes in bytes, `L` = line count. Repo total **281M** — `.venv/` 121M (untracked), `claude-dev-log-diary/` 100M (90M of it `jsonl/`), `.git` 54M on disk (pack 4.6M, rest loose objects), `.coordination/` 2.8M, `docs/` 2.6M, `specs/` 428K, `.claude/` 548K, everything else <100K. Python 3.13 / uv / pytest-describe BDD project: CLI over the macOS Apple Books SQLite+plist library. Refreshed 2026-08-15 against HEAD `9658d23` (branch `claude/bookminder-recall-5ite2s`); working tree clean, `pytest` = 53 passed in 0.52s.

## Tree

```
/home/user/BookMinder
├── CLAUDE.md              13838  264L  Project dev guidelines (BDD/TDD, style, workflow) — authoritative
├── AGENTS.md -> CLAUDE.md         symlink (no longer a separate copy)
├── GEMINI.md -> CLAUDE.md         symlink (no longer a separate copy)
├── README.md               2643  122L  Install/usage/CI badge
├── TODO.md                 1828   37L  Backlog overview; "In Progress" = ATDD restoration of the three filter stories
├── vision.md               6140  132L  Current vision: AI product-dev benchmark + story-card format
├── ORIGINAL_VISION.md     11396  223L  Historical v1.0 "BookMind" spec (superseded)
├── LICENSE                 1071        MIT
├── pyproject.toml          2095   87L  Deps, entry point, pytest/mypy/ruff config
├── pytest.ini               104    5L  testpaths=specs, *_spec.py, describe_/it_ discovery
├── conftest.py              182    7L  Adds project root to sys.path
├── .gitignore               286   29L  venv, caches, egg-info, .claude/settings.local.json
├── .pre-commit-config.yaml  793   31L  ruff format/check + mypy; auto-stages only fixed files
├── xs -> claude-dev-log-diary/tools/explore_session.py  (symlink, RESOLVES — target exists)
├── .venv/                        121M  PROVISIONED (Python 3.13.12, package installed editable) — `pytest` runs as-is
│
├── bookminder/                    68K  Production package (~287 lines of source; rest is egg-info/pycache)
│   ├── __init__.py           92    4L  Defines BookminderError base exception
│   ├── __main__.py          116    6L  `python -m bookminder` → cli.main
│   ├── cli.py              2797   96L  Click group: `list recent` / `list all`, --user/--filter, validate_filter, format
│   └── apple_books/
│       ├── __init__.py        0    0L  (intentionally empty)
│       └── library.py      5632  181L  CORE: BKLibrary sqlite + Books.plist reader; Book TypedDict,
│                                        list_recent_books/list_all_books/list_books/find_book_by_title,
│                                        SUPPORTED_FILTERS {cloud,!cloud,sample,!sample}, APPLE_EPOCH
│
├── specs/                        428K  Test suite — CONCERN-BASED layout (the 4-layer unit/integration/
│   │                                   acceptance/e2e reorg was reverted at 315dce5; those dirs survive
│   │                                   only as stale untracked __pycache__ — ignore them)
│   ├── __init__.py            0    0L
│   ├── cli_spec.py         6093  167L  CliRunner acceptance specs: list commands, filter passthrough,
│   │                                    validation, error boundary, + describe_bookminder_integration
│   ├── cli_formatting_spec.py 2765 88L  describe_format / describe_format_book_list — output shaping
│   └── apple_books/
│       ├── __init__.py        0    0L
│       ├── library_spec.py 7842  209L  Unit specs w/ mocks: supported_filters, get_user_path,
│       │                                build_books_query, row_to_book, list_books, find_book_by_title,
│       │                                list_recent_books, list_all_books
│       ├── library_integration_spec.py 3146 77L  Real fixture trees: edge cases + list_all_books
│       └── fixtures/                          ← see LAND MINES
│           ├── Books.swift                4445  81L  Small readable sample of the plist shape
│           ├── _common.sh                  283   7L  zsh path helper
│           ├── copy_book_to_fixture.sh    1932  53L  Copies a real book row into fixture DB
│           ├── create_fixture.sh          1288  42L  Creates empty fixture DB w/ correct schema
│           └── users/                     Synthetic $HOME trees per scenario:
│               ├── test_reader/           full: Books.plist 5910 + BKLibrary-fixture.sqlite 77824 (binary)
│               │                          + 401429854.epub (0 bytes, EMPTY placeholder)
│               ├── fresh_books_user/      Books.plist 369 + sqlite 8192 (binary, empty schema)
│               ├── legacy_books_user/     Books.plist 369 only (no iBooksX container)
│               ├── never_opened_user/     only .gitkeep in BKLibrary/
│               ├── corrupted_db_user/     0-byte plist + 0-byte sqlite (corruption case)
│               └── dummy_relative_user/   0-byte plist + 0-byte sqlite (relative-path case)
│
├── stories/discover/              44K  9 YAML story cards (story/status/acceptance_criteria)
│   ├── list-recent-books.yaml            1033  24L  reopened (must include samples)
│   ├── handle-user-environments.yaml     1521  30L  done
│   ├── filter-by-cloud-status.yaml        721  18L  done
│   ├── filter-by-sample-flag.yaml         903  25L  done (TODO.md: wants ATDD redo)
│   ├── validate-filter-values.yaml        793  19L  done (TODO.md: wants ATDD redo)
│   ├── filter-by-reading-status.yaml      917  24L  backlog (TODO.md: wants proper ATDD)
│   ├── filter-by-multiple-criteria.yaml   884  23L  backlog
│   ├── list-recent-books-enhanced.yaml   1185  23L  backlog
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
│   └── ui/apple/                 2.5M  14 JPEG/PNG screenshots of Apple Books UI (BINARY)
│
├── .claude/                      548K
│   ├── settings.json         502   25L  Registers PreCompact + PreToolUse hooks ONLY
│   ├── validate_git_commands.py 1102 36L  Large-file staging guard — present but NO LONGER WIRED
│   │                                       (nothing in settings.json references it; settings.local.json absent)
│   ├── hooks/precompact_flag_hook.py        1069  36L  Sets post-compaction flag
│   ├── hooks/pretooluse_context_recovery_hook.py 2128 65L  Injects context recovery after compaction
│   ├── hooks/test_compaction_hooks.py       4158 124L  Manual test script for the two hooks
│   ├── commands/{expert-council.md 1485/37L, hi.md 1038/36L}  Slash commands (both still present)
│   ├── agents/               12K  Worker definitions used by Agent-tool delegation
│   │   ├── worker-opus.md       Default single-task worker (model opus, effort xhigh)
│   │   └── worker-fable.md      High-judgment worker for synthesis/comparison (model fable, xhigh)
│   └── skills/              492K  Project skills (compiled from the diary corpus)
│       ├── bookminder/       56K  SKILL 3029/27L + 4 refs — project memory: goals-and-history,
│       │                          apple-books-domain, repo-geography-and-fixtures (13956 — holds B-21),
│       │                          current-state-and-open-decisions
│       ├── tdd-bdd/          60K  SKILL 3709/29L + 6 refs (outside-in, writing-a-spec, assertion-integrity,
│       │                          layers-and-seams, minimal-implementation, cycle-and-commits)
│       ├── pair-programming/ 48K  SKILL 2398/26L + 4 refs (mirror, reciprocal, council, anti-patterns)
│       ├── project-coordinator/ 48K  SKILL 3979/35L + 6 refs (delegation, authorization, claims,
│       │                          liveness, persistence, register)
│       └── skill-creator/   276K  Vendored upstream tooling: SKILL 33351/485L, scripts/, agents/,
│                                  eval-viewer/ — read only when authoring/evaluating a skill
│
├── .coordination/                2.8M  Coordination workspace — the session's own working memory
│   ├── repo-map.md         20732  220L  THIS FILE (session-start census; `tree` unavailable on this infra)
│   ├── threads.md          47276  149L  ★ Session coordination log; HANDOFF block at top — read first
│   ├── verified-residue.md 22698  270L  Stamped repair backlog, verified against d6df0c9
│   ├── process-evolution.md 53195 322L  Meta-analysis: how the human+AI process was built, broke, repaired
│   ├── claude-experiments.md 37356 242L  Forensics of the two Claude-autonomy experiments
│   ├── bdd-style-canonical.md 37741 194L  ★ The prescriptive BDD style guide (rules + motivation)
│   ├── bdd-style-fable.md  24083   99L  Style doc variant B (Fable 5/xhigh, git-replay method)
│   ├── bdd-style-opus2.md  37819  211L  Style doc variant C (Opus 5/xhigh, same brief as B)
│   ├── style-comparison.md 15651   77L  Judge: A vs B
│   ├── style-comparison-3way.md 11861 64L  Judge: A vs B vs C (anti-anchoring protocol)
│   ├── commit-after-red-review.md 12960 57L  Adversarial review of the commit-after-RED rule
│   ├── eval-design.md       8698   73L  TDD-discipline eval design sketch (user-approved direction)
│   ├── diary-scout.md      15068  173L  Read-only recon of claude-dev-log-diary (no bulk reads)
│   ├── day-020-repair-plan.md 20749 136L  Adversarially reviewed design for the day-020 dedup repair
│   ├── day-020-repair-report.md 14080 75L  Execution record + gate results for that repair
│   ├── skill-removals-for-project-skills.md 6166 57L  Fragments pulled from project-coordinator, awaiting absorption
│   ├── recovered/SPECS_REVIEW.md 19235 325L  2025-10-04 test-suite organization review (recovered artifact)
│   ├── mining/             1.6M  Diary-mining harvest corpus (YAML)
│   │   ├── v2/             1.4M  24 files, schema v2.2 — day-002…day-021 (+ day-020 split s1–s5); the
│   │   │                          validated corpus behind every compiled rule. Individual files 30–70K.
│   │   ├── pairing/        168K  3 files (day-010/019/021) — council-fidelity trial harvest
│   │   └── v1/             104K  Superseded pilot (day-016, day-019, compiled-pilot.md)
│   ├── compile/            636K  Compile-phase record: how the three skills were built and verified
│   │   ├── briefs.md       28703  242L  Verbatim worker briefs (replicability record)
│   │   ├── contradiction-ledger.md 33826 240L  Conflicts across the corpus + their resolutions
│   │   ├── disposition-{tdd-bdd,pair-programming,bookminder}.md  Every corpus entry dispositioned
│   │   ├── rule-index-{tdd-bdd,pair-programming,bookminder}.md   Rule ID → source → provenance rank
│   │   ├── provenance-verification-*.md (8 files, 19–61K)  Transcript-level re-verification reports;
│   │   │                          each opens with a NOTE mapping its line refs onto the repaired day-files
│   │   ├── skill-v2-changelog-*.md (3 files)  Judge passes that produced the v2 skills
│   │   └── pending-claude-md.md 13109 101L  claude-md-targeted rules with no compile owner (gardening input)
│   └── tools/               84K  rule.py (provenance toolkit), validate_mining.py (schema gate),
│                                 dupescan.py, diary-mining-full-v2.{1,2}.js + mining-slice-v2.2.js
│                                 (Workflow scripts), day-007-remap.md / day-020-remap.md (line remaps)
│
├── .github/workflows/
│   ├── main.yml             1225   53L  CI: pytest + lint
│   ├── claude.yml           4914  136L  @claude mention bot
│   ├── claude-code-review.yml 3103  79L  Auto PR review
│   └── archive-claude-logs.yml 3873 115L  DISABLED (commit churn)
│
└── claude-dev-log-diary/         100M  421 files ← PERMISSION-GATED (see LAND MINES)
    ├── README.md            3576   66L  Archive guide + "Repaired files" section (day-020, day-007)
    ├── day-001…day-021.md    10M  Hand-curated console transcripts; largest day-011 1.9M, day-020 1.5M
    │                              (repaired 2026-08-15, −23,710 dup lines), day-016 1.1M, day-021 700K,
    │                              day-007 300K (repaired 2026-08-15, −1,450 dup lines, 1 line restored)
    ├── gemini-summary-day-*.md  10 files, 11–16K each  Per-pair day summaries
    ├── moments_of_clarity.md 3254        Curated highlights
    ├── jsonl/                90M  Native session transcripts (README 2831/31L)
    │   └── cloud-2026/       90M  336 files — this session's `.jsonl` main thread plus subagents/,
    │                              workflows/, tool-results/; layout mirrors /root/.claude/projects/
    └── tools/               652K  The `xs` suite: explore_session.py, fetch_logs.py, parse_claude_jsonl.py,
                                   reconstruct.jq, plus tools/specs 408K and tools/docs 24K
```

## LAND MINES

| Hazard | Size | Rule |
|---|---|---|
| `claude-dev-log-diary/` | **100M**, 421 files | **PERMISSION-GATED.** Governed by the bookminder skill's **B-21** (`.claude/skills/bookminder/references/repo-geography-and-fixtures.md`) — read that rule before any access. In short: explicit user consent first, grants are scoped to the exact excerpt and manner named, never from a background subagent. Measured here with `du -sh` only. |
| `claude-dev-log-diary/jsonl/cloud-2026/` | **90M**, 336 files | New since the last map and the bulk of the repo's tracked weight. Machine-readable session transcripts; same B-21 gate. Grep/`jq` narrow slices only — never whole-file reads. |
| Repaired day-files | day-020 1.5M, day-007 300K | Both deduplicated 2026-08-15. **Any line reference written before that date points at the pre-repair file.** Remaps: `.coordination/tools/day-020-remap.md`, `day-007-remap.md`; pre-repair blobs recoverable per `claude-dev-log-diary/README.md` §Repaired files. |
| `docs/ui/apple/*.jpg\|png` | 2.5M / 14 files | Binary screenshots. Largest: `Previous list p2.jpg` 488K, `Previous list.jpg` 398K, `Want to Read.jpg` 313K. Never Read/grep; reference by path only. |
| `.coordination/mining/v2/*.yaml` | 1.4M / 24 files | Individual files 30–70K. The validated corpus — grep or `rule.py` first; a full read is a context burn. |
| `.coordination/compile/provenance-verification-*.md` | 19–61K each | Long evidence reports. Grep to the rule ID you need; heed each file's opening NOTE about pre-repair line refs. |
| `specs/.../All_Books*.swift` | absent here | Deliberately untracked per B-21 and **not present in this checkout**. Do not gitignore them, do not stage them, do not regenerate them to "fix" the absence. |
| `specs/.../test_reader/...BKLibrary-fixture.sqlite` | 77824 | **Binary SQLite.** Query with `sqlite3`, never Read. |
| `fresh_books_user/...sqlite` | 8192 | Binary SQLite (empty schema). |
| `docs/apple_books.md` | 26504 / 664L | Largest doc. Read in excerpts (grep to section, then offset-Read). |
| `AGENTS.md` / `GEMINI.md` | symlinks | Both now point at `CLAUDE.md` — reading them is reading the same file. Read `CLAUDE.md` once. |
| `.claude/skills/skill-creator/` | 276K | Vendored upstream; SKILL.md alone is 485L. Open only when authoring or evaluating a skill. |
| Zero-byte traps | 0 bytes | `401429854.epub`, and all `corrupted_db_user` / `dummy_relative_user` plist+sqlite files are intentionally empty — that is the fixture's point, not corruption to fix. |
| Stale `__pycache__` under `specs/{unit,integration,acceptance,e2e}/` | ~130K | Leftovers from the reverted 4-layer reorg. Untracked, ignored — do not mistake them for a live spec layout. |
| `.git` | 54M on disk | Pack is only 4.6M; the rest is loose objects from recent commits. Don't walk objects. |
| `xs` symlink | — | **NOT broken** — resolves into the gated diary directory. Execute it as the documented tool; do not Read it as a file. |

## ACCESS STRATEGY

**safe-to-read-whole** (all <10K, cheap, high signal):
- `bookminder/**` (entire production package is ~287 lines — read it all, it's the cheapest way to ground any task)
- `specs/**/*_spec.py` (four files, 2.7–7.8K each) and the fixture shell scripts / small `Books.plist` / `Books.swift`
- `stories/discover/*.yaml` (all 9 total ~8K), `TODO.md`, `pyproject.toml`, `pytest.ini`, `conftest.py`, `.pre-commit-config.yaml`, `.gitignore`
- `.claude/settings.json`, `.claude/agents/*`, `.claude/commands/*`, `.claude/hooks/*`, `.github/workflows/*`, `README.md`, `vision.md`
- Any single `.claude/skills/{bookminder,tdd-bdd,pair-programming,project-coordinator}/**` file — load the SKILL.md, then only the reference it points you to

**read-excerpts-only** (grep/offset first, never whole):
- `docs/apple_books.md` — the schema/ZSTATE reference; grep for the table or column name you need
- `CLAUDE.md` (264L) — read once per session; `AGENTS.md`/`GEMINI.md` are symlinks to it
- `.coordination/threads.md` (149L but 47K) — read the HANDOFF block first, then grep for your thread ID
- `.coordination/bdd-style-canonical.md`, `process-evolution.md`, `claude-experiments.md`, `verified-residue.md` — grep to the section
- `.coordination/mining/**`, `.coordination/compile/**` — grep by rule ID / loc, then offset-Read
- `ORIGINAL_VISION.md` and the remaining `docs/*.md` — consult only if the task names them

**delegate-to-worker** (isolate the context burn in a subagent):
- Any survey across the mining corpus or the compile reports (e.g. "which rules cite day-016?")
- Querying `BKLibrary-fixture.sqlite` contents (worker runs `sqlite3 ... ".schema"` / SELECTs and returns rows)
- Visual questions about `docs/ui/apple/` screenshots (worker Reads one image, returns a description)
- Full-suite `pytest` runs plus failure triage
- NOT diary reads — B-21 forbids background-subagent access to `claude-dev-log-diary/` outright

**do-not-touch**:
- `claude-dev-log-diary/**` without a scoped grant (B-21; that includes indirect exposure via `git diff`/`git show`/`git log -p`)
- `./xs` as a file to read (invoke as documented tool instead)
- `.git/` internals, all files under `docs/ui/`, `.venv/`, `bookminder.egg-info/`, any `__pycache__/`
- Never `git add .` (CLAUDE.md rule — and note the old staging guard `validate_git_commands.py` is no longer wired to a hook, so nothing enforces it for you)

## Orientation shortcuts
- Behavior spec of the whole system: `pytest --spec`. The suite is green as of this map: 53 passed, `.venv` already provisioned — no setup step needed.
- Feature entry point chain: `bookminder/cli.py` → `bookminder/apple_books/library.py`. Everything else is docs, fixtures, or process.
- Session start: load the `bookminder` skill (project memory), then read the HANDOFF block at the top of `.coordination/threads.md`.
- Current work item per TODO.md: restore proper ATDD for `validate-filter-values`, `filter-by-sample-flag`, `filter-by-reading-status` — note the first two are marked `status: done` in their story cards, so the card status and TODO.md disagree by design (the redo is about spec quality, not missing behavior).
