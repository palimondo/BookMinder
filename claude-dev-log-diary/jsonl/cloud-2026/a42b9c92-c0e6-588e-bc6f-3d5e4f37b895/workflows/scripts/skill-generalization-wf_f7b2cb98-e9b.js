export const meta = {
  name: 'skill-generalization',
  description: 'Strip provenance/timing and project-specific phrasing from project-coordinator skill',
  phases: [{ title: 'Generalize' }],
}
phase('Generalize')
const r = await agent(`Repo: /home/user/BookMinder. Edit .claude/skills/project-coordinator/ (SKILL.md + references/*.md, 7 files) per two author directives:

1. REMOVE PROVENANCE AND TIMING: no dates, no "since 2026-08-11", no "this engagement", no session-history narration ("was adopted after you launched...", "an overnight swarm died to this"). Rules stand as rules. Short verbatim author quotes may STAY only where the quote itself sharpens the rule's meaning (e.g. the strip-test definition); drop quotes that are merely historical evidence. Rewrite affected sentences so they read as standing policy, not memoir.

2. REMOVE PROJECT-SPECIFIC SCOPE: this skill must be a PORTABLE coordinator process for working with this author on ANY project — project specifics get their own skill later. Remove/relocate BookMinder-specific content: the mining/compile pipeline references, BookMinder file paths and corpus layout, eval-specific machinery. KEEP as portable conventions: the .coordination/threads.md substrate pattern (HANDOFF header, ledgers, parked proposals — that structure is the author's method, not this project), worker self-commit, watchdog chain, claims discipline, tier routing, all conduct rules. Anything removed that carries real knowledge goes VERBATIM into .coordination/skill-removals-for-project-skills.md (with a one-line header saying these fragments await absorption into the bookminder project skill) — relocate, never destroy.

Also update the frontmatter description to match the generalized scope (drop "BookMinder"; keep the pushy when-to-use list; what+when only, no internal structure). Run .claude/skills/skill-creator/scripts/quick_validate.py. No hard-wrapped prose.

SELF-COMMIT: git add changed/new files by name, commit "refactor: generalize project-coordinator skill; relocate project-specific fragments", push (pull --rebase retry). Return max-6-line summary: what moved to removals file, final line counts.`, { model: 'fable', effort: 'xhigh', label: 'generalize' })
return r