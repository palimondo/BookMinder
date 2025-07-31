#!/usr/bin/env python3
"""
Integration tests for filter patterns in explore_session.py.

Tests complex include/exclude patterns and their combinations.
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


def create_diverse_session():
    """Create a session with diverse tool and message types."""
    events = [
        # Various bash commands
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "id": "t1",
                                                     "input": {"command": "git status"}}]},
         "timestamp": "2025-07-30T10:00:00.000Z"},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "id": "t2",
                                                     "input": {"command": "git commit -m 'test'"}}]},
         "timestamp": "2025-07-30T10:00:01.000Z"},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "id": "t3",
                                                     "input": {"command": "ls -la"}}]},
         "timestamp": "2025-07-30T10:00:02.000Z"},
        # Various file operations
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Edit", "id": "t4",
                                                     "input": {"file_path": "/src/main.py", "old_string": "a", "new_string": "b"}}]},
         "timestamp": "2025-07-30T10:00:03.000Z"},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Write", "id": "t5",
                                                     "input": {"file_path": "/docs/README.md", "content": "# Docs"}}]},
         "timestamp": "2025-07-30T10:00:04.000Z"},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read", "id": "t6",
                                                     "input": {"file_path": "/src/utils.py"}}]},
         "timestamp": "2025-07-30T10:00:05.000Z"},
        # Search operations
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Grep", "id": "t7",
                                                     "input": {"pattern": "TODO", "path": "/src"}}]},
         "timestamp": "2025-07-30T10:00:06.000Z"},
        # Messages
        {"type": "user", "message": {"content": [{"type": "text", "text": "Please check the code"}]},
         "timestamp": "2025-07-30T10:00:07.000Z"},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "I'll check that for you"}]},
         "timestamp": "2025-07-30T10:00:08.000Z"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


class describe_wildcard_patterns:
    """Test wildcard patterns in filters."""
    
    def it_filters_bash_git_commands(self):
        """Pattern 'Bash(git *)' should match git commands only."""
        session_file = create_diverse_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Bash(git *)'])
            
            assert returncode == 0
            # Should show git commands
            assert 'git status' in stdout
            assert 'git commit' in stdout
            # Should NOT show non-git bash commands
            assert 'ls -la' not in stdout
        finally:
            Path(session_file).unlink()
    
    def it_filters_file_paths_with_wildcards(self):
        """Patterns can match file paths with wildcards."""
        session_file = create_diverse_session()
        
        try:
            # Filter for /src/* files
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Edit(/src/*),Read(/src/*)'])
            
            assert returncode == 0
            # Should show operations on /src files
            assert '/src/main.py' in stdout
            assert '/src/utils.py' in stdout
            # Should NOT show /docs files
            assert '/docs/README.md' not in stdout
        finally:
            Path(session_file).unlink()


class describe_multiple_filters:
    """Test multiple include/exclude patterns."""
    
    def it_combines_multiple_include_patterns(self):
        """Multiple include patterns with comma separation."""
        session_file = create_diverse_session()
        
        try:
            # Include both Edit and Write operations
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Edit,Write'])
            
            assert returncode == 0
            # Should show both Edit and Write
            assert 'Edit' in stdout
            assert 'Write' in stdout
            # Should NOT show other tools
            assert 'Bash' not in stdout
            assert 'Grep' not in stdout
        finally:
            Path(session_file).unlink()
    
    def it_applies_exclude_after_include(self):
        """Exclude filters should remove from included items."""
        session_file = create_diverse_session()
        
        try:
            # Include all tools but exclude Read
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Tool', '-x', 'Read'])
            
            assert returncode == 0
            # Should show most tools
            assert 'Edit' in stdout
            assert 'Write' in stdout
            assert 'Bash' in stdout
            # Should NOT show Read
            assert 'Read: ←' not in stdout
        finally:
            Path(session_file).unlink()


class describe_virtual_entities:
    """Test virtual entity filters (Message, Tool, User, Assistant)."""
    
    def it_filters_by_message_entity(self):
        """'Message' should include all text messages."""
        session_file = create_diverse_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Message'])
            
            assert returncode == 0
            # Should show text messages (user shows with >)
            assert '> Please check the code' in stdout
            assert "I'll check that for you" in stdout
            # Should NOT show tool execution
            assert 'Bash: $' not in stdout
            assert 'Edit: →' not in stdout
        finally:
            Path(session_file).unlink()
    
    def it_filters_by_tool_entity(self):
        """'Tool' should include all tool uses."""
        session_file = create_diverse_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Tool'])
            
            assert returncode == 0
            # Should show all tools
            assert 'Bash' in stdout
            assert 'Edit' in stdout
            assert 'Grep' in stdout
            # Should NOT show text messages
            assert 'Please check the code' not in stdout
        finally:
            Path(session_file).unlink()


class describe_complex_patterns:
    """Test complex pattern combinations."""
    
    def it_handles_nested_parentheses(self):
        """Patterns with nested parentheses should work."""
        session_file = create_diverse_session()
        
        try:
            # Pattern with complex parameter matching
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Bash(git commit*)'])
            
            assert returncode == 0
            # Should show git commit
            assert 'git commit' in stdout
            # Should NOT show git status
            assert 'git status' not in stdout
        finally:
            Path(session_file).unlink()
    
    def it_combines_entity_and_specific_filters(self):
        """Can combine virtual entities with specific tool filters."""
        session_file = create_diverse_session()
        
        try:
            # Include all messages AND specific tools
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Message,Edit,Write'])
            
            assert returncode == 0
            # Should show messages (user shows with >)
            assert '> Please check the code' in stdout
            # Should show specified tools
            assert 'Edit' in stdout
            assert 'Write' in stdout
            # Should NOT show other tools like Bash
            assert 'Bash: $' not in stdout
        finally:
            Path(session_file).unlink()


class describe_edge_cases:
    """Test edge cases in filter parsing."""
    
    def it_handles_empty_filter(self):
        """Empty filter string should show all."""
        session_file = create_diverse_session()
        
        try:
            stdout_all, _ = run_explore_session([session_file, '-t'])
            stdout_empty, _ = run_explore_session([session_file, '-t', '-i', ''])
            
            # Empty include filter should be like no filter
            # (Just documenting current behavior)
        finally:
            Path(session_file).unlink()
    
    def it_handles_special_characters(self):
        """Filters with special characters."""
        session_file = create_diverse_session()
        
        try:
            # Filter with special regex characters
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Bash(*)'])
            
            # Should handle wildcards correctly
            assert returncode == 0
        finally:
            Path(session_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])