# Claude Session Tools

Tools for fetching, exploring, and replaying Claude Code sessions from GitHub Actions.

## Core Tools

### fetch_logs.py / fetch_logs.sh
Download Claude Code sessions from GitHub Actions workflow logs.

```bash
# Fetch recent runs (default: 20)
python fetch_logs.py
./fetch_logs.sh

# Fetch more runs
python fetch_logs.py --limit 50

# Fetch specific run
python fetch_logs.py --run-id 16434195166

# Include raw logs for debugging
python fetch_logs.py --save-raw-logs
```

Features:
- Automatic deduplication (skips already downloaded runs)
- Proper timestamps (file creation = session start, modification = session end)
- Structured filenames: `YYYYMMDD-HHMM-{issue|pr}-N_run-{id}_session-{id}.jsonl`

**Planned**: Fetch by issue/PR number by finding Claude's sticky comment with the run ID

### explore_session.py
Interactive CLI for analyzing and exporting Claude sessions.

#### Session Discovery
Find sessions by any substring:
```bash
python explore_session.py issue-13  # Finds matching JSONL in github/
python explore_session.py run-1648  # Match by run ID
python explore_session.py 20250723 # Match by date
```

#### Interactive Exploration
```bash
python explore_session.py issue-13 --summary      # Tool usage summary
python explore_session.py issue-13 --timeline Edit # Show all edits
python explore_session.py issue-13 --git          # Show git operations
python explore_session.py issue-13 --files        # Show file changes
```

#### Tool(glob) Filtering
Uses Claude Code's permission syntax:
```bash
# Export specific tools with patterns
python explore_session.py issue-13 --export 1 46 - \
  --include "Edit(*/specs/**),Bash(git add *),Bash(git commit *)"

# Short form for all operations of a type
python explore_session.py issue-13 --export 1 46 - --include "Edit,Write"
```

### parse_claude_jsonl.py
Multi-line JSONL parser used by explore_session.py. Handles Claude's complex JSON format where objects span multiple lines.

### reconstruct.jq
JQ script to recreate console format from local Claude session JSONL files. Useful when terminal crashes without saving transcript:

```bash
jq -r -f reconstruct.jq ~/.claude/projects/-Users-palimondo-Developer-BookMinder/SESSION_ID.jsonl
```

## Replay Workflow

The key insight: Claude's Task tool can run explore_session.py directly and execute the extracted tool calls.

1. **Identify commit boundaries**:
   ```bash
   python explore_session.py issue-13 --git | grep commit
   ```

2. **Export filtered chunk**:
   ```bash
   python explore_session.py issue-13 --export 1 46 - \
     --include "Edit(*/specs/**),Edit(*/bookminder/**),Bash(git add *),Bash(git commit *)"
   ```

3. **Task delegation example**:
   ```
   Execute this command to get tool calls, then replay them exactly:
   
   python claude-dev-log-diary/tools/explore_session.py issue-13 --export 38 40 - --include "Edit" 2>/dev/null
   
   Important:
   - Run the command above to get 2 Edit operations
   - Parse the JSON output 
   - Execute each Edit exactly as specified in the JSON
   ```

This preserves exact fidelity - Claude uses its own Edit/Write/Bash tools rather than any custom replay logic.

## Design Philosophy

- Composable Unix-style tools
- Direct integration with Claude's Task tool
- Uses familiar glob patterns and Claude Code's permission syntax
- No complex replay logic - let Claude execute its own tools
- Tools work together: fetch → explore → replay