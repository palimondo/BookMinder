#!/usr/bin/env python3
"""
Characterization tests for shortcut flags in explore_session.py.

Tests -M/-U/-a/-T shortcut flags functionality.
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
    """Create a session with mixed message types."""
    events = [
        # User message
        {"type": "user", "message": {"content": [{"type": "text", "text": "Hello Claude"}]}, 
         "timestamp": "2025-07-30T10:00:00.000Z"},
        # Assistant text
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "Hello! How can I help?"}]},
         "timestamp": "2025-07-30T10:00:01.000Z"},
        # Assistant with tool
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read", "id": "tool_1",
                                                     "input": {"file_path": "/test.py"}}]},
         "timestamp": "2025-07-30T10:00:02.000Z"},
        # Tool result
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "tool_1",
                                                "content": "File contents"}]},
         "timestamp": "2025-07-30T10:00:03.000Z"},
        # Another user message
        {"type": "user", "message": {"content": [{"type": "text", "text": "Thanks!"}]},
         "timestamp": "2025-07-30T10:00:04.000Z"},
        # Assistant with another tool
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Write", "id": "tool_2",
                                                     "input": {"file_path": "/output.txt", "content": "Done"}}]},
         "timestamp": "2025-07-30T10:00:05.000Z"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


class describe_M_flag:
    """Test -M flag for all messages."""
    
    def it_shows_all_messages(self):
        """-M should show all messages (user + assistant)."""
        session_file = create_mixed_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '-M'])
            
            assert returncode == 0
            # Should show user messages
            assert 'Hello Claude' in stdout
            assert 'Thanks!' in stdout
            # Should show assistant messages
            assert 'Hello! How can I help?' in stdout
            # Should also show tools
            assert 'Read' in stdout
            assert 'Write' in stdout
        finally:
            Path(session_file).unlink()
    
    def it_is_shortcut_for_include_Message(self):
        """-M should be equivalent to -i Message."""
        session_file = create_mixed_session()
        
        try:
            stdout_m, _ = run_explore_session([session_file, '-t', '-M'])
            stdout_i, _ = run_explore_session([session_file, '-t', '-i', 'Message'])
            
            # Should produce same output
            assert stdout_m == stdout_i
        finally:
            Path(session_file).unlink()


class describe_U_flag:
    """Test -U flag for user messages."""
    
    def it_shows_only_user_messages(self):
        """-U should show only user messages."""
        session_file = create_mixed_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '-U'])
            
            assert returncode == 0
            # Should show user text messages with > prefix
            assert '> Hello Claude' in stdout
            assert '> Thanks!' in stdout
            # Should NOT show assistant messages
            assert 'Hello! How can I help?' not in stdout
            # Should NOT show tool results (they're filtered out)
            assert 'File contents' not in stdout
        finally:
            Path(session_file).unlink()


class describe_a_flag:
    """Test -a flag for assistant messages."""
    
    def it_shows_only_assistant_messages(self):
        """-a should show only assistant messages."""
        session_file = create_mixed_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '-a'])
            
            assert returncode == 0
            # Should show assistant messages
            assert 'Hello! How can I help?' in stdout
            # Should show tool uses
            assert 'Read' in stdout
            assert 'Write' in stdout
            # Should NOT show user messages
            assert 'Hello Claude' not in stdout
            assert 'Thanks!' not in stdout
        finally:
            Path(session_file).unlink()


class describe_T_flag:
    """Test -T flag for tools."""
    
    def it_shows_only_tools(self):
        """-T should show only tool calls."""
        session_file = create_mixed_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '-T'])
            
            assert returncode == 0
            # Should show tools
            assert 'Read' in stdout
            assert 'Write' in stdout
            # Should NOT show text messages
            assert 'Hello Claude' not in stdout
            assert 'Hello! How can I help?' not in stdout
            assert 'Thanks!' not in stdout
        finally:
            Path(session_file).unlink()
    
    def it_includes_tool_results_by_default(self):
        """-T should include tool results unless --no-tool-results is used."""
        session_file = create_mixed_session()
        
        try:
            stdout_with, _ = run_explore_session([session_file, '-t', '-T'])
            stdout_without, _ = run_explore_session([session_file, '-t', '-T', '--no-tool-results'])
            
            # With results should show the tool result
            assert 'File contents' in stdout_with
            # Without results should not
            assert 'File contents' not in stdout_without
        finally:
            Path(session_file).unlink()


class describe_combined_flags:
    """Test combining multiple flags."""
    
    def it_combines_flags_correctly(self):
        """Multiple flags should combine their filters."""
        session_file = create_mixed_session()
        
        try:
            # -U -a should show both user and assistant (like -M)
            stdout_ua, _ = run_explore_session([session_file, '-t', '-U', '-a'])
            stdout_m, _ = run_explore_session([session_file, '-t', '-M'])
            
            # Should be equivalent
            assert stdout_ua == stdout_m
        finally:
            Path(session_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])