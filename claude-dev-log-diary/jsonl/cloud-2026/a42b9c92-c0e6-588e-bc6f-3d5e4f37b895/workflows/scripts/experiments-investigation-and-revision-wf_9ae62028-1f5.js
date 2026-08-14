export const meta = {
  name: 'experiments-investigation-and-revision',
  description: 'Investigate Claude-experiment episodes, then revise style guide',
  phases: [{ title: 'Investigate' }, { title: 'Revise' }],
}

phase('Investigate')
const episodes = await agent(`Read-only analyst in /home/user/BookMinder (git repo, full history unshallowed). Modify nothing except your deliverable.

CONTEXT: The project author is separating THEIR intended BDD/TDD style from fallout of two experiments where Claude was given autonomy and the result was bad. Orientation: .coordination/process-evolution.md, repo-map.md, threads.md. Do NOT read claude-dev-log-diary/ contents.

INVESTIGATE TWO EPISODES chronologically, from git history (commits, diffs, messages, dates):

EPISODE A — the CLAUDE.md rewrite disaster: the author accreted guidelines over time; at some point Claude was allowed to rewrite/compress the file (dedup, contradiction removal); the compressed version was WORSE at keeping Claude working in the author's preferred way; it was reverted (process-evolution.md cites b5c84b2→9bacc8a, −62%, collateral loss of the commit-after-RED rule). Establish: full chronology, what the compression actually changed (diff-level), why it plausibly degraded behavior, what was lost in the revert crossfire, residue today.

EPISODE B — the test-suite reorganization that went wrong: at some point the diagnosis was that the SHAPE of the test suite was steering the model toward writing wrong specs, and a reorganization of the suite was attempted, which failed. Find it: look for spec-tree restructures (directory moves, unit/integration/acceptance/e2e splits, mass renames, "reorganize"/"restructure"/"move" commit subjects), what preceded them (the diagnosis), what followed (reverts, corrections, the e5c7074 fixture→mock swap if related). Establish: what was diagnosed, what change was made, by whom (bot-authored? co-authored?), how it went wrong, what was kept vs reverted, and what of TODAY's spec-tree layout is experiment fallout rather than author intent.

DELIVERABLE: .coordination/claude-experiments.md — chronological executive summary of both episodes (dates, SHAs), era mapping, and a LESSONS section: which patterns visible at HEAD are author-intent vs experiment-fallout, and what each episode teaches for a BDD style guide. No hard-wrapped prose. Return max-15-line executive summary as final text.`, { model: 'opus', effort: 'xhigh', label: 'episodes', phase: 'Investigate' })

phase('Revise')
const revision = await agent(`You are revising /home/user/BookMinder/.coordination/bdd-style-canonical.md IN PLACE. Modify no other file. Full git history available for verification.

THE AUTHOR READ THE CURRENT VERSION AND GAVE THREE CORRECTIONS:

1. THE WHY SECTION IS WRONG. It fused pair programming with verification ("a pair is someone whose claims you can check") — the author calls this totally off base, "merging unrelated concepts". Their ACTUAL motivation, in their words: pair programming is about having a partner to bounce ideas off — discussing what's the next step, how do we define the test, how do we minimize the surface area for the implementation, what are the minimal constraints to express in a spec to get the desired behavior in the next step. THAT is the discipline of pairing in BDD style. It has nothing to do with verifying claims. Rewrite the motivation layer faithfully to this. Separately true (don't delete, just don't fuse): executable specs nail verifiable invariants; long-term evolution vs one-shotting; London school/GOOS; minimal coupling of spec to implementation. Do not tie these into one clever thesis — present motivations as the author holds them, side by side.

2. STRIP ALL META-COMMENTARY about how the document came about — no mention of extractions, judges, syntheses, A/B/C, "this document", provenance notes. The deliverable is a STYLE GUIDE TO BE APPLIED: prescriptive, how-to, each rule with its motivation. Someone (human or agent) should be able to work in this style by following it.

3. SEPARATE AUTHOR INTENT FROM EXPERIMENT FALLOUT. Read .coordination/claude-experiments.md (a just-completed investigation of two episodes where Claude was given autonomy — a CLAUDE.md rewrite disaster and a test-suite reorganization gone wrong). Where the current guide presents a pattern as "the style" that the investigation shows to be fallout of those experiments rather than author intent, fix it: either drop it or explicitly mark it as a known deviation to repair. The guide must describe the style the AUTHOR was going for.

Keep: the high-level→specific structure, evidence SHAs where they teach, the lapse anatomy (as cautionary section), open-wounds list (as repair backlog). Keep mobile formatting (no hard-wrapped prose). Return max-10-line summary of what changed.`, { model: 'fable', effort: 'xhigh', label: 'revise-guide', phase: 'Revise' })

return { episodes, revision }