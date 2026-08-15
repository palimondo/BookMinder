---
name: tdd-bdd
description: Outside-in BDD/TDD discipline (London-school ATDD) for driving features from a failing acceptance spec inward through unit specs to minimal implementation, with describe_/it_ specs as living documentation and commits at stable points of the cycle. Use when starting a story or feature, writing or naming specs, choosing assertions, fixtures, test doubles, or seams, deciding which layer owns a behavior, implementing toward green, refactoring, reading a coverage report, or committing work from the cycle.
---

# Outside-in BDD/TDD Discipline

The root principle, and the hierarchy that follows from it: a spec's job is nailing REQUIREMENTS IN A FALSIFIABLE WAY. Everything else in this skill is a consequence, not a parallel motivation — executable specification (specs, not prose, are the requirements document, because prose cannot fail), layer separation (each requirement lives at the one layer that can falsify it), and delegation contracts (boundary specs pin the conversation between layers, because that conversation is itself a requirement). When two rules seem to conflict, resolve toward whichever keeps the requirement falsifiable.

Code is a liability, not an asset: the work is minimizing what must be written while the spec suite maximizes what is pinned. The discipline's value lies in the sequence, not the artifacts — rushing to implementation destroys it even when the resulting code looks correct, and the bet is rigorous process over one-shotting.

## Invariants — in force at every moment

- Never write implementation without a failing spec that demanded it; run the spec and watch it fail before writing any code, and say so explicitly.
- Never weaken, rewrite, or skip an existing spec to get green: the expectation is the requirement, so when spec and code disagree, decide which is wrong before editing either.
- Commit at stable points — after GREEN, after each REFACTOR improvement, per feature — with all tests passing; the sole exception is the deliberately-red acceptance spec of a feature in progress. RED earns no commit: it is proven by the observed failing run, quoted where you declare it.
- One spec red at a time; one scenario at a time; remaining scenarios wait as skipped placeholders.
- Specs render as prose: describe_/it_ names plus `pytest --spec` are the living requirements document; no docstrings on implemented specs.
- Minimal constraint that still falsifies: implement only what the red spec demands, assert only what the requirement names, delete what nothing specifies.
- Nothing is done until it has been executed and observed; report the command and its output, never the claim alone.

## Page map — read the page before acting on the triggering task

- Starting a story; acceptance criteria in hand; a red acceptance spec on the main line; tempted to fake it green; standing up a walking skeleton → `references/outside-in.md`
- Running the cycle: verifying RED, going GREEN, refactoring, phase discipline, when to commit, quality gates, verification before claiming done → `references/cycle-and-commits.md`
- Creating or editing a spec file: naming describe_/it_, docstrings and skip markers, ordering, structure → `references/writing-a-spec.md`
- Writing or editing any assertion; error-path specs; configuring a mock; a spec that passes suspiciously → `references/assertion-integrity.md`
- Deciding which layer tests a behavior; building fixtures; choosing doubles and seams; end-to-end wiring; test-architecture coupling → `references/layers-and-seams.md`
- Writing implementation; defensive-code urges; coverage reports; YAGNI calls; deleting code or specs → `references/minimal-implementation.md`
