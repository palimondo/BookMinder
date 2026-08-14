export const meta = {
  name: 'pilot-compile-test',
  description: 'Compile pilot mining YAMLs into skill-rulebook and triaged detector list',
  phases: [{ title: 'Compile' }],
}
phase('Compile')
const summary = await agent(`You are the COMPILE step of an eval pipeline being trialed. Inputs (read both fully):
/tmp/claude-0/-home-user-BookMinder/a42b9c92-c0e6-588e-bc6f-3d5e4f37b895/scratchpad/mining/day-019.yaml
/tmp/claude-0/-home-user-BookMinder/a42b9c92-c0e6-588e-bc6f-3d5e4f37b895/scratchpad/mining/day-016.yaml
Context (read for orientation): /home/user/BookMinder/.coordination/eval-design.md and .coordination/bdd-style-canonical.md (the style guide extracted from git history — your output should COMPLEMENT it, flag overlaps).

The project author's concern, which your output must directly answer: the mined failure modes look like 2025-era agent blunders (destructive ops, fabrication) likely trained away by current models, and the mining seemed to produce nothing for the BDD-style skill. Test whether the compile step refutes or confirms that.

PRODUCE /tmp/claude-0/-home-user-BookMinder/a42b9c92-c0e6-588e-bc6f-3d5e4f37b895/scratchpad/mining/compiled-pilot.md with three sections:

1. SKILL RULEBOOK CANDIDATES — merge and dedupe the 40 skill_rules from both files; group by theme (TDD sequence / spec style / test doubles & layers / fixtures / git & commits / working discipline); for each rule note evidence locs, taught_or_enforced status, and whether it is ALREADY covered by bdd-style-canonical.md (overlap), NEW (dialogue-only — git never showed it), or CONTRADICTS it. The NEW count is the headline: it measures what mining adds over git archaeology.

2. DETECTOR TRIAGE — every failure_mode from both files sorted into: (a) TIMELESS DISCIPLINE (incentive-driven failures current models still exhibit: assertion weakening, no-RED, kitchen-sink, vacuous asserts, state narration...) — these become eval detectors; (b) 2025-ERA AGENTIC (likely trained away: destructive ops, fabricated tool claims, interactive-command misuse) — parked as a C0 regression baseline; (c) HARNESS-SOLVED (things hooks/permissions now block mechanically). Give counts and one-line justification each.

3. PHILOSOPHY FRAGMENTS — statements of the author's design worldview recoverable from these two files (from skill_rules 'because' clauses, pairing_gems, and quoted user turns): the reasoning that should feed the skill's WHY layer. Short verbatim-ish items with locs.

End with a 5-line VERDICT: does the pilot output feed the skill or not, and what schema changes the full run needs. No hard-wrapped prose. Return the verdict + headline counts (max 10 lines) as final text.`, { model: 'opus', effort: 'xhigh', label: 'compile-pilot' })
return summary