export const meta = {
  name: 'pairing-conduct-trial',
  description: 'Trial extraction of agentic-pair-programming skill (day-010, day-019, day-021)',
  phases: [{ title: 'Extract' }],
}

const DIARY = '/home/user/BookMinder/claude-dev-log-diary'
const REPO = '/home/user/BookMinder'

const SCHEMA = `Write ONE valid YAML file (no prose outside YAML):
file: day-NNN
date: YYYY-MM-DD
agent_era: <...>
pairing_rules:
  - rule_id: <pNNN-RN>
    rule: <imperative, addressed TO THE AGENT — transpose the author's conduct into what the AGENT should do>
    class: <mirror | reciprocal | council-mechanics>   # mirror = author's verification move the agent should internalize as reflex; reciprocal = the complementary conduct the author was teaching the agent (state intent before edits, surface disagreement, offer real alternatives); council-mechanics = operable procedure for convening expert consultation
    because: <one sentence>
    because_source: <user-verbatim | user-paraphrase | agent-synthesis>   # PROVENANCE SACRED: user-verbatim requires exact quote; agent-synthesis is YOUR inference, owned by you
    quote: "<exact words, max 3 lines — mandatory for user-verbatim>"
    evidence: "day-NNN:L<line>"
    guards_against: <anti-pattern name, optional>
council_episodes:
  - loc: "day-NNN:L<line>"
    trigger: <why convened — what decision/crossroads>
    invoked_by: <user | agent>
    personas: [<names>]
    voices: <individual | flattened-to-consensus>
    disagreement_use: <how divergence between voices was used, if at all>
    outcome: <accepted | rejected-as-slop | rerun-escalated | ignored>
    fidelity:
      - persona: <name>
        assessment: <faithful | caricature | fabrication>   # THE KEY LENS: was this the expert's actual actionable position, a slogan-caricature of it, or invented fact? Judge against your best knowledge of the real person's published positions; be honest that your own knowledge has the same pretraining limits — flag uncertainty
        evidence: "<quote or paraphrase + loc>"
    user_reaction: <1 sentence>
    lesson: <1 sentence — what this episode teaches about making consultation useful>
anti_patterns:
  - name: <kebab slug: sycophantic-fold, council-as-rubber-stamp, simulacra-shallowness, alternatives-theater, or coin new>
    loc: "day-NNN:L<line>"
    quote: "<verbatim, max 3 lines>"
    what_happened: <1-2 sentences>
philosophy:
  - statement: <author worldview relevant to PAIRING or to grounding expert knowledge — especially any trace of the motivation that BookMinder exists to give models access to FULL BOOKS because pretrained expert positions are lossy summaries>
    source: <user-verbatim | user-paraphrase | agent-synthesis>
    quote: "<mandatory for user-verbatim>"
    loc: "day-NNN:L<line>"
gaps: [<looked for but absent>]
parked: [<one-liners>]

VERIFY quotes verbatim before writing. Every rule addressed to the agent, never described as user behavior.`

const prompt = (f, note) => `You are a pairing-conduct miner for the BookMinder project. Read ${DIARY}/${f}.md IN FULL, in chunks. ${note}

CONTEXT: The project author used pair programming as the core working mode and invented /expert-council to channel the model's pretrained simulacra of TDD/BDD authorities (Kent Beck, Dave Farley, Steve Freeman, Nat Pryce, etc.). The author's retrospective verdict, given today: the simulacra were often SHALLOW CARICATURES — skewed, non-actionable summaries of the real experts' positions — and this frustration is one of BookMinder's own motivations (give models the full books so principles can be extracted from primary sources). Your job: extract (1) the agentic-pair-programming skill evidence — the author's conduct transposed into rules FOR THE AGENT; (2) every /expert-council episode with a fidelity assessment of each persona; (3) pairing anti-patterns.

${SCHEMA}

DELIVERABLE + SELF-COMMIT (author-directed technique): write ${REPO}/.coordination/mining/pairing/${f}.yaml (create dir), then commit YOUR OWN deliverable: git -C ${REPO} add .coordination/mining/pairing/${f}.yaml && git -C ${REPO} commit -m "docs: pairing-conduct trial harvest ${f}" && git -C ${REPO} push. If push fails (another worker pushed first), run git -C ${REPO} pull --rebase origin claude/bookminder-recall-5ite2s then push again, up to 3 attempts with a few seconds between. Your workload file is disjoint from other workers — never touch their files. Return max-6-line summary: counts + the single clearest caricature example you found.`

phase('Extract')
const results = await parallel([
  () => agent(prompt('day-010', 'Claude Code era, user marker "> " col 0. 18 council refs, 43 persona refs — likely the council idea ORIGIN period: capture how/why the author invented it, first invocation format, initial expectations.'), { model: 'opus', effort: 'xhigh', label: 'pair:day-010' }),
  () => agent(prompt('day-019', 'claude-trace era, user marker "> " col 0. 26 council refs, 49 persona refs. Known episodes: first council verdict rejected as "AI slop adjacent" with escalated ultrathink re-run; Dave Farley persona fabricating a "2022 snapshot" fact; user forbidding Task-tool delegation of councils after nuance loss; council teaching the test-architecture layering. Mine ALL of these plus what v-mining missed.'), { model: 'opus', effort: 'xhigh', label: 'pair:day-019' }),
  () => agent(prompt('day-021', 'Claude Code era, user marker "> " col 0. 94k tokens — read in chunks. 51 council refs — the MATURE council usage peak and densest story-card discussion. Capture evolved council protocol vs earlier days and any explicit user reflection on council quality.'), { model: 'opus', effort: 'xhigh', label: 'pair:day-021' }),
])
return results.filter(Boolean)