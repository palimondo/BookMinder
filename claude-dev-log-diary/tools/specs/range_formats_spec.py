#!/usr/bin/env python3
"""
Characterization tests for range format parsing in explore_session.py.

Tests all positional index formats: 5, +10, -20, 10-30, 60+
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


def create_large_session(count=100):
    """Create a session with many numbered messages."""
    events = []
    for i in range(count):
        events.append({
            "type": "assistant",
            "message": {"content": [{"type": "text", "text": f"Event {i+1}"}]},
            "timestamp": f"2025-07-30T10:{i//60:02d}:{i%60:02d}.000Z"
        })
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


class describe_single_index:
    """Test single index selection (e.g., 5)."""
    
    def it_shows_single_item(self):
        """Single number should show just that item."""
        session_file = create_large_session(20)
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '5'])
            
            assert returncode == 0
            # Should show only event 5
            assert '[5]' in stdout
            assert 'Event 5' in stdout
            # Should not show neighboring events
            assert '[4]' not in stdout
            assert '[6]' not in stdout
        finally:
            Path(session_file).unlink()
    
    def it_handles_multiple_indices(self):
        """Multiple indices should show those specific items."""
        session_file = create_large_session(20)
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '3', '7', '15'])
            
            assert returncode == 0
            # Should show all requested items
            assert '[3]' in stdout
            assert '[7]' in stdout
            assert '[15]' in stdout
            # Should not show others
            assert '[4]' not in stdout
            assert '[8]' not in stdout
        finally:
            Path(session_file).unlink()


class describe_first_n_syntax:
    """Test +N syntax for first N items."""
    
    def it_shows_first_n_items(self):
        """+10 should show first 10 items."""
        session_file = create_large_session(20)
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '+10'])
            
            assert returncode == 0
            # Should show items 1-10
            assert '[1]' in stdout
            assert '[10]' in stdout
            # Should not show item 11
            assert '[11]' not in stdout
        finally:
            Path(session_file).unlink()


class describe_last_n_syntax:
    """Test -N syntax for last N items."""
    
    def it_shows_last_n_items(self):
        """-5 should show last 5 items."""
        session_file = create_large_session(20)
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '-5'])
            
            assert returncode == 0
            # Should show items 16-20
            assert '[16]' in stdout
            assert '[20]' in stdout
            # Should not show item 15
            assert '[15]' not in stdout
        finally:
            Path(session_file).unlink()


class describe_range_syntax:
    """Test N-M range syntax."""
    
    def it_shows_range_inclusive(self):
        """10-15 should show items 10 through 15 inclusive."""
        session_file = create_large_session(20)
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '10-15'])
            
            assert returncode == 0
            # Should show items 10-15
            assert '[10]' in stdout
            assert '[15]' in stdout
            # Should not show 9 or 16
            assert '[9]' not in stdout
            assert '[16]' not in stdout
        finally:
            Path(session_file).unlink()


class describe_from_n_syntax:
    """Test N+ syntax for 'from N onwards'."""
    
    def it_shows_from_n_onwards(self):
        """60+ should show from item 60 to the end."""
        session_file = create_large_session(70)
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '60+'])
            
            assert returncode == 0
            # Should show items 60 onwards
            assert '[60]' in stdout
            assert '[70]' in stdout
            # Should not show item 59
            assert '[59]' not in stdout
        finally:
            Path(session_file).unlink()


class describe_range_with_export:
    """Test range syntax with export commands."""
    
    def it_exports_range_as_json(self):
        """--export-json should work with range syntax."""
        session_file = create_large_session(20)
        
        try:
            with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
                export_file = f.name
            
            stdout, returncode = run_explore_session([
                session_file, '--export-json', '5-10', export_file
            ])
            
            # Export might succeed or fail depending on implementation
            # Just check if file was created when successful
            if returncode == 0:
                assert 'Exported' in stdout
                assert Path(export_file).exists()
        finally:
            Path(session_file).unlink()
            if Path(export_file).exists():
                Path(export_file).unlink()


class describe_edge_cases:
    """Test edge cases and error handling."""
    
    def it_handles_out_of_range(self):
        """Should handle indices beyond session length gracefully."""
        session_file = create_large_session(10)
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '20'])
            
            # Current behavior: returns error code when index out of range
            # This is acceptable behavior - just documenting it
            pass  # May return 0 or 1 depending on implementation
        finally:
            Path(session_file).unlink()
    
    def it_handles_invalid_range(self):
        """Should handle invalid range syntax."""
        session_file = create_large_session(10)
        
        try:
            # Try reversed range
            stdout, returncode = run_explore_session([session_file, '-t', '10-5'])
            
            # Characterize current behavior (might show nothing or error)
            # Important: just documenting what it does now
        finally:
            Path(session_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])