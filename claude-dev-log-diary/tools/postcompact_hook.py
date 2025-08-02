#!/usr/bin/env python3
"""
PostCompact hook for automatic context recovery.

This hook triggers after Claude Code has compacted the conversation.
It uses the compaction summary to guide context recovery.
"""
import json
import sys
import os

# Read hook input
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

trigger = input_data.get("trigger", "")
session_id = input_data.get("session_id", "")
custom_instructions = input_data.get("custom_instructions", "")

# For auto-compact, provide context recovery instructions
if trigger == "auto":
    context_recovery_prompt = """
## IMPORTANT: Context Recovery Required

The conversation has been auto-compacted due to context limits. To recover critical context:

1. Use the xs tool to analyze the current session:
   ```
   ./xs {session_id} -S "important|critical|TODO|bug|fix"
   ```

2. Use Task delegation for deep context recovery:
   ```
   Task: "Deep context recovery from session {session_id}"
   ```
   
   Follow the pattern in claude-dev-log-diary/tools/context_recovery_pattern.md

3. Check your todo list to understand current work:
   - Review pending high-priority items
   - Note what was in_progress before compaction

4. Key areas to investigate:
   - Recent design decisions
   - Unresolved bugs or issues
   - User corrections or redirections
   - Any "MARK" annotations

Remember: Avoid the post-compaction failure mode of rushing to implementation.
First understand where you were and what you were doing.
""".format(session_id=session_id[:8] if session_id else "current")
    
    # Add to context via additionalContext
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostCompact",
            "additionalContext": context_recovery_prompt
        }
    }
    print(json.dumps(output))
    sys.exit(0)

# For manual compact, just pass through
sys.exit(0)