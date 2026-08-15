export const meta = {
  name: 'detector-suite-build',
  description: 'Build the eval detector suite: one agent per detector family, then an aggregation report',
  phases: [
    { title: 'Implement', detail: 'one agent per family: design, implement, run controls' },
    { title: 'Report', detail: 'aggregate control results + rule-coverage audit' },
  ],
}

const COMMON = `Repo /home/user/BookMinder, branch claude/bookminder-recall-5ite2s. You are building ONE detector family of the BookMinder TDD-eval detector suite.
CONTEXT (read in this order): .coordination/eval-design.md (T1/T2 detector roles, enforcement ladder); .coordination/commit-after-red-review.md (VERDICT: F1 commit-grammar detectors are RETIRED as instruments — the author retired commit-after-RED entirely; transcript evidence outranks DAG evidence; harness snapshots will supply measurement resolution); .coordination/compile/rule-index-tdd-bdd.md (each rule row carries a detector-family flag or detector_candidate note — your family's flagged rules are your requirements); use 'source .venv/bin/activate; python3 .coordination/tools/rule.py -c 40 <corpus-id>' to read any rule's source evidence.
HISTORY ACCESS: the clone may be shallow — run 'git fetch --unshallow 2>/dev/null || git fetch --deepen=10000 2>/dev/null || true' before any history work. Known control anchors: gold-standard ATDD era = roughly May-June 2025 history; documented lapse era begins after commit 6f786cc; e5c7074 is the documented tautological-mock swap; the spec tree at HEAD is concern-based (specs/cli_spec.py etc.).
DELIVERABLES (yours alone, self-committed): .coordination/detectors/<family>.py — a runnable CLI detector (argparse; --repo for DAG detectors, --transcript for transcript detectors; exit 0 clean / 1 findings; findings printed as one line each: named failure mode + location); .coordination/detectors/<family>.md — spec doc: which T-rule IDs it covers, detection logic, how to run, and a CONTROL RESULTS table you actually ran (positive controls must pass clean, negative controls must trip — a detector that cannot reproduce a documented catch is not done); test fixtures if needed under .coordination/detectors/fixtures/<family>/.
CONTROLS DISCIPLINE: run your detector against real history/transcripts, record real output. If a documented negative control cannot be reproduced (e.g. the lapse predates recoverable history), say so in the doc and substitute a synthetic fixture, labeled synthetic.
FORM: never hard-wrap prose in .md files; no praise, no meta-narration. COMMIT: batch git add <your paths> && git commit -m "<why>" in one command, then git push -u origin claude/bookminder-recall-5ite2s as a SEPARATE command (retry 4x backoff on network failure only). Concurrent sibling agents are committing disjoint files — never git add -A.`

const FAMILIES = [
  {
    key: 'f1b_red_first_in_time',
    brief: `FAMILY F1b — red-first-in-time (transcript detector; replaces the retired F1 commit-grammar family). Input: a Claude-Code-native session transcript (JSONL). Detect: implementation-file edits that precede any observed failing run of the spec that names the behavior (spec edit + failing pytest for it must appear earlier in time); claimed-RED never actually run; a first-run-PASS on a new spec treated as done (no investigation actions following). Also emit the retro-staged-grammar signal from the review: commit contents implying a red state that the transcript timeline contradicts. Rule requirements: rule-index rows flagged F1 (11 rules) — reinterpret each as a transcript-observable check per the review's F1b framing; document any F1-flagged rule that is NOT transcript-observable as uncovered. Controls: build minimal synthetic JSONL fixtures (clean TDD sequence = pass; edit-before-red = trip; claimed-red-never-run = trip). Structure the JSONL fixture format on the real one: claude-dev-log-diary/jsonl/cloud-2026/*.jsonl (grep a few event shapes; do not read whole).`,
  },
  {
    key: 'f2_assertion_integrity',
    brief: `FAMILY F2 — assertion-integrity (git-DAG + AST detector). For a commit range: AST-diff every *_spec.py between parent and child; detect an existing it_ whose assertion set got WEAKER (assertion removed, == relaxed to in/truthiness, exact set relaxed to cardinality or non-empty, added disjunction that passes under contradictory outcomes); tautological mocks (asserting a value the same mock supplies); fixture-cardinality assertions encoding behavioral contracts. Rule requirements: rule-index rows flagged F2 (11 rules) + ledger L-01 both-rules. Controls: e5c7074 (documented tautological-mock swap) MUST trip; a sample of gold-era spec-evolving commits MUST pass clean; if e5c7074's content is unrecoverable from history, synthetic fixture labeled as such.`,
  },
  {
    key: 'f3_minimality_residue',
    brief: `FAMILY F3 — minimality residue (mutation-lite). The author ruled the 100% coverage gate IS the primary F3 detector — do NOT rebuild coverage. Build only the residue detector: code that specs execute but no assertion forces. Method: cheap mutation sampling — for implementation lines/branches in bookminder/, apply simple mutants (invert conditional, delete branch body, swap constant), run the suite, report mutants that survive with the line and the nearest covering spec. Bound the runtime (sample or per-function cap, document the bound). Rule requirements: rule-index rows flagged F3 (12 rules) — cover the unforced-code subset; route pure-YAGNI/process rules to the doc's uncovered list (they are judge-rubric material). Controls: HEAD's suite must yield at least one known survivor if any exists (report honestly either way); a synthetic forced/unforced pair fixture proves both directions.`,
  },
  {
    key: 'f4_layering',
    brief: `FAMILY F4 — layering and seams (static detector over a tree). Detect: CLI layer owning domain knowledge (bookminder/cli.py referencing DB schema names/paths the library should own); specs bypassing the front-door seam (monkeypatching private module names instead of passing --user/user_home); delegation contracts unspecified (vocabulary constants redefined rather than imported — the cli.SUPPORTED_FILTERS is library.SUPPORTED_FILTERS borrow); spec files asserting through implementation identifiers rather than observable behavior. Rule requirements: rule-index rows flagged F4 (9 rules) + ledger L-09. Controls: HEAD must trip on the documented unspecified-borrow case (specs patch cli.SUPPORTED_FILTERS; the identity assertion is absent — verify at HEAD first, cite line); gold-era tree states must pass on the checks that apply to them.`,
  },
  {
    key: 'f5_claim_vs_action',
    brief: `FAMILY F5 — claim-vs-action (transcript detector). Input: CC-native JSONL transcript. Detect: assistant asserts test outcomes ("tests pass", "all green", "suite passes") with no matching successful pytest tool-call earlier in the same span; quantitative claims (counts, percentages, line numbers) with no tool-call provenance in the span; completion claims ("done", "implemented", "fixed") with no corresponding edit/commit action; retraction hygiene (a corrected claim whose earlier copies in the transcript are never re-addressed). Rule requirements: rule-index rows flagged F5 (12 rules). Controls: synthetic JSONL fixtures both directions; plus run against a real slice of claude-dev-log-diary/jsonl/cloud-2026/ (bounded — pick one agent transcript under 1M) and record what it flags, as a realism check labeled exploratory, not a control.`,
  },
  {
    key: 'f6_refactor_honesty',
    brief: `FAMILY F6 — refactor-honesty (git-DAG detector). For any commit whose message claims refactoring: run the PARENT commit's spec files against the CHILD's implementation (behavior must be preserved — specs from before must pass after); flag spec-file behavioral edits smuggled into refactor commits (AST-visible assertion changes); flag implementation additions (new public functions/branches) labeled refactor. Rule requirements: rule-index rows flagged F6 (2 rules) + skill cycle rules on refactor scope. Controls: find real refactor-labeled commits in history (gold era) — must pass; synthetic negative fixture (refactor commit that changes behavior) — must trip. Note in the doc how the detector handles missing/changed test infrastructure across old commits (pin: run under the child's environment, skip uncollectable specs loudly).`,
  },
]

const RESULT_SCHEMA = {
  type: 'object',
  required: ['family', 'script_path', 'rules_covered', 'rules_uncovered', 'controls', 'commit_sha'],
  properties: {
    family: { type: 'string' },
    script_path: { type: 'string' },
    doc_path: { type: 'string' },
    rules_covered: { type: 'array', items: { type: 'string' } },
    rules_uncovered: { type: 'array', items: { type: 'string' }, description: 'flagged rules this detector cannot cover, with reason encoded as "T-NN: reason"' },
    controls: {
      type: 'object',
      required: ['positives_clean', 'negatives_tripped'],
      properties: {
        positives_clean: { type: 'boolean' },
        negatives_tripped: { type: 'boolean' },
        detail: { type: 'string' },
      },
    },
    commit_sha: { type: 'string' },
    notes: { type: 'string' },
  },
}

phase('Implement')
log('Building 6 detector families in parallel')
const results = await parallel(
  FAMILIES.map((f) => () =>
    agent(`${COMMON}\n\n${f.brief}\n\nName your deliverables .coordination/detectors/${f.key}.py and ${f.key}.md. Your structured return must report real control results, not intentions.`, {
      label: `build:${f.key}`,
      phase: 'Implement',
      schema: RESULT_SCHEMA,
    })
  )
)

const landed = results.filter(Boolean)
log(`${landed.length}/6 families landed`)

phase('Report')
const summary = JSON.stringify(landed, null, 2)
const report = await agent(
  `Repo /home/user/BookMinder, branch claude/bookminder-recall-5ite2s. Six detector-family builders just finished; their structured results:\n${summary}\n\nWrite .coordination/detectors/README.md — the suite's front page: (1) family × status table (script, rules covered count, controls passed both directions yes/no); (2) rule-coverage audit — cross-check against .coordination/compile/rule-index-tdd-bdd.md: every rule flagged detector-covered or detector_candidate must appear in some family's rules_covered or rules_uncovered; list any rule NO family accounts for; (3) the uncovered-rules list with reasons (these route to the judge rubric); (4) usage: how the eval harness runs the suite over a trial (one command per family, inputs); (5) honest gaps section from the builders' notes. Verify each claimed script exists and runs (--help) before writing its row. Never hard-wrap prose. Commit ONLY the README (batch add+commit one command), then push -u origin claude/bookminder-recall-5ite2s as a separate command (retry 4x backoff network-only). RETURN (max 6 lines): coverage audit result, families fully green, gaps count, commit SHA.`,
  { label: 'report', phase: 'Report' }
)

return { families: landed.map((r) => ({ family: r.family, controls: r.controls, sha: r.commit_sha })), report }
