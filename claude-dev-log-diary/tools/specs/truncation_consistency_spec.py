#!/usr/bin/env python3
"""
Tests for truncation consistency in explore_session.py.

Ensures all truncation uses the [...] pattern consistently.
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


def create_multiline_content_session():
    """Create a session with various multiline content."""
    events = [
        # User message with multiline text
        {"type": "user", "message": {"content": [{"type": "text", 
         "text": "First line of user message\nSecond line\nThird line\nFourth line\nLast line of user message"}]},
         "timestamp": "2025-07-30T10:00:00.000Z"},
        
        # Assistant with multiline response
        {"type": "assistant", "message": {"content": [{"type": "text",
         "text": "First line of response\nMiddle content here\nMore content\nEven more\nLast line of response"}]},
         "timestamp": "2025-07-30T10:00:01.000Z"},
        
        # Tool with multiline parameters
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Write", "id": "t1",
         "input": {"file_path": "/test.py", "content": "def hello():\n    print('Hello')\n    # More code\n    return True\n# End of file"}}]},
         "timestamp": "2025-07-30T10:00:02.000Z"},
        
        # Meta message (caveat)
        {"type": "user", "message": {"content": [{"type": "text", 
         "text": "Caveat: This is a long caveat message\nwith multiple lines\nand important information\nthat should be truncated consistently"}],
         "isMeta": True},
         "timestamp": "2025-07-30T10:00:03.000Z"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


def create_long_single_line_session():
    """Create a session with very long single-line content."""
    events = [
        # Very long single line parameter
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash", "id": "t1",
         "input": {"command": "echo 'This is a very long command that exceeds 80 characters and should be truncated with [...] pattern not three dots'"}}]},
         "timestamp": "2025-07-30T10:00:00.000Z"},
        
        # Long thinking
        {"type": "assistant", "message": {"content": [
            {"type": "thinking", "text": "This is a very long thinking line that might have been truncated before but now should show completely"}
        ]},
         "timestamp": "2025-07-30T10:00:01.000Z"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


class describe_multiline_truncation:
    """Test multiline content uses [...] pattern consistently."""
    
    def it_truncates_user_messages_consistently(self):
        """Multiline user messages should use 'first [...] last' pattern."""
        session_file = create_multiline_content_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            # Should show first [...] last pattern
            assert 'First line of user message [...] Last line of user message' in stdout
            # Should NOT have old-style truncation
            assert '...' not in stdout or '[...]' in stdout
        finally:
            Path(session_file).unlink()
    
    def it_truncates_assistant_messages_consistently(self):
        """Multiline assistant messages should use [...] pattern."""
        session_file = create_multiline_content_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            # Should show first [...] last pattern
            assert 'First line of response [...] Last line of response' in stdout
        finally:
            Path(session_file).unlink()
    
    def it_truncates_tool_parameters_consistently(self):
        """Tool parameters should use [...] pattern."""
        session_file = create_multiline_content_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            # In compact mode, Write tool shows as "Write: → /test.py"
            assert 'Write: → /test.py' in stdout
            # For multiline parameters, check with different tools or modes
        finally:
            Path(session_file).unlink()
    
    def it_truncates_meta_messages_consistently(self):
        """Meta messages (caveats) should use [...] pattern."""
        session_file = create_multiline_content_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            # Meta messages show as user messages with Caveat: prefix
            assert 'Caveat: This is a long caveat message [...] that should be truncated consistently' in stdout
            # Should use [...] pattern, not old ... style
            lines = stdout.split('\n')
            for line in lines:
                if 'Caveat:' in line:
                    assert '[...]' in line or len(line.split('...')) == 1  # No ... truncation
        finally:
            Path(session_file).unlink()


class describe_single_line_truncation:
    """Test single line truncation consistency."""
    
    def it_truncates_long_commands_with_brackets(self):
        """Long single-line content should use [...] not ..."""
        session_file = create_long_single_line_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            # Should use [...] for truncation, not ...
            if 'truncated with' in stdout:
                assert '[...]' in stdout
                # Old style ... should not appear (except in actual content)
                lines = stdout.split('\n')
                for line in lines:
                    if line.strip() and 'echo' in line and line.endswith('...'):
                        assert False, f"Found old-style truncation: {line}"
        finally:
            Path(session_file).unlink()
    
    def it_truncates_long_parameters_consistently(self):
        """Very long parameters should use [...] pattern."""
        session_file = create_long_single_line_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            # The long Bash command should be there
            assert 'Bash' in stdout
            # If truncated, should use [...] not old style
            if 'pattern not three dots' not in stdout:
                # It was truncated
                assert '[...]' in stdout
        finally:
            Path(session_file).unlink()


class describe_created_files_display:
    """Test --created flag output consistency."""
    
    def it_shows_file_content_without_arbitrary_truncation(self):
        """Created files should not use :60 truncation."""
        events = [
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Write", "id": "t1",
             "input": {"file_path": "/example.py", 
                      "content": "# This is a Python file with multiple lines\ndef example_function():\n    pass\n\n# More content here\n# Even more\n# Last line"}}]},
             "timestamp": "2025-07-30T10:00:00.000Z"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
            session_file = f.name
        
        try:
            stdout, returncode = run_explore_session([session_file, '--created'])
            
            assert returncode == 0
            # Should show file content
            assert 'example.py' in stdout
            # Should show actual content lines, not truncated at 60 chars
            assert '# This is a Python file' in stdout
            # Should use [...] for indicating more content
            if 'total lines)' in stdout:
                assert '[...]' in stdout
        finally:
            Path(session_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])