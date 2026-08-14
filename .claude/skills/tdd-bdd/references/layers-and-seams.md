# Layers, seams, fixtures, and doubles

Layer separation follows from falsifiability: each requirement is tested at the one layer that can falsify it, and the conversation between layers is itself a requirement, pinned by a delegation contract.

## Layer ownership

- **T-66** Test each behavior at exactly one layer — the layer that can falsify it: unit specs own domain mapping (raw value to domain field), integration specs own data selection (which records the query returns), acceptance specs own coordination and user-visible output — an acceptance spec that knows a domain detail has absorbed a rule that belongs below, duplicates that layer, and breaks when implementation details move.
- **T-67** Classify each spec by what it depends on (the GOOS vocabulary): a spec that reads a real machine's state is an integration test, and only machine-independent specs gate CI — mislabelling an integration test as a unit test is what makes CI unreliable.
- **T-68** When a spec fails on one machine and passes on another, first ask whether the divergent state is a legitimate product state the implementation wrongly excludes, and only then treat it as a test defect — diagnosing a real bug as "brittle test, mock it" ships the bug.
- **T-69** One spec per behavior across the whole suite: never a second copy of a spec for a second environment or layer — decide which layer owns the behavior, because two suites specifying one behavior will eventually disagree and then neither is authoritative.
- **T-70** A boundary spec mocks the collaborating subsystem and asserts the delegation contract only — the error surfaced to the user, no traceback leaked, the collaborator called correctly — never the lower layer's specific cases, which its own specs already own; one representative case proves the contract, and this is also why a boundary spec must not depend on any fixture being configured just so.
- **T-71** Keep exactly one subprocess end-to-end spec whose only job is proving the wiring — it is the only spec that exercises the real entry point — and run every other spec in-process at its own layer, because a second subprocess spec only re-tests behavior, slowly.

## Seams

- **T-72** Fixtures enter through the front door — the product's own parameter (a synthetic home directory, an explicit path argument) — never by monkeypatching a private name, which couples the spec to an implementation identifier and bypasses the very path-construction code the spec claims to test. A module-constant seam is substitutable in-process only (it is resolved at import time and unpatchable across a process boundary); state that limitation whenever you rely on one.
- **T-73** Choose the seam before writing the assertion: monkeypatch mutates the current interpreter only and cannot influence anything launched as a subprocess — a patch that cannot reach the code under test produces a red that proves nothing and masquerades as legitimate RED.
- **T-74** Keep test-environment knowledge out of production code: a production function must never branch on identifiers that exist only in the spec tree — the shipped program would behave differently for names the user cannot see.
- **T-75** Never encode the developer's home directory, username, or machine into production code, tooling, or assertions — a spec or script that only passes on one machine specifies that machine, not the behavior.

## Fixtures

- **T-76** Fixtures are observations, not constructions: build them by copying complete records out of the real system and reducing to the minimal set the scenarios need — never hand-author rows, invent field values, or create a fixture whose only justification is reaching an uncovered branch, because an invented fixture encodes your beliefs and the spec then verifies your own stub. Explore the real system read-only; extend the fixture only when reality shows a case worth capturing. Announce any directory you add under the fixture tree in the turn you add it — an empty directory is invisible to `git status`, so an unannounced speculative fixture tree cannot be audited.
- **T-77** Never edit a fixture to make a failing spec pass while the domain fact it encodes is still unknown — a fixture bent to fit a guess makes the guess unfalsifiable and the spec meaningless; validate the assumption against the real source first.
- **T-78** Any behavior gated on a time window is specified with controlled time — fixtures are frozen snapshots, so a recency assertion against them silently rots into a false pass or a false fail.
- **T-79** When a spec depends on an otherwise-empty directory tree, commit a single `.gitkeep` at the leaf — git tracks files, not directories, so an untracked fixture tree is silently destroyed and the spec then passes for the wrong reason.

## Doubles

- **T-80** The double's name states what the test is for: a double that only supplies data is a stub (a plain dict will do); reach for a Mock only when the spec verifies calls — a Mock where a stub suffices implies an interaction assertion that never happens.
- **T-81** For pure-function specs, build inputs with a stub helper that defaults every field (`row_stub(**overrides)`) and name in each call only the fields under test; construct test objects with only the fields the assertion depends on — irrelevant fields hide the variable being varied and falsely signal that their values matter.
- **T-82** Name a patch handle after the full function being patched (`mock_list_recent`, not `mock_list`) — a truncated handle becomes ambiguous the moment a sibling collaborator is patched in the same file.

## Restructuring a suite

- **T-83** Move coverage before you remove it: land the replacement specs at the new layer and see them pass before deleting the specs they replace, and before converting or deleting an end-to-end spec, locate which lower-layer spec covers each behavior it carried and add the missing ones first — the gap between delete and replace is a window in which the behavior is unspecified, and that window is where regressions enter. Check coverage across the move: a drop after the replacements land is evidence they exercise a different path than the specs they replaced, never an accepted cost of the restructuring — find the line and explain it before committing the deletion.
- **T-84** Probe test-architecture coupling by deliberate mutation: break one implementation detail (drop a column, misspell a key), run the whole suite, record which specs fail, revert — the blast radius of a one-line change is the objective measure of how much each layer knows about the layer below. Then restructure toward a target stated as a falsifiable sentence ("after this, only the N specs that own that detail fail on that mutation") and re-check it after each step — a restructuring with a goal but no test for the goal cannot be judged to have succeeded.
