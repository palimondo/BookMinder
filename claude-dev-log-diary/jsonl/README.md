# jsonl/ — native session transcripts

Full session transcripts in the agentic system's NATIVE format, preserved for later analysis — the same optionality the day-files earned for the 2025 era. Day-files are the human-readable console shadow; these are the machine-readable source: every prompt, tool call, tool result, and subagent brief, verbatim.

## Layout

- `cloud-2026/` — Claude Code cloud-infra sessions (current era). Native layout preserved exactly as it lives under `/root/.claude/projects/<project>/` in the session container:
  - `<session-uuid>.jsonl` — the main-thread transcript (append-only event log).
  - `<session-uuid>/subagents/agent-*.jsonl` — one full transcript per Agent-tool worker, including its brief (first user message) and every action. `agent-*.meta.json` carries routing metadata (agent type, model).
  - `<session-uuid>/subagents/workflows/` — per-agent transcripts of Workflow-tool fan-out runs.
  - `<session-uuid>/workflows/` — workflow journals and the exact orchestration scripts that ran.
  - `<session-uuid>/tool-results/` — oversized tool-result blobs referenced from the transcripts.
- `local-2025/` — (reserved) the 2025-era JSONL backups from the author's local machine, when uploaded. Any `*.jsonl` landing here triggers the standing intake: dupescan against existing day-files, then a mining pass over new material (see `.coordination/threads.md` thread 0e).

## Session index

| session | era | span | what happened |
|---|---|---|---|
| `a42b9c92-c0e6-588e-bc6f-3d5e4f37b895` | cloud-2026 | 2026-08-10 → | Reevaluation session, first CC cloud test drive: diary mining swarm (24 YAML harvest), contradiction ledger, compile of the three skills (tdd-bdd / pair-programming / bookminder), smoke-test verification. |

## Sync discipline (cloud sessions)

The container is ephemeral; the repo is the only durable store. The transcript grows append-only, so re-copying is cheap for git:

1. Snapshot = `cp -r` the session's `.jsonl` + directory from `/root/.claude/projects/<project>/` into `cloud-2026/`, commit, push.
2. The session's coordinator re-snapshots at every persistence sweep / watchdog firing and before any anticipated session end. A snapshot is always safe: files are append-only or immutable, so the latest copy strictly extends the previous one.
3. The final events of a session (including its own last sync commit) are only capturable by the NEXT session or a post-hoc fetch — a transcript cannot contain its own completion. Accepted limitation; the tail loss is minutes, not days.

## Analysis

The `xs` tool at the project root was built for 2025-format transcripts; format drift is expected (it broke on every CC format churn — see day-file lore). Treat these files as the stable source and adapt tooling per era, not the other way around.
