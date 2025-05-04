# Pre-commit Workflow for BookMinder

## Pre-commit Configuration

BookMinder uses pre-commit hooks to enforce code quality and consistency. The hooks configuration:

1. **Excludes claude-dev-log-diary files**: All hooks exclude files in this directory to allow for manual handling of development logs.

2. **Auto-stages fixed files**: The configuration now automatically stages only files that were modified by hooks, not all changed files.

3. **Current hooks**:
   - **Code Formatting**: trailing-whitespace, end-of-file-fixer, black
   - **Code Quality**: flake8, mypy
   - **Repo Hygiene**: check-yaml, check-added-large-files

## Auto-fix vs Manual Fix

Our pre-commit hooks are set up to handle two types of issues:

1. **Auto-fixable issues**: Issues like trailing whitespace, missing newlines, and code formatting are automatically fixed and staged.

2. **Manual-fix issues**: Issues like type errors (mypy), linting errors (flake8) require manual fixes.

## Working with Development Logs

For the claude-dev-log-diary files:

1. **Excluded from hooks**: These files are excluded from all pre-commit hooks
2. **Manual staging**: Use `git add claude-dev-log-diary/day-XXX.md` to stage them explicitly
3. **Separate commits**: Consider making separate commits for dev logs

## Type Annotation Improvements

Our `mypy` hook currently identifies missing type annotations but doesn't block commits. To improve type safety:

1. Add return type annotations to functions in:
   - `bookminder/apple_books/library.py`
   - `specs/apple_books/library_spec.py`

2. Consider enabling stricter mypy checks in the future
