# BookMinder TODO

## List Recently Read Books via CLI [COMPLETED]

### User Story
As a reader using Apple Books,  
I want to see my recently read books via command line,  
So that I can quickly check what I'm actively reading.

### Acceptance Criteria
```gherkin
Feature: List recent books
  Scenario: Show recently read books with enhanced properties
    When I run "bookminder list recent"
    Then I see up to 10 books
    And each book shows: Title, Author, Progress %, Content Type, Sample status, and Cloud status
    And books are ordered by last read date (newest first)
    And Content Type is "Book" for EPUBs and "PDF" for PDFs
    And Sample status is indicated by "Sample" if applicable
    And Cloud status is indicated by "☁️" if applicable
    Examples:
      | Output Format                                                              |
      | "The Left Hand of Darkness - Ursula K. Le Guin (32%) Book"                 |
      | "Tiny Experiments - Anne-Laure Le Cunff (1%) Book Sample"                  |
      | "Lao Tzu: Tao Te Ching - Ursula K. Le Guin (8%) Book ☁️"                   |
      | "record-layer-paper - Christos Chrysa... (1%) PDF ☁️"                      |
      | "Snow Crash - Neal Stephenson (0%) Book Sample ☁️"                       |
      | "MELITTA CAFFEO SOLO - Unknown Author (100%) PDF"                          |
```

## Admin Access to Other Users' Libraries [COMPLETED]

### User Story
As a system administrator,
I want to examine another user's Apple Books library,
So that I can help troubleshoot issues or manage shared devices.

### Acceptance Criteria
```gherkin
Feature: Access other users' Apple Books libraries
  
  Scenario: Admin examines another user's books
    When I run "bookminder list recent --user alice"
    Then I see alice's recently read books
    
  Scenario: User who never opened Apple Books
    When I run "bookminder list recent --user never_opened_user"
    Then I see "Apple Books not found. Has it been opened on this account?"
    
  Scenario: User with empty library
    When I run "bookminder list recent --user fresh_books_user"
    Then I see "No books currently being read"
    
  Scenario: User with legacy installation (missing database)
    When I run "bookminder list recent --user legacy_books_user"
    Then I see "Apple Books database not found."
```

### Implementation Notes
- Discovered through testing needs - tests couldn't use real Apple Books data
- Implemented as --user parameter to specify which user's library to examine
- Created test fixtures for different user scenarios based on real-world validation
- Feature serves dual purpose: testing infrastructure and legitimate admin use case

## NEXT: Better Error Handling with ATDD [CR]

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

## Research: ZSTATE Values for Cloud Status

### Goal
To definitively map `ZSTATE` values in `BKLibrary.sqlite` to the "Cloud" status of books in Apple Books UI.

### Hypothesis
Specific `ZSTATE` integer values correspond to books that are in iCloud but not downloaded locally.

### Research Steps
1.  Identify books in Apple Books UI that are clearly in iCloud but not downloaded (showing a cloud icon).
2.  Query `BKLibrary.sqlite` for these specific books and record their `ZSTATE` values.
3.  Identify books that are downloaded locally and record their `ZSTATE` values.
4.  Compare `ZSTATE` values to infer their meaning (e.g., `ZSTATE = 5` might mean cloud-only, `ZSTATE = 1` might mean downloaded).

### Acceptance Criteria (for research outcome)
- A clear mapping of `ZSTATE` values to "Cloud" status (e.g., `ZSTATE = 5` means cloud-only).
- Updated documentation in `docs/apple_books.md` with this mapping.
