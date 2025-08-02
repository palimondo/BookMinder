#!/usr/bin/env python3
"""Test script for the two-hook compaction recovery system."""
import glob
import json
import subprocess
import sys
import time
from pathlib import Path


def run_hook(hook_script: str, input_data: dict) -> subprocess.CompletedProcess:
    """Run a hook script with given input."""
    result = subprocess.run(
        [sys.executable, hook_script],
        input=json.dumps(input_data),
        capture_output=True,
        text=True
    )
    return result

def test_two_hook_system() -> None:
    """Test the complete two-hook flow."""
    print("=== Testing Two-Hook Compaction Recovery System ===\n")

    session_id = "test123456789"

    # Step 1: Simulate PreCompact
    print("1. Simulating PreCompact hook (auto-compaction about to happen)...")
    precompact_input = {
        "trigger": "auto",
        "session_id": session_id,
        "timestamp": "2025-01-01T10:00:00Z"
    }

    result = run_hook("precompact_flag_hook.py", precompact_input)
    if result.returncode != 0:
        print(f"   ERROR: PreCompact hook failed: {result.stderr}")
    else:
        print(f"   SUCCESS: {result.stderr.strip()}")

    # Check flag was created
    flag_files = glob.glob(f"/tmp/.claude_compaction_{session_id[:8]}*.json")
    if flag_files:
        print(f"   Flag created: {flag_files[0]}")
        flag_content = Path(flag_files[0]).read_text()
        print(f"   Flag content: {flag_content}")
    else:
        print("   ERROR: No flag file found!")
        return

    print("\n2. Simulating time passing (compaction happens)...")
    time.sleep(1)

    # Step 2: Simulate PreToolUse after compaction
    print("\n3. Simulating PreToolUse hook (first tool use after compaction)...")
    pretooluse_input = {
        "tool": "Bash",
        "input": {"command": "ls -la"}
    }

    result = run_hook("pretooluse_context_recovery_hook.py", pretooluse_input)
    if result.returncode != 0:
        print(f"   ERROR: PreToolUse hook failed: {result.stderr}")
    else:
        if result.stdout:
            output = json.loads(result.stdout)
            context = output.get('hookSpecificOutput', {}).get('additionalContext', '')
            print("   SUCCESS: Context recovery prompt injected:")
            print("   " + "\n   ".join(context.split('\n')[:10]))  # First 10 lines
        else:
            print("   No output (normal - no flag found)")

    # Check flag was deleted
    flag_files = glob.glob(f"/tmp/.claude_compaction_{session_id[:8]}*.json")
    if flag_files:
        print(f"   WARNING: Flag still exists: {flag_files}")
    else:
        print("   SUCCESS: Flag was cleaned up")

    # Step 3: Verify subsequent tool uses are not affected
    print("\n4. Simulating second PreToolUse (should be normal)...")
    result = run_hook("pretooluse_context_recovery_hook.py", pretooluse_input)
    if result.stdout:
        print("   WARNING: Still getting context prompts!")
    else:
        print("   SUCCESS: No context prompt (as expected)")

def test_edge_cases() -> None:
    """Test edge cases."""
    print("\n\n=== Testing Edge Cases ===\n")

    # Test manual compact (should not create flag)
    print("1. Testing manual compact (should not create flag)...")
    manual_input = {
        "trigger": "manual",
        "session_id": "manual123"
    }
    result = run_hook("precompact_flag_hook.py", manual_input)
    flag_files = glob.glob("/tmp/.claude_compaction_manual*.json")
    if flag_files:
        print("   ERROR: Flag created for manual compact!")
    else:
        print("   SUCCESS: No flag for manual compact")

    # Test missing session_id
    print("\n2. Testing auto-compact without session_id...")
    no_session_input = {
        "trigger": "auto"
    }
    result = run_hook("precompact_flag_hook.py", no_session_input)
    print(f"   Exit code: {result.returncode}")

if __name__ == "__main__":
    # Clean up any old flags first
    old_flags = glob.glob("/tmp/.claude_compaction_*.json")
    for flag in old_flags:
        Path(flag).unlink()
        print(f"Cleaned up old flag: {flag}")

    if old_flags:
        print()

    test_two_hook_system()
    test_edge_cases()
