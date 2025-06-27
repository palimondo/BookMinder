# BookMinder TODO

This document serves as a high-level overview of the project backlog.
Detailed user stories and acceptance criteria are managed as YAML story cards
in the `stories/` directory, following the format defined in `vision.md`.

## Completed Features
- **List Recently Read Books via CLI:** (See `stories/discover/list-recent-books.yaml`)
- **Admin Access to Other Users' Libraries:** (See `stories/admin/access-other-users-libraries.yaml`)
- **Better Error Handling with ATDD:** (See `stories/error_handling/handle-missing-apple-books.yaml`)

## Current Backlog (Stories in `stories/` directory)

### Discover Column
- `stories/discover/list-recent-books-enhanced.yaml`
- `stories/discover/filter-by-sample-flag.yaml`
- `stories/discover/filter-by-cloud-status.yaml`
- `stories/discover/filter-by-reading-status.yaml`
- `stories/discover/pagination.yaml`

### Research
- `stories/research/zstate-cloud-mapping.yaml`

# BookMinder TODO

This document serves as a high-level overview of the project backlog.
Detailed user stories and acceptance criteria are managed as YAML story cards
in the `stories/` directory, following the format defined in `vision.md`.

## Completed Features
- **List Recently Read Books via CLI:** (See `stories/discover/list-recent-books.yaml`)
- **Handle Diverse User Environments:** (See `stories/discover/handle-user-environments.yaml`)

## Current Backlog (Stories in `stories/` directory)

### Discover Column
- `stories/discover/list-recent-books-enhanced.yaml`
- `stories/discover/filter-by-sample-flag.yaml`
- `stories/discover/filter-by-cloud-status.yaml`
- `stories/discover/filter-by-reading-status.yaml`
- `stories/discover/pagination.yaml`

## Research Backlog

### ZSTATE Values for Cloud Status

**Goal:** To definitively map `ZSTATE` values in `BKLibrary.sqlite` to the "Cloud" status of books in Apple Books UI.

**Hypothesis:** Specific `ZSTATE` integer values correspond to books that are in iCloud but not downloaded locally.

**Research Steps:**
1.  Identify books in Apple Books UI that are clearly in iCloud but not downloaded (showing a cloud icon).
2.  Query `BKLibrary.sqlite` for these specific books and record their `ZSTATE` values.
3.  Identify books that are downloaded locally and record their `ZSTATE` values.
4.  Compare `ZSTATE` values to infer their meaning (e.g., `ZSTATE = 5` might mean cloud-only, `ZSTATE = 1` might mean downloaded).

**Acceptance Criteria (for research outcome):**
- A clear mapping of `ZSTATE` values to "Cloud" status (e.g., `ZSTATE = 5` means cloud-only).
- Updated documentation in `docs/apple_books.md` with this mapping.

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


