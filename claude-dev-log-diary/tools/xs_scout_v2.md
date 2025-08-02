# XS Tool Context Retrieval Guide

You have the `xs` tool for exploring Claude session logs. Your actions in this Task are NOT visible to the parent session, so you must report comprehensively.

## Important Architectural Note
Your tool calls and intermediate outputs are NOT visible in the parent session's transcript. Only your final response will be seen. Therefore:
- Report every command you tried
- Include relevant error messages
- Don't assume the parent can debug your work

## Citation Format
When you find relevant information, cite it as:
- `[session:seq]` - e.g., `[1e83:247]` for event 247 in session 1e83
- `[session:seq-seq]` - e.g., `[1e83:247-250]` for a range
- This allows navigation via: `./xs 1e83 -t 247`

## Tool Restrictions
- Use ONLY xs for session exploration
- Do NOT use find, grep, rg, or other search tools
- Do NOT browse directories manually
- If xs lacks needed functionality, report this as a limitation

## Task
[Specific request here]

## Required Report Structure
### Findings
- What you discovered (with citations)
- Relevant quotes demonstrating the finding

### Commands Executed
- List each xs command you tried
- Note which worked and which failed

### Tool Assessment
- Usability issues encountered
- Missing features that would have helped
- Error messages (include exact command that caused them)

### Recommendations
- Suggested improvements to xs
- Alternative approaches if xs couldn't complete the task