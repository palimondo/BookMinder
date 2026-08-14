export const meta = {
  name: 'opus-rebrief-and-3way',
  description: 'Opus 5 re-run with Fable-identical brief, then three-way comparison',
  phases: [{ title: 'Re-extract' }, { title: 'Compare' }],
}

const EXTRACT_PROMPT = `You are a read-only analyst in /home/user/BookMinder (git repo, full history already unshallowed — 390 commits). Do not modify tracked files.

GOAL: Extract a precise characterization of the BDD/TDD style the author (palimondo) was aiming for, by rewinding to the start of git history and replaying the evolution of Python code only. Your reader is the author: a professional developer, London-school/GOOS practitioner, who wants an exact, well-written account of the desired qualities of spec and implementation code.

PRIMARY LENS — MOTIVATION. Do not merely catalog observed regularities; for every practice you identify, reconstruct WHY the author does it that way: what failure it prevents, what value it protects, what first principle it follows. Derive rationale from the semantics of the artifact itself where possible (e.g. an integration test exists to exercise the real collaborator — mocking it would verify your own stub, so real fixtures there aren't a preference, they're definitional; London-school mocks are for roles/protocols you own at architectural boundaries in unit specs, never for the thing being integrated against). State every rule as a motivated principle — "X because Y" — not as a pattern report. Where the history shows a correction (revert, replacement, deletion), treat it as the author teaching the principle: name the principle. Where you cannot recover a motivation, say so explicitly rather than papering over it.

SCOPE: *.py files in bookminder/, specs/ (and any earlier test/spec dirs they were renamed from), conftest.py. EXCLUDE entirely: CLAUDE.md/AGENTS.md/docs edits, the xs tool sidequest, and NEVER open the claude-dev-log-diary/ directory. Orientation: you MAY read exactly two files in .coordination/ — repo-map.md and process-evolution.md (repo layout and process-history context). You MUST NOT read ANY other file in .coordination/ (bdd-style.md, bdd-style-fable.md, style-comparison.md, threads.md, or anything else there) — prior attempts at this same task exist and your run must stay uncontaminated. Do not grep them, do not open them.

METHOD: git log --reverse --oneline -- '*.py' ':!claude-dev-log-diary' then walk the sequence with git show on key commits. Watch the play-by-play: specs written before impl? describe_/it_ naming and granularity; assertion strength/style; fixture strategy; how minimal each GREEN implementation is; refactor commits; reverts/corrections. TODO.md says after commit 6f786cc ATDD discipline lapsed — contrast the gold-standard period before vs. the lapse: what specifically degraded.

DELIVERABLE: Write /home/user/BookMinder/.coordination/bdd-style-opus2.md covering:
1. Spec style rules with concrete code examples from real commits (cite short SHAs)
2. Implementation style qualities (minimalism, structure, typing)
3. Observed TDD cadence in commit sequence (RED/GREEN/REFACTOR rhythm)
4. What the gold standard means here and exactly how the post-6f786cc lapse deviated
Dense, evidence-cited, no filler. FORMATTING: do not hard-wrap prose — one line per paragraph/bullet (the doc is read on mobile where every newline renders as a line break). Then return a summary of max 15 lines as your final text.`

phase('Re-extract')
await agent(EXTRACT_PROMPT, { model: 'opus', effort: 'xhigh', label: 'bdd-style-opus2', phase: 'Re-extract' })

phase('Compare')
const verdict = await agent(`You are a read-only judge in /home/user/BookMinder (git repo, full history unshallowed). You may write only your deliverable file.

CONTEXT: Three independent characterizations of this project's BDD/TDD style exist, all extracted from the same git history:
- A: .coordination/bdd-style.md — Opus 5, default effort, original brief (dense evidence-cited rules; NO motivation lens, no orientation docs).
- B: .coordination/bdd-style-fable.md — Fable (Claude Fable 5), xhigh effort, brief = original PLUS motivation-first lens ("every rule as X-because-Y") plus orientation docs (repo-map.md, process-evolution.md).
- C: .coordination/bdd-style-opus2.md — Opus 5, xhigh effort, brief and advantages IDENTICAL to B's. C exists to isolate the model variable: same brief, same effort, same context — only the model differs from B.

PROTOCOL (order matters, to avoid anchoring):
1. FIRST read only C and score it on the rubric: (a) rationale depth — motivated principles vs pattern reports; (b) writing quality; (c) evidence accuracy — spot-check at least 8 cited SHAs against git history (git show), flag misattributions/confabulations; (d) insight — findings requiring inference beyond observation.
2. THEN read A and B and the prior two-way verdict in .coordination/style-comparison.md. Score A and B on the same rubric yourself (you may agree or disagree with the prior judge).
3. Discriminating probes for C (these separated B from A last round — check them explicitly): does C notice that fa0bc72 silently mutated the failing test's patch target (library.SUPPORTED_FILTERS → cli.SUPPORTED_FILTERS) inside a GREEN commit? Does C identify e5c7074 as where fixture acceptance tests were swapped for tautological mock versions? Does C treat per-layer mock placement as definitional rather than preferential? Also credit any genuine finds C makes that B missed.
4. VERDICT: with the brief now controlled, what remains between B and C is model capability (modulo run variance — say so). Answer: how much of the A→B gap did the brief close (A→C delta)? What residual gap is model-attributable (C vs B)? Was the prior verdict ("primarily brief-induced, secondary model component") right?

DELIVERABLE: Write /home/user/BookMinder/.coordination/style-comparison-3way.md — scores table for A/B/C, probe results, verdict, and a recommendation on which doc (or merge) should become canonical. No hard-wrapped prose (mobile rendering). Return a max-12-line summary as final text.`, { model: 'fable', effort: 'xhigh', label: '3way-judge', phase: 'Compare' })

return verdict