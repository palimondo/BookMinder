# F4 — layering and seams detector

Static detector over one tree state (working tree or any git revision). It answers: does this tree keep behavior at the layer that can falsify it, route fixtures through the front-door seam, and specify its delegation contracts — or does the CLI own domain knowledge, do specs reach through implementation identifiers, and do borrows go unspecified?

## Rules covered

| Check (failure mode) | Rule | Detection logic |
|---|---|---|
| cli-owns-domain-knowledge | T-66 | CLI-layer files (`cli.py`, `__main__.py`) scanned for library-owned domain tokens: Core Data column names (`\bZ[A-Z][A-Z_]{2,}\b`), `BKLibrary`, `Books.plist`, `com.apple`, `iBooksX`, `sqlite`, `Library/Containers`. The CLI knowing a schema name has absorbed a rule that belongs below. |
| test-knowledge-in-production | T-74 | Production files scanned for spec-tree identifiers (`pytest`, `PYTEST_CURRENT_TEST`, `CliRunner`, `monkeypatch`, `unittest`, `specs/`, `fixtures/users`, `test_reader`). A production branch on a test-only name ships behavior the user cannot see. |
| private-seam-patch | T-72, L-09 | All `patch("a.b._x")`, `patch.object(m, "_x")`, `monkeypatch.setattr(...)` targets in specs; final component starting with a single underscore is a private-name seam bypassing the front door (`--user`/`user_home`). |
| unspecified-borrow | T-72, L-09 | A spec patches `mod.CONST` where the production module `mod` imports `CONST` (uppercase vocabulary constant) from an origin module, and no spec anywhere asserts the delegation contract (`assert mod.CONST is/== origin.CONST`). The borrow is load-bearing for the patch to be meaningful, and nothing specifies it. |
| internal-identifier-patch | T-61 | A spec patches a name defined inside the target production module itself (not imported into it) — stubbing the module's internal structure and asserting through an implementation identifier rather than observable behavior. Patching a name the module imports (the collaborator boundary) is not flagged. Module-constant seam patches (L-09 side_a pattern, e.g. `BOOKS_PATH`) land here; per L-09 the compiled rule prefers the front door and the constant seam carries an in-process-only caveat. |
| duplicated-vocabulary-constant | T-69 | The same uppercase module-level constant assigned in two or more production modules — vocabulary redefined instead of one module owning it and others importing it. |
| duplicate-spec-across-layers | T-69 | The same `it_` spec name defined in more than one spec file — two suites specifying one behavior will eventually disagree, and then neither is authoritative. |
| lower-layer-text-in-boundary-spec | T-70, T-61 | Message fragments (≥12 chars) harvested from `raise` statements in non-CLI production modules; any spec function that mocks a collaborator and asserts a literal matching such a fragment is pinning the lower layer's wording instead of the sentinel its own double injected. |
| multiple-subprocess-entrypoint-specs | T-71 | Counts `it_` specs driving the entry point via `subprocess` (directly or through a local helper). Fires only when the tree also has an in-process seam (`CliRunner`) — then one wiring spec proves the entry point and the rest re-test behavior slowly. Trees whose only CLI seam is subprocess (pre-in-process-era architecture) are not flagged. |
| machine-state-in-unit-spec | T-67 | `Path.home()`, `expanduser`, `environ["HOME"]` in spec files not labeled `integration`/`e2e` — a spec reading a real machine's state is an integration test, and only machine-independent specs gate CI. |
| absolute-machine-path-in-spec | T-61 | Plain string literals (f-string parts excluded, so paths constructed from test inputs are exempt) starting with `/Users/` or `/home/` in acceptance-layer spec files (`cli*`, `acceptance/`, `e2e/`). Unit specs of the path-mapping contract itself (e.g. `_get_user_path("bob") == Path("/Users/bob")`) are out of scope by design. |

Not covered: **T-83** (move coverage before you remove it). It is an ordering rule over a commit sequence — replacement specs must land and pass before the specs they replace are deleted — which no single-tree static scan can express; it needs the commit DAG (deletion diff vs. prior addition diff) or the transcript timeline, i.e. an F1/F6-shaped instrument, and per the commit-after-red review the transcript is the ground truth for ordering claims anyway.

## How to run

```
python3 .coordination/detectors/f4_layering.py --repo <repo-root> [--rev <sha>] [--package bookminder] [--specs specs]
```

Exit 0 clean, exit 1 with one line per finding: `<failure-mode>: <path>:<line> <detail> (rule)`. With `--rev` the tree is read from git blobs, so historical states need no checkout.

## Control results (all runs real, 2026-08-15, detector at this commit)

| Control | Tree | Expectation | Result |
|---|---|---|---|
| negative (documented unspecified-borrow) | HEAD working tree (branch claude/bookminder-recall-5ite2s) | trips | TRIPPED — `unspecified-borrow: specs/cli_spec.py:100` (spec patches `bookminder.cli.SUPPORTED_FILTERS`, borrowed from `bookminder.apple_books.library`; no identity assertion exists in any spec). Verified at HEAD before writing the detector: `specs/cli_spec.py:100` is `with patch('bookminder.cli.SUPPORTED_FILTERS', {'foo', 'bar'}):` and `bookminder/cli.py:9-14` imports the constant from the library. Exit 1. |
| additional live findings at HEAD | same run | — | `internal-identifier-patch: specs/cli_spec.py:55,67` (patching `bookminder.cli.format`, defined in the module under test); `duplicate-spec-across-layers: it_shows_books_for_user_with_reading_progress` in `specs/apple_books/library_integration_spec.py:44` and `specs/cli_spec.py:132`; `multiple-subprocess-entrypoint-specs: specs/cli_spec.py:132,144,155` (3 subprocess specs beside a CliRunner seam); `machine-state-in-unit-spec: specs/apple_books/library_spec.py:40` (`Path.home()`). All are genuine properties of the restored pre-reorg spec tree at HEAD. |
| negative (documented front-door lapse, historical) | rev 9a6319f (2025-06-27, parent of 8e632f6 "Remove monkeypatch") | trips | TRIPPED — `private-seam-patch: specs/apple_books/library_spec.py:18` (`monkeypatch.setattr("bookminder.apple_books.library._books_plist", ...)`), the exact seam 8e632f6 removed in favor of the front door. Exit 1. |
| positive (gold era, post-front-door) | rev 99b18cc (2025-06-28) | clean | CLEAN, exit 0. |
| positive (gold era, post-front-door) | rev 086fbea (2025-06-27) | clean | CLEAN, exit 0. |
| era-scoped, not a control | rev 2d331e9 (2025-05-29) | — | trips `internal-identifier-patch: specs/apple_books/library_spec.py:11` (patches module constant `BOOKS_PATH`). Expected under the compiled rulebook: this tree predates the front-door practice (L-09 side_a era, ratified against 2026-08-13), so it is not used as a positive control for seam checks. |
| negative (synthetic) | `fixtures/f4_layering/violating/` | trips | TRIPPED on all five checks with no recoverable live instance: `cli-owns-domain-knowledge` (bookminder/cli.py:3,13,14,15 — sqlite3, BKLibrary, ZTITLE), `test-knowledge-in-production` (cli.py:10,11 — test_reader, specs/), `duplicated-vocabulary-constant` (SUPPORTED_FILTERS defined in cli.py:6 and apple_books/library.py:3), `lower-layer-text-in-boundary-spec` (specs/cli_spec.py:9), `absolute-machine-path-in-spec` (specs/cli_spec.py:10). Exit 1. Fixture is synthetic and labeled as such — no historical tree state with a domain-token-bearing cli.py or duplicated vocabulary constant was found in recoverable history (checked via detector runs over era anchors), so these controls are constructed. |

## Scoping notes

- The T-71 check's CliRunner gate is what makes gold-era trees pass honestly rather than by exemption list: pre-in-process-era architecture had subprocess as its only CLI seam, and T-71's violation is *redundant* subprocess specs once an in-process seam exists.
- The unspecified-borrow identity-assertion search is textual (`assert ... NAME is/== ... NAME` across all spec files); adding the missing one-line contract spec (`assert cli.SUPPORTED_FILTERS is library.SUPPORTED_FILTERS`) clears the finding, which is the repair the rule prescribes.
- Detector is repo-agnostic in mechanism but BookMinder-tuned in vocabulary (domain tokens, package defaults); `--package`/`--specs` cover layout drift.
