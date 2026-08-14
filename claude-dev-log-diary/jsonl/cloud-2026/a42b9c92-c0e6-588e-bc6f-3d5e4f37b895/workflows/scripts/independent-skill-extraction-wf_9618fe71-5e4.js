export const meta = {
  name: 'independent-skill-extraction',
  description: 'Independent extraction of project-coordinator skill from live session transcript',
  phases: [{ title: 'Extract' }],
}
phase('Extract')
const r = await agent(`You are an INDEPENDENT extractor. Source: this very session's transcript at /root/.claude/projects/-home-user-BookMinder/a42b9c92-c0e6-588e-bc6f-3d5e4f37b895.jsonl (4.5MB JSONL — a coordinator agent + a project author running a multi-day reevaluation with worker swarms).

INDEPENDENCE CONSTRAINT: do NOT read .claude/skills/project-coordinator/SKILL.md, .coordination/threads.md, or .coordination/eval-design.md — a coordinator-authored skill already exists and your value is extracting WITHOUT its lens, so the two can be diffed. Also skip .coordination/mining/ contents.

METHOD: First write a small Python filter to scratchpad (/tmp/claude-0/-home-user-BookMinder/a42b9c92-c0e6-588e-bc6f-3d5e4f37b895/scratchpad/) that extracts from the JSONL only: user-role message text and assistant-role text blocks (SKIP tool_result contents, tool_use inputs over ~500 chars, and system entries — they are enormous). Read the filtered output in chunks, in order.

MISSION: Extract the WORKING PROCESS of this coordinator+author pair as an operable skill: every author directive, correction, preference, and adopted rule about HOW TO WORK — delegation practices (worker tiers, WHEN TO USE FABLE OR FORKS vs Opus workers, effort levels), persistence/recording discipline, git/commit conventions, swarm operations (launching, authorization, slicing, killing, resuming), container-survival tactics, communication register (verbosity, praise, narration, attribution), claims/verification discipline, approval boundaries, error-handling after author pushback. Capture rules the coordinator ADOPTED after failures, and also directives the author gave that were possibly NOT fully absorbed — mark those specially. The author suspects the existing skill missed specifics (e.g. when to fork a Fable worker with full context vs spawning fresh Opus workers).

DELIVERABLE: write /tmp/claude-0/-home-user-BookMinder/a42b9c92-c0e6-588e-bc6f-3d5e4f37b895/scratchpad/skill-independent.md — a complete standalone SKILL.md draft (frontmatter: name project-coordinator) in imperative voice, rules grounded in what actually happened (cite the user's short verbatim phrases where they anchor a rule). Include a final section "POSSIBLY UNABSORBED" for directives you found that seem under-implemented. No hard-wrapped prose. Return max-10-line summary: rule count by area + the 3 most notable items you expect the coordinator's own version to have missed.`, { model: 'opus', effort: 'xhigh', label: 'skill-extract' })
return r