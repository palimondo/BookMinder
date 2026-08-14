export const meta = {
  name: 'diary-mining-pilot',
  description: 'Pilot rationale-mining on day-019 (Claude) and day-016 (Gemini)',
  phases: [{ title: 'Mine' }],
}

const SCHEMA = `Write a single valid YAML file with EXACTLY this schema (omit empty keys; no prose outside YAML):
file: day-NNN
date: YYYY-MM-DD
agent_era: <claude-code | claude-code-via-claude-trace | gemini-cli>
failure_modes:
  - name: <kebab-case slug — use the controlled vocabulary below when it fits, coin a new slug only when nothing fits>
    loc: "day-NNN:L<line>"
    quote: "<verbatim, max 3 lines>"
    what_happened: <1-2 sentences>
    user_intervention: <1 sentence — what the user did>
    outcome: <1 sentence — fixed / reverted / persisted / unresolved>
    detectable_by: <git | transcript | both>
    detector_candidate: <1-2 sentences — a mechanical check over commits/tool-calls, or "judge-rubric: <criterion>">
    rule_origin: <CLAUDE.md section name IF this incident plausibly birthed a rule — tag in passing, never hunt>
skill_rules:
  - rule: <imperative, one sentence — something the user taught that a style skill must encode>
    because: <the motivation, one sentence>
    evidence: "day-NNN:L<line>"
    taught_or_enforced: <taught-once | repeated | needed-enforcement>
pairing_gems:
  - loc: "day-NNN:L<line>"
    why_exemplary: <1-2 sentences — a moment the pairing discipline WORKED>
parked:
  - <one-line observation that is interesting but out of scope — the parking lot for everything off-schema>

Controlled vocabulary for failure_mode names: structure-hijack, same-name-weakening, tautological-mock, vacuous-assertion, no-red-verification, refactor-mislabel, fabricated-claim, instruction-drift, unauthorized-destructive-op, scope-creep, defensive-code-unrequested, comment-noise, wrong-layer-test, premature-implementation.

ACCEPTANCE CRITERIA: every failure_mode has quote+loc+detector_candidate; every skill_rule traces to evidence; anything off-schema goes to parked as one line. Quotes verbatim from the transcript, max 3 lines each.`

phase('Mine')
const results = await parallel([
  () => agent(`You are a rationale miner. Read /home/user/BookMinder/claude-dev-log-diary/day-019.md IN FULL (5383 lines, Claude Code session via claude-trace, 2025-07-07 era) — read sequentially in chunks. Also skim .coordination/diary-scout.md §5 for format quirks first. User turns start with "> " at column 0; assistant turns with ⏺.

MISSION: extract material for (a) a TDD/BDD-discipline eval and (b) a BDD-style skill. Mine the USER's corrective/interrogative turns and the incidents around them. Known landmarks to find and mine (do not stop at them): ~L470 user halts agent mid sqlite3 UPDATE on a fixture DB; expert-council retro rejected as "AI slop"; revert order ~L1247; ATDD teaching arc in second half ("We are practicing ATDD, we should be going outside-in", "Where are we in the TDD cycle?").

${SCHEMA}

DELIVERABLE: write /tmp/claude-0/-home-user-BookMinder/a42b9c92-c0e6-588e-bc6f-3d5e4f37b895/scratchpad/mining/day-019.yaml (create dir; scratchpad destination for user review — repo commit only after explicit user approval). Return max-8-line summary: counts per section + the single most eval-valuable find.`, { model: 'opus', effort: 'xhigh', label: 'mine:day-019' }),
  () => agent(`You are a rationale miner. Read /home/user/BookMinder/claude-dev-log-diary/day-016.md IN FULL (7718 lines, Gemini CLI session, 2025-07-04 era) — read sequentially in chunks. Also skim .coordination/diary-scout.md §5 for format quirks first. CRITICAL FORMAT NOTE: this file box-wraps everything; user turns match "^│  > " (TWO spaces after the bar) — the scout report's "│ >" single-space regex is WRONG and returns zero. Assistant turns use ✦. Whitespace-normalize lines before quoting (strip box-drawing frame and padding).

MISSION: extract material for (a) a TDD/BDD-discipline eval and (b) a BDD-style skill. Mine the USER's corrective/interrogative turns and the incidents around them. Known landmarks to find and mine (do not stop at them): ~L1390 fixture-vs-real-DB rm scare ("Wait!!! What did you rm last time?!"); ~L641 self-documenting-code rule taught; ~L4835 commit-prefix-convention discussion; staging/git-rm correction and revert order ~L5041; 75 story-card references — capture card-workflow rationale.

${SCHEMA}

DELIVERABLE: write /tmp/claude-0/-home-user-BookMinder/a42b9c92-c0e6-588e-bc6f-3d5e4f37b895/scratchpad/mining/day-016.yaml (create dir; scratchpad destination for user review — repo commit only after explicit user approval). Return max-8-line summary: counts per section + the single most eval-valuable find.`, { model: 'opus', effort: 'xhigh', label: 'mine:day-016' }),
])
return results.filter(Boolean)