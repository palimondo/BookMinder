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

### Running Tests

```bash
pytest                          # Run all tests
pytest --spec                   # View tests as specifications
pytest --cov=bookminder         # Check test coverage
```

### Code Quality

We use pre-commit hooks to enforce code quality. Run manually:

```bash
pre-commit run --all-files
```

## License

MIT
