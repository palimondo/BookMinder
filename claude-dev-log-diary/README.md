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