# explore_session.py Design Decisions

This document explains the rationale behind various formatting and design choices in explore_session.py. These decisions were made based on usability testing, user feedback, and practical experience with Claude Code session logs.

## Display Symbols

### ⏺ (Assistant Messages)
**Decision**: Use ⏺ (play button) for all assistant output
**Rationale**: 
- Visually distinct from user input (>)
- Suggests "playing" or "executing" actions
- Consistent with Claude Code's visual language
- Single symbol reduces visual clutter

### > (User Messages)  
**Decision**: Use > for user messages
**Rationale**:
- Traditional shell/REPL prompt convention
- Immediately recognizable as user input
- Lightweight and unobtrusive
- Works well in both compact and expanded views

### Tool-Specific Symbols
**Decision**: Use semantic symbols for common tools
- `$` for Bash commands
- `→` for Edit/Write/MultiEdit (writing to files)
- `←` for Read (reading from files)

**Rationale**:
- Provides instant visual recognition
- Arrows show data flow direction
- $ is universally recognized for shell commands
- Reduces need to read tool names

## Parameter Display

### Multiline Parameter Truncation
**Decision**: Use `[...]` pattern for multiline parameters
**Format**: `first_line [...] last_line` or `first_line [...]` if last line is empty

**Rationale**:
- Shows both start and end of content (most informative parts)
- [...] is a standard ellipsis pattern in programming
- Consistent with how Claude Code displays truncated content
- More informative than simple character truncation

### Empty Content Display
**Decision**: Show "(No content)" for empty tool results
**Rationale**:
- Explicitly indicates the tool ran but returned nothing
- Prevents confusion about whether result was loaded
- More informative than blank space
- Consistent with other CLI tools

## Display Modes

### Compact Mode (Default)
**Decision**: One line per event with essential information
**Rationale**:
- Maximum information density for scanning
- Fits more events on screen
- Good for getting overview of session
- Similar to git log --oneline

### Truncated Mode
**Decision**: Show first 3 lines of output with "… +N lines"
**Rationale**:
- Matches Claude Code's default console display
- 3 lines usually enough to identify content
- "… +N lines" clearly indicates more content
- Removed "(ctrl+r to expand)" as it's not interactive

### Full Mode
**Decision**: Complete output without truncation
**Rationale**:
- Sometimes you need to see everything
- Useful for debugging or detailed analysis
- Preserves all formatting and content

## Filtering System

### Include/Exclude Duality
**Decision**: Keep separate --include and --exclude flags
**Rationale**:
- More explicit than single --filter flag
- Clear mental model: start with all, include subset, then exclude
- Allows complex filtering: "all tools except Read"
- Consistent with other Unix tools (grep -v, find -not)

### Virtual Entities
**Decision**: Support Message, Tool, User, Assistant as filter entities
**Rationale**:
- Natural language filtering
- Groups related items (all messages, all tools)
- More intuitive than remembering all tool names
- Extensible for future entity types

### Wildcard Support
**Decision**: Support glob patterns in filters like `Bash(git *)`
**Rationale**:
- Powerful filtering without regex complexity
- Familiar glob syntax from shell
- Covers most common use cases
- Easier to type than regex

## Timeline Architecture

### Unified Timeline
**Decision**: Merge tools and messages into single chronological view
**Rationale**:
- Shows actual flow of conversation
- Context is preserved (what prompted each tool use)
- Single source of truth for event ordering
- Enables consistent filtering across all event types

### Tool Results Inclusion
**Decision**: Include tool results by default when filtering for tools
**Rationale**:
- Results are part of the tool execution
- Often need to see what a tool returned
- Can be disabled with --no-tool-results if not wanted
- More useful default behavior

## Export Formats

### JSON Array vs JSONL
**Decision**: Support both --json (array) and --jsonl (stream) to stdout
**Rationale**:
- JSON array: Easy to process with jq, standard format
- JSONL: Streamable, one object per line, grep-friendly
- stdout output: More Unix-like than requiring file parameter
- Preserves original JSONL structure for replay workflows

### Raw Object Preservation
**Decision**: Export includes complete original JSONL objects
**Rationale**:
- Enables session replay in Claude Code
- Preserves all metadata and fields
- No information loss during export
- Supports future tools that might need original format

## Command Line Interface

### Free Parameters for Ranges
**Decision**: Allow ranges as free parameters after flags
**Example**: `explore_session.py session.jsonl -t 10-20`

**Rationale**:
- More natural command line flow
- Consistent with other CLI tools (head -20, tail -50)
- Reduces typing (no --range flag needed)
- Flexible positioning after other options

### Shortcut Flags
**Decision**: Provide -M/-U/-a/-T shortcuts for common filters
**Rationale**:
- Faster for frequent operations
- Memorable mnemonics (M=messages, U=user, etc.)
- Power user convenience
- Still support long-form for discoverability

## Error Handling

### Graceful Degradation
**Decision**: Continue processing even with parse errors
**Rationale**:
- Partial results better than no results
- Session logs might be corrupted or incomplete
- User can still extract useful information
- Errors logged to stderr, not mixed with output

### Empty States
**Decision**: Show informative messages for empty results
**Rationale**:
- Confirms the tool ran successfully
- Distinguishes "no matches" from "error occurred"
- Helps users refine their filters
- Better than silent empty output

## Performance Considerations

### Lazy Loading
**Decision**: Parse entire session upfront, filter in memory
**Rationale**:
- Session files typically small enough (< 100MB)
- Enables multiple operations without re-parsing
- Simpler implementation than streaming
- Fast enough for interactive use

### Timeline Building
**Decision**: Build timeline once, cache for session
**Rationale**:
- Many operations need the full timeline
- Sorting is expensive, do it once
- Memory usage acceptable for typical sessions
- Enables fast filtering operations

## Future Considerations

These decisions create a foundation that supports:
- Additional display modes if needed
- New tool types without code changes
- Extended filtering syntax
- Performance optimizations if sessions grow larger
- Integration with other tools in the ecosystem

The key principle throughout is maintaining simplicity while providing power user features. Default behaviors should be sensible, with advanced features discoverable but not required.