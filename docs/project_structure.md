# BookMinder Project Structure

This document explains the key configuration files and project structure decisions.

## Configuration Files

### conftest.py

The `conftest.py` file at the project root serves a critical purpose in our testing setup:

- **Import Path Resolution**: Adds the project root to Python's module search path, ensuring tests can import from the `bookminder` package without installation
- **Test Discovery**: Enables pytest to discover and run tests correctly with our BDD structure
- **Fixture Location**: Serves as the standard location for test fixtures (we currently don't have any yet)

Without this file, tests would fail to import the project modules when running pytest.

### pytest.ini

The `pytest.ini` file configures our Behavior-Driven Development (BDD) testing approach:

- `testpaths = specs`: Look for tests in the 'specs' directory instead of the default 'tests'
- `python_files = *_spec.py`: Use *_spec.py pattern for test files instead of the default test_*.py
- `python_functions = it_*`: Use BDD-style function naming (it_does_something) instead of test_*
- `python_classes = describe_*`: Use BDD-style class naming (describe_feature) instead of Test*

This configuration enables the "living documentation" style output with `pytest --spec`, creating readable, nested test output.

### pyproject.toml

The `pyproject.toml` file follows PEP 621 for modern Python packaging and includes:

- **Project Metadata**: Name, version, description, etc.
- **Dependencies**: Both core and development dependencies
- **Build Configuration**: Setuptools configuration
- **Tool Configuration**: Settings for Black, pytest, mypy, and flake8

This single file centralizes all project configuration that was previously spread across multiple files.

## Directory Structure

The project follows a minimal structure, adhering to YAGNI principles:

```
bookminder/
├── bookminder/
│   ├── __init__.py
│   └── apple_books/
│       ├── __init__.py
│       └── library.py
├── docs/
│   └── project_structure.md
├── specs/
│   ├── __init__.py
│   └── apple_books/
│       ├── __init__.py
│       └── library_spec.py
├── conftest.py
├── pytest.ini
└── pyproject.toml
```

We only create directories and files as needed for implemented functionality, avoiding premature structure creation.

## Package Structure

The `__init__.py` files serve multiple purposes:

1. **Package Markers**: Make directories importable as Python packages
2. **Import Resolution**: Enable proper imports within the package
3. **Test Discovery**: Help pytest discover and load test modules correctly

While Python 3.3+ made these files optional with implicit namespace packages, we use them to ensure reliable test discovery and package distribution.

## Future Considerations

As the project grows, we may consider:

1. **src Layout**: Moving package code to a src/ directory for better isolation
2. **Test Fixtures**: Adding shared fixtures in conftest.py
3. **Entry Points**: Adding CLI interface via pyproject.toml entry_points

These changes would be implemented only when required by actual development needs, following our minimal implementation philosophy.
