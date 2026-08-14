export const meta = {
  name: 'skill-restructure',
  description: 'Rework project-coordinator skill per skill-writing best practices',
  phases: [{ title: 'Rework' }],
}
phase('Rework')
const r = await agent(`Repo: /home/user/BookMinder. Task: restructure an overlong skill per skill-writing best practices, using the vendored authoring toolkit.

READ FIRST: .claude/skills/skill-creator/SKILL.md and whatever of its references/ you need — follow ITS guidance on SKILL.md length, progressive disclosure, description/trigger-phrase design, and reference-file structure. Also run its scripts/quick_validate.py on your result if applicable.

THEN restructure .claude/skills/project-coordinator/SKILL.md (currently ~220 lines, violates length best practice — the author didn't read it; he trusted and then balked). Requirements from the author, verbatim intent: "structured in two chapters and separate markdown documents with trigger phrases for loading the specific things… more compact with proper triggering phrases to ensure that the page swapping of knowledge occurs correctly."

Design: SKILL.md becomes a COMPACT ROUTER — the always-loaded core must fit what a coordinator needs at every moment (the non-negotiable conduct invariants + the map of when to load which chapter), with explicit trigger phrases ("when launching or managing workers/swarms, read references/operations.md"; "when writing to the user or handling his feedback, read references/conduct.md" — that style). Split the body into ~2 reference chapters (the author said two; if the material genuinely demands a third, justify it in one line of the commit message): likely split = OPERATIONS (delegation/tiers/tool-routing, swarm ops, reclamation survival, git conventions, claims discipline, persistence machinery) vs CONDUCT+GOVERNANCE (register, attribution, approval boundaries, scope control, after-pushback, context protection). PRESERVE ALL CONTENT — this is restructuring, not summarizing; every rule and verbatim anchor survives, just relocated. Keep the POSSIBLY UNABSORBED audit section wherever it fits (it awaits author review). Keep frontmatter name: project-coordinator; rewrite description with strong trigger phrases per skill-creator guidance. No hard-wrapped prose.

DELIVERABLE + SELF-COMMIT: the restructured .claude/skills/project-coordinator/ (SKILL.md + references/*.md), git add the directory's files by name, commit "refactor: restructure project-coordinator skill per skill-creator best practices", push (pull --rebase retry if rejected). Return max-8-line summary: final SKILL.md line count, chapter layout, and what skill-creator guidance drove the key choices.`, { model: 'fable', effort: 'xhigh', label: 'skill-rework' })
return r