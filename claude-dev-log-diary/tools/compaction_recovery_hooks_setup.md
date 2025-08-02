# Compaction Recovery Hooks Setup

## Problem Solved

After auto-compaction, Claude often rushes into wrong work, especially in "auto-accept edits" mode. This two-hook system prevents that by injecting context recovery instructions after compaction.

## How It Works

Since there's no PostCompact hook, we use a two-hook system:

1. **PreCompact hook** - Detects imminent auto-compaction and writes a flag file to `/tmp/.claude_compaction_{session_id}.json`
2. **PreToolUse hook** - Checks for any compaction flags and injects context recovery prompt
3. **Flag is deleted** - Prevents repeated triggers
4. **Multi-instance safe** - Each session gets its own flag file

## Installation

Add to your Claude Code settings (`~/.claude/settings.json` or `.claude/settings.json`):

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "auto",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/claude-dev-log-diary/tools/precompact_flag_hook.py"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/claude-dev-log-diary/tools/pretooluse_context_recovery_hook.py"
          }
        ]
      }
    ]
  }
}
```

## Testing

1. **Manual test of flag system**:
   ```bash
   # Simulate PreCompact
   echo '{"trigger": "auto", "session_id": "test123"}' | python precompact_flag_hook.py
   
   # Check flag was created
   ls -la /tmp/.claude_compaction_*.json
   
   # Simulate PreToolUse
   echo '{"tool": "Bash", "input": {}}' | python pretooluse_context_recovery_hook.py
   ```

2. **Real test**:
   - Enable hooks with `/hooks reload`
   - Fill context to ~90% to trigger auto-compact
   - Observe that context recovery prompt appears before first tool use

## Benefits

- **Prevents wrong work** - Stops Claude from rushing into implementation
- **Preserves context** - Uses Task delegation to analyze without using main context
- **Works with auto-accept** - Intervenes even when edits are auto-accepted
- **Self-cleaning** - Flag file is deleted after use

## Debugging

Check flag file status:
```bash
ls -la /tmp/.claude_compaction_*.json
```

Clean up stale flags if needed:
```bash
rm -f /tmp/.claude_compaction_*.json
```

Enable debug output by adding to hooks:
```python
print(f"DEBUG: {message}", file=sys.stderr)
```