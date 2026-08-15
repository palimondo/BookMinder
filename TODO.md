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

### Reopened filters: revert and redo through outside-in ATDD
- **Ruling (2026-08-15, revised same day):** the post-6f786cc filter implementations will be reverted and re-derived through the full outside-in process — story card first, failing acceptance test, then inward. The discipline is the point; working code derived unit-first without an acceptance test driving it is not kept on the strength of working.
- **Timing:** deferred until the compiled skills are ratified and in place — the redo then doubles as the first conditioned trial of the eval (same stories, proper process, skill-guided).
- **Kept now:** the story cards (refined requirements) stay, status reopened; implementation and specs stay in the tree untouched until the redo begins, so nothing is half-removed.
- PR #18 (the earlier semantic-revert attempt) is unmergeable since the spec-tree restore; only its intent carries forward into this plan.

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