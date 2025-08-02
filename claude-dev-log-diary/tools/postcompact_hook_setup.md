# PostCompact Hook Setup

## Purpose

This hook automatically provides context recovery instructions when Claude Code performs an auto-compact due to context limits.

## Installation

Add to your Claude Code settings (`~/.claude/settings.json` or `.claude/settings.json`):

```json
{
  "hooks": {
    "PostCompact": [
      {
        "matcher": "auto",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/claude-dev-log-diary/tools/postcompact_hook.py"
          }
        ]
      }
    ]
  }
}
```

## How it Works

1. When context reaches ~90% and auto-compact triggers
2. The hook detects `"trigger": "auto"`
3. It injects context recovery instructions
4. After compaction, Claude will see these instructions and know how to recover context

## Testing

You can test manually with:
```bash
echo '{"trigger": "auto", "session_id": "e5837401-4f84-46e0-932f-eead7c00c678"}' | python postcompact_hook.py
```

## Benefits

- Prevents the "rush to implementation" failure mode after compaction
- Provides systematic approach to context recovery
- Leverages xs tool and Task delegation
- Maintains continuity across compaction events