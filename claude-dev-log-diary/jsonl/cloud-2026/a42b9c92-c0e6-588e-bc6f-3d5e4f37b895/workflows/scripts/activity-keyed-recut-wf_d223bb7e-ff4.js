export const meta = {
  name: 'activity-keyed-recut',
  description: 'Restructure project-coordinator skill into activity-keyed pages',
  phases: [{ title: 'Recut' }],
}
phase('Recut')
const r = await agent(`Repo: /home/user/BookMinder. You have FULL AUTHORITY to restructure .claude/skills/project-coordinator/ as you see fit — the author explicitly authorized a fresh redesign, unconstrained by the current two-chapter layout.

READ FIRST: .claude/skills/skill-creator/SKILL.md + its references on progressive disclosure and description design. Then read the current skill: SKILL.md + references/operations.md + references/conduct.md.

THE PROBLEM you are solving (author's critique, paraphrased): the current two coarse chapters both trigger on any substantial coordination turn, so the split spares no context — page-swapping is theater. Pages must align with ACTIVATION MOMENTS so a typical trigger loads ONE small page: e.g. a watchdog firing needs swarm-liveness/resume knowledge only; composing a reply to the author needs register rules only; an authorization question needs approval boundaries only; launching workers needs tier-routing/briefing only; a persistence sweep needs substrate/recording rules only. Design the page set yourself (likely 4-7 pages, ~25-60 lines each) — you are not bound by any prior cut, and you may also tighten the 31-line core if you can do better.

CONSTRAINTS: preserve ALL rules and their verbatim anchors (restructure, not summarize — you may deduplicate true redundancy); keep frontmatter name project-coordinator; description must carry trigger phrases per skill-creator guidance; each page opens with one line saying exactly when it should have been loaded; no hard-wrapped prose; run skill-creator's scripts/quick_validate.py on the result. The POSSIBLY UNABSORBED section was absorbed and deleted by the author's order — do not resurrect it.

DELIVERABLE + SELF-COMMIT: the restructured skill directory (delete obsolete files with git rm), git add/rm by name, commit "refactor: activity-keyed page structure for project-coordinator skill", push (pull --rebase retry if rejected). Return max-8-line summary: page list with line counts and each page's activation trigger.`, { model: 'fable', effort: 'xhigh', label: 'recut' })
return r