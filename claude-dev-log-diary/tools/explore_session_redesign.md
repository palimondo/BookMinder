# explore_session.py Redesign

## Overview

This document captures the planned improvements to explore_session.py based on user feedback and usability analysis.

## Current Issues

### Core Architecture
1. **Fragmented views**: Timeline shows tools, conversation shows dialogue - no unified view
2. **Mixed concerns**: Filters change display format instead of just selecting events
3. **Special cases everywhere**: --conversation, --tools have special display logic

### Syntax & Usability
1. **Inconsistent range syntax**: Export uses `START END`, conversation uses `START-END`
2. **Confusing timeline usage**: Requires empty string `""` to show all tools
3. **Limited filtering**: Range/limit only works on export and conversation

### Display Issues
1. **Missing tool parameters**: Grep, TodoWrite, and others show no parameters in timeline
2. **Multiline tool output formatting**:
   - Need proper indentation for tool results
   - Truncation should show first N lines then "… +X lines"
   - Empty results should show "(No content)"
3. **Export format confusion**:
   - Current --export-json writes to file
   - Should consider --json as display format to stdout
   - More Unix-like to use shell redirection

## Design Principles

- **Unified interface**: Consistent syntax across all commands
- **Separation of concerns**: Filters control WHAT to show, display modes control HOW
- **Progressive disclosure**: Compact by default, detailed on demand
- **Maintain include/exclude duality**: No renaming to "filter"
- **Incremental implementation**: Small, testable changes
- **No special cases**: Display modes work the same regardless of filtering

## Display Modes

### 1. Compact Mode (Default)
Single line per item, showing essential information with first/last line for context:
```
[1] > Run the tests please
[2] ⏺ I'll run the tests for you now
[3] ⏺ Bash(pytest)
[4] ⏺ Read(test_results.txt)
[5] ⏺ All tests passed successfully!
```

### 2. Truncated Mode
Console-style with 3-line preview (mimics Claude Code's default console output):
```
⏺ I'll run the tests for you now

⏺ Bash(pytest)
  ⎿  Waiting…
  
  ⎿  ============================= test session starts ======
     platform darwin -- Python 3.13.5, pytest-8.3.5, pluggy-1.6.0
     rootdir: /Users/palimondo/Developer/BookMinder
     … +47 lines

⏺ All tests passed successfully!
```

Note: The "… +N lines" is sufficient for static logs. Claude Code adds "(ctrl+r to expand)" 
for interactive use, but we omit this as it's noise in static output.

### 3. Full Mode
Complete output with rich formatting (markdown, syntax highlighting):
- Shows complete tool inputs and outputs
- No truncation of messages
- Similar to Claude Code's expanded view (ctrl+r)

### 4. JSON Mode (Proposed Redesign)
Instead of `--export-json START-END FILE`, consider:
- `--json`: Output filtered timeline as JSONL to stdout
- Let shell handle redirection: `./explore_session.py SESSION --json > output.jsonl`
- More Unix-like and composable
- Removes need for special export command

## Compact Format Tool Parameters

### Currently Implemented
- `Edit/Write/MultiEdit`: → filename
- `Bash`: $ command...
- `Read`: ← filename

### To Be Added
- `Grep`: "pattern" in path
- `TodoWrite`: Updated N todos (X status, Y status)
- `LS`: path
- `Glob`: pattern
- `Task`: "description"
- `WebFetch`: url
- `WebSearch`: "query"

## Command Structure

### Timeline (Unified View)
```bash
# Show everything (tools + conversation)
./explore_session.py SESSION --timeline

# Show only tools or conversation
./explore_session.py SESSION --timeline tools
./explore_session.py SESSION --timeline conversation

# Range support (consistent START-END format)
./explore_session.py SESSION --timeline 50-100    # Items 50-100
./explore_session.py SESSION --timeline -50       # Last 50 items

# Display modes
./explore_session.py SESSION --timeline --truncated
./explore_session.py SESSION --timeline --full
```

### Filtering
```bash
# Include/exclude patterns (works with all views)
./explore_session.py SESSION --timeline --include "Edit,Write"
./explore_session.py SESSION --timeline --exclude "Read,Grep"
```

### Specialized Shortcuts
```bash
# Git operations (equivalent to: --timeline tools --include "Bash(git *)")
./explore_session.py SESSION --git

# File operations (equivalent to: --timeline tools --include "Edit,Write,MultiEdit")
./explore_session.py SESSION --files
```

### Export
```bash
# Renamed for clarity, with consistent range syntax
./explore_session.py SESSION --export-json 1-50 output.json
```

## Completed Work

### Architecture
1. ✅ Centralized filter_timeline method
2. ✅ Tool results included when filtering for tools  
3. ✅ Deprecated show_conversation (uses timeline internally)
4. ✅ Free parameter syntax for ranges/indices

### Display Fixes
1. ✅ Basic truncated mode implementation
2. ✅ Line numbers in truncated mode when filtering
3. ✅ [...] separator for assistant messages in compact mode
4. ✅ Consistent ⏺ symbol for all assistant output
5. ✅ Empty tool results show "(No content)"
6. ✅ Proper truncation format "… +N lines"

### Features
1. ✅ --git shortcut implementation
2. ✅ Include/exclude filtering with glob patterns
3. ✅ --no-tool-results flag to control result inclusion
4. ✅ --show-numbers flag to force line numbers in truncated mode

## Implementation Phases

### Phase 0: Architecture Cleanup (✅ COMPLETED)
1. ✅ Separated filtering from display
2. ✅ Consolidated filter logic with centralized filter_timeline
3. ✅ Removed special display logic from show_conversation

### Phase 1: Display Mode Fixes (✅ COMPLETED)
1. ✅ Fixed [...] separator for assistant messages
2. ✅ Fixed ⏺ symbol consistency 
3. ✅ Show "(No content)" for empty tool results
4. ✅ Proper truncation format (removed interactive-only text)

### Phase 2: Enhanced Tool Parameters (✅ COMPLETED)
1. ✅ Add Grep parameter display: "pattern" in path
2. ✅ Add TodoWrite parameter display with status counts
3. ✅ Add parameters for all tools (LS, Glob, Task, WebFetch, WebSearch)
4. ✅ Add special symbols for Bash ($), Edit/Write (→), Read (←)
5. ✅ Refactor --files to use centralized filtering

### Phase 3: Unified Timeline Structure (✅ MOSTLY COMPLETE)
1. ✅ Create data structure merging tools and conversation chronologically
2. ✅ Update show_timeline to handle 'all', 'tools', 'conversation' modes
3. ✅ Maintain backward compatibility

### Phase 4: Consistent Range Handling (✅ COMPLETED)
1. ✅ parse_range utility already exists: handles "5", "1-50", "+10", "-20"
2. ✅ All commands use consistent free parameter syntax
3. ✅ Changed export from "START END OUTPUT" to "RANGE OUTPUT"

### Phase 5: Polish & Redesign (✅ COMPLETED)
1. ✅ Implement --full mode for complete output
2. ✅ Redesigned export:
   - Added `--json` as display format to stdout (JSON array)
   - Added `--jsonl` as display format to stdout (newline-delimited JSON)
   - Kept `--export-json` for writing to files
   - Both JSON and JSONL formats supported
3. ✅ Implement --git as shortcut (already done)
4. ✅ Implement --files as shortcut (uses centralized filtering)
5. ✅ Add support for todo result formatting with checkboxes

## Examples After Implementation

```bash
# Quick scan for commits
./explore_session.py 943dff12 --timeline | grep "git commit"

# See context around specific items
./explore_session.py 943dff12 --timeline 55-65 --truncated

# Export filtered tools
./explore_session.py issue-13 --export-json 1-100 tools.json --include "Edit,Write"

# Show last 50 conversation items
./explore_session.py issue-13 --timeline conversation -50

# Export as JSON array to stdout
./explore_session.py session.jsonl --timeline --json | jq '.[].tool.name' | sort | uniq -c

# Stream as JSONL for processing
./explore_session.py session.jsonl --timeline --jsonl --include "Edit" | jq -r '.tool.parameters.file_path'
```

## Notes

- Input files are JSONL, but export creates JSON (array of tool calls)
- Console formatting follows patterns from reconstruct.jq
- Backward compatibility not required - clean breaks acceptable
- Each phase should be tested and committed independently

## Edge Cases to Handle

Based on reconstruct.jq analysis, these cases need special handling:

1. **Slash Commands**: User messages with `<command-name>` and `<command-message>` tags
   - Format as `> /command-name` in timeline
   - Example: `/expert-council`, `/compact`

2. **Bash Command Invocation**: Direct bash commands using `!command` syntax
   - Not currently handled in reconstruct.jq
   - Should display as `> !command` in timeline

3. **Context Loading**: Using `@filename` to load file context
   - Not currently handled in reconstruct.jq  
   - Should display as `> @filename` in timeline

4. **Empty Protocol Messages**: Empty user messages that are protocol artifacts
   - Often appear at session start or between assistant responses
   - Currently shown as `[empty]` but could be hidden in default view

5. **Interrupted Requests**: Messages containing "[Request interrupted by user"
   - reconstruct.jq skips these
   - Should be handled gracefully in timeline