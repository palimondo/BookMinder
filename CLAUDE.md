# BookMinder Development Guide

## Core Philosophy
- **Code is liability** - Minimize implementation, maximize value
- **Tests document behavior** - BDD `describe`/`it` style specifications
- **Scientific approach** - Form hypotheses, test assumptions
- **YAGNI principle** - Build only what's needed now
- **Fast feedback loops** - Small changes, frequent validation

## Development Workflow

### BDD Cycle
1. **Red**: Write failing test for specific behavior
2. **Green**: Minimal code to pass the test  
3. **Refactor**: Improve while keeping tests green
4. **Commit**: Small, focused commits with clear messages

### Essential Checks
- All tests pass: `pytest`
- Code quality: `pre-commit run --all-files` 
- Requirements documented in TODO.md
- Changes match acceptance criteria

## Commands

### Setup
```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
pre-commit install
```

### Development
- **Test**: `pytest` (fast feedback)
- **Test docs**: `pytest --spec` (living documentation)
- **Coverage**: `pytest --cov=bookminder --cov-report=term-missing`
- **Format**: `ruff format .`
- **Lint**: `ruff check --fix .`
- **Type check**: `mypy .`
- **Run**: `python -m bookminder`

## Code Standards

### Python Style
- Python 3.13, ruff formatting (line length 88)
- Type hints for functions and parameters
- Imports: stdlib, third-party, local (alphabetized)
- Naming: snake_case functions, CamelCase classes, UPPERCASE constants

### Testing
- Tests in `specs/` directory as `<module>_spec.py`
- Use `pytest-describe` syntax: `describe_context()` / `it_behavior()`
- Focus on behavior, not implementation
- No docstrings in implemented tests - code IS the specification
- Test layers: unit/ → integration/ → acceptance/ → e2e/

### Documentation
- Self-documenting code over verbose comments
- Minimal docstrings for complex functions only
- Never add redundant comments that restate code

## Project Context

### Story Management
- Stories in `stories/` as YAML files with user story format
- TODO.md tracks implementation order and progress
- Status field required: backlog, in_progress, done, reopened, research

### Git Workflow  
- Two commits per BDD cycle: after GREEN, after REFACTOR
- Descriptive commit messages explaining WHY
- Stage files explicitly by name (avoid `git add .`)
- Use `git mv` for tracked file moves

### File Operations
- Documentation in `docs/` directory
- Empty `__init__.py` files (no boilerplate)
- Only create files needed for current functionality
- Ask permission before accessing `claude-dev-log-diary/`

### Maintenance
- Update AI model version in pyproject.toml contributors
- Sync changes to AGENTS.md and GEMINI.md when requested
- Keep package metadata current

## Anti-patterns
- Premature optimization
- Large untested implementations  
- Complex solutions to simple problems
- Implementation without clear requirements
- "Just in case" functionality
- Creating unused files or directories