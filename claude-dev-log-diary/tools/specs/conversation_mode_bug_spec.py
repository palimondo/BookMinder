#!/usr/bin/env python3
"""
Characterization test for conversation mode bug.

Documents current behavior where -M -x Tool still shows tool announcements.
"""
import subprocess
from pathlib import Path
import tempfile
import json
import pytest


def run_explore_session(args):
    """Run explore_session.py with given arguments and return output."""
    tools_dir = Path(__file__).parent.parent  # specs/ -> tools/
    cmd = ['./explore_session.py'] + args
    result = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True, 
        cwd=tools_dir
    )
    return result.stdout, result.returncode


def create_mixed_session():
    """Create a session with messages and tools."""
    events = [
        # User message
        {"type": "user", "message": {"content": [{"type": "text", "text": "Please check the git status"}]},
         "timestamp": "2025-07-30T10:00:00.000Z"},
        
        # Assistant with text and tool
        {"type": "assistant", "message": {"content": [
            {"type": "text", "text": "I'll check the git status for you."},
            {"type": "tool_use", "name": "Bash", "id": "t1", "input": {"command": "git status"}}
        ]},
         "timestamp": "2025-07-30T10:00:01.000Z"},
        
        # Tool result
        {"type": "message", "data": {"tool_results": [{"tool_use_id": "t1", "content": "On branch main"}]},
         "timestamp": "2025-07-30T10:00:02.000Z"},
        
        # Assistant with only tools (this generates tool announcement)
        {"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Bash", "id": "t2", "input": {"command": "git log --oneline -5"}},
            {"type": "tool_use", "name": "Read", "id": "t3", "input": {"file_path": "/README.md"}}
        ]},
         "timestamp": "2025-07-30T10:00:03.000Z"},
        
        # Tool results
        {"type": "message", "data": {"tool_results": [
            {"tool_use_id": "t2", "content": "abc123 Latest commit\ndef456 Previous commit"},
            {"tool_use_id": "t3", "content": "# Project README"}
        ]},
         "timestamp": "2025-07-30T10:00:04.000Z"},
        
        # Assistant text only
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "The repository is on the main branch."}]},
         "timestamp": "2025-07-30T10:00:05.000Z"},
        
        # User response
        {"type": "user", "message": {"content": [{"type": "text", "text": "Thanks!"}]},
         "timestamp": "2025-07-30T10:00:06.000Z"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


class describe_conversation_mode_exclude_tools:
    """Test -M -x Tool combination (conversation mode excluding tools)."""
    
    def it_previously_showed_tool_announcements(self):
        """BUG FIXED: Tool announcements used to appear even when tools were excluded."""
        pytest.skip("This bug has been fixed - keeping test for documentation")
        
        session_file = create_mixed_session()
        
        try:
            # -M includes messages, -x Tool should exclude all tool-related items
            stdout, returncode = run_explore_session([session_file, '-M', '-x', 'Tool'])
            
            assert returncode == 0
            
            # Previous buggy behavior: tool announcements appeared
            assert '[Tools: Bash, Read]' in stdout
            
            # What we want: only user and assistant text messages
            assert '> Please check the git status' in stdout
            assert "I'll check the git status for you." in stdout
            assert 'The repository is on the main branch.' in stdout
            assert '> Thanks!' in stdout
            
            # Tool commands should NOT appear (except in user's text)
            assert 'Bash(git status)' not in stdout
            assert 'Bash(git log' not in stdout
            assert 'git log' not in stdout
            
        finally:
            Path(session_file).unlink()
    
    def it_should_filter_out_tool_announcements(self):
        """DESIRED: No tool announcements when excluding tools."""
        # Remove skip now that we've implemented the fix
        
        session_file = create_mixed_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-M', '-x', 'Tool'])
            
            assert returncode == 0
            
            # Desired behavior: NO tool announcements
            assert '[Tools:' not in stdout
            
            # Only conversation content
            lines = stdout.strip().split('\n')
            # Should have exactly 4 conversation lines
            conversation_lines = [l for l in lines if l.strip() and not l.startswith('--')]
            assert len(conversation_lines) == 4
            
        finally:
            Path(session_file).unlink()


class describe_message_mode_behavior:
    """Test -M flag behavior in isolation."""
    
    def it_includes_all_text_messages(self):
        """Message mode should include all user and assistant text."""
        session_file = create_mixed_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-M'])
            
            assert returncode == 0
            
            # Should include all messages
            assert '> Please check the git status' in stdout
            assert "I'll check the git status for you." in stdout
            assert 'The repository is on the main branch.' in stdout
            assert '> Thanks!' in stdout
            
            # Also includes tool announcements (when no exclusion)
            assert '[Tools: Bash, Read]' in stdout
            
        finally:
            Path(session_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])