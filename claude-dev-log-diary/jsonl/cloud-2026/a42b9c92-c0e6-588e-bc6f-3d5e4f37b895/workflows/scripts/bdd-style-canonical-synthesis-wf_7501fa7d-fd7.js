export const meta = {
  name: 'bdd-style-canonical-synthesis',
  description: 'Synthesize canonical BDD/TDD style doc from B and C extractions',
  phases: [{ title: 'Synthesize' }],
}
phase('Synthesize')
const summary = await agent(`You are writing the canonical synthesis of the BookMinder BDD/TDD style characterization — the doc the project author will actually read, and the test of whether we understood their high-level goals. Repo: /home/user/BookMinder. Modify no file except your deliverable.

SESSION CONTEXT (read first): .coordination/threads.md — especially "Meta-goals (user's own framing)" and "Project history (user's account)". The author's frame, stated in their own words this session: the project tests whether an LLM can be a good pair programmer; executable specifications are the verifiable truth that nails invariants; the art is slicing the problem and designing specs with minimal coupling to implementation; London school per GOOS; the Apple Books schema shifts under the tool with every release, so this is a testbed for long-term software evolution, the opposite of one-shotting problems known from pretraining.

INPUTS (read all): .coordination/bdd-style-fable.md (B) and .coordination/bdd-style-opus2.md (C) — the two extractions to integrate; .coordination/style-comparison-3way.md and .coordination/style-comparison.md — judge findings, including two judge-only discoveries (e5c7074 swapped fixture acceptance tests for tautological mock versions; HEAD still patches cli.SUPPORTED_FILTERS at specs/acceptance/cli_spec.py:67, so the CLI→library delegation property is unspecified today). The original bdd-style.md (A) is discarded per the author — you may lift its HEAD-residue audit items only if they earn their place. Verify any claim you are unsure of against git directly (full history is unshallowed).

STRUCTURE — strictly high-level → specific (the author explicitly wants this order):
1. WHY: the motivation layer. What this style is FOR, in the author's frame. Write it as understanding, not quotation.
2. THE PRINCIPLES: each layer of the test architecture and its definitional logic (why mocks belong exactly where they do, per layer); minimalism-by-deletion; YAGNI as testability; discipline as a property of the sequence, not the snapshot.
3. THE PRACTICE: concrete play-by-play with SHAs — gold-standard cadence, the strongest worked examples from B and C (fa0bc72 patch-target mutation, fixture front-door injection via --user, exact-equality calibration per layer, revert-and-narrate corrections).
4. THE LAPSE: anatomy of the post-6f786cc degradation (and the earlier crack), each failure named as the principle it violated.
5. OPEN WOUNDS AT HEAD: what is still broken/unspecified today — short, actionable.

QUALITY BAR: every rule motivated (X because Y); no filler; no pattern-reports without rationale; honest where motivation is unrecoverable. Integrate, don't concatenate — resolve B/C disagreements by checking git; prefer C's ground-level precision and B's meta-insight where both hold. Reader is the author personally, a GOOS practitioner reading on a phone: NO hard-wrapped prose (one line per paragraph/bullet).

DELIVERABLE: Write /home/user/BookMinder/.coordination/bdd-style-canonical.md. Return a max-10-line summary noting anything you corrected or dropped from B/C and why.`, { model: 'fable', effort: 'xhigh', label: 'canonical-synthesis' })
return summary