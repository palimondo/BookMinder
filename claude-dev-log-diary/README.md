# Claude Development Log Archive

Archive of Claude Code sessions for BookMinder development, preserving both GitHub Actions logs and local session transcripts.

## Contents

- `day-*.md` - Console transcripts from Claude Code sessions (manual copy from terminal)
- `github/*.jsonl` - JSONL extracted from GitHub Actions Claude Code runs
- `reconstruct.jq` - JQ script to recreate console format from JSONL files
- `fetch_logs.py` - Python script to extract JSONL from GitHub Actions logs
- `fetch_logs.sh` - Bash script to extract JSONL from GitHub Actions logs

## Fetching GitHub Logs

Both Python and Bash scripts provide identical functionality:

```bash
# Fetch recent runs (default: 20)
python fetch_logs.py
# or
./fetch_logs.sh

# Fetch more runs
python fetch_logs.py --limit 50
./fetch_logs.sh --limit 50

# Fetch specific run
python fetch_logs.py --run-id 16434195166
./fetch_logs.sh --run-id 16434195166

# Include raw logs for debugging failed extractions
python fetch_logs.py --save-raw-logs
./fetch_logs.sh --save-raw-logs
```

### Features

- **Automatic deduplication**: Scripts skip already downloaded runs
- **Proper timestamps**: File creation time = session start, modification time = session end
- **Structured filenames**: `YYYYMMDD-HHMM-{issue|pr}-N_run-{id}_session-{id}.jsonl`
- **Handles both log formats**: Works with old "Run Claude Code" and new "UNKNOWN STEP" formats

## Reconstructing Console Output

When terminal crashes without saving transcript:
```bash
jq -r -f reconstruct.jq ~/.claude/projects/-Users-palimondo-Developer-BookMinder/SESSION_ID.jsonl
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