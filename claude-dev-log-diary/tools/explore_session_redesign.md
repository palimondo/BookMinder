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
2. **Compact mode bugs**:
   - [...] separator only works for user messages, not assistant
   - Inconsistent bullet symbols (different sizes on different lines)
3. **Truncated mode bugs**:
   - Empty tool results show blank line instead of "(No content)"
   - Missing proper truncation format: "... +X lines (ctrl+r to expand)"
   - Tool results need proper spacing to match Claude Code output

## Design Principles

- **Unified interface**: Consistent syntax across all commands
- **Separation of concerns**: Filters control WHAT to show, display modes control HOW
- **Progressive disclosure**: Compact by default, detailed on demand
- **Maintain include/exclude duality**: No renaming to "filter"
- **Incremental implementation**: Small, testable changes
- **No special cases**: Display modes work the same regardless of filtering

## Display Modes

### 1. Compact Mode (Default)
Single line per item, showing essential information:
```
[1]  USER: Run the tests please
[2]  CLAUDE: I'll run the tests for you now
[3]  Bash: pytest
[4]  Read: test_results.txt
[5]  CLAUDE: All tests passed successfully!
```

### 2. Truncated Mode
Console-style with 3-line preview (based on reconstruct.jq):
```
[3] ⏺ Bash(pytest)
    ⎿  ============================= test session starts ======
       platform darwin -- Python 3.13.5, pytest-8.3.5, pluggy-1.6.0
       rootdir: /Users/palimondo/Developer/BookMinder
       … +47 lines
```

### 3. Full Mode
Complete output without truncation.

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

1. ✅ Basic truncated mode implementation
2. ✅ Centralized filter_timeline method
3. ✅ Line numbers in truncated mode when filtering
4. ✅ Tool results included when filtering for tools
5. ✅ --git shortcut implementation
6. ✅ Free parameter syntax for ranges/indices

## Implementation Phases

### Phase 0: Architecture Cleanup (CURRENT PRIORITY)
1. **Separate filtering from display**:
   - Remove special display logic from filter methods
   - Make filters only control event selection
   - Make display modes work consistently regardless of filters
2. **Consolidate filter logic**:
   - Single filter_timeline method that all commands use
   - Remove duplicate filtering code
   - Clean up message/tool filtering inconsistencies
3. **Remove special cases**:
   - --conversation should just filter for messages, not change display
   - --tools should just filter for tools
   - Display format should be orthogonal to what's being filtered

### Phase 1: Fix Display Mode Bugs
1. **Compact mode fixes**:
   - Add [...] separator for assistant messages (currently only works for user)
   - Fix inconsistent bullet symbols (use • consistently)
   - Maintain first/last line display for context
2. **Truncated mode fixes**:
   - Show "(No content)" for empty tool results
   - Implement proper truncation: "... +X lines (ctrl+r to expand)"
   - Fix spacing to match Claude Code output
   - Keep line numbers when filtering (already implemented)

### Phase 2: Enhanced Tool Parameters
1. Add Grep parameter display (pattern and path)
2. Add TodoWrite parameter display with todo formatting
3. Add parameters for remaining tools (LS, Glob, Task, etc.)
4. Test and commit each addition

### Phase 3: Unified Timeline Structure
1. Create data structure merging tools and conversation chronologically
2. Update show_timeline to handle 'all', 'tools', 'conversation' modes
3. Maintain backward compatibility

### Phase 4: Consistent Range Handling
1. Create parse_range utility: handles "START-END" and "-N" formats
2. Update all commands to use consistent syntax
3. Change export from "START END OUTPUT" to "START-END OUTPUT"

### Phase 5: Polish
1. Implement --full mode for complete output
2. Rename --export to --export-json with better help text
3. Implement --git and --files as shortcuts
4. Add support for todo result formatting with checkboxes

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