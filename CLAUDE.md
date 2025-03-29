# BookMinder Development Guidelines

## Build Commands
- Setup: `pip install -r requirements.txt`
- Run: `python bookminder.py`
- Test all: `pytest`
- Single test: `pytest tests/test_file.py::test_function`
- Test coverage: `pytest --cov=bookminder`
- Lint: `flake8`
- Type check: `mypy .`

## Code Style
- **Python Version**: 3.9+
- **Formatting**: Follow PEP 8, max line length 88 (Black)
- **Imports**: Group standard library, third-party, local imports; alphabetize within groups
- **Types**: Use type hints for all functions and parameters
- **Documentation**: 
  - Prefer self-documenting code over verbose docstrings
  - Minimal, focused docstrings for complex functions only
- **Error Handling**: Use specific exceptions with context; include meaningful error messages
- **Naming**: snake_case for functions/variables, CamelCase for classes, UPPERCASE for constants
- **Style**: Favor functional over procedural where appropriate; prioritize conciseness
- **Tests**: Write tests first; focus on behavior, not implementation

## Requirements Gathering
- Begin each feature with a requirements dialogue
- Structure the dialogue to establish:
  1. User's goal and expected outcome
  2. Necessary inputs and expected outputs
  3. Edge cases and error conditions
  4. Acceptance criteria in concrete terms
- Document requirements in the TODO.md file
- Translate requirements directly into acceptance tests
- Reference requirements in commit messages

## TDD Discipline
- Always start with a failing acceptance test based on gathered requirements
- Verify each test fails (RED) before implementing
- Document the nature of test failures before fixing
- Implement only what's needed to make tests pass (GREEN)
- Refactor only after tests pass, never during implementation
- Verify test coverage - no implementation without a failing test first
- Follow the TDD cycle workflow:
  1. Gather requirements and document them
  2. Write a failing acceptance test
  3. Write a failing unit test
  4. Make the test pass
  5. Refactor
  6. Repeat steps 3-5 until acceptance test passes
  7. Update TODO.md to reflect progress

## Session Workflow
- Start sessions with clear, limited scope
- Define acceptance criteria upfront through requirements dialogue
- Save logs after completing acceptance tests
- Use `/clear` to reset context after major milestones
- Commit code before clearing context
- Keep implementation incremental and focused
- Batch related tool calls where possible
- Monitor token usage during development
- Maintain TODO.md as a living document of progress and priorities

## Git Workflow
- Make two distinct commits in the TDD cycle:
  1. After GREEN phase (tests + minimal implementation)
  2. After REFACTOR phase (code improvements)
- Commit messages should be descriptive and explain the "why" behind changes
- Reference the specific requirements being addressed in commit messages
- Focus on what the change accomplishes, not just what files were modified
- Each commit should be small, focused, and preserve working state
- No implementation should be written without its corresponding test first