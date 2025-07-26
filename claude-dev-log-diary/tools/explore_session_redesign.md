# explore_session.py Redesign

## Overview

This document captures the planned improvements to explore_session.py based on user feedback and usability analysis.

## Current Issues

1. **Fragmented views**: Timeline shows tools, conversation shows dialogue - no unified view
2. **Inconsistent range syntax**: Export uses `START END`, conversation uses `START-END`
3. **Confusing timeline usage**: Requires empty string `""` to show all tools
4. **Limited filtering**: Range/limit only works on export and conversation
5. **Missing tool parameters**: Grep, TodoWrite, and others show no parameters in timeline

## Design Principles

- **Unified interface**: Consistent syntax across all commands
- **Progressive disclosure**: Compact by default, detailed on demand
- **Maintain include/exclude duality**: No renaming to "filter"
- **Incremental implementation**: Small, testable changes

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

## Implementation Phases

### Phase 1: Enhanced Compact Timeline
1. Add Grep parameter display (pattern and path)
2. Add TodoWrite parameter display (todo count summary)
3. Test and commit each addition

### Phase 2: Unified Timeline Structure
1. Create data structure merging tools and conversation chronologically
2. Update show_timeline to handle 'all', 'tools', 'conversation' modes
3. Maintain backward compatibility

### Phase 3: Consistent Range Handling
1. Create parse_range utility: handles "START-END" and "-N" formats
2. Update all commands to use consistent syntax
3. Change export from "START END OUTPUT" to "START-END OUTPUT"

### Phase 4: Display Modes
1. Implement --truncated mode with console-style formatting
2. Implement --full mode for complete output
3. Keep compact as default

### Phase 5: Polish
1. Rename --export to --export-json with better help text
2. Implement --git and --files as shortcuts
3. Add remaining tool parameters

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