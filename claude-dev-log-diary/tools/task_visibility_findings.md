# Task Sub-Agent Visibility Findings

## Critical Discovery (2025-08-02)
**MARKED for deja vu analysis**

### What We Learned
After rigorous testing comparing the golden output with xs-accessible transcripts, we discovered:

1. **Interactive Claude Code sessions show MORE than JSONL transcripts**
   - With Ctrl+R in Claude Code, you can see sub-agent's internal tool calls
   - Example: `find claude-dev-log-diary/ -name "*.jsonl"` visible at line 140 in golden output
   - This same command is NOT in the JSONL that xs can access

2. **What IS visible in JSONL transcripts:**
   - Task invocation with parameters
   - Sub-agent's response/return value
   - NOT the sub-agent's intermediate steps

3. **Architectural Implications:**
   - We cannot debug Task failures by examining sub-agent actions
   - Sub-agents must report their own errors/issues
   - The `isSidechain: true` flag indicates separate context, not visible actions

## Updated Strategy for Task Delegation

### Prompt Design Must Include:
1. **Explicit error reporting** - Sub-agents must describe what went wrong
2. **Command echo for debugging** - Ask them to report commands tried
3. **Self-contained troubleshooting** - They can't rely on us seeing their work

### Example Refined Prompt Structure:
```markdown
## Debug Requirements
- Report each command you try with its result
- If a command fails, include: exact command, error message, what you tried next
- Do not use fallback tools (find, grep, rg) - only use xs
```

## Deja Vu Note
User mentioned having deja vu about this discovery. Possible that:
- We discovered this limitation before in a previous session?
- The pattern of "thinking we can see more than we can" is recurring?
- Worth searching for previous discussions about Task visibility

## Testing Methodology
To verify Task visibility in future:
1. Compare golden output (Ctrl+R expanded) with xs output
2. Look for specific tool calls in sub-agent section
3. Use --json mode to examine raw JSONL structure
4. Search for `isSidechain` markers