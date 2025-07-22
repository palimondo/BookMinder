# BookMinder Development Guidelines - Performance Review

<!-- PERFORMANCE ISSUE #1: COGNITIVE OVERLOAD
The file starts immediately with dense, structured information without context or prioritization.
This can overwhelm Claude Code's processing and decision-making capabilities.
IMPACT: May cause inconsistent adherence to guidelines due to information overload.
CROSS-REF: See Issue #3 (redundancy) and Issue #7 (decision paralysis) -->

<core_philosophy>
## Core Programming Philosophy

<!-- PERFORMANCE ISSUE #2: MIXED ABSTRACTION LEVELS
This section mixes high-level philosophy with specific implementation details.
The bullets jump from conceptual ("Code is a liability") to tactical ("Design for testability").
IMPACT: Creates cognitive dissonance and makes it harder to apply principles consistently. -->

- **Code is a liability, not an asset** - Minimize implementation while maximizing value
- **Executable specifications over documentation** - Tests document behavior and validate assumptions via Behavior-Driven Development (BDD) with `describe`/`it` style tests (RSpec/Jest-like)
- **Scientific approach** - Think hard and form a clear hypotheses before implementation
- **Disciplined engineering** - Apply evidence-based practices consistently
- **Minimize code** - Every line should justify its existence
- **Simple solutions** - Favor straightforward approaches over clever ones
- **YAGNI** - "You Aren't Gonna Need It" - Don't build features until required
- **Design for testability** - Structure code to enable isolated testing

<!-- PERFORMANCE ISSUE #3: REDUNDANCY WITH LATER SECTIONS
Many of these principles are repeated in more detail in later sections (anti-patterns, tdd_discipline).
IMPACT: Forces Claude to process the same information multiple times, potentially causing confusion about which version to follow. 
CROSS-REF: Lines 39-48 (anti-patterns), Lines 121-160 (TDD discipline) -->
</core_philosophy>

<implementation_process>
## Implementation Process

<!-- PERFORMANCE ISSUE #4: PRESCRIPTIVE PROCESS RIGIDITY
This section is extremely prescriptive with numbered steps that may not apply to all situations.
The rigid 4-step process could prevent adaptive problem-solving.
IMPACT: May cause Claude Code to follow process even when it's not appropriate for the task. -->

1. **Start with clear acceptance criteria**
   - Define precise, testable outcomes before writing any code
   - Document edge cases and expected behaviors
   - Focus on the "what" before the "how"

2. **Formulate working hypotheses**
   - Document assumptions about the problem space
   - Create small tests to validate each hypothesis
   - Use tests to explore the problem space methodically

3. **Value incremental progress**
   - Make small, focused changes
   - Commit frequently at stable points
   - Maintain working software throughout development

4. **Prioritize feedback loops**
   - Value fast, frequent feedback
   - Use tests as the primary feedback mechanism
   - Measure progress through working, tested features

<!-- PERFORMANCE ISSUE #5: OVERLAP WITH TDD SECTION
This process overlaps significantly with the BDD/TDD discipline section (lines 121-160).
IMPACT: Creates redundancy and potential for following conflicting guidance.
CROSS-REF: Lines 121-160 (BDD/TDD Discipline) -->
</implementation_process>

<anti-patterns>
## Anti-patterns to Avoid

<!-- PERFORMANCE ISSUE #6: NEGATIVE FRAMING WITHOUT POSITIVE ALTERNATIVES
Lists what NOT to do without always providing clear alternatives.
IMPACT: May cause analysis paralysis as Claude tries to avoid all these patterns simultaneously. -->

- Premature optimization
- Large untested implementations
- Complex solutions to simple problems
- Rushing to code without clear requirements
- Adding "just in case" functionality
- Prioritizing implementation over working tests
- Creating files that don't serve immediate requirements
- Adding unnecessary comments or docstrings

<!-- PERFORMANCE ISSUE #7: CONFLICTS WITH PERFORMANCE NEEDS
Some anti-patterns may conflict with performance requirements (e.g., "rushing to code" vs. quick responses).
IMPACT: Creates decision paralysis when speed and quality both matter.
CROSS-REF: Session workflow (lines 162-173) mentions "limited scope" which could conflict with thoroughness expectations. -->
</anti-patterns>

<package_structure>
## Python Package Structure

<!-- PERFORMANCE ISSUE #8: PROJECT-SPECIFIC DETAILS IN GENERAL GUIDELINES
This section is very specific to Python package structure but placed early in general guidelines.
IMPACT: Non-Python tasks may still be influenced by these Python-specific rules. -->

- **Minimal Package Structure**: Only create directories and files needed for current functionality
- **Empty __init__.py Files**: Keep `__init__.py` files empty; they exist only to make Python's import system work
- **No Premature Modules**: Don't create modules until you have functionality to put in them
- **Avoid Boilerplate**: Don't add docstrings to empty `__init__.py` files or test files
- **No Implementation Without Tests**: Never create implementation files without corresponding tests

<!-- PERFORMANCE ISSUE #9: ABSOLUTE STATEMENTS
"Never" and "always" statements can be problematic when exceptions are needed.
IMPACT: May cause Claude to refuse reasonable exceptions to rules.
CROSS-REF: Similar absolute language throughout document (lines 92, 227-228) -->
</package_structure>

<build_commands>
## Build Commands

<!-- PERFORMANCE ISSUE #10: TOOL-SPECIFIC KNOWLEDGE EMBEDDING
Embedding specific tool commands and their options creates brittleness.
IMPACT: Instructions become outdated as tools evolve; Claude may use wrong command syntax. -->

- Setup uv (Recommended): See `docs/uv_setup.md`
  - Create virtual environment: `uv venv`
  - Activate: `source .venv/bin/activate`
  - Install development dependencies: `uv pip install -e ".[dev]"`
- Setup Pre-commit Hooks: `pre-commit install`
- Run: `python -m bookminder`
- **Test all (Fast Feedback)**: `pytest`
- **View Living Documentation**: `pytest --spec` (Use to understand requirements via test output)
- **Check Test Coverage**: `pytest --cov=bookminder --cov-report=term-missing`
- **Lint and Format** (manual):
  - Format: `ruff format .`
  - Lint: `ruff check --fix .`
  - Type check: `mypy .`
  - Run all checks: `pre-commit run --all-files`

<!-- PERFORMANCE ISSUE #11: COMMAND DUPLICATION
Some commands are repeated in different contexts throughout the file.
IMPACT: Increases file length and processing time without adding value.
CROSS-REF: Git commands repeated in git_workflow section (lines 218-229) -->
</build_commands>

<code_style>
## Code Style

<!-- PERFORMANCE ISSUE #12: INFORMATION DENSITY OVERLOAD
This section packs too many different concerns (formatting, typing, documentation, testing, naming) together.
IMPACT: Makes it difficult to find and apply relevant guidance quickly. -->

- **Python Version**: 3.13
- **Formatting and Linting**: Use ruff (max line length 88)
  - Automated via pre-commit hooks
  - Run formatter manually: `ruff format .`
  - Run linter manually: `ruff check --fix .`
- **Type Checking**: Use mypy for static type analysis
  - Automated via pre-commit hooks
  - Run manually: `mypy .`
- **Imports**: Group standard library, third-party, local imports; alphabetize within groups
- **Types**: Use type hints for all functions and parameters
- **Documentation**:
  - Prefer self-documenting code over verbose docstrings
  - Minimal, focused docstrings for complex functions only
  - **NEVER add redundant comments** that restate what the code already expresses

<!-- PERFORMANCE ISSUE #13: CONFLICTING DOCUMENTATION GUIDANCE
Earlier the file says to avoid unnecessary comments/docstrings, but here provides detailed rules about them.
IMPACT: Creates uncertainty about when to add documentation.
CROSS-REF: Line 47 (anti-patterns), Lines 100-105 (test docstrings) -->

- **Error Handling**: Use specific exceptions with context; include meaningful error messages
- **Naming**: snake_case for functions/variables, CamelCase for classes, UPPERCASE for constants
- **Style**: Favor functional over procedural where appropriate; prioritize conciseness
- **Tests**:
  - Write tests first; focus on behavior, not implementation
  - Use `pytest-describe` syntax (`describe_...`/`it_...`) with descriptive names stating context and behavior
  - Docstring conventions:
    - Keep docstrings in skipped/pending tests as specifications to implement
    - Remove docstrings from implemented tests - the code IS the specification
    - Test names and assertions should tell the complete story without docstrings
  - Do not add comments in specs files that merely restate what the code is doing
  - Name spec files as `<module_name>_spec.py` following BDD conventions
  - Use `pytest --spec` to generate readable documentation from test structure

<!-- PERFORMANCE ISSUE #14: TEST GUIDANCE FRAGMENTATION
Test-related guidance is scattered across multiple sections (here, tdd_discipline, requirements_gathering).
IMPACT: Makes it difficult to get a complete picture of testing requirements.
CROSS-REF: Lines 108-119 (requirements_gathering), Lines 121-160 (tdd_discipline) -->
</code_style>

<requirements_gathering>
## Requirements Gathering

<!-- PERFORMANCE ISSUE #15: PROCESS BEFORE CONTEXT
This section assumes a formal requirements gathering process but doesn't address when it's needed.
IMPACT: May cause unnecessary overhead for simple tasks. -->

- Begin each feature with a requirements dialogue
- Structure the dialogue to establish:
  1. User's goal and expected outcome
  2. Necessary inputs and expected outputs
  3. Edge cases and error conditions
  4. Acceptance criteria in concrete terms
- Document requirements in the TODO.md file
- Translate requirements directly into acceptance tests using the BDD `describe`/`it` structure.
- Reference requirements in commit messages

<!-- PERFORMANCE ISSUE #16: CROSS-SECTION DEPENDENCIES
This section assumes TODO.md exists and has a specific structure, but that's not established earlier.
IMPACT: Creates dependencies between sections that may not be clear to Claude.
CROSS-REF: Lines 172-173 (session_workflow mentions TODO.md), Lines 175-216 (backlog_management details TODO.md structure) -->
</requirements_gathering>

<tdd_discipline>
## BDD/TDD Discipline

<!-- PERFORMANCE ISSUE #17: EXTREME PROCESS RIGIDITY
This is the most prescriptive section with detailed step-by-step instructions and multiple checklists.
IMPACT: May slow down development significantly and create decision paralysis for simple changes. -->

- Always start with a failing BDD acceptance test based on requirements.
  - We follow the **outside-in ATDD** approach: the acceptance test stays RED until the feature is fully implemented and that's OK. When it passes, we know the feature is complete.
- **Write Failing Test**: Define the next behavior using a `describe_...` / `it_...` structure and assertion.
- **Run & Verify RED**: Execute the *specific new test* (e.g., `pytest path/to/test.py::describe_context::it_behavior`) and confirm it fails.
- **Implement GREEN**: Write the minimum production code to pass the failing test.
- **Run All Tests**: Execute `pytest` to confirm success and no regressions.
- **Commit After GREEN**: Make first commit with passing test and minimal implementation.
- **Refactor**: Improve code while keeping all tests green.
- **Commit After Refactor**: Make second commit if any refactoring was done.
- **Coverage Check**: Verify code coverage (via `pytest --cov`) after implementation.
- **Update TODO.md**: Move completed stories to "Completed Features" section.
- Repeat cycle for each behavior.

### Implementation Checklist

<!-- PERFORMANCE ISSUE #18: EXCESSIVE CHECKLIST COGNITIVE LOAD
Three separate checklists with 19 total items may overwhelm decision-making processes.
IMPACT: May cause Claude to spend excessive time on checklist verification rather than solving problems. -->

Before writing any code, verify:
1. ✓ Do we have a clear requirement defined in TODO.md?
2. ✓ Have we written a failing test for this specific requirement?
3. ✓ Is the test descriptively named with `describe_`/`it_` structure?
4. ✓ Is the test focused on behavior (what) not implementation (how)?
5. ✓ Does the test actually verify meaningful behavior, not just types or structure?
6. ✓ Are assertions strong enough to catch real bugs or missing functionality?

Before implementing any feature, verify:
1. ✓ Have we run the test and confirmed it fails (RED)?
2. ✓ Is our planned implementation the minimal solution?
3. ✓ Are we following YAGNI principles (no "just in case" code)?
4. ✓ Are we only adding files and directories required NOW?

Before committing, verify:
1. ✓ Do all tests pass (GREEN)?
2. ✓ Have we removed redundant or unnecessary code?
3. ✓ Are we maintaining adequate test coverage?
4. ✓ Have we run linters and formatters (via pre-commit) to ensure code quality?
5. ✓ Have we removed ALL redundant comments and docstrings?
6. ✓ Does our commit message explain WHY (not just WHAT)?
7. ✓ Have we avoided adding unnecessary files?
8. ✓ Is our code self-documenting without relying on comments?

<!-- PERFORMANCE ISSUE #19: CHECKLIST REDUNDANCY
Many checklist items repeat guidance from other sections.
IMPACT: Processing the same requirements multiple times in different formats.
CROSS-REF: Overlaps with core_philosophy, anti-patterns, code_style, and git_workflow sections -->
</tdd_discipline>

<session_workflow>
## Session Workflow

<!-- PERFORMANCE ISSUE #20: META-COGNITIVE OVERHEAD
This section adds meta-process thinking that may not be relevant to actual coding tasks.
IMPACT: May cause Claude to spend cognitive resources on session management rather than problem-solving. -->

- Start sessions with clear, limited scope
- Define acceptance criteria upfront through requirements dialogue
- Save logs after completing acceptance tests
- Use `/clear` to reset context after major milestones
- Commit code before clearing context
- Keep implementation incremental and focused
- Batch related tool calls where possible
- Monitor token usage during development
- Maintain TODO.md as a living document of progress and priorities

<!-- PERFORMANCE ISSUE #21: CONFLICTING GUIDANCE ON SCOPE
"Limited scope" conflicts with thorough process requirements from other sections.
IMPACT: Creates tension between speed and thoroughness requirements.
CROSS-REF: Lines 17-36 (implementation_process requires thorough analysis), Lines 121-160 (TDD requires comprehensive testing) -->
</session_workflow>

<backlog_management>
## Backlog Management

<!-- PERFORMANCE ISSUE #22: COMPLEX ORGANIZATIONAL SYSTEM
Introduces a complex story management system with YAML files and specific directory structures.
IMPACT: Adds cognitive overhead for simple tasks that don't need formal story management. -->

- User stories are defined as YAML files in the `stories/` directory
- Stories are organized by story map columns (e.g., `discover/`, `decide/`, `deliver/`)
- TODO.md provides a high-level overview with stories listed in suggested implementation order
- Story file names should be descriptive and action-oriented where it makes sense
- Test naming should flow naturally from story names:
  - Story: `filter-by-cloud-status.yaml`
  - Test describe: `describe_bookminder_list_with_filter()` (names the feature/command)
  - Test it: `it_filters_by_cloud_status()` (concise, matches story name)
- This creates a natural rhythm in `pytest --spec` output
- Implementation order in TODO.md should reflect natural feature progression and dependencies
- Mark stories as partially complete with specific notes about what remains

### Story Card Structure

<!-- PERFORMANCE ISSUE #23: DETAILED SPECIFICATION FOR SIMPLE CONCEPT
Provides detailed YAML structure specification that may be overkill for many tasks.
IMPACT: May cause Claude to spend time on story card creation when it's not needed. -->

Each story card is a YAML file with the following structure:

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

- `backlog`: The story is defined but not yet started
- `in_progress`: Development has begun
- `done`: The story is fully implemented, tested, and deployed
- `reopened`: Previously done story that needs further refinement or implementation changes
- `research`: For research stories, indicating active investigation

This system ensures clarity, machine-readability, and granular progress tracking for each story.

<!-- PERFORMANCE ISSUE #24: OVER-ENGINEERING SIMPLE WORKFLOWS
The story management system may be more complex than needed for typical development tasks.
IMPACT: May cause Claude to create unnecessary structure and process overhead. -->
</backlog_management>

<git_workflow>
## Git Workflow

<!-- PERFORMANCE ISSUE #25: RESTRICTIVE COMMIT PATTERNS
Mandates specific two-commit pattern that may not always be appropriate.
IMPACT: May force unnecessary commits or prevent optimal commit organization. -->

- Make two distinct commits in the TDD/BDD cycle:
  1. After GREEN phase (passing BDD test + minimal implementation).
  2. After REFACTOR phase (code improvements, tests still passing).
- Commit messages should be descriptive and explain the "why" behind changes
- Reference the specific requirements being addressed in commit messages
- Focus on what the change accomplishes, not just what files were modified
- Each commit should be small, focused, and preserve working state (all tests passing).
- Stage all files after running pre-commit hooks that modify files, to ensure fixes are included in commit
- Never use `git add .` - always stage files explicitly by name to avoid accidentally committing large or sensitive files

<!-- PERFORMANCE ISSUE #26: ABSOLUTE PROHIBITIONS
"Never use git add ." is an absolute statement that may not always be appropriate.
IMPACT: May prevent legitimate use of staging shortcuts when appropriate.
CROSS-REF: Similar absolute language throughout document creates rigidity -->
</git_workflow>

<project_maintenance>
## Project Maintenance

<!-- PERFORMANCE ISSUE #27: MAINTENANCE INSTRUCTIONS IN DEVELOPMENT GUIDELINES
Project maintenance tasks are mixed with development workflow instructions.
IMPACT: Adds cognitive load for tasks that don't require maintenance considerations. -->

- Regularly verify the AI's model version in the pyproject.toml contributors list
- Update the contributors list whenever Claude is upgraded to a newer version
- Keep package metadata current and accurate in pyproject.toml
- Review docs/ directory content periodically to ensure documentation reflects current state
- Maintain LICENSE file with correct attribution and current year
- These instructions are duplicated in AGENTS.md and GEMINI.md for use with other agentic coding systems, therefore when updating these instructions, always ask the user if changes should be applied to CLAUDE.md, AGENTS.md, and GEMINI.md

<!-- PERFORMANCE ISSUE #28: META-INSTRUCTION COMPLEXITY
The instruction about updating other similar files adds meta-cognitive overhead.
IMPACT: Creates uncertainty about scope of changes and when to ask about other files. -->
</project_maintenance>

<file_operations>
## File Operations and Git Hygiene

<!-- PERFORMANCE ISSUE #29: MIXED ABSTRACTION LEVELS AGAIN
Combines high-level principles (git hygiene) with specific technical commands (git mv).
IMPACT: Makes it harder to apply appropriate guidance for different situations. -->

- **Always use `git mv` for moving files**: When relocating tracked files, always use `git mv` instead of regular `mv` to maintain proper Git history
- **Place documentation in docs/ directory**: Keep all documentation files in the docs/ directory with lowercase, underscore-separated names
- **Never access `claude-dev-log-diary/` directory without first asking for explicit user permission**: This directory contains complete console transcripts (hundreds of KBs) for historical analysis

<!-- PERFORMANCE ISSUE #30: PROJECT-SPECIFIC RESTRICTIONS
Specific directory restrictions that may not apply to general development tasks.
IMPACT: May cause unnecessary caution or questions for tasks that don't involve those directories. -->

- **Verify each development step in isolation**: Test each step of the development workflow to ensure it works as expected before documenting it
- **Test project setup on a clean environment**: Regularly verify that project setup works correctly from scratch
- **Test commands in fresh shells**: Ensure all documented commands work in new terminal sessions

<!-- PERFORMANCE ISSUE #31: EXCESSIVE VERIFICATION REQUIREMENTS
Multiple verification and testing requirements that may be overkill for simple changes.
IMPACT: May slow down development with unnecessary verification steps. -->
</file_operations>

<!-- 
OVERALL PERFORMANCE ASSESSMENT:

CRITICAL ISSUES:
1. Cognitive Overload (Issues #1, #12, #18): Too much information presented at once
2. Redundancy (Issues #3, #11, #14, #19): Same information repeated in multiple places  
3. Over-specification (Issues #4, #17, #23): Excessive detail and rigid processes
4. Conflicting Guidance (Issues #13, #21): Contradictory requirements
5. Absolute Statements (Issues #9, #26): Inflexible rules that prevent adaptation

RECOMMENDATIONS FOR IMPROVEMENT:
1. Reduce overall length by consolidating redundant sections
2. Separate high-level principles from detailed implementation guidance
3. Make processes adaptive rather than rigid
4. Remove or simplify excessive checklists
5. Use guidelines rather than absolute rules
6. Group related concerns together more logically
7. Separate project-specific details from general development guidance

PERFORMANCE IMPACT:
The current structure likely causes inconsistent Claude Code performance due to:
- Decision paralysis from too many rules and checklists
- Processing overhead from redundant information
- Conflicts between speed and thoroughness requirements
- Cognitive overload reducing focus on actual problem-solving
-->