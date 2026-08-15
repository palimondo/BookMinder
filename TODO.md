# BookMinder TODO

This document serves as a high-level overview of the project backlog.
Detailed user stories and acceptance criteria are managed as YAML story cards
in the `stories/` directory, following the format defined in `vision.md`.

## Completed Features
- **List Recently Read Books via CLI:** (See `stories/discover/list-recent-books.yaml`) [REOPENED: needs to include samples]
- **Handle Diverse User Environments:** (See `stories/discover/handle-user-environments.yaml`)
- **ZSTATE Values for Cloud Status:** (Research completed, mapping updated in `docs/apple_books.md`)
- **Filter by Cloud Status:** (See `stories/discover/filter-by-cloud-status.yaml`)
- **Documentation Cleanup:** Removed retrospective AI meta-docs (commit eea59e3)
- **Validate Filter Values:** (See `stories/discover/validate-filter-values.yaml`) [REOPENED: outside-in lapse after 6f786cc — kept working code, debt is the vacuous-spec repair below]
- **Filter by Sample Flag:** (See `stories/discover/filter-by-sample-flag.yaml`) [REOPENED: same lapse — kept working code, debt is the vacuous-spec repair below]

## In Progress

### Reopened-filter spec repair
- **Ruling (2026-08-15):** keep the working post-6f786cc implementation; the process lapse (unit-first without an acceptance test, acceptance backfilled) left correct code with two vacuous specs. Full re-implementation rejected as costing ~35 production lines and ~10 green specs to repair 2 assertions.
- **Debt:** `library_spec.py it_filters_by_sample_status` and `cli_spec.py it_filters_recent_books_by_sample_status` pass vacuously — no fixture sample has reading progress, so `list recent --filter sample` matches nothing. Repair: copy a real in-progress sample into the fixture via `copy_book_to_fixture.sh` (author's machine), then tighten both assertions to exact expected titles.
- PR #18 (semantic revert) is superseded by this ruling and unmergeable since the spec-tree restore.

## Current Backlog (Stories in `stories/` directory)

### Discover Column
- `stories/discover/filter-by-reading-status.yaml`
- `stories/discover/filter-by-multiple-criteria.yaml`
- `stories/discover/list-recent-books-enhanced.yaml`
- `stories/discover/pagination.yaml`

## Future Features (High-Level)
1. MCP server interface
2. Extract highlights with context
3. Export to Markdown