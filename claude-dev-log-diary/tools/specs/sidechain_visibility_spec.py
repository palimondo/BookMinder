#!/usr/bin/env python3
"""
Characterization test for sidechain event visibility.

Tests whether xs properly handles or filters sidechain events from Task sub-agents.
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


def create_session_with_sidechain():
    """Create a session with Task invocation and sidechain events."""
    events = [
        # Main session Task invocation
        {
            "type": "assistant",
            "isSidechain": False,
            "message": {
                "content": [{
                    "type": "tool_use",
                    "name": "Task",
                    "id": "task_123",
                    "input": {
                        "description": "Test task",
                        "prompt": "Do something"
                    }
                }]
            },
            "timestamp": "2025-01-01T10:00:00Z"
        },
        # Sidechain event - sub-agent receives prompt
        {
            "type": "user",
            "isSidechain": True,
            "message": {
                "role": "user",
                "content": "Do something"
            },
            "timestamp": "2025-01-01T10:00:01Z"
        },
        # Sidechain event - sub-agent responds
        {
            "type": "assistant",
            "isSidechain": True,
            "message": {
                "content": [{
                    "type": "text",
                    "text": "I'll do something for you"
                }]
            },
            "timestamp": "2025-01-01T10:00:02Z"
        },
        # Sidechain event - sub-agent uses tool
        {
            "type": "assistant",
            "isSidechain": True,
            "message": {
                "content": [{
                    "type": "tool_use",
                    "name": "Bash",
                    "id": "bash_123",
                    "input": {"command": "find . -name '*.txt'"}
                }]
            },
            "timestamp": "2025-01-01T10:00:03Z"
        },
        # Main session - Task result
        {
            "type": "user",
            "isSidechain": False,
            "message": {
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": "task_123",
                    "content": "Task completed successfully"
                }]
            },
            "timestamp": "2025-01-01T10:00:04Z"
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


class describe_sidechain_visibility:
    """Test how xs handles sidechain events from Task sub-agents."""
    
    def it_currently_shows_sidechain_events(self):
        """CURRENT BEHAVIOR: xs shows sidechain events as regular events."""
        session_file = create_session_with_sidechain()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t'])
            
            assert returncode == 0
            
            # Current behavior: sidechain events are visible
            assert "Do something" in stdout  # Sidechain user message
            assert "I'll do something for you" in stdout  # Sidechain assistant response
            assert "find . -name '*.txt'" in stdout  # Sidechain tool use
            
            # Count total events
            lines = [l for l in stdout.split('\n') if l.strip() and l.startswith('[')]
            # xs expands events: Task invocation (2 lines) + 3 sidechain + 1 result + 1 continuation
            assert len(lines) == 7
            
        finally:
            Path(session_file).unlink()
    
    def it_shows_sidechain_in_summary(self):
        """Summary should reflect sidechain events in counts."""
        session_file = create_session_with_sidechain()
        
        try:
            stdout, returncode = run_explore_session([session_file])
            
            assert returncode == 0
            
            # xs uses different format for summary
            assert "Assistant: 3" in stdout  # Counts all assistant messages including sidechain
            
            # Should count sidechain tools
            assert "Bash:" in stdout
            
        finally:
            Path(session_file).unlink()
    
    def it_includes_sidechain_in_search(self):
        """Search should find content in sidechain events."""
        session_file = create_session_with_sidechain()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-S', 'find'])
            
            assert returncode == 0
            
            # Should find the sidechain Bash command
            assert "Found 1 match" in stdout
            assert "find . -name" in stdout
            
        finally:
            Path(session_file).unlink()


class describe_potential_sidechain_filtering:
    """Test what would happen if we filtered sidechain events."""
    
    @pytest.mark.skip("Feature not implemented - shows desired behavior")
    def it_could_filter_sidechain_events(self):
        """POTENTIAL: xs could filter out sidechain events."""
        session_file = create_session_with_sidechain()
        
        try:
            # Hypothetical flag to exclude sidechain
            stdout, returncode = run_explore_session([session_file, '-t', '--no-sidechain'])
            
            assert returncode == 0
            
            # Would only show main session events
            assert "Do something" not in stdout  # No sidechain content
            assert "Task completed successfully" in stdout  # Main session result
            
            # Would show only 2 events (Task invocation + result)
            lines = [l for l in stdout.split('\n') if l.strip() and l.startswith('[')]
            assert len(lines) == 2
            
        finally:
            Path(session_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])