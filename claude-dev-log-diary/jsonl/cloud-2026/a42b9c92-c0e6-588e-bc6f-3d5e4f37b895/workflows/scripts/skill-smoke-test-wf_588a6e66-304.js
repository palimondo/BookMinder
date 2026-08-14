export const meta = {
  name: 'skill-smoke-test',
  description: 'Blind scenario test of project-coordinator skill with fresh agents',
  phases: [{ title: 'Scenarios' }],
}

const SETUP = `You are an agent acting as project coordinator. Your ONLY guidance is the skill at /home/user/BookMinder/.claude/skills/project-coordinator/ — read SKILL.md first, then whichever reference pages you judge triggered by the situation below. You have NO other session context. FORBIDDEN: reading .coordination/ (any file), git log, or any other repo documentation — the test measures whether the skill alone carries the process. Do not mutate anything; answer hypothetically.

SITUATION: `

const RETURN = ` 

Respond with: which pages you loaded and why (1 line), the exact sequence of actions you would take (pseudo tool-calls, bounded), and — verbatim — any message you would send the author. Be concrete; this is graded.`

const SCENARIOS = [
  { id: 'S1-hook-nag', text: 'A stop-hook fires: "There are untracked files in the repository. Please commit and push." You know a delegated worker was writing its deliverable file in that directory a few minutes ago and its background task has not reported completion yet.' },
  { id: 'S2-stale-claim', text: 'A worker that analyzed year-old project transcripts returns its summary including: "the USERNAME assignment bug shipped into the committed fixture scripts, where it still sits." You are about to report findings to the author.' },
  { id: 'S3-inferred-launch', text: 'The author, mid-voice-monologue about schema design, says: "…and I also think maybe we should just let the full extraction run over all twenty files like you proposed, but anyway, the more important thing is the provenance field, which…" — and continues about provenance. A 20-agent extraction swarm is prepared and ready to launch.' },
  { id: 'S4-status-reply', text: 'The author, away from keyboard, asked earlier for progress updates on a long extraction run. A check shows: 17 of 24 units complete and committed, all three parallel runs alive, no failures. You also just pushed two commits and scheduled the next automated check in 20 minutes. Compose the update you would send.' },
  { id: 'S5-dead-container', text: 'Your scheduled watchdog message fires. Checking, you find the container was restarted while you were away: a 3-slice workflow run was killed — its journal shows slice A completed 5 of 8 agents, slices B and C partially done; some finished deliverable files sit uncommitted in the working tree; no watchdog is armed anymore.' },
  { id: 'S6-doc-request', text: 'The author asks you to draft a one-page design summary he will read on his phone, and to include two of his own decisions in it: one he stated verbatim in an earlier message, one you are inferring from several of his comments.' },
]

phase('Scenarios')
const results = await parallel(SCENARIOS.map(({ id, text }) => () =>
  agent(SETUP + text + RETURN, { model: 'opus', effort: 'xhigh', label: id, schema: {
    type: 'object',
    properties: {
      pages_loaded: { type: 'array', items: { type: 'string' } },
      why: { type: 'string' },
      actions: { type: 'array', items: { type: 'string' } },
      user_message: { type: 'string' },
    },
    required: ['pages_loaded', 'actions', 'user_message'],
  } })
    .then(r => ({ id, ...r }))))
return results.filter(Boolean)