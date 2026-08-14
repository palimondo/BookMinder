export const meta = {
  name: 'diary-recon-scout',
  description: 'Reconnaissance of claude-dev-log-diary: inventory, coverage, story-card overlap',
  phases: [{ title: 'Scout' }],
}
phase('Scout')
const report = await agent(`Read-only scout in /home/user/BookMinder. The user has JUST authorized reconnaissance inside claude-dev-log-diary/ (previously gated). This is RECON, not bulk processing — a multi-agent swarm may follow later; your job is the lay of the land. The dir is ~12M / 83 files: NEVER read a large file whole. Use ls -la, du, wc -l, head/tail, grep with head_limit, and small sampled excerpts only.

QUESTIONS, in priority order:

1. INVENTORY: what is in claude-dev-log-diary/? Full tree with sizes. Classify each file/subdir: raw console transcripts? JSONL session transcripts? Gemini-produced day summaries (day-001..day-021 known to exist)? tools/ (the xs sidequest — skip its internals)? Other artifacts? Note formats and naming conventions.

2. TIME COVERAGE: for each transcript-like class, what date range does it cover? (Derive from filenames, first/last lines, file mtimes, git log of the dir.) Where exactly does full-transcript coverage STOP?

3. THE OVERLAP QUESTION (user's key concern): when were the YAML story cards introduced and actively used? (git log --follow on stories/ — the migration commits and the era of card-driven development, roughly July 2025 per prior analysis; pin exact dates.) Does the story-card era OVERLAP the period covered by full transcripts in the diary, or did transcripts stop before cards arrived? Answer precisely: overlap window with dates, or gap size.

4. INTENT RECOVERABILITY SAMPLE: pick ONE early session transcript and read its opening ~100-200 lines plus one or two small sampled windows. Qualitatively: how much of the USER's intent/motivation lives in the dialogue vs what git commits preserve? Quote 2-3 SHORT illustrative user utterances (a few lines each, no more). Estimate signal density: is swarm-processing these likely to recover design rationale that exists nowhere else?

5. SWARM FEASIBILITY NOTES: per-file token estimates, natural sharding (by session? by day?), and any format quirks a swarm should know.

DELIVERABLE: .coordination/diary-scout.md — inventory table, coverage timeline, overlap verdict, recoverability assessment with the short quotes, swarm notes. No hard-wrapped prose. Return a max-12-line summary with the overlap verdict stated first.`, { model: 'opus', effort: 'xhigh', label: 'diary-scout' })
return report