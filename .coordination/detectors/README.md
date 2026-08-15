# Detector Suite — TDD/BDD Process-Fidelity Instruments

Six detector families that mechanically check an eval trial (transcript JSONL + git repo state) against the rules in `.coordination/compile/rule-index-tdd-bdd.md`. Each family has a script, a spec doc recording its controls, and (where needed) labeled fixtures under `fixtures/`. Every script exits 0 clean / 1 findings, one line per finding; F3 additionally exits 2 on operational error (red baseline).

## Family × status

All six scripts verified present and runnable (`--help`) on 2026-08-15.

| Family | Script | Rules covered | Controls (positives clean / negatives tripped) | Commit |
|---|---|---|---|---|
| F1b red-first-in-time | `f1b_red_first_in_time.py` | 6 (T-10, T-11, T-12, T-14, T-17, T-33) | yes / yes | 8bdfea5 |
| F2 assertion-integrity | `f2_assertion_integrity.py` | 13 (T-51–T-55, T-57–T-60, T-64, T-91, L-01(a), L-01(b)) | yes / yes | 087fafe |
| F3 minimality-residue | `f3_minimality_residue.py` | 6 (T-15, T-85, T-86, T-88, T-89, T-92) | yes / yes | a3e4b3d |
| F4 layering | `f4_layering.py` | 9 (T-61, T-66, T-67, T-69–T-72, T-74, L-09) | yes / yes | 934ea14 |
| F5 claim-vs-action | `f5_claim_vs_action.py` | 11 (T-23, T-26, T-27, T-29, T-30, T-31, T-34, T-77, T-87, T-98, T-100) | yes / yes | a6bb5a2 |
| F6 refactor-honesty | `f6_refactor_honesty.py` | 2 (T-20 partial, T-21) | yes / yes | 93b06cd |

Where a real-history control instance did not exist, negatives run on labeled synthetic fixtures (see each family's doc for the full control table with actual run outputs).

## Rule-coverage audit

Cross-checked against `.coordination/compile/rule-index-tdd-bdd.md` (tallies: 58 rules flagged detector-covered, 24 flagged detector_candidate).

**Detector-covered rules: all 58 accounted for.** The union of every family's `rules_covered` + `rules_uncovered` exactly matches the index's per-family flags: F1 11/11, F2 11/11, F3 12/12, F4 9/9, F5 13/13, F6 2/2. 44 are mechanically covered by a shipped detector (plus ledger rules L-01(a), L-01(b), L-09, which the index does not tally); 14 were examined by their assigned family and found not mechanizable there — each is listed below with its reason and routes to the judge rubric.

**detector_candidate rules: NO family accounts for these 24.** They were flagged mechanically checkable but no established family claimed them; they remain unbuilt: T-05, T-22, T-25, T-28, T-32, T-35, T-36, T-37, T-38, T-39, T-40, T-42, T-45, T-46, T-49, T-63, T-73, T-75, T-76, T-78, T-79, T-82, T-96, T-97. Until instruments exist, these also route to the judge rubric (or a future F7+ builder pass).

## Uncovered rules (route to judge rubric)

From F1b:
- **T-01** — outermost-boundary choice requires story-card semantics, not transcript-observable; its red-first component is subsumed by the edit-before-red check.
- **T-02** — feature-completeness of a red acceptance spec is not transcript-decidable; fake-green is assertion-content (F2) territory.
- **T-03** — acceptance-vs-unit spec distinction is not derivable from paths in the concern-based spec tree; the ordering component is subsumed by edit-before-red.
- **T-04** — one-red-at-a-time cannot use failing-count thresholds because the sanctioned deliberately-red acceptance spec makes two simultaneous failures legitimate and is not mechanically identifiable.
- **T-19** — refactor-the-specs-too is a positive obligation with no transcript event marking its absence; belongs to the T3 judge.

From F3:
- **T-16** — property of a single change's shape (append vs restructure), not of the end-state tree; judge-rubric material over the diff.
- **T-41** — static spec-file comment hygiene; implementation mutation cannot see spec text; spec-lint/judge material.
- **T-48** — duplicate parallel spec suites are a process/DAG property, not a mutation target; judge/DAG material.
- **T-93** — speculative files/dirs/docs have no specs executing them, so nothing to mutate; pure YAGNI/process, judge material.
- **T-94** — refactor-phase preparatory structure is a process-timing rule over the commit sequence; judge material.
- **T-99** — shared-helper two-consumer rule is spec-organization over commit content; judge material.

From F4:
- **T-83** — ordering rule over a commit sequence (replacement specs must land and pass before deleting the specs they replace); not expressible as a single-tree static property; needs the commit DAG or transcript timeline (an F1/F6-shaped instrument).

From F5:
- **T-09** — which data source is "real" vs fixture is environment semantics, and evidential-sufficiency statements are judge territory; only its numeric-report component is incidentally covered by quantitative-claim-no-provenance.
- **T-65** — the day-007 inert-seam green was backed by a real run, so claim-vs-action timeline matching cannot see it; proving a seam took effect needs assertion-content semantics (F2/T3 judge).

From F6:
- **T-20 (partial)** — the "count the refactorings in this diff" mixture clause is not mechanizable from tree states; proxied by impl-public-addition/impl-branch-addition, remainder stays T3 rubric. The third-commit grammar clause is commit-grammar territory retired as an instrument by the commit-after-red-review verdict.

## Usage — running the suite over a trial

A trial supplies two inputs: the trial's session transcript(s) (Claude-Code-native JSONL) and the trial's git repo (with the commit range the trial produced, `<base>..<head>`). One command per family:

```sh
# F1b — transcript timeline: red-first ordering, commit grammar, uncommitted green
python3 .coordination/detectors/f1b_red_first_in_time.py --transcript <session.jsonl>

# F2 — git DAG + AST: assertion weakening/vacuity across the trial's commits
python3 .coordination/detectors/f2_assertion_integrity.py --repo <repo> --range <base>..<head>

# F3 — mutation-lite over the trial's end state: code executed but not forced by assertions
python3 .coordination/detectors/f3_minimality_residue.py --repo <repo>          # add --rev via checkout, or --package/--max-mutants to tune

# F4 — static layering/seam checks over the end-state tree (no checkout needed for history)
python3 .coordination/detectors/f4_layering.py --repo <repo> --rev <head>

# F5 — transcript claims vs tool-call actions
python3 .coordination/detectors/f5_claim_vs_action.py --transcript <session.jsonl>

# F6 — refactor-labeled commits: parent-spec replay + AST checks
python3 .coordination/detectors/f6_refactor_honesty.py --repo <repo> --range <base>..<head>
```

Multi-transcript trials (subagents): run F1b and F5 once per JSONL. F3 and F6 execute the suite in subprocesses and need the repo's `.venv` importable from the invoking environment; F3's runtime is roughly max_mutants × baseline suite time (~26 s on this repo). Exit codes: 0 clean, 1 findings (F3 also: 2 operational error, e.g. red baseline). Aggregate verdict: any exit 1 is a finding for the judge to weigh, not an automatic trial failure — several modes are explicitly review-tier (see docs).

## Honest gaps

- **F1b**: real-fail-then-one-shot defeats retro-staged-grammar (caught instead by red-commit-missing); full forgery resistance is assigned to harness snapshots. Built for eval-run coding transcripts — on a meta-session about TDD, historical narration produced 3 claimed-red-never-run hits (inspected, domain-bound, not bugs in scope). Negatives are synthetic: the documented lapse era has no recoverable Claude-Code-native JSONL.
- **F2**: four rules partially covered by declared scope — T-58 only the mechanizable subclass (stub-guaranteed absence assertions), T-59's stale-datum half needs a suite run (T2 tier), T-60's static form is not mechanizable (covered on the diff side via assertion-removed), T-64's relabel-as-dummy half is rubric-tier. literal-swap-same-name is review-tier by design (T-55's required dialogue can't be in the DAG). Known recall trade: single-word expectation swaps are suppressed by the identifier-rename heuristic. Structurally blind to specs born weak at GREEN (snapshot substrate needed). Default-excludes `claude-dev-log-diary/`.
- **F3**: no real-history positive control exists (no era presumed residue-free); the clean direction is proven only by a labeled synthetic forced fixture. Sampling is capped (4/function, 60 total) — survivors are a lower bound. Instrument bug found and fixed during controls (stale-pyc via (mtime, size) collision; `PYTHONDONTWRITEBYTECODE=1` now forced) — documented so extensions don't rediscover it.
- **F4**: era-scoped — pre-front-door trees (e.g. 2d331e9) trip internal-identifier-patch by design; the T-71 check is gated on an in-process seam existing in the tree, so pre-CliRunner architectures pass honestly. HEAD currently carries live findings (unspecified-borrow at `specs/cli_spec.py:100` and four more) — a trial run against this repo inherits them unless repaired first.
- **F5**: claim regexes carry negation/prospective guards and quantitative provenance errs clean on small digit strings — both trade recall for precision. Retraction hygiene is operationalized narrowly (contradiction-without-retraction within 20 events). The day-013 fixture-edit lapse survives only as console markdown, so its negative control is a labeled synthetic reconstruction. Note: the rule index tallies 13 F5-flagged rules where the build brief said 12.
- **F6**: a behavior change whose covering specs are rewritten in the same commit leaves no baseline-green conviction path — spec-expectation-changed is the tripwire; finer resolution belongs to the harness snapshot substrate. Replay skips are loud, not silent (SKIP-BASELINE / SKIP-UNCOLLECTABLE), but a skipped spec is unverified, not verified.
- **Suite-wide**: all transcript detectors assume Claude-Code-native JSONL (tool_use/tool_result pairing); console-markdown transcripts are out of scope. The 24 detector_candidate rules have no instrument at all. Forgery-resistant evidence (vs a model that games commit grammar) is deferred to the harness snapshot substrate per the commit-after-red-review verdict.
