#!/usr/bin/env python3
"""PreCompact hook that sets a flag for post-compaction intervention."""
import json
import sys
from pathlib import Path


# Flag file location - use /tmp with session ID for multi-instance safety
def get_flag_file(session_id: str) -> Path:
    """Get flag file path including session ID."""
    return Path(f"/tmp/.claude_compaction_{session_id[:8]}.json")

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

trigger = input_data.get("trigger", "")
session_id = input_data.get("session_id", "")

if trigger == "auto" and session_id:
    # Write flag file with session info
    flag_file = get_flag_file(session_id)
    flag_data = {
        "trigger": trigger,
        "session_id": session_id,
        "timestamp": input_data.get("timestamp", "")
    }
    flag_file.write_text(json.dumps(flag_data))

    # Log for debugging
    print(f"Set compaction flag at {flag_file}", file=sys.stderr)

# Always exit cleanly
sys.exit(0)
