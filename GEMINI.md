# BookMinder Development Guidelines for Gemini

## Project Overview
This project, BookMinder, is a Python tool designed to extract content and highlights from Apple Books, primarily for analysis with Large Language Models (LLMs). As an AI agent, I will focus on data extraction and processing from Apple's ecosystem and adhere to the specific coding practices outlined in this document.

## Core Programming Philosophy
- **Code is a liability, not an asset**: Minimize implementation while maximizing value.
- **Executable specifications over documentation**: Tests document behavior and validate assumptions via Behavior-Driven Development (BDD) with `describe`/`it` style tests.
- **Scientific approach**: Form clear hypotheses before implementation.
- **Disciplined engineering**: Apply evidence-based practices consistently.
- **Minimize code**: Every line should justify its existence.
- **Simple solutions**: Favor straightforward approaches over clever ones.
- **YAGNI**: "You Aren't Gonna Need It" - Don't build features until required.
- **Design for testability**: Structure code to enable isolated testing.

## Implementation Process
1.  **Start with clear acceptance criteria**: Define precise, testable outcomes before writing any code. Focus on the "what" before the "how".
2.  **Formulate working hypotheses**: Document assumptions and create small tests to validate each hypothesis.
3.  **Value incremental progress**: Make small, focused changes and commit frequently at stable points.
4.  **Prioritize feedback loops**: Value fast, frequent feedback, primarily through tests.

## Anti-patterns to Avoid
- Premature optimization.
- Large untested implementations.
- Complex solutions to simple problems.
- Rushing to code without clear requirements.
- Adding "just in case" functionality.
- Prioritizing implementation over working tests.
- Creating files that don't serve immediate requirements.
- Adding unnecessary comments or docstrings.

## Python Package Structure
- **Minimal Package Structure**: Only create directories and files needed for current functionality.
- **Empty __init__.py Files**: Keep `__init__.py` files empty; they exist only to make Python's import system work.
- **No Premature Modules**: Don't create modules until you have functionality to put in them.
- **Avoid Boilerplate**: Don't add docstrings to empty `__init__.py` files or test files.
- **No Implementation Without Tests**: Never create implementation files without corresponding tests.

## Build Commands
- **Activate environment**: `source .venv/bin/activate` (always required).
- **Test all (Fast Feedback)**: `pytest`
- **View Living Documentation**: `pytest --spec` (Use to understand requirements via test output).
- **Check Test Coverage**: `pytest --cov=bookminder --cov-report=term-missing`
- **Lint and Format**:
    - Format: `ruff format .`
    - Lint: `ruff check --fix .`
    - Type check: `mypy .`
    - Run all checks (via pre-commit): `pre-commit run --all-files`

## Code Style
- **Python Version**: 3.13.
- **Formatting and Linting**: Use `ruff` (max line length 88).
- **Type Checking**: Use `mypy` for static type analysis.
- **Imports**: Group standard library, third-party, local imports; alphabetize within groups.
- **Types**: Use type hints for all functions and parameters.
- **Documentation**: Prefer self-documenting code. Minimal, focused docstrings for complex functions only. NEVER add redundant comments.
- **Error Handling**: Use specific exceptions with context; include meaningful error messages.
- **Naming**: `snake_case` for functions/variables, `CamelCase` for classes, `UPPERCASE` for constants. Test functions should follow BDD style: `describe_context_or_class` and `it_should_behave_this_way`.
- **Style**: Favor functional over procedural where appropriate; prioritize conciseness.
- **Tests**: Write tests first; focus on behavior, not implementation. Use `pytest-describe` syntax. Do not add docstrings or comments in specs files. Name spec files as `<module_name>_spec.py`.

## Requirements Gathering
- Begin each feature with a requirements dialogue to establish:
    1.  User's goal and expected outcome.
    2.  Necessary inputs and expected outputs.
    3.  Edge cases and error conditions.
    4.  Acceptance criteria in concrete terms.
- Document requirements in the `TODO.md` file.
- Translate requirements directly into acceptance tests using the BDD `describe`/`it` structure.

## BDD/TDD Discipline
- Always start with a failing BDD acceptance test.
- **Write Failing Test**: Define the next behavior using a `describe_...` / `it_...` structure and assertion.
- **Run & Verify RED**: Execute the specific new test and confirm it fails.
- **Implement GREEN**: Write the minimum production code to pass the failing test.
- **Run All Tests**: Execute `pytest` to confirm success and no regressions.
- **Commit After GREEN**: Make first commit with passing test and minimal implementation.
- **Refactor**: Improve code while keeping all tests green.
- **Commit After Refactor**: Make second commit if any refactoring was done.
- **Coverage Check**: Verify code coverage after implementation.
- **Update TODO.md**: Move completed stories to "Completed Features" section.
- Repeat cycle for each behavior.

### Implementation Checklist (Before writing any code)
1.  ✓ Do we have a clear requirement defined in `TODO.md`?
2.  ✓ Have we written a failing test for this specific requirement?
3.  ✓ Is the test descriptively named with `describe_`/`it_` structure?
4.  ✓ Is the test focused on behavior (what) not implementation (how)?
5.  ✓ Does the test actually verify meaningful behavior, not just types or structure?
6.  ✓ Are assertions strong enough to catch real bugs or missing functionality?

### Implementation Checklist (Before implementing any feature)
1.  ✓ Have we run the test and confirmed it fails (RED)?
2.  ✓ Is our planned implementation the minimal solution?
3.  ✓ Are we following YAGNI principles (no "just in case" code)?
4.  ✓ Are we only adding files and directories required NOW?

### Implementation Checklist (Before committing)
1.  ✓ Do all tests pass (GREEN)?
2.  ✓ Have we removed redundant or unnecessary code?
3.  ✓ Are we maintaining adequate test coverage?
4.  ✓ Have we run linters and formatters (via pre-commit) to ensure code quality?
5.  ✓ Have we removed ALL redundant comments and docstrings?
6.  ✓ Does our commit message explain WHY (not just WHAT)?
7.  ✓ Have we avoided adding unnecessary files?
8.  ✓ Is our code self-documenting without relying on comments?

## Session Workflow
- Start sessions with clear, limited scope.
- Define acceptance criteria upfront through requirements dialogue.
- Save logs after completing acceptance tests.
- Use `/clear` to reset context after major milestones.
- Commit code before clearing context.
- Keep implementation incremental and focused.
- Batch related tool calls where possible.
- Monitor token usage during development.
- Maintain `TODO.md` as a living document of progress and priorities.

## Story Management
To effectively manage the project backlog and track progress, we utilize YAML story cards.

### Story Card Structure
Each story card is a YAML file (e.g., `stories/discover/my-new-feature.yaml`) with the following structure:

```yaml
story:
  as_a: <user role>
  i_want: <what they want to achieve>
  so_that: <why they want it>
status: <current status of the story>

acceptance_criteria:
  - scenario: <scenario description>
    when: <precondition or action>
    then: <expected outcome>
    # Optional: and, given, but clauses as needed
```

### Status Field
The `status` field is mandatory for each story card and indicates its current state. Possible values include:

-   `backlog`: The story is defined but not yet started.
-   `in_progress`: Development has begun.
-   `done`: The story is fully implemented, tested, and deployed.
-   `reopened`: Previously done story that needs further refinement or implementation changes.
-   `research`: For research stories, indicating active investigation.

This system ensures clarity, machine-readability, and granular progress tracking for each story.

## Git Workflow
- Make two distinct commits in the TDD/BDD cycle:
    1.  After GREEN phase (passing BDD test + minimal implementation).
    2.  After REFACTOR phase (code improvements, tests still passing).
- Commit messages should be descriptive and explain the "why" behind changes.
- Reference the specific requirements being addressed in commit messages.
- Focus on what the change accomplishes, not just what files were modified.
- Each commit should be small, focused, and preserve working state (all tests passing).
- Stage all files after running pre-commit hooks that modify files, to ensure fixes are included in commit.
- Never use `git add .` - always stage files explicitly by name to avoid accidentally committing large or sensitive files.

### Pre-Commit Hook Behavior
This project uses `pre-commit` hooks with `ruff` for linting and formatting. When you attempt to commit, these hooks run automatically.

- **`ruff` (linter):** Runs `ruff check --fix`. If it finds fixable issues, it modifies the files in your working directory.
- **`ruff-format` (formatter):** Runs `ruff format`. If it finds formatting changes, it modifies the files in your working directory.

If any hook modifies a staged file, `pre-commit` will fail the commit and inform you that files were modified. This is a deliberate design to ensure you explicitly stage the changes made by the hooks.

**Strategy for Committing:**
It is common to need to attempt a commit multiple times when `ruff-format` makes changes. The typical workflow is:
1.  Make your code changes and `git add` them.
2.  Run `git commit`.
3.  If the commit fails due to `ruff-format` modifying files, `pre-commit` will report this.
4.  Immediately run `git commit` again. Often, the second attempt will succeed as `ruff-format` has already applied its changes and the files are now in the desired format.

If the commit continues to fail, ensure your local `ruff` version is up-to-date and that there are no conflicting local editor settings that might be re-formatting files after `ruff` runs.

## Project Contribution
When contributing to the project, it is important to give proper credit to the contributor.

### Adding a Contributor
1.  Add the contributor to the `authors` list in `pyproject.toml`.
2.  The format for an AI contributor is `{name = "<Full Model Name> (<model-identifier>)"}`. For example, `{name = "Gemini 2.5 Flash (gemini-2.5-flash)"}`. This should be updated whenever the model is upgraded to a new version.

### Signing Commits
All commits should be signed by the author. For AI-generated commits, the signature should precisely credit the model used for the session.

-   The standard is to use a single `Co-Authored-By:` line for the active model (e.g., `gemini-2.5-pro`).
-   I will assume I am `gemini-2.5-pro` unless you notify me that the system has switched models during a session. In the rare case that multiple models contribute to a single commit, a `Co-Authored-By:` line should be included for each.

Example for a standard session:
```
🤖 Generated with [Gemini CLI](https://github.com/google-gemini/gemini-cli)

Co-Authored-By: Gemini 2.5 Pro (gemini-2.5-pro) <noreply@google.com>
```

## Custom Slash Commands

This project uses custom slash commands stored in the `.claude/commands/` directory to automate frequent or complex prompts. Since I do not have native support for these commands like the Claude CLI, I will follow a specific convention:

-   When you issue a command like `Execute \command_name`, I will look for a corresponding file named `command_name.md` inside the `.claude/commands/` directory.
-   I will then treat the contents of that file as the primary prompt for my next action.
-   At the beginning of our sessions, I will list the contents of the `.claude/commands/` directory to familiarize myself with the available custom commands.

## File Operations and Git Hygiene
- **Always use `git mv` for moving files**: When relocating tracked files, always use `git mv` instead of regular `mv` to maintain proper Git history.
- **Place documentation in docs/ directory**: Keep all documentation files in the `docs/` directory with lowercase, underscore-separated names.
- **Never access `claude-dev-log-diary/` directory without first asking for explicit user permission**: This directory contains complete console transcripts (hundreds of KBs) for historical analysis.
- **Verify each development step in isolation**: Test each step of the development workflow to ensure it works as expected before documenting it.
- **Test project setup on a clean environment**: Regularly verify that project setup works correctly from scratch.
- **Test commands in fresh shells**: Ensure all documented commands work in new terminal sessions.

## Additional Instructions
- **Modifying Core Files**: Avoid modifying files in utility directories unless the task explicitly relates to them. Do not update dependencies in `pyproject.toml` without explicit approval or if it's a direct requirement.
- **Introducing New Libraries**: Consider standard library or existing dependencies first. If a new third-party library is necessary, highlight it when proposing changes.
- **Creating New Files**: Create new files (modules, specs) as needed. All new Python code files with logic must have corresponding test files in `specs/`.
- **Code Clarity and Comments**: Add comments for complex logic, non-obvious decisions, or important context.
- **File Management**: Use `git mv` for moving/renaming files. Place documentation in `docs/`.
- **Environment and Commands**: Always ensure you are in the correct virtual environment. Verify commands in fresh shells.
- **Focus on Requirements**: Ensure all changes directly address a stated requirement or agreed-upon improvement.
- **Agent Self-Correction**: Analyze failures, revise plans, and retry.
- **Instruction Synchronization**: These instructions are duplicated in `CLAUDE.md` and `AGENTS.md`. When updating these instructions, I will ask the user if changes should be applied to all three files.
