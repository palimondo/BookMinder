export const meta = {
  name: 'verified-residue-sweep',
  description: 'Verify all present-tense repo claims from mining corpus against HEAD',
  phases: [{ title: 'Sweep' }],
}
phase('Sweep')
const r = await agent(`You are the claims-verification stage (design: .coordination/eval-design.md "Claims-verification design"). Repo: /home/user/BookMinder, work against CURRENT HEAD of the working tree.

TASK: Sweep these sources for every PRESENT-TENSE claim about the current repository state ("still at HEAD", "currently", "sits at", "remains", "is live", "unspecified today", file:line references presented as current, defects said to persist):
1. All 24 files in .coordination/mining/v2/*.yaml (fields: what_happened, outcome, parked, gaps, detector notes)
2. .coordination/mining/pairing/*.yaml (3 files)
3. .coordination/bdd-style-canonical.md §5 (open wounds / repair backlog) and any other present-tense claims in it
4. .coordination/claude-experiments.md LESSONS section residue claims

For EACH claim: (a) state it, (b) construct the executable check (grep pattern / file:line read / command with expected output), (c) RUN the check, (d) verdict: VERIFIED@<short-sha of HEAD> | FALSE-AT-HEAD (was true historically, since cured — name the curing event if visible in git log) | NEVER-TRUE (claim wrong even for source time, if evident) | UNCHECKABLE (state why — e.g. requires macOS/real Apple Books).

Known calibration cases (your sweep must agree or explain): the zsh USERNAME=$1 bug is FALSE-AT-HEAD (scripts now use FIXTURE_USER=$1); docs/apple_books.md:561-area evidence-free "ZISSAMPLE IS NULL OR ZISSAMPLE = 0" defensiveness was reported VERIFIED at HEAD by a miner — re-verify; the cli.py "test comment" and cli_spec.py patch-target claims predate the spec-tree restoration (commit "revert: restore spec tree to pre-reorg checkpoint") — many §5 wounds may have been cured or resurrected by that restoration, check each against the CURRENT tree, not the tree the documents described.

DELIVERABLE: write /home/user/BookMinder/.coordination/verified-residue.md — header states HEAD sha + date; then (1) REPAIR BACKLOG: claims VERIFIED at HEAD (the true current defect list), each with its check inline so it can be re-run; (2) CLOSED: FALSE-AT-HEAD items with curing event; (3) UNCHECKABLE list; (4) sweep stats. No hard-wrapped prose. Self-commit: git add the file by name, commit "docs: verified-residue - stamped repair backlog from claims sweep", push (retry with pull --rebase if rejected). Return max-8-line summary: counts per verdict + any surprise.`, { model: 'opus', effort: 'xhigh', label: 'residue-sweep' })
return r