#!/usr/bin/env python3
"""
Characterization test for broken pipe error handling.

Documents proper handling of SIGPIPE when output is piped to head/tail.
"""
import subprocess
from pathlib import Path
import tempfile
import json
import pytest
import signal
import sys


def create_large_session():
    """Create a session with many events to trigger broken pipe."""
    events = []
    for i in range(100):
        events.append({
            "type": "assistant",
            "message": {"content": [{"type": "text", "text": f"Message {i+1} with some content to make it longer"}]},
            "timestamp": f"2025-07-30T10:{i:02d}:00.000Z"
        })
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


class describe_broken_pipe_handling:
    """Test broken pipe error handling when piping to head."""
    
    def it_should_handle_sigpipe_gracefully(self):
        """Should exit silently when receiving SIGPIPE."""
        session_file = create_large_session()
        
        try:
            # Run explore_session piped to head
            tools_dir = Path(__file__).parent.parent
            cmd = f"cd {tools_dir} && ./explore_session.py {session_file} -t | head -5"
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True
            )
            
            # Should not show BrokenPipeError in stderr
            assert 'BrokenPipeError' not in result.stderr
            assert 'Exception ignored' not in result.stderr
            
            # Should have some output
            assert result.stdout.strip() != ''
            
            # Should have exactly 5 lines (what head requested)
            lines = result.stdout.strip().split('\n')
            assert len(lines) == 5
            
        finally:
            Path(session_file).unlink()
    
    def it_should_exit_cleanly_with_tail(self):
        """Should also work correctly with tail."""
        session_file = create_large_session()
        
        try:
            tools_dir = Path(__file__).parent.parent
            cmd = f"cd {tools_dir} && ./explore_session.py {session_file} -t | tail -5"
            
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True
            )
            
            # Should not show errors
            assert 'BrokenPipeError' not in result.stderr
            assert 'Exception ignored' not in result.stderr
            
            # Should have exactly 5 lines
            lines = result.stdout.strip().split('\n')
            assert len(lines) == 5
            
        finally:
            Path(session_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])