export const meta = {
  name: 'style-doc-comparison',
  description: 'Compare Opus vs Fable BDD-style characterizations',
  phases: [{ title: 'Compare' }],
}
phase('Compare')
const summary = await agent(`You are a read-only judge in /home/user/BookMinder (git repo, full history unshallowed). Do not modify tracked files except writing your deliverable.

TASK: Compare two independent characterizations of this project's BDD/TDD style, both extracted from the same git history:
- A: .coordination/bdd-style.md — by an Opus 5 worker at default effort; brief asked for dense evidence-cited rules; no orientation docs.
- B: .coordination/bdd-style-fable.md — by a Fable (Claude Fable 5) worker at xhigh effort; same core brief PLUS a motivation-first lens ("state every rule as X-because-Y") and access to .coordination/repo-map.md and process-evolution.md for orientation.

The project author read A through ~section 1.5 and was dissatisfied: A catalogs observed regularities without reconstructing WHY — e.g. it reports "real fixtures replaced mocks in integration tests" without noting that mocking the thing being integrated against is self-refuting, so real fixtures there are definitional, not preferential. The author wants to know whether this shallowness is attributable to the weaker model or to the brief.

METHOD:
1. Read both docs fully. Score each on: (a) rationale depth — rules as motivated principles vs pattern reports; (b) writing quality — prose clarity, structure, information density, readability; (c) evidence accuracy — spot-check at least 8 cited SHAs from EACH doc against actual git history (git show); flag any misattributed or confabulated citations; (d) insight — findings that required inference, not just observation.
2. Attribution analysis: for each major difference, judge whether it plausibly traces to (i) the motivation-lens instruction B received, (ii) orientation-context advantage, (iii) effort level, or (iv) intrinsic model capability. Be honest that these are confounded; look for discriminating evidence — e.g. rationale-shaped reasoning A produced UNPROMPTED anywhere, or places B went beyond what its brief demanded (beyond-brief inference suggests capability, not prompt).
3. Verdict: is A's shallowness brief-induced, model-induced, or both? What would a re-briefed Opus likely achieve?

DELIVERABLE: Write /home/user/BookMinder/.coordination/style-comparison.md. Dense, specific, quote both docs where it matters. No hard-wrapped prose — one line per paragraph/bullet (mobile rendering). Return a max-12-line summary as final text.`, { model: 'fable', effort: 'xhigh', label: 'style-compare' })
return summary