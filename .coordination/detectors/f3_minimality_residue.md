# F3 — minimality residue (mutation-lite)

The author ruled the 100% coverage gate IS the primary F3 detector. This detector covers only the residue the gate is structurally blind to: code that specs *execute* (so coverage is green) but no assertion *forces*. The signature: mutate the code, and the suite still passes. That is executable proof that no spec ever demanded the mutated behavior — the mechanical end-state trace of implementation that outran its specs.

## Rule coverage

Covered (the unforced-code subset of the 12 F3-flagged rules):

- **T-15** — implement only the branch the red spec demands. A symmetric or negated branch added without a spec has no assertion pulling on it; inverting its conditional or deleting its body survives the suite (`unforced-branch`, `unforced-branch-body`).
- **T-85** — no implementation without a failing spec that demanded it. The detector supplies the end-state evidence: a surviving mutant marks behavior for which no failing spec ever existed. (The *temporal* half — was there a RED moment — is F1b's transcript territory.)
- **T-86** — no defensive code no spec demanded. Guards, fallback defaults, and handler bodies that no spec forces are exactly where mutants survive; HEAD's `'Unknown'`-fallback survivors below are this class live.
- **T-88** — the forbidden third option (a test whose purpose is merely to execute a flagged line) is directly exposed: such a test executes the line but kills no mutants on it, so the line stays flagged here even though the coverage gate went green.
- **T-89** — retrofit tests written to raise the number are exposed the same way: execution without forcing leaves residue. The uncovered-line half of T-88/T-89 provenance work belongs to the coverage gate, which runs first.
- **T-92** — the executed half only: a capability the fixtures cannot falsify shows up as surviving mutants on its lines. A capability the fixtures cannot even *exercise* is uncovered lines — the coverage gate's catch, not this detector's.

Uncovered — routed to judge rubric / other instruments (reasons also in the structured return):

- **T-16** (append, don't restructure, when adding to working output) — a property of a single change's *shape*, not of the end-state tree; needs diff-level judgment.
- **T-41** (no restating comments in specs; explanation goes in the failure message) — static spec-file hygiene; mutation of implementation code cannot see spec comments. Trivially greppable, but it is spec-text lint, not minimality residue.
- **T-48** (restyle specs in place, never a parallel suite) — a process/DAG property about duplicate suites; not a mutation target.
- **T-93** (only files/dirs a current spec demands; YAGNI for docs and tooling) — pure YAGNI/process; speculative *files* have no mutants to survive because they have no specs executing them at all.
- **T-94** (refactor phase only simplifies what exists; no preparatory structure) — process-timing rule; judge material against the diff sequence.
- **T-99** (shared fixture/helper needs two consuming specs in the same commit) — spec-organization rule over commit content; not mutation-detectable.

## Detection logic

1. Copy the target tree (ignoring `.git`, `.venv`, caches, `claude-dev-log-diary`, `.coordination`) to a temp workdir, so concurrent work in the live repo is never touched. The workdir's package shadows the venv's editable install because `python -m pytest` puts cwd first on `sys.path` (verified empirically; the setuptools editable finder is *appended* to `sys.meta_path`).
2. Baseline: run the suite; abort (exit 2) if red — residue is undefined on a red suite. Baseline wall time sets the per-mutant timeout (5x, min 10s).
3. Coverage pass with `--cov-context=test` and JSON contexts: yields the executed-line set (only executed lines are mutated — unexecuted lines are the coverage gate's finding, not ours) and the per-line covering-spec contexts used in reports.
4. Enumerate mutation sites over the package AST, in deterministic order, skipping docstrings and annotation subtrees. Operators: `invert-conditional` (`if t:` -> `if not t:`, incl. ternaries), `delete-branch-body` (`if` body -> `pass`), `swap-comparison` (`==`<->`!=`, `<`<->`>=`, `in`<->`not in`, `is`<->`is not`, ...), `swap-constant` (`True`<->`False`, `n`->`n+1`, `'s'`->`'sXX'`).
5. Sample deterministically: sites sorted by line, capped per function (default 4) and globally (default 60).
6. Per mutant: rewrite the file via AST transform + `ast.unparse`, run the full suite, restore the file. Suite passes -> survivor. Every pytest subprocess runs with `PYTHONDONTWRITEBYTECODE=1` — all `XX`-append mutants of a file share a byte size, and CPython's pyc invalidation key is (mtime-seconds, size), so sub-second consecutive runs would otherwise execute a stale pyc of the *previous* mutant. This was a real bug caught by the controls: the first HEAD run reported `--filter` and the `list` group name as survivors; manual application of those mutants failed the suite.
7. Report one line per survivor: named failure mode, `file:line`, function, mutant description, nearest covering spec (sorted-first test context of the line; `(import-time only)` when only module import executes it).

Runtime bound: worst case `max_mutants x (5 x baseline)`; in practice sequential suite runs, so ~`max_mutants x baseline`. On this repo (0.5s suite, 56 sampled mutants) a full run is ~26s. `--max-mutants` / `--per-function-cap` tune the budget; sampling is deterministic, so repeated runs are comparable.

## How to run

```
source .venv/bin/activate
python .coordination/detectors/f3_minimality_residue.py --repo /home/user/BookMinder
python .coordination/detectors/f3_minimality_residue.py --repo <dir> --package <pkg> [--max-mutants N] [--per-function-cap N] [--verbose] [--keep-workdir]
```

Exit 0 clean, 1 findings, 2 operational error (red baseline, missing package, coverage failure). `--verbose` streams per-mutant kill/survive to stderr.

## CONTROL RESULTS (all runs real, 2026-08-15, HEAD = 8bdfea5)

| control | target | expected | actual |
|---|---|---|---|
| positive, synthetic forced pair | `fixtures/f3_minimality_residue/forced` (`--package mini --per-function-cap 8`) | exit 0, no survivors | exit 0, `clean: all 6 sampled mutants killed` |
| negative, synthetic unforced pair | `fixtures/f3_minimality_residue/unforced` (same flags) | exit 1, survivors incl. all four mutant classes | exit 1, 6/6 survived: `unforced-branch`, `unforced-branch-body`, `unforced-comparison`, 3x `unforced-constant` |
| negative, real history | repo HEAD, defaults | honest report either way | exit 1, **11/56 sampled mutants survived** |
| determinism | two consecutive HEAD runs | byte-identical findings | identical (diff clean) |
| false-survivor audit | manual `sed` of the `artistName` survivor into the live tree + full suite | suite stays green if the finding is genuine | 53 passed — the spec asserts `"author" in book`, never its value |

The synthetic pair shares one implementation (`classify`), differing only in spec strength: the forced spec pins both branch outcomes at the boundary (`classify(-1)`, `classify(0)`), killing every mutant including the off-by-one `0 -> 1`; the unforced spec executes both branches (coverage-identical, so the primary F3 gate passes both fixtures) but asserts only `isinstance(..., str)`, so every mutant survives. That is the residue definition in miniature.

HEAD survivors (real findings, current tree): the `APPLE_EPOCH` constants (the `updated` timestamp is never value-asserted), the `BKLibrary directory not found:` message prefix (executed by the legacy-installation spec, text unasserted — consistent with T-70's assert-type-not-text ruling, so arguably acceptable residue), the `'Unknown'` title/author fallbacks in `_row_to_book` and `list_books` (T-86-class defensive defaults no spec forces), the `'artistName'` plist key (author value never asserted from the plist path), two click help texts, and the `'No books currently being read'` empty-list message. Findings are leads for the T-88 provenance procedure (delete or spec), not automatic verdicts.

Real-history *positive* control: none exists — mutation residue is a graded property and no era of this repo is presumed residue-free, so the clean direction is proven by the synthetic forced fixture (labeled synthetic per controls discipline). The documented tautological-mock era (e5c7074) needs no historical checkout to demonstrate: its descendant pattern (mock-heavy CLI specs that execute much and force little) is visible in the HEAD survivors above.
