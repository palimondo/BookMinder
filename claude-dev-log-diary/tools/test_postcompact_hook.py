#!/usr/bin/env python3
"""
Test script for PostCompact hook debugging.

Usage:
    python test_postcompact_hook.py
"""
import json
import subprocess
import sys

def test_hook(test_case):
    """Test the hook with given input."""
    print(f"\n=== Testing: {test_case['name']} ===")
    print(f"Input: {json.dumps(test_case['input'], indent=2)}")
    
    # Run the hook
    result = subprocess.run(
        [sys.executable, 'postcompact_hook.py'],
        input=json.dumps(test_case['input']),
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"ERROR: Hook failed with code {result.returncode}")
        print(f"Stderr: {result.stderr}")
        return
    
    if result.stdout:
        try:
            output = json.loads(result.stdout)
            print(f"Output: {json.dumps(output, indent=2)}")
            if 'hookSpecificOutput' in output:
                context = output['hookSpecificOutput'].get('additionalContext', '')
                print(f"\nGenerated context:\n{context}")
        except json.JSONDecodeError:
            print(f"Raw output: {result.stdout}")

# Test cases
test_cases = [
    {
        'name': 'Auto-compact with full info',
        'input': {
            'trigger': 'auto',
            'session_id': 'e5837401-4f84-46e0-932f-eead7c00c678',
            'message_index': 1234
        }
    },
    {
        'name': 'Auto-compact without message index',
        'input': {
            'trigger': 'auto',
            'session_id': 'e5837401-4f84-46e0-932f-eead7c00c678'
        }
    },
    {
        'name': 'Manual compact (should pass through)',
        'input': {
            'trigger': 'manual',
            'session_id': 'e5837401-4f84-46e0-932f-eead7c00c678'
        }
    },
    {
        'name': 'Invalid JSON',
        'input': 'not json'
    }
]

if __name__ == '__main__':
    for test_case in test_cases:
        if isinstance(test_case['input'], str):
            # Special case for invalid JSON test
            print(f"\n=== Testing: {test_case['name']} ===")
            result = subprocess.run(
                [sys.executable, 'postcompact_hook.py'],
                input=test_case['input'],
                capture_output=True,
                text=True
            )
            print(f"Exit code: {result.returncode}")
            print(f"Stderr: {result.stderr}")
        else:
            test_hook(test_case)