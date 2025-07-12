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

## In Progress
- **Filter by Sample Flag:** (See `stories/discover/filter-by-sample-flag.yaml`) - Implementing !sample filter
- **Validate Filter Values:** (See `stories/discover/validate-filter-values.yaml`) - Adding validation for invalid filters

## Current Backlog (Stories in `stories/` directory)

### Discover Column
- `stories/discover/filter-by-reading-status.yaml`
- `stories/discover/filter-by-multiple-criteria.yaml`
- `stories/discover/list-recent-books-enhanced.yaml`
- `stories/discover/pagination.yaml`

## Key TDD Lessons Learned
- **Violation**: We added error handling WITHOUT tests first (violated TDD)
- **Violation**: We retrofitted tests for coverage (Coverage-Driven Development, not TDD)
- **Success**: Real data analysis helped remove unnecessary defensive code
- **Success**: 100% coverage achieved, but through wrong approach
- **Lesson**: Write acceptance tests for error cases FIRST

## Future Features (High-Level)
1. MCP server interface
2. Extract highlights with context
3. Export to Markdown