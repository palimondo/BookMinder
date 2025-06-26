# BookMinder

[![BookMinder CI](https://github.com/palimondo/BookMinder/actions/workflows/main.yml/badge.svg)](https://github.com/palimondo/BookMinder/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/palimondo/BookMinder/branch/main/graph/badge.svg)](https://codecov.io/gh/palimondo/BookMinder)

A tool to extract content and highlights from Apple Books for LLM analysis.

## Features

- List books from Apple Books library
- Extract table of contents from EPUB files
- Extract highlighted passages with context
- Export in Markdown format for LLM consumption

## Developer Setup

### Requirements

- Python 3.13 (automatically managed by uv)
- macOS (for Apple Books access)

### Quick Start

Clone and setup:
```bash
git clone https://github.com/palimondo/BookMinder.git
cd BookMinder
```

Install uv if not already installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
See [docs/uv_setup.md](docs/uv_setup.md) for more details.

Create environment and install dependencies:
```bash
uv venv --python 3.13
source .venv/bin/activate
uv pip install -e ".[dev]"
pre-commit install
```

Verify setup works:
```bash
pytest --spec
```

> **IMPORTANT**: Always activate the virtual environment with `source .venv/bin/activate` in each new terminal session before running any commands.

## Usage

```python
from bookminder.apple_books.library import list_books, find_book_by_title

books = list_books()
book = find_book_by_title("Growing Object-Oriented Software, Guided by Tests")
```

### Command Line Usage

After installation, the `bookminder` command is available.

List recently read books with reading progress:
```bash
bookminder list recent
```

This shows up to 10 books you're currently reading, ordered by last read date.

#### Admin Usage

As an administrator, you can examine another user's Apple Books library:
```bash
bookminder list recent --user alice
```

This requires appropriate permissions to access the specified user's Library directory.

## Development Workflow

This project follows Test-Driven Development (TDD) with Behavior-Driven Development (BDD) style tests.

### Running Tests

Activate environment first (always required):
```bash
source .venv/bin/activate
```

Run tests with BDD output for living documentation:
```bash
pytest --spec
```

Run specific tests:
```bash
pytest specs/apple_books/library_spec.py --spec
```

Check test coverage:
```bash
pytest --cov=bookminder --cov-report=term-missing
```

### Code Quality

Run all pre-commit checks:
```bash
pre-commit run --all-files
```

Or run individual tools:
```bash
ruff format .
ruff check --fix .
mypy .
```

## License

MIT
