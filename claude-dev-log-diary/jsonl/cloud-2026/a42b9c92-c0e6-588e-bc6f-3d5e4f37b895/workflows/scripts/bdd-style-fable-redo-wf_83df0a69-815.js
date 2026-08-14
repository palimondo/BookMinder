export const meta = {
  name: 'bdd-style-fable-redo',
  description: 'Fresh Fable xhigh re-characterization of BookMinder BDD/TDD style',
  phases: [{ title: 'Analyze' }],
}
phase('Analyze')
const summary = await agent(`You are a read-only analyst in /home/user/BookMinder (git repo, full history already unshallowed — 390 commits). Do not modify tracked files.

GOAL: Extract a precise characterization of the BDD/TDD style the author (palimondo) was aiming for, by rewinding to the start of git history and replaying the evolution of Python code only. Your reader is the author: a professional developer, London-school/GOOS practitioner, who wants an exact, well-written account of the desired qualities of spec and implementation code.

PRIMARY LENS — MOTIVATION. Do not merely catalog observed regularities; for every practice you identify, reconstruct WHY the author does it that way: what failure it prevents, what value it protects, what first principle it follows. Derive rationale from the semantics of the artifact itself where possible (e.g. an integration test exists to exercise the real collaborator — mocking it would verify your own stub, so real fixtures there aren't a preference, they're definitional; London-school mocks are for roles/protocols you own at architectural boundaries in unit specs, never for the thing being integrated against). State every rule as a motivated principle — "X because Y" — not as a pattern report. Where the history shows a correction (revert, replacement, deletion), treat it as the author teaching the principle: name the principle. Where you cannot recover a motivation, say so explicitly rather than papering over it.

SCOPE: *.py files in bookminder/, specs/ (and any earlier test/spec dirs they were renamed from), conftest.py. EXCLUDE entirely: CLAUDE.md/AGENTS.md/docs edits, the xs tool sidequest, and NEVER open the claude-dev-log-diary/ directory except: you MAY read the two orientation reports .coordination/repo-map.md and .coordination/process-evolution.md (they give you the repo layout and process-history context). You MUST NOT read .coordination/bdd-style.md — a prior attempt at this same task exists there and your run must stay uncontaminated by it. Do not grep for it, do not open it.

METHOD: git log --reverse --oneline -- '*.py' ':!claude-dev-log-diary' then walk the sequence with git show on key commits. Watch the play-by-play: specs written before impl? describe_/it_ naming and granularity; assertion strength/style; fixture strategy; how minimal each GREEN implementation is; refactor commits; reverts/corrections. TODO.md says after commit 6f786cc ATDD discipline lapsed — contrast the gold-standard period before vs. the lapse: what specifically degraded.

DELIVERABLE: Write /home/user/BookMinder/.coordination/bdd-style-fable.md covering:
1. Spec style rules with concrete code examples from real commits (cite short SHAs)
2. Implementation style qualities (minimalism, structure, typing)
3. Observed TDD cadence in commit sequence (RED/GREEN/REFACTOR rhythm)
4. What the gold standard means here and exactly how the post-6f786cc lapse deviated
Dense, evidence-cited, no filler. FORMATTING: do not hard-wrap prose — one line per paragraph/bullet (the doc is read on mobile where every newline renders as a line break). Then return a summary of max 15 lines as your final text.`, { model: 'fable', effort: 'xhigh', label: 'bdd-style-fable' })
return summary