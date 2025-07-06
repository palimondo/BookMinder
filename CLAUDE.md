# BookMinder Development Guidelines

<core_philosophy>
## Core Programming Philosophy
- **Code is a liability, not an asset** - Minimize implementation while maximizing value
- **Executable specifications over documentation** - Tests document behavior and validate assumptions via Behavior-Driven Development (BDD) with `describe`/`it` style tests (RSpec/Jest-like)
- **Scientific approach** - Think hard and form a clear hypotheses before implementation
- **Disciplined engineering** - Apply evidence-based practices consistently
- **Minimize code** - Every line should justify its existence
- **Simple solutions** - Favor straightforward approaches over clever ones
- **YAGNI** - "You Aren't Gonna Need It" - Don't build features until required
- **Design for testability** - Structure code to enable isolated testing
</core_philosophy>

<implementation_process>
## Implementation Process
1. **Start with clear acceptance criteria**
   - Define precise, testable outcomes before writing any code
   - Document edge cases and expected behaviors
   - Focus on the "what" before the "how"

2. **Formulate working hypotheses**
   - Document assumptions about the problem space
   - Create small tests to validate each hypothesis
   - Use tests to explore the problem space methodically

3. **Value incremental progress**
   - Make small, focused changes
   - Commit frequently at stable points
   - Maintain working software throughout development

4. **Prioritize feedback loops**
   - Value fast, frequent feedback
   - Use tests as the primary feedback mechanism
   - Measure progress through working, tested features
</implementation_process>

<anti-patterns>
## Anti-patterns to Avoid
- Premature optimization
- Large untested implementations
- Complex solutions to simple problems
- Rushing to code without clear requirements
- Adding "just in case" functionality
- Prioritizing implementation over working tests
- Creating files that don't serve immediate requirements
- Adding unnecessary comments or docstrings
</anti-patterns>

<package_structure>
## Python Package Structure
- **Minimal Package Structure**: Only create directories and files needed for current functionality
- **Empty __init__.py Files**: Keep `__init__.py` files empty; they exist only to make Python's import system work
- **No Premature Modules**: Don't create modules until you have functionality to put in them
- **Avoid Boilerplate**: Don't add docstrings to empty `__init__.py` files or test files
- **No Implementation Without Tests**: Never create implementation files without corresponding tests
</package_structure>

<build_commands>
## Build Commands
- Setup uv (Recommended): See `docs/uv_setup.md`
  - Create virtual environment: `uv venv`
  - Activate: `source .venv/bin/activate`
  - Install development dependencies: `uv pip install -e ".[dev]"`
- Setup Pre-commit Hooks: `pre-commit install`
- Run: `python -m bookminder`
- **Test all (Fast Feedback)**: `pytest`
- **View Living Documentation**: `pytest --spec` (Use to understand requirements via test output)
- **Check Test Coverage**: `pytest --cov=bookminder --cov-report=term-missing`
- **Lint and Format** (manual):
  - Format: `ruff format .`
  - Lint: `ruff check --fix .`
  - Type check: `mypy .`
  - Run all checks: `pre-commit run --all-files`
</build_commands>

<code_style>
## Code Style
- **Python Version**: 3.13
- **Formatting and Linting**: Use ruff (max line length 88)
  - Automated via pre-commit hooks
  - Run formatter manually: `ruff format .`
  - Run linter manually: `ruff check --fix .`
- **Type Checking**: Use mypy for static type analysis
  - Automated via pre-commit hooks
  - Run manually: `mypy .`
- **Imports**: Group standard library, third-party, local imports; alphabetize within groups
- **Types**: Use type hints for all functions and parameters
- **Documentation**:
  - Prefer self-documenting code over verbose docstrings
  - Minimal, focused docstrings for complex functions only
  - **NEVER add redundant comments** that restate what the code already expresses
- **Error Handling**: Use specific exceptions with context; include meaningful error messages
- **Naming**: snake_case for functions/variables, CamelCase for classes, UPPERCASE for constants
- **Style**: Favor functional over procedural where appropriate; prioritize conciseness
- **Tests**:
  - Write tests first; focus on behavior, not implementation
  - Use `pytest-describe` syntax (`describe_...`/`it_...`) with descriptive names stating context and behavior
  - Docstring conventions:
    - Keep docstrings in skipped/pending tests as specifications to implement
    - Remove docstrings from implemented tests - the code IS the specification
    - Test names and assertions should tell the complete story without docstrings
  - Do not add comments in specs files that merely restate what the code is doing
  - Name spec files as `<module_name>_spec.py` following BDD conventions
  - Use `pytest --spec` to generate readable documentation from test structure
</code_style>

<requirements_gathering>
## Requirements Gathering
- Begin each feature with a requirements dialogue
- Structure the dialogue to establish:
  1. User's goal and expected outcome
  2. Necessary inputs and expected outputs
  3. Edge cases and error conditions
  4. Acceptance criteria in concrete terms
- Document requirements in the TODO.md file
- Translate requirements directly into acceptance tests using the BDD `describe`/`it` structure.
- Reference requirements in commit messages
</requirements_gathering>

<tdd_discipline>
## BDD/TDD Discipline
- Always start with a failing BDD acceptance test based on requirements.
  - We follow the **outside-in ATDD** approach: the acceptance test stays RED until the feature is fully implemented and that's OK. When it passes, we know the feature is complete.
- **Write Failing Test**: Define the next behavior using a `describe_...` / `it_...` structure and assertion.
- **Run & Verify RED**: Execute the *specific new test* (e.g., `pytest path/to/test.py::describe_context::it_behavior`) and confirm it fails.
- **Implement GREEN**: Write the minimum production code to pass the failing test.
- **Run All Tests**: Execute `pytest` to confirm success and no regressions.
- **Commit After GREEN**: Make first commit with passing test and minimal implementation.
- **Refactor**: Improve code while keeping all tests green.
- **Commit After Refactor**: Make second commit if any refactoring was done.
- **Coverage Check**: Verify code coverage (via `pytest --cov`) after implementation.
- **Update TODO.md**: Move completed stories to "Completed Features" section.
- Repeat cycle for each behavior.

### Implementation Checklist
Before writing any code, verify:
1. ✓ Do we have a clear requirement defined in TODO.md?
2. ✓ Have we written a failing test for this specific requirement?
3. ✓ Is the test descriptively named with `describe_`/`it_` structure?
4. ✓ Is the test focused on behavior (what) not implementation (how)?
5. ✓ Does the test actually verify meaningful behavior, not just types or structure?
6. ✓ Are assertions strong enough to catch real bugs or missing functionality?

Before implementing any feature, verify:
1. ✓ Have we run the test and confirmed it fails (RED)?
2. ✓ Is our planned implementation the minimal solution?
3. ✓ Are we following YAGNI principles (no "just in case" code)?
4. ✓ Are we only adding files and directories required NOW?

Before committing, verify:
1. ✓ Do all tests pass (GREEN)?
2. ✓ Have we removed redundant or unnecessary code?
3. ✓ Are we maintaining adequate test coverage?
4. ✓ Have we run linters and formatters (via pre-commit) to ensure code quality?
5. ✓ Have we removed ALL redundant comments and docstrings?
6. ✓ Does our commit message explain WHY (not just WHAT)?
7. ✓ Have we avoided adding unnecessary files?
8. ✓ Is our code self-documenting without relying on comments?
</tdd_discipline>

<session_workflow>
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
</session_workflow>

<backlog_management>
## Backlog Management
- User stories are defined as YAML files in the `stories/` directory
- Stories are organized by story map columns (e.g., `discover/`, `decide/`, `deliver/`)
- TODO.md provides a high-level overview with stories listed in suggested implementation order
- Story file names should be descriptive and action-oriented where it makes sense
- Test naming should flow naturally from story names:
  - Story: `filter-by-cloud-status.yaml`
  - Test describe: `describe_bookminder_list_with_filter()` (names the feature/command)
  - Test it: `it_filters_by_cloud_status()` (concise, matches story name)
- This creates a natural rhythm in `pytest --spec` output
- Implementation order in TODO.md should reflect natural feature progression and dependencies
- Mark stories as partially complete with specific notes about what remains
</backlog_management>

<git_workflow>
## Git Workflow
- Make two distinct commits in the TDD/BDD cycle:
  1. After GREEN phase (passing BDD test + minimal implementation).
  2. After REFACTOR phase (code improvements, tests still passing).
- Commit messages should be descriptive and explain the "why" behind changes
- Reference the specific requirements being addressed in commit messages
- Focus on what the change accomplishes, not just what files were modified
- Each commit should be small, focused, and preserve working state (all tests passing).
- Stage all files after running pre-commit hooks that modify files, to ensure fixes are included in commit
- Never use `git add .` - always stage files explicitly by name to avoid accidentally committing large or sensitive files
</git_workflow>

<project_maintenance>
## Project Maintenance
- Regularly verify the AI's model version in the pyproject.toml contributors list
- Update the contributors list whenever Claude is upgraded to a newer version
- Keep package metadata current and accurate in pyproject.toml
- Review docs/ directory content periodically to ensure documentation reflects current state
- Maintain LICENSE file with correct attribution and current year
- These instructions are duplicated in AGENTS.md and GEMINI.md for use with other agentic coding systems, therefore when updating these instructions, always ask the user if changes should be applied to CLAUDE.md, AGENTS.md, and GEMINI.md
</project_maintenance>

<file_operations>
## File Operations and Git Hygiene
- **Always use `git mv` for moving files**: When relocating tracked files, always use `git mv` instead of regular `mv` to maintain proper Git history
- **Place documentation in docs/ directory**: Keep all documentation files in the docs/ directory with lowercase, underscore-separated names
- **Never access `claude-dev-log-diary/` directory without first asking for explicit user permission**: This directory contains complete console transcripts (hundreds of KBs) for historical analysis
- **Verify each development step in isolation**: Test each step of the development workflow to ensure it works as expected before documenting it
- **Test project setup on a clean environment**: Regularly verify that project setup works correctly from scratch
- **Test commands in fresh shells**: Ensure all documented commands work in new terminal sessions
</file_operations>