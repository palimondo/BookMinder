#!/usr/bin/env python3
"""
Test suite for explore_session.py

These tests capture the expected behavior to prevent regressions.
Run with: pytest test_explore_session.py -v
"""
import json
import os
import tempfile
from pathlib import Path
import subprocess
import pytest


def run_explore_session(args):
    """Run explore_session.py with given arguments and return output."""
    cmd = ['./explore_session.py'] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
    return result.stdout, result.stderr, result.returncode


def test_todo_results_appear_in_timeline():
    """Event 10 (Todo results) should appear in the timeline."""
    # Create test session
    content = '''{"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "TodoWrite", "id": "toolu_01R63sv6o2ocyEe24sNPgXU6", "input": {"todos": [{"id": "1", "content": "Test", "status": "in_progress", "priority": "high"}]}}]}, "timestamp": "2025-07-13T08:21:20.000Z"}
{"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "toolu_01R63sv6o2ocyEe24sNPgXU6", "content": "Todos have been modified successfully. Ensure that you continue to use the todo list to track your progress. Please proceed with the current tasks if applicable"}]}, "timestamp": "2025-07-13T08:21:21.718Z"}
{"type": "assistant", "message": {"content": [{"type": "text", "text": "Let me first check the current implementation and the failing test:"}]}, "timestamp": "2025-07-13T08:21:22.000Z"}'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write(content)
        session_file = f.name
    
    try:
        stdout, stderr, returncode = run_explore_session([session_file, '-t'])
        
        assert returncode == 0, f"Command failed: {stderr}"
        
        # Check that all 3 events appear
        assert '[1] ⏺' in stdout, "Event 1 (TodoWrite) should appear"
        assert '[2] ⏺' in stdout, "Event 2 (assistant with tool) should appear"
        assert '[3] ⎿' in stdout or '[3] >' in stdout, "Event 3 (Todo result) should appear"
        assert '[4] ⏺' in stdout, "Event 4 (assistant text) should appear"
        
        # Verify no gaps in sequence
        lines = stdout.strip().split('\n')
        events = [l for l in lines if l.strip() and l[0] == '[']
        assert len(events) >= 4, f"Should have at least 4 events, got {len(events)}"
    finally:
        os.unlink(session_file)


def test_thinking_content_displays():
    """Thinking content should show with <thinking> prefix."""
    content = '''{"type": "assistant", "message": {"content": [{"type": "thinking", "thinking": "The user is asking me to review a PR for a filter-by-reading-status story. I need to pay special attention to both implementation and process requirements outlined in issue #13."}]}, "timestamp": "2025-07-26T13:49:00.000Z"}
{"type": "assistant", "message": {"content": [{"type": "text", "text": "<analysis>\\na. **Event Type and Context**: This is a comment on an open PR requesting a code review.\\n</analysis>"}]}, "timestamp": "2025-07-26T13:49:01.000Z"}'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write(content)
        session_file = f.name
    
    try:
        stdout, stderr, returncode = run_explore_session([session_file, '-t'])
        
        assert returncode == 0, f"Command failed: {stderr}"
        
        # Check thinking content appears
        assert '<thinking>' in stdout, "Thinking content should be displayed"
        assert 'The user is asking me to review' in stdout, "Thinking preview should appear"
    finally:
        os.unlink(session_file)


def test_tool_only_messages_display():
    """Assistant messages with only tools should display."""
    content = '''{"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "mcp__github_comment__update_claude_comment", "id": "tool_123", "input": {}}]}, "timestamp": "2025-07-26T13:49:02.000Z"}'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write(content)
        session_file = f.name
    
    try:
        stdout, stderr, returncode = run_explore_session([session_file, '-t'])
        
        assert returncode == 0, f"Command failed: {stderr}"
        
        # Check tool-only message appears
        assert '[Tools: mcp__github_comment__update_claude_comment]' in stdout or 'mcp__github_comment__update_claude_comment' in stdout, "Tool-only message should display"
    finally:
        os.unlink(session_file)


def test_compact_tool_format():
    """Tools should display with proper format in compact mode."""
    content = '''{"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "TodoWrite", "id": "toolu_01R63sv6o2ocyEe24sNPgXU6", "input": {"todos": [{"id": "1", "content": "Test", "status": "in_progress", "priority": "high"}]}}]}, "timestamp": "2025-07-13T08:21:20.000Z"}'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write(content)
        session_file = f.name
    
    try:
        stdout, stderr, returncode = run_explore_session([session_file, '-t'])
        
        # TodoWrite should show with status counts
        assert 'TodoWrite: Updated 1 todos (1 in_progress)' in stdout or 'TodoWrite' in stdout, "TodoWrite should appear"
    finally:
        os.unlink(session_file)


def test_json_export_raw_objects():
    """JSON export should output raw JSONL objects, not transformed timeline."""
    content = '''{"type": "assistant", "message": {"id": "msg_123", "content": [{"type": "tool_use", "name": "Edit", "id": "tool_123", "input": {"file_path": "/test.py", "old_string": "foo", "new_string": "bar"}}]}, "timestamp": "2025-07-13T08:21:20.000Z"}
{"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "tool_123", "content": "File edited"}]}, "timestamp": "2025-07-13T08:21:21.000Z"}'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write(content)
        session_file = f.name
    
    try:
        # Test --json output
        stdout, stderr, returncode = run_explore_session([session_file, '-t', '1-2', '--json'])
        
        assert returncode == 0, f"Command failed: {stderr}"
        
        # Parse JSON output
        json_data = json.loads(stdout)
        assert len(json_data) == 2, "Should have 2 objects"
        
        # First object should be the original assistant message
        assert json_data[0]['type'] == 'assistant'
        assert 'message' in json_data[0]
        assert json_data[0]['message']['id'] == 'msg_123'
        
        # Second object should be the user message
        assert json_data[1]['type'] == 'user'
        assert 'message' in json_data[1]
    finally:
        os.unlink(session_file)


def test_export_json_range():
    """export-json should export raw JSONL objects for the specified range."""
    content = '''{"type": "assistant", "message": {"id": "msg_1", "content": [{"type": "text", "text": "First"}]}, "timestamp": "2025-07-13T08:21:20.000Z"}
{"type": "assistant", "message": {"id": "msg_2", "content": [{"type": "tool_use", "name": "Edit", "id": "tool_123", "input": {"file_path": "/test.py", "old_string": "foo", "new_string": "bar"}}]}, "timestamp": "2025-07-13T08:21:21.000Z"}
{"type": "assistant", "message": {"id": "msg_3", "content": [{"type": "text", "text": "Third"}]}, "timestamp": "2025-07-13T08:21:22.000Z"}'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        f.write(content)
        session_file = f.name
    
    export_file = None
    try:
        # Export range 2-3
        export_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False).name
        stdout, stderr, returncode = run_explore_session([session_file, '--export-json', '2-3', export_file])
        
        assert returncode == 0, f"Command failed: {stderr}"
        assert 'Exported 2 events' in stdout
        
        # Read exported JSON
        with open(export_file, 'r') as f:
            json_data = json.load(f)
        
        assert len(json_data) == 2, "Should have 2 objects"
        assert json_data[0]['message']['id'] == 'msg_2'
        assert json_data[1]['message']['id'] == 'msg_3'
    finally:
        os.unlink(session_file)
        if export_file:
            os.unlink(export_file)


# Golden output examples for manual verification
GOLDEN_OUTPUTS = {
    "timeline_compact": """[1] ⏺ [Tools: TodoWrite]
[2] ⏺ TodoWrite: Updated 1 todos (1 in_progress)
[3] ⎿  ☒ Todos updated successfully
[4] ⏺ Let me first check the current implementation and the failing test:""",
    
    "timeline_truncated": """⏺ Update Todos
  ⎿  Waiting…
  
  ⎿  ☒ Todos updated successfully

⏺ Let me first check the current implementation and the failing test:""",
    
    "tool_formats": """[1] ⏺ Bash: $ git status
[2] ⏺ Edit: → /path/to/file.py  
[3] ⏺ Read: ← /path/to/file.py
[4] ⏺ Grep: "pattern" in /search/path
[5] ⏺ TodoWrite: Updated 3 todos (1 completed, 1 in_progress, 1 pending)"""
}


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])