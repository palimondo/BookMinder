#!/usr/bin/env python3
"""
Characterization tests for context line options in explore_session.py.

Tests -A/--after-context, -B/--before-context, -C/--context functionality.
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


def create_numbered_session():
    """Create a session with numbered messages for easy context testing."""
    events = []
    for i in range(10):
        events.append({
            "type": "assistant",
            "message": {"content": [{"type": "text", "text": f"Message {i+1}"}]},
            "timestamp": f"2025-07-30T10:00:{i:02d}.000Z"
        })
    
    # Add a specific tool use in the middle
    events[5] = {
        "type": "assistant",
        "message": {"content": [{"type": "tool_use", "name": "Read", "id": "tool_123",
                               "input": {"file_path": "/target.py"}}]},
        "timestamp": "2025-07-30T10:00:05.000Z"
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


class describe_after_context:
    """Test -A/--after-context functionality."""
    
    def it_shows_lines_after_match(self):
        """Should show N lines after each match."""
        session_file = create_numbered_session()
        
        try:
            # Search for the Read tool and show 2 lines after
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Read', '-A', '2'])
            
            assert returncode == 0
            # Should show the Read tool (item 6)
            assert 'Read(/target.py)' in stdout
            # Should show 2 lines after (items 7 and 8)
            assert 'Message 7' in stdout
            assert 'Message 8' in stdout
            # Should NOT show item 9
            assert 'Message 9' not in stdout
        finally:
            Path(session_file).unlink()
    
    def it_works_with_long_form(self):
        """--after-context should work same as -A."""
        session_file = create_numbered_session()
        
        try:
            stdout_short, _ = run_explore_session([session_file, '-t', '-i', 'Read', '-A', '2'])
            stdout_long, _ = run_explore_session([session_file, '-t', '-i', 'Read', '--after-context', '2'])
            
            assert stdout_short == stdout_long
        finally:
            Path(session_file).unlink()


class describe_before_context:
    """Test -B/--before-context functionality."""
    
    def it_shows_lines_before_match(self):
        """Should show N lines before each match."""
        session_file = create_numbered_session()
        
        try:
            # Search for the Read tool and show 2 lines before
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Read', '-B', '2'])
            
            assert returncode == 0
            # The Read tool appears as items 6-7, so -B 2 shows item 5
            assert 'Message 5' in stdout
            # Should show the Read tool
            assert 'Read(/target.py)' in stdout
            # Should NOT show item 4
            assert 'Message 4' not in stdout
        finally:
            Path(session_file).unlink()


class describe_context:
    """Test -C/--context functionality."""
    
    def it_shows_lines_before_and_after(self):
        """Should show N lines both before and after match."""
        session_file = create_numbered_session()
        
        try:
            # Search for the Read tool and show 1 line of context
            stdout, returncode = run_explore_session([session_file, '-t', '-i', 'Read', '-C', '1'])
            
            assert returncode == 0
            # Context shows around the matched Read tool events
            assert 'Read(/target.py)' in stdout
            assert 'Message 7' in stdout  # After context
            # The tool announcement [Tools: Read] is also shown
            assert '[Tools: Read]' in stdout
        finally:
            Path(session_file).unlink()


class describe_context_with_search:
    """Test context options with search functionality."""
    
    def it_shows_context_around_search_matches(self):
        """Context should work with -S/--search."""
        session_file = create_numbered_session()
        
        try:
            # Search for "Message 5" and show context
            stdout, returncode = run_explore_session([session_file, '-S', 'Message 5', '-C', '1'])
            
            assert returncode == 0
            assert 'Found' in stdout  # Should show match count
            # Should show context around Message 5
            assert 'Message 4' in stdout
            assert 'Message 5' in stdout
            # Next item is the tool announcement
            assert '[Tools: Read]' in stdout
        finally:
            Path(session_file).unlink()


class describe_visual_gaps:
    """Test visual gaps between non-contiguous items."""
    
    def it_shows_gaps_in_timeline(self):
        """Should show visual gaps when sequence numbers are not contiguous."""
        session_file = create_numbered_session()
        
        try:
            # Show only items 2, 5, and 8 (non-contiguous)
            stdout, returncode = run_explore_session([session_file, '-t', '2', '5', '8'])
            
            assert returncode == 0
            
            lines = stdout.strip().split('\n')
            # Should have empty lines between non-contiguous items
            # Find positions of our items
            item2_idx = next(i for i, l in enumerate(lines) if '[2]' in l)
            item5_idx = next(i for i, l in enumerate(lines) if '[5]' in l)
            item8_idx = next(i for i, l in enumerate(lines) if '[8]' in l)
            
            # Should have gap (empty line) between 2 and 5
            assert lines[item2_idx + 1] == '' or item5_idx > item2_idx + 1
            # Should have gap between 5 and 8
            assert lines[item5_idx + 1] == '' or item8_idx > item5_idx + 1
        finally:
            Path(session_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])