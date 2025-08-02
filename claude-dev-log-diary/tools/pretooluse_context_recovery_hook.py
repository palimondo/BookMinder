#!/usr/bin/env python3
"""
PreToolUse hook that detects post-compaction state and injects context recovery.
"""
import json
import sys
import glob
from pathlib import Path

# Flag file pattern - look for any compaction flags
FLAG_PATTERN = "/tmp/.claude_compaction_*.json"

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

# Check for any compaction flag files
flag_files = glob.glob(FLAG_PATTERN)
if flag_files:
    # Process the first flag found (should only be one per session)
    flag_file = Path(flag_files[0])
    
    try:
        flag_data = json.loads(flag_file.read_text())
        session_id = flag_data.get('session_id', 'unknown')
        
        # Delete the flag immediately to prevent repeated triggers
        flag_file.unlink()
        
        # Generate context recovery prompt
        context_prompt = f"""## STOP: Auto-compaction just occurred!

Before rushing into any work, recover context using Task delegation:

```
Use Task to analyze session {session_id[:8] if session_id else 'current'} following @claude-dev-log-diary/tools/context_recovery_pattern.md

Key commands:
- Timeline overview: xs {session_id[:8]} -t 
- Last todo state: xs {session_id[:8]} -i TodoWrite -C 1 | tail -5
- Recent decisions: xs {session_id[:8]} -S "decision|approach|should"
```

DO NOT proceed with any implementation until context is recovered."""
        
        # Output the prompt
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": context_prompt,
                "shouldBlock": False  # Don't block, just inject context
            }
        }
        print(json.dumps(output))
        sys.exit(0)
        
    except Exception as e:
        print(f"Error reading flag file {flag_file}: {e}", file=sys.stderr)
        # Clean up corrupted flag
        flag_file.unlink(missing_ok=True)

# No flag, proceed normally
sys.exit(0)