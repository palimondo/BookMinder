# Claude Development Log Archive

Archive of Claude Code sessions for BookMinder development, preserving both GitHub Actions logs and local session transcripts.

## Contents

- `day-*.md` - Console transcripts from Claude Code sessions (manual copy from terminal)
- `github/*.jsonl` - JSONL extracted from GitHub Actions Claude Code runs
- `tools/` - Suite of tools for fetching, exploring, and replaying Claude sessions

## Tools

See [tools/README.md](tools/README.md) for detailed documentation of:
- **fetch_logs.py/sh** - Download sessions from GitHub Actions
- **explore_session.py** - Analyze and export sessions with filtering
- **parse_claude_jsonl.py** - Parse multi-line JSONL format

Quick start:
```bash
# Fetch recent sessions
python tools/fetch_logs.py

# Explore a session
python tools/explore_session.py issue-13 --summary

# Export specific tool calls for replay
python tools/explore_session.py issue-13 --export 1 46 - \
  --include "Edit(*/specs/**),Bash(git add *),Bash(git commit *)"
```
- **Handles both log formats**: Works with old "Run Claude Code" and new "UNKNOWN STEP" formats

## Reconstructing Console Output

When terminal crashes without saving transcript:
```bash
jq -r -f tools/reconstruct.jq ~/.claude/projects/-Users-palimondo-Developer-BookMinder/SESSION_ID.jsonl
```

## Future Vision: Intelligence System

These archives will enable:

1. **Behavioral Analysis**
   - Interrupt patterns → ATDD compliance failures
   - Bug introduction patterns
   - Impact of reasoning on code quality

2. **Project Knowledge Graph**
   - Hierarchical memory from session history
   - Timeline of decisions and evolution
   - Context recovery for "why did we do X?"

3. **AI Augmentation Research**
   - Benchmarks for coding assistants
   - Tools to prevent common failures
   - Long-term memory systems

## Notes

- Local Claude sessions auto-purge after 30 days (backup regularly!)
- GitHub Actions logs expire after CI retention period
- JSONL files contain complete tool I/O (unlike truncated console logs)
## Repaired files

- **day-020.md** — repaired 2026-08-15. The file was a hand-assembled sequence of five console pastes of one session, two of which were redundant; 23,710 duplicate lines were deleted (delete-only, no kept line edited or re-wrapped), leaving an editorial appendix and trailer after the transcript body. Pre-repair blob `27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2` (56,185 lines) — recover with `git cat-file blob 27a5ad7d51f6de8db0ef3361df7bc9c9adc034a2 > claude-dev-log-diary/day-020.md`. Line remap: `.coordination/tools/day-020-remap.md`; gate results: `.coordination/day-020-repair-report.md`. Pre-repair locs ≤31128 are unchanged; locs ≥45520 shift by −23710.
- **day-007.md** — repaired 2026-08-15. Four console pastes of one day, the fourth of which opened by re-rendering the whole of the second; 1,450 duplicate lines (pre-repair 6214-7663) were deleted. One line was restored, not deleted: the earlier paste had dropped the console's `> ` author-turn marker at line 3116, which the deleted rendering preserved, so it was verified byte-for-byte against that witness and put back — the only line in the file whose bytes differ from the pre-repair capture. Pre-repair blob `2b1776656183cce5c73dd82a7c89eed6c69eeec0` (8,127 lines) — recover with `git cat-file blob 2b1776656183cce5c73dd82a7c89eed6c69eeec0 > claude-dev-log-diary/day-007.md`. Line remap: `.coordination/tools/day-007-remap.md`. Pre-repair locs ≤6213 are unchanged; locs 7660-7661 resolve to 3116-3117; locs ≥7664 shift by −1450.
