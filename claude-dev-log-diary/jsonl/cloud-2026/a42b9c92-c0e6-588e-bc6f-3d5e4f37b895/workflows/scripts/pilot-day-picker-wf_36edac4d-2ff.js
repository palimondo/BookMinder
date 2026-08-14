export const meta = {
  name: 'pilot-day-picker',
  description: 'Pick one Claude day and one Gemini day for the mining pilot',
  phases: [{ title: 'Pick' }],
}
phase('Pick')
const picks = await agent(`Read-only scout in /home/user/BookMinder. First read .coordination/diary-scout.md — the full reconnaissance of claude-dev-log-diary/ (inventory, per-file token estimates, format quirks, user-turn counts). You are authorized to sample inside claude-dev-log-diary/.

TASK: We will pilot a rationale-mining swarm on exactly TWO day-files before the full run: one Claude-agent day and one Gemini-CLI day (days 011-016 are Gemini). Pick the best candidates.

Criteria, priority order: (1) NO sharding — exclude day-020; prefer ~20–50k tokens; (2) overlap era (day-010..day-019) — story-card-era rationale is the target; (3) maximize density of USER corrective/interrogative turns (discipline enforcement, design pushback, style teaching — remember Gemini files box-wrap user prompts as \`│ >\`, so \`^> \` greps return 0 spuriously there); (4) days with known incidents/decisions beat quiet execution days.

Method: light sampling only — grep turn markers with counts, read a few small windows (~40-60 lines) at high-density spots to gauge corrective quality. NO bulk reads.

Return as final text (no file output): ONE Claude pick + ONE Gemini pick, each justified in 3-4 lines (size, era, expected yield, notable content sampled), plus one-line runner-ups. Max 18 lines total.`, { model: 'opus', effort: 'xhigh', label: 'day-picker' })
return picks