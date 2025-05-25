# BookMinder

[![BookMinder CI](https://github.com/palimondo/BookMinder/actions/workflows/main.yml/badge.svg)](https://github.com/palimondo/BookMinder/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/palimondo/BookMinder/branch/main/graph/badge.svg)](https://codecov.io/gh/palimondo/BookMinder)

A tool to extract content and highlights from Apple Books for LLM analysis.

## Features

- List books from Apple Books library
- Extract table of contents from EPUB files
- Extract highlighted passages with context
- Export in Markdown format for LLM consumption

## Setup

### Requirements

- Python 3.13 (automatically managed by uv)
- macOS (for Apple Books access)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/palimondo/BookMinder.git
   cd BookMinder
   ```

2. Create a virtual environment with uv
   ```bash
   uv venv --python 3.13
   source .venv/bin/activate
   ```

   > **IMPORTANT**: You must activate the virtual environment in each new terminal session before running any commands for this project. If you see commands like `pytest` failing with "command not found", it likely means the virtual environment is not activated.

   > **FIRST TIME SETUP**: If you don't have uv installed, run:
   > ```bash
   > curl -LsSf https://astral.sh/uv/install.sh | sh
   > ```
   > See `docs/uv_setup.md` for more details.

3. Install dependencies
   ```bash
   # Install development dependencies
   uv pip install -e ".[dev]"
   ```

4. Set up pre-commit hooks (for development)
   ```bash
   pre-commit install
   ```

## Usage

```python
from bookminder.apple_books.library import list_books, find_book_by_title

# List all books
books = list_books()

# Find a specific book
book = find_book_by_title("Growing Object-Oriented Software, Guided by Tests")
```

## Development

This project follows Test-Driven Development (TDD) principles with Behavior-Driven Development (BDD) style tests.

### Setting Up Your Environment

1. **Activate the virtual environment**:
   ```bash
   # If you haven't created the virtual environment yet:
   uv venv --python 3.13

   # Activate it (this must be done in each new terminal session)
   source .venv/bin/activate
   ```

2. **Verify you're using the correct Python**:
   ```bash
   # Should show a path inside the .venv directory
   which python
   ```

3. **Install dependencies** (only needed once):
   ```bash
   # Install the project in development mode
   uv pip install -e ".[dev]"
   ```

### Running Tests

**Remember**: Always activate the virtual environment first with `source .venv/bin/activate` before running any commands.

```bash
# Run all tests
pytest

# Run all tests with BDD/spec output for living documentation
pytest --spec

# Run specific tests
pytest specs/apple_books/library_spec.py --spec

# Run tests with verbose output
pytest --spec -v

# Check test coverage
pytest --cov=bookminder --cov-report=term-missing
```

### Code Quality

We use pre-commit hooks to enforce code quality. Run manually:

```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Install pre-commit (one time setup)
pre-commit install

# Run all checks manually
pre-commit run --all-files

# Run formatting only
ruff format .

# Run linting only
ruff check --fix .

# Run type checking only
mypy .
```

For more detailed information about using uv, see [docs/uv_setup.md](docs/uv_setup.md).

## License

MIT
