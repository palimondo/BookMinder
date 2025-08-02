# PostCompact Hook Setup

## Purpose

This hook provides a minimal self-prompt after auto-compaction that triggers Task delegation for context recovery. The hook:
- Detects auto-compaction events
- Extracts session ID and message index
- Generates a brief prompt referencing the context recovery pattern
- Lets Task sub-agent handle the heavy lifting

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
2. The hook detects `"trigger": "auto"` and extracts session info
3. It injects a minimal self-prompt suggesting Task delegation
4. Claude sees the prompt and uses Task to recover context
5. The Task sub-agent loads the recovery pattern and analyzes the session
6. Main session preserves its limited context while sub-agent does the work

## Testing

You can test manually with:
```bash
echo '{"trigger": "auto", "session_id": "e5837401-4f84-46e0-932f-eead7c00c678"}' | python postcompact_hook.py
```

## Benefits

- **Minimal context usage** - Main session preserves its limited context
- **Deep analysis** - Sub-agent can thoroughly analyze the session
- **Proven pattern** - Uses established context recovery methodology
- **Self-contained** - Sub-agent gets all needed info from session transcript
- **Prevents failure modes** - Avoids rushing to implementation after compaction