# BookMinder

A tool to extract content and highlights from Apple Books for LLM analysis.

## Features

- List books from Apple Books library
- Extract table of contents from EPUB files
- Extract highlighted passages with context
- Export in Markdown format for LLM consumption

## Setup

### Requirements

- Python 3.9+
- macOS (for Apple Books access)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/BookMinder.git
   cd BookMinder
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   > **IMPORTANT**: You must activate the virtual environment in each new terminal session before running any commands for this project. If you see commands like `pytest` failing with "command not found", it likely means the virtual environment is not activated.

3. Install dependencies
   ```bash
   # For basic usage
   pip install -r requirements.txt

   # For development
   pip install -e ".[dev]"
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
   python3 -m venv venv

   # Activate it (this must be done in each new terminal session)
   source venv/bin/activate
   ```

2. **Verify you're using the correct Python**:
   ```bash
   # Should show a path inside the venv directory
   which python
   ```

3. **Install dependencies** (only needed once):
   ```bash
   # Install project dependencies
   pip install -r requirements.txt

   # Install the project in development mode
   pip install -e .
   ```

### Running Tests

**Remember**: Always activate the virtual environment first with `source venv/bin/activate` before running any commands.

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
pytest --cov=bookminder
```

### Code Quality

We use pre-commit hooks to enforce code quality. Run manually:

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Install pre-commit (one time setup)
pip install pre-commit
pre-commit install

# Run all checks manually
pre-commit run --all-files

# Run formatting only
black .

# Run linting only
flake8

# Run type checking only
mypy .
```

## License

MIT
