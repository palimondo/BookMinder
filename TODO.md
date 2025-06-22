# BookMinder TODO

## Current Goal: List Recently Read Books via CLI

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