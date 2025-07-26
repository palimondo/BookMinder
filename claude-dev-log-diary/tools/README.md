# Claude Session Replay Tools (Work in Progress)

**Status**: These tools are work in progress and require proper development process to complete due to their complexity.

## What We Currently Have

### 1. `replay_claude_session.py` - Universal Replay Tool (Incomplete)
- **Purpose**: Parse and replay any Claude session from JSONL logs
- **Current state**:
  - Has basic structure with ToolCall, ToolResult, and Commit dataclasses
  - Has `--start` and `--end` parameters for commit ranges
  - Has dry-run mode support
- **Issues**:
  - JSONL parsing is broken (doesn't handle multi-line JSON format)
  - Execution part is just a placeholder
  - No actual tool implementation

### 2. `parse_claude_jsonl.py` - JSONL Parser
- **Purpose**: Extract tool calls from Claude's multi-line JSONL format
- **Current state**:
  - Correctly handles multi-line JSON objects
  - Extracts tool calls and groups them by commits
  - Good for viewing/analyzing sessions
- **Issues**:
  - Read-only, no execution capability
  - Hardcoded to skip MCP tools

### 3. `extract_tool_calls.py` - Alternative Parser
- **Purpose**: Extract tool calls with different output format
- **Current state**:
  - Attempts line-by-line JSON parsing
  - Groups edits by commits
- **Issues**:
  - Doesn't work with multi-line JSONL format
  - Assumes incorrect JSON structure

### 4. `extract_commits.sh` - Bash Extractor
- **Purpose**: Quick extraction using grep/sed
- **Current state**:
  - Fast extraction of commits and file modifications
  - Good for quick overview
- **Issues**:
  - No execution capability
  - Limited to pattern matching

## Universal Replay Tool Design

### Goals
Create a tool that can replay any Claude session with fine-grained control over what gets executed.

### Proposed Usage
```bash
replay_claude_session.py <jsonl_file> [options]

Options:
  --start-tool N      Start from tool call N (1-based)
  --end-tool M        End at tool call M (inclusive)
  --start-commit N    Start from commit N
  --end-commit M      End at commit M  
  --only-commits      Only replay git commits (skip intermediate edits)
  --skip-tests        Don't run tests between commits
  --dry-run          Show what would be done (default)
  --execute          Actually run the commands
  --interactive      Confirm each action
  --filter TOOL      Only replay specific tools (Edit, Write, Bash, etc)
  --after TIMESTAMP   Start after specific timestamp
  --before TIMESTAMP  End before specific timestamp
```

### Key Features Needed

1. **Robust JSONL Parsing**
   - Handle multi-line JSON objects
   - Extract all tool calls with metadata
   - Build index of tool calls by number, type, and timestamp
   - Group related tool calls (e.g., edits before commits)

2. **Tool Execution Engine**
   - Implement actual execution for each tool type:
     - `Edit`: Apply text replacements to files
     - `Write`: Create/overwrite files
     - `MultiEdit`: Apply multiple edits in sequence
     - `Bash`: Execute shell commands
     - `Task`: Special handling to pass ranges to sub-agents
   - Respect CLAUDE.md rules (e.g., explicit file staging)

3. **Replay Control**
   - Support multiple range selection methods
   - Allow filtering by tool type
   - Interactive mode for confirmation
   - Rollback capability on failure

4. **Safety Features**
   - Dry-run by default
   - Backup modified files
   - Validate tool calls before execution
   - Check git status before operations

### Implementation Challenges

1. **JSONL Format**: The logs use multi-line JSON, not standard JSONL
2. **Tool Diversity**: Each tool has different parameters and behaviors
3. **State Management**: Tracking what's been executed and handling failures
4. **Task Tool**: Requires special handling to launch agents with ranges
5. **Performance**: Large session logs (500KB+) need efficient parsing

### Development Process Required

Due to the complexity, this tool requires:
1. **Proper specifications** following ATDD practices
2. **Test-driven development** with comprehensive test coverage
3. **Incremental implementation** starting with basic features
4. **Integration testing** with real session logs

## Next Steps

1. Create proper story YAML file for the replay tool
2. Design test scenarios covering various use cases
3. Implement following TDD practices per CLAUDE.md
4. Consider using existing parsing from `parse_claude_jsonl.py` as base

## Notes

- The immediate need (recreating issue #13 branch) is handled by the hardcoded `replay_issue_13.py`
- These tools were created during exploratory work to understand the log format
- Future implementation should follow BookMinder's development standards