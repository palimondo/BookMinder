export const meta = {
  name: 'diary-mining-full-v2b',
  description: 'Full-scope schema-v2 mining, deduplicated corpus (relaunch after container restart)',
  phases: [{ title: 'Mine' }],
}

const OUT = '/tmp/claude-0/-home-user-BookMinder/a42b9c92-c0e6-588e-bc6f-3d5e4f37b895/scratchpad/mining/v2'
const DIARY = '/home/user/BookMinder/claude-dev-log-diary'
const SHARDS = `${OUT}/shards`

const SCHEMA = `Write ONE valid YAML file (no prose outside YAML) with this schema — omit empty keys:
file: <day-NNN or day-020-sN>
date: YYYY-MM-DD
agent_era: <claude-code-research-preview | claude-code | gemini-cli | claude-code-via-claude-trace>
model: <model name if identifiable; note silent downgrades with locs>
sub_sessions: [<line ranges if the file contains multiple sessions>]
philosophy:
  - statement: <the author's design-worldview point>
    source: <user-verbatim | user-paraphrase | agent-synthesis>   # PROVENANCE IS SACRED: user-verbatim REQUIRES exact quote; agent-synthesis means YOUR inference, clearly owned by you, never attributed to the author
    quote: "<exact words, max 3 lines — mandatory when source is user-verbatim>"
    loc: "day-NNN:L<line>"
    feeds: <skill-why | judge-anchor>
skill_rules:
  - rule_id: <dNNN-RN>
    rule: <imperative, one sentence>
    because: <motivation, one sentence>
    because_source: <user-verbatim | user-paraphrase | agent-synthesis>
    quote: "<mandatory when because_source is user-verbatim>"
    evidence: "day-NNN:L<line>"
    taught_or_enforced: <taught-once | repeated | needed-enforcement>
    skill_target: <tdd-bdd | project-memory | pair-programming | claude-md>   # generic discipline vs BookMinder/Apple-Books-specific lore vs pairing CONDUCT (how to collaborate: challenge designs, propose alternatives, verify Socratically) vs repo config
    overlap: <none | "CLAUDE.md <section>" | "canonical §N.N" | both>   # check BOTH /home/user/BookMinder/CLAUDE.md and .coordination/bdd-style-canonical.md
    feasibility: <ok | "needs-rework: <why>">   # executable as written in a non-interactive agent harness?
failure_modes:
  - name: <kebab slug; controlled vocabulary: structure-hijack, same-name-weakening, tautological-mock, vacuous-assertion, no-red-verification, refactor-mislabel, fabricated-claim, instruction-drift, unauthorized-destructive-op, scope-creep, defensive-code-unrequested, comment-noise, wrong-layer-test, premature-implementation, unverified-diagnosis, prod-code-bent-to-fixture, assertion-weakening; coin new only if nothing fits>
    era_class: <timeless-discipline | 2025-agentic | harness-solved | model-artifact>
    detector_family: <F1-red-first-grammar | F2-assertion-integrity | F3-minimality | F4-layering | F5-claim-vs-action | F6-refactor-honesty | new:<name>>
    loc: "day-NNN:L<line>"
    quote: "<verbatim, max 3 lines>"
    what_happened: <1-2 sentences>
    user_intervention: <1 sentence>
    outcome: <fixed | reverted | persisted | unresolved + 1 clause>
    detectable_by: <git | transcript | both>
    detector_candidate: <1-2 sentences>
    rule_origin: <CLAUDE.md section, or "unknown" — MANDATORY field>
pairing_gems:
  - loc: "day-NNN:L<line>"
    why_exemplary: <1-2 sentences>
gaps:
  - <thing you looked for but found NO instance of, e.g. "no commit-after-RED practice (rule postdates this session)" — makes absence distinguishable from oversight>
parked:
  - <one-line off-scope observations>

VERIFY every quote verbatim against the source before writing. ACCEPTANCE: every failure_mode has quote+loc+detector_candidate+rule_origin; every skill_rule has evidence+skill_target+overlap; every user-verbatim item has its exact quote.`

const minerPrompt = (path, era, note, outName) => `You are a rationale miner for the BookMinder project. Read ${path} IN FULL, sequentially in chunks. Era: ${era}. ${note}

Orientation (read first, briefly): /home/user/BookMinder/.coordination/diary-scout.md §5 (format quirks). For overlap checks read /home/user/BookMinder/CLAUDE.md and /home/user/BookMinder/.coordination/bdd-style-canonical.md as needed.

MISSION (priority order): (1) PHILOSOPHY — the author's design worldview stated in dialogue: why TDD-as-process, executable-truth reasoning, slicing/minimal-constraint thinking, London-school-in-Python adaptations, story-card workflow rationale. (2) SKILL RULES — practices the author taught, each targeted to the right skill (generic tdd-bdd vs BookMinder project-memory vs pair-programming conduct vs claude-md). (2b) PAIRING CONDUCT deserves active hunting, not incidental capture: how the author critiques proposed designs, demands alternatives, asks Socratic verification questions, halts-and-asks-for-explanation, and invokes /expert-council (his mechanism for channeling the model's pretrained BDD/TDD expert simulacra) — record HOW councils are convened, which personas appear, how disagreement between voices is used, and what makes a council round succeed or get rejected; encode reusable conduct as skill_rules with skill_target: pair-programming. (3) FAILURE MODES — record all, but classify era_class honestly; timeless-discipline failures matter most, 2025-agentic ones are catalog-only. (4) pairing_gems, gaps, parked.

${SCHEMA}

DELIVERABLE: ${OUT}/${outName}.yaml. Return max-6-line summary: counts per section + best find.`

phase('Mine')
const FILES = [
  { f: 'day-002', era: 'claude-code-research-preview', note: 'ALSO read day-001.md first (44 lines of hand-written notes — fold any signal into your output). User marker "> " col 0, assistant ⏺. Contains the project requirements dialogue and the diary-protection incident (~L889).' },
  { f: 'day-003', era: 'claude-code-research-preview', note: 'User marker "> " col 0.' },
  { f: 'day-004', era: 'claude-code-research-preview', note: 'User marker "> " col 0.' },
  { f: 'day-005', era: 'claude-code', note: 'User marker "> " col 0.' },
  { f: 'day-006', era: 'claude-code', note: 'User marker "> " col 0. Known: contains the fabricated-metrics episode the user called out (draft claimed "44% code reduction").' },
  { f: 'day-007', era: 'claude-code', note: 'User marker "> " col 0. DUPLICATION WARNING: L6396-L7658 is a copy-paste duplicate of L1852-L3114 (transcript re-paste, verified by shingle scan) — SKIP the L6396-L7658 range entirely; mine each incident once at its first occurrence.' },
  { f: 'day-008', era: 'claude-code', note: 'User marker "> " col 0.' },
  { f: 'day-009', era: 'claude-code', note: 'User marker "> " col 0. Session reportedly ended when credits ran out.' },
  { f: 'day-010', era: 'claude-code', note: 'User marker "> " col 0. Story-card era begins around here.' },
  { f: 'day-011', era: 'gemini-cli', note: 'Gemini CLI: assistant ✦, user marker plain "> ". 96k tokens — largest single-agent file; read in chunks. Contains the story-card system BIRTH (~L8985-9600): mine that dialogue deeply for philosophy.' },
  { f: 'day-012', era: 'gemini-cli', note: 'User marker plain "> ". Known incident: "Why are you completely overwriting cli_spec?!? WTF!!!".' },
  { f: 'day-013', era: 'gemini-cli', note: 'User marker plain "> ".' },
  { f: 'day-014', era: 'gemini-cli', note: 'User marker plain "> ". Small file (7k).' },
  { f: 'day-015', era: 'gemini-cli', note: 'BOX-WRAPPED: user marker is "│  > " (bar, TWO spaces). Strip box-drawing frames before quoting.' },
  { f: 'day-016', era: 'gemini-cli', note: 'BOX-WRAPPED: user marker "│  > " (TWO spaces). Known: rm scare ~L1390, real-DB DELETE ~L3767, git-restore catastrophe ~L5077, silent pro→flash downgrades (~L2003+) — tag post-downgrade failures era_class: model-artifact.' },
  { f: 'day-017', era: 'claude-code-via-claude-trace', note: 'User marker "> " col 0. 117 story-card refs.' },
  { f: 'day-018', era: 'claude-code-via-claude-trace', note: 'User marker "> " col 0. 158 user turns — densest interactive file; mine thoroughly.' },
  { f: 'day-019', era: 'claude-code-via-claude-trace', note: 'User marker "> " col 0. Known: fixture-UPDATE halt ~L470, vacuous disjunctive assert ~L303, "passes by accident" ~L336, revert order ~L1247, ATDD teaching arc in second half.' },
  { f: 'day-021', era: 'claude-code', note: 'User marker "> " col 0. 94k tokens, read in chunks. Densest story-card discussion in the archive (427 refs); mine card-workflow philosophy deeply.' },
]

const SHARD_NOTE = (s, range) => `This is deduplicated shard ${s} of day-020 (multi-session Claude Code file, 2025-07-05→07-09; the original file contained two giant re-pasted blocks which have been REMOVED — you see unique content only, original range ${range}). EVERY LINE IS PREFIXED with its ORIGINAL day-020 line number and a tab: cite locs as "day-020:L<that prefix number>" — no arithmetic needed. User marker "> " (after the number prefix). Set file: day-020-${s}.`

const S20 = [
  { s: 's1', range: 'L1-L7206' },
  { s: 's2', range: 'L7207-L14500' },
  { s: 's3', range: 'L14501-L21810' },
  { s: 's4', range: 'L21811-L31129' },
  { s: 's5', range: 'L54839-L56185 (unique tail that only exists in the second paste)' },
]

const results = await parallel([
  ...FILES.map(({ f, era, note }) => () =>
    agent(minerPrompt(`${DIARY}/${f}.md`, era, note, f), { model: 'opus', effort: 'xhigh', label: `mine:${f}`, phase: 'Mine' })),
  ...S20.map(({ s, range }) => () =>
    agent(minerPrompt(`${SHARDS}/day-020-${s}.md`, 'claude-code', SHARD_NOTE(s, range), `day-020-${s}`), { model: 'opus', effort: 'xhigh', label: `mine:day-020-${s}`, phase: 'Mine' })),
])

const done = results.filter(Boolean)
log(`${done.length}/24 miners returned`)
return { completed: done.length, summaries: done }
