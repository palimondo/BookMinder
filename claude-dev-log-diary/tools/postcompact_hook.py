#!/usr/bin/env python3
"""
PostCompact hook for automatic context recovery.

This hook triggers after Claude Code has compacted the conversation.
It generates a minimal self-prompt to use Task delegation for context recovery.
"""
import json
import sys

# Read hook input
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

trigger = input_data.get("trigger", "")
session_id = input_data.get("session_id", "")
message_index = input_data.get("message_index", "")  # Index where compaction occurred

# For auto-compact, provide minimal self-prompt
if trigger == "auto":
    # Generate minimal self-prompt that instructs Claude to use Task delegation
    self_prompt = f"""## Auto-compaction detected

Use Task to recover context:
- Session ID: {session_id[:8] if session_id else 'current'}
- Compaction point: message {message_index if message_index else 'unknown'}
- Recovery pattern: @claude-dev-log-diary/tools/context_recovery_pattern.md

Delegate to Task with: xs {session_id} {message_index if message_index else ''}"""
    
    # Return the prompt as additionalContext
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostCompact",
            "additionalContext": self_prompt
        }
    }
    print(json.dumps(output))
    sys.exit(0)

# For manual compact, just pass through
sys.exit(0)