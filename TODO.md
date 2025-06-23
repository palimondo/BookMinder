# BookMinder TODO

## List Recently Read Books via CLI [COMPLETED]

### User Story
As a reader using Apple Books,  
I want to see my recently read books via command line,  
So that I can quickly check what I'm actively reading.

### Acceptance Criteria
```gherkin
Feature: List recent books
  Scenario: Show recently read books
    When I run "bookminder list recent"
    Then I see up to 10 books
    And each book shows: Title, Author, Progress %
    And books are ordered by last read date (newest first)
```

## NEXT: Better Error Handling with ATDD

### Missing Acceptance Tests for Error Cases
```gherkin
Feature: Handle missing Apple Books gracefully

  Scenario: User without Apple Books installed
    Given the Apple Books database does not exist
    When I run "bookminder list recent"
    Then I see a helpful message "No Apple Books database found"
    And the exit code is 0

  Scenario: User with corrupted Apple Books database
    Given the Apple Books database is corrupted
    When I run "bookminder list recent"
    Then I see a helpful message "Error reading Apple Books database"
    And the exit code is 0

  Scenario: User with Apple Books but no books in progress
    Given the Apple Books database exists
    But no books have reading progress > 0
    When I run "bookminder list recent"
    Then I see a message "No books currently being read"
    And the exit code is 0
```

### Key TDD Lessons Learned
- **Violation**: We added error handling WITHOUT tests first (violated TDD)
- **Violation**: We retrofitted tests for coverage (Coverage-Driven Development, not TDD)
- **Success**: Real data analysis helped remove unnecessary defensive code
- **Success**: 100% coverage achieved, but through wrong approach
- **Lesson**: Write acceptance tests for error cases FIRST

### Examples
```
$ bookminder list recent
The Pragmatic Programmer - Dave Thomas & Andy Hunt (73%)
Continuous Delivery - Dave Farley & Jez Humble (45%)
Test Driven Development - Kent Beck (22%)
```

### Edge Cases to Consider
- Books in iCloud but not downloaded locally
- Sample books from Book Store  
- PDFs and other non-book content
- Books never opened (0% progress)
- Finished books (100% progress)

## Future Features
1. CLI list recent ← current
2. MCP server interface
3. Extract highlights with context
4. Export to Markdown