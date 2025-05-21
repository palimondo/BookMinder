# Setting up BookMinder with UV

This guide explains how to set up the BookMinder project using [uv](https://github.com/astral-sh/uv), a modern Python package manager and virtual environment tool.

## Why uv?

- **Speed**: uv is significantly faster than pip for installing packages
- **Simplicity**: Combines virtual environment creation and package installation
- **Reliability**: Improved dependency resolution
- **Portability**: Easy to install on any system, including fresh installations

## Fresh macOS Installation

If you're on a completely fresh macOS installation:

1. **Install Command Line Tools** (if prompted):
   ```bash
   xcode-select --install
   ```
   Follow the prompts to install the basic developer tools (includes git).

2. **Install uv** (standalone binary):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Clone the repository**:
   ```bash
   git clone https://github.com/palimondo/BookMinder.git
   cd BookMinder
   ```

4. **Create a virtual environment and install dependencies**:
   ```bash
   uv venv --python 3.13
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

5. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Working with uv

### Basic Commands

- **Create a virtual environment**:
  ```bash
  uv venv --python 3.13
  ```

- **Activate the virtual environment**:
  ```bash
  source .venv/bin/activate  # Unix/macOS
  ```

- **Install project in development mode**:
  ```bash
  uv pip install -e ".[dev]"
  ```

- **Run the tests**:
  ```bash
  pytest
  ```

- **View test documentation**:
  ```bash
  pytest --spec
  ```

### Development Workflow

1. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Run tests to see failing tests**:
   ```bash
   pytest
   ```

3. **Implement the required functionality**

4. **Run tests with coverage**:
   ```bash
   pytest --cov=bookminder --cov-report=term-missing
   ```

5. **Format and lint your code**:
   ```bash
   ruff check --fix .
   ruff format .
   ```

Or rely on pre-commit hooks to automatically format and lint your code when committing.

## Converting from pip/venv

If you're currently using pip and venv, the transition to uv is straightforward:

1. **Remove old virtual environment**:
   ```bash
   rm -rf venv/
   ```

2. **Create new environment with uv**:
   ```bash
   uv venv --python 3.13
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

That's it! You're now using uv for your Python environment management.
