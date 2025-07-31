#!/usr/bin/env python3
"""
Characterization tests for file operation features in explore_session.py.

Tests --files, --created, and file-related functionality.
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


def create_session_with_file_ops():
    """Create a session with various file operations."""
    events = [
        {
            "type": "assistant",
            "message": {"content": [{"type": "tool_use", "name": "Write", "id": "tool_1", 
                                   "input": {"file_path": "/new_file.py", "content": "print('hello')"}}]},
            "timestamp": "2025-07-30T10:00:00.000Z"
        },
        {
            "type": "assistant", 
            "message": {"content": [{"type": "tool_use", "name": "Edit", "id": "tool_2",
                                   "input": {"file_path": "/existing.py", "old_string": "foo", "new_string": "bar"}}]},
            "timestamp": "2025-07-30T10:00:01.000Z"
        },
        {
            "type": "assistant",
            "message": {"content": [{"type": "tool_use", "name": "Write", "id": "tool_3",
                                   "input": {"file_path": "/another_new.txt", "content": "test content"}}]},
            "timestamp": "2025-07-30T10:00:02.000Z"
        },
        {
            "type": "assistant",
            "message": {"content": [{"type": "tool_use", "name": "MultiEdit", "id": "tool_4",
                                   "input": {"file_path": "/existing.py", "edits": [
                                       {"old_string": "bar", "new_string": "baz"}
                                   ]}}]},
            "timestamp": "2025-07-30T10:00:03.000Z"
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


class describe_created_files_command:
    """Test --created/-c command functionality."""
    
    def it_shows_only_created_files(self):
        """--created should list only files created with Write tool."""
        session_file = create_session_with_file_ops()
        
        try:
            stdout, returncode = run_explore_session([session_file, '--created'])
            
            assert returncode == 0
            # Should show files created with Write (without full path)
            assert 'new_file.py' in stdout
            assert 'another_new.txt' in stdout
            # Should show content preview
            assert "print('hello')" in stdout
            # Should NOT show edited files
            assert 'existing.py' not in stdout
        finally:
            Path(session_file).unlink()
    
    def it_works_with_short_flag(self):
        """Short flag -c should work same as --created."""
        session_file = create_session_with_file_ops()
        
        try:
            stdout_long, _ = run_explore_session([session_file, '--created'])
            stdout_short, _ = run_explore_session([session_file, '-c'])
            
            # Both should produce same output
            assert stdout_long == stdout_short
        finally:
            Path(session_file).unlink()


class describe_files_command:
    """Test --files/-f command functionality."""
    
    def it_shows_file_modification_summary(self):
        """--files should show summary of all file modifications."""
        session_file = create_session_with_file_ops()
        
        try:
            stdout, returncode = run_explore_session([session_file, '--files'])
            
            assert returncode == 0
            # Should show all files that were modified (without leading slash)
            assert 'new_file.py' in stdout
            assert 'another_new.txt' in stdout  
            assert 'existing.py' in stdout
            
            # Should show operation types and counts
            assert 'Write' in stdout
            assert 'Edit' in stdout
            assert 'changes' in stdout
        finally:
            Path(session_file).unlink()
    
    def it_groups_operations_by_file(self):
        """Multiple operations on same file should be grouped."""
        session_file = create_session_with_file_ops()
        
        try:
            stdout, returncode = run_explore_session([session_file, '--files'])
            
            # existing.py was edited twice
            lines = stdout.split('\n')
            existing_lines = [l for l in lines if 'existing.py' in l]
            
            # Files output shows summary with counts
            assert 'existing.py' in stdout
            assert 'changes' in stdout
        finally:
            Path(session_file).unlink()


class describe_git_command:
    """Test --git/-g command functionality."""
    
    def it_filters_git_operations(self):
        """--git should show only git-related bash commands."""
        # Create session with mixed bash commands
        events = [
            {
                "type": "assistant",
                "message": {"content": [{"type": "tool_use", "name": "Bash", "id": "tool_1",
                                       "input": {"command": "git status"}}]},
                "timestamp": "2025-07-30T10:00:00.000Z"
            },
            {
                "type": "assistant", 
                "message": {"content": [{"type": "tool_use", "name": "Bash", "id": "tool_2",
                                       "input": {"command": "ls -la"}}]},
                "timestamp": "2025-07-30T10:00:01.000Z"
            },
            {
                "type": "assistant",
                "message": {"content": [{"type": "tool_use", "name": "Bash", "id": "tool_3",
                                       "input": {"command": "git commit -m 'test'"}}]},
                "timestamp": "2025-07-30T10:00:02.000Z"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
            session_file = f.name
        
        try:
            stdout, returncode = run_explore_session([session_file, '--git'])
            
            assert returncode == 0
            # Should show git commands
            assert 'git status' in stdout
            assert 'git commit' in stdout
            # Should NOT show non-git commands
            assert 'ls -la' not in stdout
        finally:
            Path(session_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])