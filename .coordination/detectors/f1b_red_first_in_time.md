# F1b — red-first-in-time (transcript detector)

Replaces the retired F1 commit-grammar family per `.coordination/commit-after-red-review.md`: the commit DAG is a claim, the transcript is the action. This detector reads a Claude-Code-native session transcript (JSONL) and checks that a failing run of a spec was actually observed, in time, before the events that presuppose it — implementation edits, RED claims in assistant prose, and commits whose messages imply a red state.

## Run

```
python3 .coordination/detectors/f1b_red_first_in_time.py --transcript <session.jsonl>
```

Exit 0 = clean, exit 1 = findings. One finding per line: `<failure-mode> [T-rule] line=<jsonl-line> ts=<timestamp>: <detail>`.

## Event model

Events are extracted in transcript order; tool effects register at `tool_result` time (errored edits do not count as edits). Recognized events: file edits via Write/Edit/MultiEdit/NotebookEdit plus a Bash redirect/tee-into-`.py` heuristic, classified as spec (`*_spec.py`, `test_*.py`, `specs/`, `tests/`), impl (other `.py` outside `.coordination/`, `.claude/`, `docs/`, `scratchpad/`, `claude-dev-log-diary/`, excluding `conftest.py`), or story (`stories/*.yaml`); pytest runs (pytest in command position, including `python -m pytest` and `uv run pytest`) with pass/fail read from the tool result — `is_error`, `N failed`, `N errors`, `FAILED`, `ERROR`, `ModuleNotFoundError`, `ImportError`, `Traceback` all count as failing, which is deliberate: per T-11 any failure that tells you what to build next is legitimate RED, import and collection errors included; git commits with `-m` message capture; assistant text blocks.

## Checks (named failure modes)

| failure mode | rule | trips when |
|---|---|---|
| edit-before-red | T-10 (core of T-01/T-03) | an implementation-file edit occurs before any observed failing pytest run that followed a spec edit |
| claimed-red-never-run | T-10 | assistant text claims a red state ("fails as expected", "RED confirmed", "watched it fail", ...) with no failing pytest run observed anywhere earlier in the transcript |
| first-run-pass-treated-as-done | T-12 | the first observed run of a newly edited spec passes and the next 20 events contain neither an edit to that spec nor investigation language ("should have failed", "never red", "defect in the spec", ...) |
| red-commit-missing | T-14 | an implementation edit follows an observed failing run with no git commit between the failure and the edit |
| retro-staged-grammar | T-14 / F1a×F1b | a commit message implies a red state (`RED:` subject or "failing spec/test") but the latest observed pytest run before the commit was passing or absent — the review's discipline-theater signal: DAG grammar contradicted by the timeline |
| green-not-committed | T-17 | after a red-to-green transition, a spec or impl edit occurs before any commit |
| story-edit-before-story-commit | T-33 | a spec or impl edit occurs while an edited story card is uncommitted |
| story-card-mixed-with-code | T-33 | one git add/commit command stages story-card files together with spec/impl files |

## Rule coverage

Covered (transcript-observable): **T-10** (edit-before-red + claimed-red-never-run), **T-11** (as detector behavior: the RED definition accepts import/collection/environment failures, so a legitimate non-assertion RED cannot trip edit-before-red), **T-12** (first-run-pass-treated-as-done), **T-14** (red-commit-missing + retro-staged-grammar), **T-17** (green-not-committed), **T-33** (both story checks).

Not covered, with reasons:

- **T-01** — which boundary is "outermost" for a story requires story-card semantics; not mechanically decidable from the transcript. Its red-first component (watch the opening spec fail) is subsumed by edit-before-red.
- **T-02** — "acceptance spec stays RED until the feature is fully implemented" needs a notion of feature-completeness; faking it green is assertion-content territory (F2), not timeline territory.
- **T-03** — distinguishing acceptance from unit specs is not possible from paths in this repo's concern-based spec tree (`specs/cli_spec.py`); the spec-before-impl ordering it implies is subsumed by edit-before-red.
- **T-04** — "one spec red at a time" cannot use a failing-count threshold because the sanctioned deliberately-red acceptance spec makes two simultaneous failures legitimate by design, and the acceptance spec is not mechanically identifiable (see T-03).
- **T-19** — "refactor the specs too" is a positive obligation with no transcript event marking its absence; grading it needs the judge (T3), not a timeline detector.

## Control results

All fixtures are **synthetic**, structured on the real Claude-Code JSONL event shapes grepped from `claude-dev-log-diary/jsonl/cloud-2026/`. The documented historical lapses (post-6f786cc era, e5c7074 tautological-mock swap) predate any recoverable Claude-Code-native JSONL — the repo's only real JSONL transcript is the 2026-08 coordination session, which contains no TDD coding work — so the negative controls cannot be reproduced from real transcripts and are substituted per the controls discipline.

Run 2026-08-15, `.coordination/detectors/fixtures/f1b/`:

| control | fixture | expected | actual | exit |
|---|---|---|---|---|
| positive | clean_tdd.jsonl (story commit → spec → observed FAIL → RED commit → impl → suite PASS → GREEN commit → refactor commit) | clean | no findings | 0 |
| negative | edit_before_red.jsonl | edit-before-red | edit-before-red line=4; first-run-pass-treated-as-done line=7 (inherent: the never-red spec's first run passes) | 1 |
| negative | claimed_red_never_run.jsonl | claimed-red-never-run | claimed-red-never-run line=3; edit-before-red line=5; retro-staged-grammar line=9; first-run-pass-treated-as-done line=7 (cascade is real: a fabricated RED implies all four) | 1 |
| negative | first_run_pass.jsonl | first-run-pass-treated-as-done, isolated | first-run-pass-treated-as-done line=4, sole finding | 1 |
| negative | retro_staged.jsonl (clean cycle 1, then spec+impl one-shot with selective staging faking the grammar in cycle 2) | retro-staged-grammar | retro-staged-grammar line=20; first-run-pass-treated-as-done line=18 | 1 |
| negative | uncommitted_green_and_mixed.jsonl | T-17 + T-33 modes | story-edit-before-story-commit line=4; green-not-committed line=14; story-card-mixed-with-code line=16 | 1 |

Real-data run: `claude-dev-log-diary/jsonl/cloud-2026/a42b9c92-*.jsonl` (2,959 lines) → 3 findings, all claimed-red-never-run, exit 1. Inspected each: all three are historical narration in a meta-session about TDD ("verified RED" describing the July 2025 gold-standard sequence at line 77, a detector-design sketch quoting "claimed-RED verified" at line 538, a recap of a past mutation-proof "watched the test fail" at line 1514). None is a present-tense claim about work in that session. This bounds the detector's domain: it is built for eval-run coding transcripts, where such phrases are process claims; on meta-discussion transcripts the claimed-red text check will hit narration about red states. An earlier iteration also tripped retro-staged-grammar on commit messages containing "commit-after-RED" (the rule's own name); the message pattern was tightened to grammar-shaped claims (`RED:` subject / "failing spec") and those four false positives cleared without weakening any fixture catch.

## Known limitations

- edit-before-red is satisfied for the whole transcript once any spec has been seen edited-then-failing (the task's literal ordering requirement). This avoids false positives on legitimate green-state refactoring, at the cost of not re-arming per cycle; per-cycle strictness would need refactor-phase attribution, which belongs to the harness-snapshot substrate the review assigns measurement to.
- A candidate who runs a real failing spec, one-shots the implementation, and only then commits in RED/GREEN order defeats retro-staged-grammar but not red-commit-missing, which catches exactly that ordering (impl edit between failure and first commit).
- Spec-to-behavior matching is by file basename; a failing run of any edited spec earns RED globally rather than per behavior. Node-id-level matching is possible from pytest output but unearned until fixture evidence shows basename granularity misses real cases.
- Edits made outside recognized tools (e.g. `sed -i`, patches applied by scripts) are invisible except for the redirect/tee heuristic.
