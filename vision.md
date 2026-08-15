# BookMinder Vision: AI Product Development Benchmark

## Overview

BookMinder is two things at once: a working tool that extracts content and highlights from Apple Books for LLM analysis, and a live benchmark for AI-augmented product development. The benchmark tests AI collaboration across the entire product lifecycle - from product vision to working software - under strict BDD/ATDD/TDD discipline.

## The Empirical Thesis

The project exists to test a bet: that BDD/ATDD/TDD process discipline leads to measurably better architecture, because the discipline provides more learning opportunities to discover more optimal solutions. It creates a better environment for requirements discovery and forces co-evolution of the executable specification alongside the implementation - the spec and the code improve each other instead of one trailing the other.

The thesis carries a precondition: LLMs, or the harnesses around them, must be able to encode and enforce the process - walk the walk, not merely describe it. How much enforcement the harness must supply at each step is itself an open question the benchmark probes: an enforcement ladder from bare instructions up to hard tooling.

The testbed is chosen deliberately. The Apple Books database schema evolves with each release, so the project tests long-term software evolution - the opposite of one-shotting problems the model already knows from pretraining.

### Comparative Axes

- **Model x harness**: can cheaper models perform each step of the process under stronger harnesses? The target is the Pareto frontier on performance, cost, and speed - not a single champion model.
- **Language**: is one programming language better suited than another for this process?
- **Library**: does one library produce better results than another?

## Why Books: Product Feeds Process

Pretrained simulacra of TDD/BDD experts proved shallow - skewed, non-actionable summaries of real positions. A core BookMinder motivation is giving the model access to full books as consultation material, so actionable principles can be extracted from primary sources rather than from what survived pretraining summarization. The product (book access) feeds the process (disciplined development) that builds the product.

## The Story Mapping Approach

Following Jeff Patton's User Story Mapping methodology, BookMinder structures product development as a user journey with vertical slices of functionality.

### User Journey (Walking Skeleton)

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Discover   │ │   Access    │ │   Review    │ │   Export    │
│   Books     │ │  Content    │ │ Highlights  │ │   Share     │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
      │               │               │               │
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│List recent  │ │Open book at │ │View my      │ │Export to    │ [MVP]
│books ✓      │ │last position│ │highlights   │ │Markdown     │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
      │               │               │               │
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│Filter by    │ │Extract page │ │Add context  │ │Sync to      │ [Enhancement]
│collection   │ │content      │ │to highlight │ │Obsidian     │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

### Story Card Format

Each story contains full context - the who, what, and why - along with concrete acceptance criteria:

```yaml
# stories/discover/list-recent-books.yaml
story:
  as_a: reader using Apple Books
  i_want: to see my recently read books via command line
  so_that: I can quickly check what I'm actively reading
  
acceptance_criteria:
  - scenario: Show recently read books
    when: I run "bookminder list recent"
    then:
      - I see up to 10 books
      - Each book shows: Title, Author, Progress %
      - Books are ordered by last read date (newest first)
      
  - scenario: Handle missing Apple Books
    given: Apple Books is not installed
    when: I run "bookminder list recent"
    then: I see "No Apple Books database found"
```

## Three-Level Benchmark

Each level can be run across the comparative axes above - varying the model tier and the rung of the enforcement ladder - to locate where discipline survives and where it needs harness support.

### Level 1: Product Owner Augmentation
- **Input**: High-level product vision and user needs
- **AI Task**: Create story map and break down into story cards
- **Output**: Structured story cards with acceptance criteria
- **Evaluation**: Do stories cover user journey? Are they properly sized? Is context clear?

### Level 2: Technical Translation
- **Input**: Story cards with acceptance criteria
- **AI Task**: Convert to executable specifications
- **Output**: `describe_`/`it_` spec skeletons ready for outside-in BDD
- **Evaluation**: Do specs capture all acceptance criteria? Are they testable?

### Level 3: Implementation
- **Input**: Executable specifications
- **AI Task**: Implement code following TDD discipline
- **Output**: Working software with comprehensive tests
- **Evaluation**: Do all acceptance tests pass? Is coverage complete? Is code maintainable? Did the process hold - and does the resulting architecture show it?

## Value Proposition

### For AI Researchers
- Tests AI understanding across abstraction levels
- Provides clear evaluation criteria at each stage
- Creates reproducible benchmark scenarios

### For Product Owners
- Demonstrates AI augmentation of product thinking
- Shows how AI can help translate vision to specifications
- Provides patterns for effective AI collaboration

### For Development Teams
- Tests real-world development workflow
- Emphasizes TDD/BDD discipline
- Creates living documentation through examples

## Project Structure

```
BookMinder/
├── vision.md                 # This file - product vision and benchmark thesis
├── stories/                  # User story cards (YAML format)
│   └── discover/             # First journey column; later columns added when reached
│       ├── list-recent-books.yaml
│       └── ...
├── bookminder/               # Implementation: cli.py → apple_books/library.py
└── specs/                    # Executable specifications (pytest-describe, organized by concern)
    ├── cli_spec.py
    ├── cli_formatting_spec.py
    └── apple_books/
        ├── library_spec.py
        └── library_integration_spec.py
```

## Next Steps

1. Complete MVP stories in the Discover column
2. Document benchmark evaluation criteria
3. Create example runs showing AI performance at each level
4. Open source as reference implementation for AI product development

## Key Principles

- **Start with user value**: Every story must connect to user needs
- **Maintain traceability**: Vision → Stories → Specs → Code
- **Test at every level**: Not just code, but product thinking
- **Document learnings**: What works and doesn't in AI collaboration

This vision transforms BookMinder from a utility into a framework for understanding and improving AI-augmented product development.
