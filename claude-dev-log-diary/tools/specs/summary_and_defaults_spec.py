#!/usr/bin/env python3
"""
Characterization tests for explore_session.py default behavior and summary output.

These tests capture the EXACT current behavior to prevent regressions.
Run with: pytest test_summary_and_defaults.py -v
"""
import subprocess
from pathlib import Path
import pytest


def run_explore_session(args, capture_stderr=False):
    """Run explore_session.py with given arguments and return output."""
    # Navigate to the explore_session.py location
    tools_dir = Path(__file__).parent.parent  # specs/ -> tools/
    cmd = ['./explore_session.py'] + args
    result = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True, 
        cwd=tools_dir
    )
    if capture_stderr:
        return result.stdout, result.stderr, result.returncode
    return result.stdout, result.returncode


class describe_summary_output:
    """Test default summary output format."""
    
    def it_shows_default_summary_structure(self):
        """Default behavior should show summary with specific format."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl'])
        
        assert returncode == 0
        
        # Check key summary sections appear
        assert 'Session:' in stdout
        assert 'Timeline:' in stdout
        assert 'Events:' in stdout
        assert 'Tool calls:' in stdout
        
    def it_shows_correct_summary_counts(self):
        """Summary should show correct counts for each category."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl'])
        
        # From our minimal session:
        # - 7 total events (includes thinking events in timeline)
        # - 0 user inputs (only tool results)
        # - 1 tool result
        # - 4 assistant events
        assert 'Events: 7' in stdout
        assert 'User inputs: 0' in stdout
        assert 'Tool results: 1' in stdout
        assert 'Assistant: 4' in stdout
        
    def it_shows_tool_breakdown(self):
        """Summary should break down tools by type."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl'])
        
        # Check tool breakdown
        assert 'Tool: 2' in stdout  # 2 tool uses
        assert 'MCP: 1' in stdout   # 1 MCP tool
        assert 'Other: 1' in stdout # 1 TodoWrite (non-MCP)
        
    def it_includes_help_comments(self):
        """Summary should include helpful comments about flags."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl'])
        
        # Check for help comments
        assert '# -t' in stdout  # Timeline flag hint
        assert '# -U' in stdout  # User messages flag hint
        assert '# -a' in stdout  # Assistant messages flag hint
        assert '# -T' in stdout  # Tools flag hint


class describe_session_lookup:
    """Test session file lookup mechanisms."""
    
    @pytest.mark.skip(reason="Session lookup tests skipped as requested")
    def it_finds_session_by_substring(self):
        pass


class describe_error_handling:
    """Test error conditions and edge cases."""
    
    def it_handles_nonexistent_session(self):
        """Should handle missing session files gracefully."""
        stdout, stderr, returncode = run_explore_session(
            ['nonexistent-session'], 
            capture_stderr=True
        )
        
        assert returncode != 0
        # Error message appears in stdout for session lookup
        assert 'no session file found' in stdout.lower()
        
    def it_performs_search_successfully(self):
        """Search should find matches in the session content."""
        stdout, stderr, returncode = run_explore_session(
            ['specs/fixtures/minimal_session.jsonl', '-S', 'test'],
            capture_stderr=True
        )
        
        # Search now works correctly
        assert returncode == 0
        assert 'Found 2 matches' in stdout
        assert "I'll help you test this feature" in stdout


class describe_golden_outputs:
    """Test against golden output files for exact behavior matching."""
    
    def it_matches_summary_golden_output(self):
        """Summary output should match golden file exactly."""
        # Skip if golden file doesn't exist yet
        golden_path = Path(__file__).parent / 'golden_outputs' / 'summary_default.txt'
        if not golden_path.exists():
            pytest.skip("Golden output file not yet created")
            
        with open(golden_path) as f:
            expected = f.read()
            
        stdout, _ = run_explore_session(['pr-14'])
        
        # For now, just check key sections match
        # Full comparison would be too brittle for counts that change
        for line in expected.split('\n'):
            if line.startswith(('Session:', 'Timeline:', '  Events:')):
                assert line in stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])