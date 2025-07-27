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
# Basic exploration
python explore_session.py issue-13 -s             # Show summary (default)
python explore_session.py issue-13 -t             # Show full timeline
python explore_session.py issue-13 -t 10-20       # Show timeline items 10-20
python explore_session.py issue-13 -t +20         # Show first 20 items
python explore_session.py issue-13 -t -30         # Show last 30 items

# Virtual entities (NEW!)
python explore_session.py issue-13 -t -m          # Show all messages
python explore_session.py issue-13 -t -u          # Show user messages only
python explore_session.py issue-13 -t -a          # Show assistant messages
python explore_session.py issue-13 -t -T          # Show all tools
python explore_session.py issue-13 -t -T --no-tool-results  # Tools without output

# Combining filters
python explore_session.py issue-13 -t -m -x User  # Assistant messages only
python explore_session.py issue-13 -t -i Message,Read  # Messages and Read operations

# Traditional shortcuts
python explore_session.py issue-13 --git          # Show git operations
python explore_session.py issue-13 --files        # Show file changes summary
```

#### Advanced Filtering
Virtual entities and tool patterns:
```bash
# Virtual entities: Message, Tool, User, Assistant
python explore_session.py issue-13 -t -i Message  # All messages
python explore_session.py issue-13 -t -i Tool     # All tools
python explore_session.py issue-13 -t -i User,Assistant  # All messages

# Tool patterns (Claude Code syntax)
python explore_session.py issue-13 -t -i "Bash(git *)"     # Git commands
python explore_session.py issue-13 -t -i "Edit(*.py)"      # Python edits
python explore_session.py issue-13 -t -i "Read(*test*)"    # Reading test files

# Export with filters
python explore_session.py issue-13 --export-json 1-46 output.json \
  -i "Edit(*/specs/**),Bash(git add *),Bash(git commit *)"
```

#### Display Modes
```bash
# Compact mode (default) - one line per item
python explore_session.py issue-13 -t

# Truncated mode - 3-line preview (like Claude console)
python explore_session.py issue-13 -t --truncated

# Full mode - complete output
python explore_session.py issue-13 -t --full

# JSON output for piping
python explore_session.py issue-13 -t --json | jq '.[] | select(.type=="tool")'
python explore_session.py issue-13 -t --jsonl | grep '"type":"message"'
```

### parse_claude_jsonl.py
Multi-line JSONL parser used by explore_session.py. Handles Claude's complex JSON format where objects span multiple lines.

### reconstruct.jq
JQ script to recreate console format from local Claude session JSONL files. Useful when terminal crashes without saving transcript:

```bash
jq -r -f reconstruct.jq ~/.claude/projects/-Users-palimondo-Developer-BookMinder/SESSION_ID.jsonl
```

## Session Analysis Use Cases

This tool helps analyze Claude Code's behavior and debug issues:

```bash
# "What did the user actually ask for?"
explore_session.py issue-13 -t -u                    # User messages only

# "What was Claude's interpretation?" 
explore_session.py issue-13 -t -a                    # Assistant responses

# "What tools did Claude use (without the noise)?"
explore_session.py issue-13 -t -T --no-tool-results  # Actions without output

# "Did Claude understand the error messages?"
explore_session.py issue-13 -t -a -i Tool            # Responses + tool results

# "What files did Claude read repeatedly?"
explore_session.py issue-13 -t -i Read --json | \
  jq -r '.[] | select(.type=="tool") | .tool.parameters.file_path' | \
  sort | uniq -c | sort -n

# "Show the conversation around a specific error"
explore_session.py issue-13 -t 140-160 -m            # Messages in range

# "What happened after the user interrupted?"
explore_session.py issue-13 -t | grep -B5 -A5 "interrupted"
```

## Replay Workflow

The key insight: Claude's Task tool can run explore_session.py directly and execute the extracted tool calls.

1. **Identify commit boundaries**:
   ```bash
   python explore_session.py issue-13 --git | grep commit
   ```

2. **Export filtered chunk**:
   ```bash
   python explore_session.py issue-13 --export-json 1-46 - \
     -i "Edit(*/specs/**),Edit(*/bookminder/**),Bash(git add *),Bash(git commit *)"
   ```

3. **Task delegation example**:
   ```
   Execute this command to get tool calls, then replay them exactly:
   
   python claude-dev-log-diary/tools/explore_session.py issue-13 --export-json 38-40 - -i Edit 2>/dev/null
   
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