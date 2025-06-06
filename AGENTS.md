## Project Overview
This project, BookMinder, is a Python tool designed to extract content and highlights from Apple Books, primarily for analysis with Large Language Models (LLMs). The AI agent working on this project should understand its focus on data extraction and processing from Apple's ecosystem and adhere to the specific coding practices outlined in this document and in `CLAUDE.md`.

## Code Layout
- `bookminder/` - Main application logic (analogous to an `app/` directory).
- `bookminder/__init__.py` - Package marker.
- `specs/` - Unit and integration tests (using Pytest with `pytest-describe` for BDD style).
- `docs/` - Project documentation.
- `AGENTS.md` - This file, providing guidance for AI agents.
- `CLAUDE.md` - Specific guidelines for development with the Claude AI model.
- `README.md` - General information and setup instructions.
- `pyproject.toml` - Project metadata and dependencies (managed by UV).
- `TODO.md` - Task tracking for development.
- Note: This project does not currently use HTML templates or a dedicated `static/` directory. Utility scripts, if any, would typically be in a `scripts/` directory, but one is not currently present.

## Setup & Dependencies
- **Python version**: 3.13 (managed by `uv`).
- **Dependency Management**: Uses `uv` with `pyproject.toml`.
- **Setup Steps**:
    1. Clone the repository.
    2. Install `uv` if not already present: `curl -LsSf https://astral.sh/uv/install.sh | sh` (See `docs/uv_setup.md` for more details).
    3. Create the virtual environment: `uv venv --python 3.13` (or simply `uv venv` if ` .tool-versions` or similar is configured).
    4. Activate the virtual environment: `source .venv/bin/activate`.
    5. Install dependencies: `uv pip install -e ".[dev]"`.
    6. Install pre-commit hooks: `pre-commit install`.
- **Environment Variables**: No special environment variables are typically needed for standard development and testing. If specific external services or configurations were to be integrated in the future that require API keys or custom paths, they might use environment variables (e.g., managed via a `.env` file), but this is not a current requirement for core functionality or tests.

## Building & Running
- **Running the Application**: The main application can be run (if it's a CLI tool) using `python -m bookminder` after activating the virtual environment.
- **Agent Operation**: Typically, an AI agent will interact with this project as a library or by running specific scripts/tests. Direct execution of the main application might not be common for agent tasks unless specifically testing CLI behavior.
- **No Build Step**: Being a Python project, there isn't a separate "build" step for typical development workflows. Installation of dependencies is covered under "Setup & Dependencies".

## Testing
- **Test Runner**: `pytest` is used for all tests. Tests are located in the `specs/` directory.
- **Running All Tests**:
    - For standard output: `pytest`
    - For concise output: `pytest -q`
    - For BDD-style "living documentation" output: `pytest --spec` (Recommended to understand requirements).
- **Running Specific Tests**:
    - To run a specific file: `pytest specs/path_to_your_test_file.py --spec`
    - To run a specific test function/method within a file (using `pytest-describe` BDD syntax): `pytest specs/path_to_test.py::describe_context::it_behavior`
- **Test Coverage**:
    - Check test coverage: `pytest --cov=bookminder --cov-report=term-missing`
    - New code should be covered by tests.
- **Agent Responsibility**:
    - **Before committing, always run the full test suite (`pytest`) and ensure all tests pass.**
    - The AI agent must run the full test suite after making any changes.
    - All new features should include accompanying tests in the `specs/` folder.
    - If fixing a bug, add a regression test when possible.
- **Test Philosophy**: This project follows Test-Driven Development (TDD) with Behavior-Driven Development (BDD) style tests. Tests are written first to define behavior.

## Linting & Formatting
- **Primary Tool**: `ruff` is used for both formatting and linting. `mypy` is used for type checking.
- **Configuration**: Settings for these tools (e.g., line length 88, PEP 8 adherence, import sorting) are managed in `pyproject.toml` and enforced by `ruff`.
- **Automation**: These checks are automated via pre-commit hooks. Ensure hooks are installed with `pre-commit install`.
- **Manual Execution**:
    - Format code: `ruff format .`
    - Lint code (with auto-fix): `ruff check --fix .`
    - Type check: `mypy .`
    - Run all checks as pre-commit would: `pre-commit run --all-files`
- **Agent Responsibility**:
    - **The AI agent must fix any linting, formatting, or type errors it introduces.**
    - It's recommended to run `pre-commit run --all-files` or the individual commands (`ruff format .`, `ruff check --fix .`, `mypy .`) before committing changes.
    - CI pipelines will likely fail if linting or type errors are present.

## Coding Conventions

This project emphasizes disciplined engineering, minimal and simple solutions, and a strong adherence to Behavior-Driven Development (BDD) / Test-Driven Development (TDD).

**Core Principles:**
- **Minimize Code, Maximize Value**: Every line of code is a liability; ensure it directly contributes to a required feature.
- **YAGNI (You Aren't Gonna Need It)**: Do not implement functionality "just in case."
- **Simple Solutions First**: Prefer straightforward, clear, and maintainable approaches over overly complex or "clever" ones.
- **Design for Testability**: Structure code to be easily testable in isolation.
- **Executable Specifications**: Tests (especially BDD-style `specs`) are the primary documentation of behavior.

**Development Process:**
- **Understand Requirements Thoroughly**:
    - Before coding, ensure requirements are crystal clear. This includes the user's goal, necessary inputs/outputs, edge cases, and precise acceptance criteria.
    - Refer to `TODO.md` for documented requirements. If anything is unclear or missing, seek clarification before proceeding.
- **Formulate and Test Hypotheses**: For complex problems or unclear areas, formulate explicit hypotheses about behavior or solutions. Create small, targeted tests to validate these assumptions early.
- **Test-Driven Development (TDD/BDD)**:
    - Always write a failing test *before* writing implementation code.
    - Tests should define behavior (`what`), not just implementation details (`how`).
    - Use the `describe_... / it_...` BDD syntax for tests in `specs/` files (e.g., `specs/my_module_spec.py`).
- **Incremental Progress**: Make small, focused changes and commit frequently at stable (all tests passing) points.

**Code Style & Structure:**
- **Python Version**: 3.13.
- **Formatting & Linting**: Enforced by `ruff` (see "Linting & Formatting" section). Adheres to PEP 8 with a line length of 88.
- **Type Hinting**: Use type hints for all function signatures (parameters and return types). Enforced by `mypy`.
- **Naming Conventions**:
    - `snake_case` for functions, methods, variables, and module/package names.
    - `CamelCase` for classes.
    - `UPPER_SNAKE_CASE` for constants.
    - Test functions should follow BDD style: `describe_context_or_class` and `it_should_behave_this_way`.
- **Modules and Packages (`bookminder/` directory)**:
    - Maintain a minimal package structure. Only create directories and files as needed for current functionality.
    - `__init__.py` files should generally be empty and exist only to mark directories as packages. Avoid adding code or docstrings to them unless strictly necessary.
- **Docstrings & Comments**:
    - Prefer self-documenting code (clear naming, logical structure).
    - Add docstrings to functions/methods only if their purpose or usage is complex or not immediately obvious from the name and signature. Keep them concise.
    - **Avoid redundant comments** that merely restate what the code clearly shows. Comments should explain *why* something is done a certain way if it's non-obvious, not *what* is being done.
    - No docstrings in test files (`specs/`); the BDD function names are self-documenting.
- **Imports**: Group imports: standard library, then third-party, then local application imports. Alphabetize within groups. `ruff` will enforce this.
- **Error Handling**: Use specific exception types. Error messages should be meaningful and provide context.
- **Functional Preferences**: Prefer list comprehensions, generator expressions, and functional constructs (like `map`, `filter`) over verbose loops where they improve clarity and conciseness.
- **Global State**: Avoid global state. Pass context or dependencies explicitly.

**Testing Specifics:**
- All new features must include accompanying tests in the `specs/` folder.
- When fixing a bug, add a regression test to prevent recurrence.
- Ensure tests have strong assertions that genuinely verify behavior.

**Anti-Patterns to Avoid:**
- Premature optimization.
- Large, untested blocks of implementation.
- Adding functionality not directly tied to a current, specific requirement.
- Writing implementation code before a failing test.
- Unnecessary files, comments, or boilerplate.

**Key Development Checks:**

*   **Before Starting Work:**
    *   ✓ Is there a clear requirement defined (e.g., in `TODO.md` or from user input)?
    *   ✓ Are acceptance criteria, inputs/outputs, and edge cases understood?
*   **During Implementation (TDD/BDD Cycle):**
    *   ✓ Have you written a failing test for the specific behavior you are about to implement?
    *   ✓ Is the test descriptively named (e.g., `describe_...::it_...`) and focused on behavior?
    *   ✓ (After writing code) Is the implementation the *minimal* necessary to pass the current test? (YAGNI)
    *   ✓ Do *all* tests pass after your change? (`pytest`)
*   **Before Committing:**
    *   ✓ Have all tests passed? (`pytest`)
    *   ✓ Has the code been formatted and linted? (`ruff format .`, `ruff check --fix .`)
    *   ✓ Has type checking passed? (`mypy .`) (Or run `pre-commit run --all-files`)
    *   ✓ Is the code self-documenting? Have redundant comments/docstrings been removed?
    *   ✓ Does the commit message clearly explain the "why" and "what" of the changes?
    *   ✓ Are only necessary files included in the commit?

## Commit & PR Guidelines

**Commit Messages:**
- **Format**: Strive to follow Conventional Commits format where appropriate (e.g., `feat: ...`, `fix: ...`, `refactor: ...`, `test: ...`, `docs: ...`, `chore: ...`).
- **Content**:
    - Provide a short, clear summary of what changed.
    - Explain the "why" behind the changes, not just "what" was modified.
    - Reference specific requirements from `TODO.md` or issue numbers if applicable.
    - Focus on what the change *accomplishes* for the user or system.
- **TDD/BDD Cycle Commits**:
    - This project encourages commits at two key stages in the TDD/BDD cycle:
        1. After achieving a **GREEN** state (new BDD test passes with minimal implementation).
        2. After a **REFACTOR** phase (code is cleaned up, tests still pass).
- **Atomicity**: Each commit should be small, focused, and maintain a working state (all tests and linters passing).

**Pull Requests (PRs):**
- **Description**: When the agent creates a PR, it should include a clear description summarizing:
    - The changes made.
    - The reasons for these changes.
    - How the changes address the requirements.
- **Issue Linking**: If a GitHub issue exists for the work, reference it in the PR description (e.g., "Closes #123").
- **CI Checks**: The project's Continuous Integration (CI) pipeline runs tests and linters on each PR. Ensure these all pass locally before considering a PR ready for review and definitely before merging.

## Additional Instructions

- **Modifying Core Files**:
    - Avoid modifying files in utility directories like `scripts/` (if such a directory is created for devops purposes) unless the task explicitly relates to them.
    - Do not update dependencies in `pyproject.toml` (e.g., adding new libraries or changing versions) without explicit approval or if it's a direct requirement of the assigned task.
- **Introducing New Libraries**:
    - If new functionality is required, first consider if it can be achieved using the Python standard library or existing project dependencies.
    - If a new third-party library seems necessary, this should be discussed or highlighted when proposing changes.
- **Creating New Files**:
    - The agent can create new files (e.g., new modules, new spec files) as needed for new features or refactoring.
    - All new Python code files containing logic or features must be accompanied by corresponding test files in the `specs/` directory and covered by tests.
- **Code Clarity and Comments**:
    - While the project values self-documenting code, feel free to add comments to explain particularly complex logic, non-obvious decisions, or important context that isn't clear from the code itself.
- **File Management**:
    - **Moving/Renaming Files**: Always use `git mv old_path new_path` for moving or renaming files tracked by Git. This preserves their history.
    - **Documentation Files**: Project documentation (like this `AGENTS.md` or `README.md`) should be placed in the root directory or in the `docs/` directory. Use lowercase, underscore-separated names for new documents in `docs/`.
- **Environment and Commands**:
    - Always ensure you are in the correct virtual environment (`source .venv/bin/activate`) before running any project-specific commands.
    - If documenting or testing a sequence of commands, verify them in a fresh shell session to ensure they work correctly from a clean state.
- **Focus on Requirements**: Ensure all changes directly address a stated requirement or an agreed-upon improvement. Avoid speculative or "nice-to-have" additions unless specifically requested.
- **Agent Self-Correction**: If a subtask fails or an approach doesn't work, the agent should analyze the failure, potentially revise its plan or approach, and retry. Documenting these iterations can be helpful.
