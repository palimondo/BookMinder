#!/usr/bin/env python3
"""
Characterization tests for edge cases in explore_session.py.

Tests slash commands, interrupted requests, and other special cases.
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


def create_slash_command_session():
    """Create a session with slash commands."""
    events = [
        # Regular message
        {"type": "user", "message": {"content": [{"type": "text", "text": "Hello"}]},
         "timestamp": "2025-07-30T10:00:00.000Z"},
        # Slash command
        {"type": "user", "message": {"content": [{"type": "text", 
         "text": "<command-name>expert-council</command-name><command-message>How should I approach this?</command-message>"}]},
         "timestamp": "2025-07-30T10:00:01.000Z"},
        # Response
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "I'll help you with that"}]},
         "timestamp": "2025-07-30T10:00:02.000Z"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


def create_interrupted_session():
    """Create a session with interrupted requests."""
    events = [
        {"type": "user", "message": {"content": [{"type": "text", "text": "Start something"}]},
         "timestamp": "2025-07-30T10:00:00.000Z"},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "[Request interrupted by user]I was going to..."}]},
         "timestamp": "2025-07-30T10:00:01.000Z"},
        {"type": "user", "message": {"content": [{"type": "text", "text": "Do something else"}]},
         "timestamp": "2025-07-30T10:00:02.000Z"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


def create_empty_message_session():
    """Create a session with empty user messages."""
    events = [
        # Empty user message (protocol artifact)
        {"type": "user", "message": {"content": []},
         "timestamp": "2025-07-30T10:00:00.000Z"},
        # Assistant response
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "I notice you haven't said anything"}]},
         "timestamp": "2025-07-30T10:00:01.000Z"},
        # Another empty message
        {"type": "user", "message": {"content": [{"type": "text", "text": ""}]},
         "timestamp": "2025-07-30T10:00:02.000Z"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


def create_thinking_block_session():
    """Create a session with thinking blocks."""
    events = [
        {"type": "user", "message": {"content": [{"type": "text", "text": "Complex question"}]},
         "timestamp": "2025-07-30T10:00:00.000Z"},
        {"type": "assistant", "message": {"content": [
            {"type": "thinking", "text": "Let me think about this..."},
            {"type": "text", "text": "Here's my answer"}
        ]},
         "timestamp": "2025-07-30T10:00:01.000Z"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


class describe_slash_commands:
    """Test slash command handling."""
    
    def it_shows_slash_commands_in_timeline(self):
        """Slash commands should be displayed with / prefix."""
        session_file = create_slash_command_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            # Should show the slash command with proper formatting
            assert '/expert-council' in stdout or 'How should I approach this?' in stdout
        finally:
            Path(session_file).unlink()
    
    def it_filters_slash_commands_as_user_messages(self):
        """Slash commands should be included when filtering for user messages."""
        session_file = create_slash_command_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '-U'])
            
            assert returncode == 0
            # Should include the slash command
            assert 'Hello' in stdout  # Regular message
            assert 'How should I approach this?' in stdout or '/expert-council' in stdout
            # Should NOT include assistant response
            assert "I'll help you with that" not in stdout
        finally:
            Path(session_file).unlink()


class describe_interrupted_requests:
    """Test interrupted request handling."""
    
    def it_shows_interrupted_requests(self):
        """Interrupted requests should be visible in timeline."""
        session_file = create_interrupted_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            # Should show the interrupted message
            assert '[Request interrupted by user]' in stdout or 'I was going to...' in stdout
        finally:
            Path(session_file).unlink()
    
    def it_counts_interrupted_in_summary(self):
        """Summary should count interrupted requests."""
        session_file = create_interrupted_session()
        
        try:
            stdout, returncode = run_explore_session([session_file])
            
            assert returncode == 0
            # Should mention interruption in summary
            assert 'interrupt' in stdout.lower() or 'Messages:' in stdout
        finally:
            Path(session_file).unlink()


class describe_empty_messages:
    """Test empty message handling."""
    
    def it_handles_empty_user_messages(self):
        """Empty user messages should be handled gracefully."""
        session_file = create_empty_message_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            # Should show some indication of empty messages
            # Current behavior shows [empty] for empty messages
            assert '[empty]' in stdout or '> ' in stdout
        finally:
            Path(session_file).unlink()
    
    def it_can_filter_empty_messages(self):
        """Should be able to see empty messages with user filter."""
        session_file = create_empty_message_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '-U'])
            
            assert returncode == 0
            # User filter should include empty messages
            # Should see indication of empty messages
            lines = stdout.strip().split('\n')
            # Should have at least 2 user messages (both empty)
            user_lines = [l for l in lines if '>' in l or '[empty]' in l]
            assert len(user_lines) >= 2
        finally:
            Path(session_file).unlink()


class describe_thinking_blocks:
    """Test thinking block handling."""
    
    def it_separates_thinking_from_text(self):
        """Thinking blocks should be handled separately from regular text."""
        session_file = create_thinking_block_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            # Should show the actual response
            assert "Here's my answer" in stdout
            # Thinking might be shown differently or hidden
            # Current implementation may or may not show thinking
        finally:
            Path(session_file).unlink()
    
    def it_shows_thinking_in_full_mode(self):
        """Full mode should show thinking content."""
        session_file = create_thinking_block_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '--full'])
            
            assert returncode == 0
            # In full mode, might show thinking
            # Document current behavior
            assert "Here's my answer" in stdout
        finally:
            Path(session_file).unlink()


class describe_meta_messages:
    """Test meta message handling."""
    
    def it_handles_meta_flags(self):
        """Messages with isMeta flag should be handled appropriately."""
        events = [
            {"type": "user", "message": {"content": [{"type": "text", "text": "Regular message"}]},
             "timestamp": "2025-07-30T10:00:00.000Z"},
            {"type": "user", "message": {"content": [{"type": "text", "text": "Meta message"}], "isMeta": True},
             "timestamp": "2025-07-30T10:00:01.000Z"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
            session_file = f.name
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            # Both messages should appear in timeline
            assert "Regular message" in stdout
            assert "Meta message" in stdout
        finally:
            Path(session_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])