# F2 — assertion-integrity detector

Git-DAG + AST detector over spec files (`*_spec.py`, `*_test.py`). For each commit in a range it AST-diffs every spec file against the first parent, pairs `it_` functions by name — same file or cross-file within the commit, so a "pure move" that rewrites bodies under unchanged names (the e5c7074 mechanism) is diffed, not trusted — and reports weakened assertion sets plus static integrity defects in new or modified spec bodies. Per the commit-after-red-review verdict, F2-over-DAG is structurally blind to a spec first committed already-weakened at GREEN; this detector covers what the DAG can prove, and the same static checks are snapshot-ready (they take any two tree states) when harness snapshots supply finer resolution.

## Rules covered

| T-rule | detection mode(s) |
|---|---|
| T-51 (spec must fail against empty stub; guard loop asserts) | `unguarded-conditional-assertion`, `nonemptiness-guard-removed`, `tautological-mock-echo` |
| T-52 (exact identity sets; no contracts via fixture cardinality) | `exact-set-relaxed-to-cardinality`, `fixture-cardinality-contract` |
| T-53 (never weaken to pass the fixture; no fixture-derived counts) | `equality-relaxed`, `fixture-cardinality-contract`, `literal-swap-same-name` |
| T-54 (failing fixture assertion: fix data or value, keep strength) | `assertion-removed`, `literal-swap-same-name` |
| T-55 (never change asserted literal under unchanged it_ name) | `literal-swap-same-name` |
| T-57 (no disjunctive assertions) | `disjunctive-assertion` (static), `disjunction-added` (diff) |
| T-58 (assert presence of correct behavior, not absence of wrong impl) | `mock-guaranteed-absence` — the mechanizable subclass: an absence assertion guaranteed by the test's own stub; general negative-space assertions stay rubric-tier |
| T-59 (name the property, don't pin incidental fixture content) | `emptiness-as-expectation`, `mock-guaranteed-absence`; the stale-datum half (assert names data the fixture no longer contains) needs a run of the suite, not the AST — T2/rubric |
| T-60 (error-path: message + discriminating fragment, keep both) | diff side via `assertion-removed` (dropping either required assertion trips); the static both-present form is not mechanizable — which paths share a message is not in the AST |
| T-64 (mock making an argument irrelevant; no dummy relabeling) | `tautological-mock-echo`, `mock-swapped-under-same-name`; the relabel-as-dummy half is rubric-tier |
| T-91 (never skip to restore green; no skip beside shipped code) | `skip-to-restore-green`, `skip-as-stand-in` |
| L-01(a) (identity sets where membership IS the requirement) | `equality-relaxed`, `exact-set-relaxed-to-cardinality` guard the identity-set ideal against relaxation |
| L-01(b) (no behavioral contract via fixture cardinality) | `fixture-cardinality-contract` (`len(x) == N` / `> N` / `>= N` for N past the non-emptiness guard, which stays legal) |

## Detection logic

Diff checks — run on every `it_`/`test_` pair whose body fingerprint (statements + decorators) changed; pairing is by qualified name in the same file, falling back to bare `it_` name across the commit's other changed/added spec files (relocations are reported with `(was <old file>)`):

- `assertion-removed` — parent assertions (plus `mock.assert_*` calls) dropped with none added; suppressed when the removed assertion's expression reappears anywhere in the child file (e.g. moved into a shared helper, as in b4e376d).
- `equality-relaxed` — an `==` assertion replaced by membership (`in`) or truthiness over the same subject.
- `exact-set-relaxed-to-cardinality` — `x == [..]` replaced by `len(x)` comparison over the same subject.
- `literal-swap-same-name` — same assertion structure, different constant, unchanged `it_` name. Two precision suppressions: coordinated identifier renames (all differing constants are identifier-like strings on both sides, the ec91c40 TypedDict-field case) and membership strengthenings (the new needle contains the old one, the 7a88f6a case). Review-tier by design: the DAG cannot contain T-55's required "decide and state which is wrong" dialogue, so this surfaces candidates.
- `disjunction-added` — a top-level `or` assertion the parent version did not have.
- `nonemptiness-guard-removed` — parent guarded against empty output (`len(x) > 0` / truthiness), child does not; an exact equality against a non-empty literal collection counts as guarded (3d2bab6 strengthened `len > 0` into an identity set — not a finding).
- `mock-swapped-under-same-name` — a spec with no mocks replaced by a `patch(...)` + `return_value`-fed spec under an unchanged `it_` name (day-013-class, the e5c7074 mechanism).
- `skip-to-restore-green` — an existing implemented spec gained a skip/xfail marker.

Static checks — run on new functions and on the changed side of modified pairs (only findings absent from the parent version are reported, so long-lived defects do not re-flag on unrelated edits):

- `disjunctive-assertion` — top-level `or` in an assert; passes under contradictory outcomes.
- `fixture-cardinality-contract` — `len(x)` compared to a constant beyond the non-emptiness guard.
- `tautological-mock-echo` — an `==`/`is` assertion against the very expression assigned as a mock's `return_value`. `mock.assert_called_once_with(...)` collaboration asserts are not flagged — argument-wiring is legitimate London-school.
- `mock-guaranteed-absence` — a `return_value`-fed spec (not `side_effect` — a raising mock makes absence assertions falsifiable, e.g. `"Traceback" not in output`) asserting `S not in output` where `S` occurs in no other string in the test: the stub cannot produce it, the assertion cannot fail.
- `unguarded-conditional-assertion` — every assertion in the function sits inside a loop or conditional with no unconditional assertion or non-emptiness guard before it; passes vacuously on empty output (the day-002 and 677a251 pattern).
- `emptiness-as-expectation` — sole assertion pins emptiness (`== []`, `len == 0`, `not x`) under an `it_` name promising positive behavior.
- `skip-as-stand-in` — a new skip-marked spec committed in the same commit that touches production code.

## How to run

```
python3 .coordination/detectors/f2_assertion_integrity.py --repo <path> --range A..B
python3 .coordination/detectors/f2_assertion_integrity.py --repo <path> --commit SHA [--commit SHA2]
```

Exit 0 clean, 1 findings; one finding per line: `SHA mode file::describe::it_name -- detail`. `--no-static` restricts to diff-based weakening checks; `--exclude PREFIX` overrides the default path exclusion (`claude-dev-log-diary/` — the xs tool's own specs, not product specs). Ranges walk first-parent only.

## CONTROL RESULTS (all runs executed against this repo at a06a75f, 2026-08-15)

| control | kind | expected | actual |
|---|---|---|---|
| `--commit e5c7074` (documented tautological-mock swap under a "pure move" message) | negative | trips | TRIPPED, exit 1, 4 findings: `mock-swapped-under-same-name` on both relocated tests (`it_filters_recent_books_by_sample_status`, `it_excludes_samples_from_recent_books`, each tagged `(was specs/cli_spec.py)`), `nonemptiness-guard-removed` on it_excludes, `mock-guaranteed-absence` ("stub never supplies 'Sample'") |
| `--range e7a5fa4~1..d8b5722` — 27 gold-era ATDD commits (2025-05-30 and 2025-06-23 blocks) | positive | clean | CLEAN, exit 0 |
| `--commit b246d7b` (2025-07-13; the documented vacuous `'Sample Book' not in` assert) | negative | trips | TRIPPED: `mock-swapped-under-same-name` + `mock-guaranteed-absence` |
| `--commit 9e7bd38` (2025-04-13, day-002 — the incident that generated T-51) | negative | trips | TRIPPED: 2× `unguarded-conditional-assertion` (`it_includes_basic_metadata_for_each_book`, `it_can_sort_books_by_last_update_date`) |
| `--commit 6769f2f` (2025-06-27, day-010; author himself reverted it in 1b07bd5) | negative | trips | TRIPPED: `skip-as-stand-in` on `it_handles_permission_denied_with_helpful_message` |
| `--commit 3103e4d` (2025-06-27, day-010 d010-R3: skip added to implemented spec, re-enabled later by 20b03dc) | negative | trips | TRIPPED: `skip-to-restore-green` on `it_returns_books_with_reading_progress` |
| `--range 6f786cc..HEAD` lapse-era sweep | survey | findings map to documented incidents | 11 findings, all accounted: b246d7b (2), 5b42ae0 (2× unguarded-conditional), 677a251 (the documented vacuous conditional), e5c7074 (4), 315dce5 (the 2026-08 spec-tree restore reintroducing 677a251's conditional — correct static observation on reintroduced code) |
| synthetic fixture (`fixtures/f2_assertion_integrity/make_fixture_repo.py`) — SYNTHETIC, labeled: modes with no recoverable real-history instance | synthetic negative | all modes fire | ALL FIRE: `equality-relaxed`, `literal-swap-same-name`, `exact-set-relaxed-to-cardinality`, `assertion-removed`, `skip-to-restore-green`, `disjunction-added`+`disjunctive-assertion`, `tautological-mock-echo`, `fixture-cardinality-contract`, `emptiness-as-expectation`, `skip-as-stand-in` (10 lines, exit 1) |

Calibration false positives found and eliminated during control runs, each now a coded suppression: b4e376d (returncode asserts moved into `_run_cli_with_user` helper — file-level assertion lookup), ec91c40 (coordinated `progress` → `reading_progress_percentage` TypedDict rename — identifier-rename suppression), 7a88f6a (error-message needle grew to contain the old one — membership-strengthening suppression), 3d2bab6 (`len > 0` upgraded to exact identity set — exact-nonempty-equality counts as guard).

The 2025-06-27 day-010 block (`--range 3103e4d~1..086fbea`) additionally yields `disjunctive-assertion` on 0dd8aa0 and three `literal-swap-same-name` on 7de114d/53e570a (error-message expectations rewritten to track changed production output under unchanged names) — treated as documented-era true positives, not controls: they sit in the mined day-010 session alongside the condemned-and-reverted episodes.

## Known limitations

- Single-word expectation swaps (`== "ready"` → `== "done"`) are suppressed by the identifier-rename heuristic; precision on ec91c40-class renames was bought with recall there.
- `fixture-cardinality-contract` also fires on exact counts over inline locally-built data, which T-81 exempts; zero such hits in `specs/` across all history (the pattern exists only in the excluded diary tree), so no suppression was added.
- Cross-file assertion relocation into helpers is recognized within a file, not across files.
- A spec born weak in its first commit trips static checks, but a weakening that happens between tool calls inside one commit is invisible to any DAG detector — that is the snapshot substrate's job (commit-after-red-review, alternative (a)).
