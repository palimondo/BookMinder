# BookMinder TODO

This document serves as a high-level overview of the project backlog.
Detailed user stories and acceptance criteria are managed as YAML story cards
in the `stories/` directory, following the format defined in `vision.md`.

## Completed Features
- **List Recently Read Books via CLI:** (See `stories/discover/list-recent-books.yaml`)
- **Handle Diverse User Environments:** (See `stories/discover/handle-user-environments.yaml`)
- **ZSTATE Values for Cloud Status:** (Research completed, mapping updated in `docs/apple_books.md`)

## Current Backlog (Stories in `stories/` directory)

### Development Process Improvements
- **Prevent accidental staging**: Use [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) to create a PreToolUse hook that blocks `git add .` and `git add -A` commands in Bash tool calls. This will prevent the recurring issue of accidentally staging large fixture files like All_Books*.swift. The hook should check if the command contains these patterns and return a blocked message suggesting to stage files explicitly by name.

### Discover Column
- `stories/discover/filter-by-cloud-status.yaml` (Partially complete: cloud filtering done, negation pending)
- `stories/discover/filter-by-sample-flag.yaml`
- `stories/discover/filter-by-multiple-criteria.yaml`
- `stories/discover/filter-by-reading-status.yaml`
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