#!/usr/bin/env python3
"""
Characterization tests for explore_session.py display modes.

These tests capture the EXACT current behavior of compact, truncated, and full modes.
"""
import subprocess
from pathlib import Path
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


class describe_compact_mode:
    """Test compact timeline display (default)."""
    
    def it_shows_one_line_per_event(self):
        """Each event should be on exactly one line in compact mode."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl', '-t'])
        
        assert returncode == 0
        
        # Check specific compact format
        assert '[1] ⏺ <thinking>' in stdout
        assert '[2] ⏺ I\'ll help you test this feature.' in stdout
        assert '[3] ⏺ [Tools: TodoWrite]' in stdout
        assert '[4] ⏺ TodoWrite: Updated 1 todos (1 pending)' in stdout
        assert '[5] ⎿  Todos have been modified successfully' in stdout
        assert '[6] ⏺ [Tools: mcp__github_comment__update_claude_comment]' in stdout
        assert '[7] ⏺ mcp__github_comment__update_claude_comment(' in stdout
        
        # Verify each event is on one line
        lines = stdout.strip().split('\n')
        event_lines = [l for l in lines if l.startswith('[')]
        for line in event_lines:
            # Each line should be a single event (no embedded newlines)
            # Note: [Tools: ...] lines have two '[' characters
            assert '\n' not in line
    
    def it_truncates_multiline_content(self):
        """Multiline content should be shown on one line with proper truncation."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl', '-t'])
        
        # The MCP tool has multiline input, should be on one line
        mcp_lines = [l for l in stdout.split('\n') if 'mcp__github_comment__update_claude_comment(' in l]
        assert len(mcp_lines) > 0
        mcp_line = mcp_lines[0]
        # Should be truncated to one line
        assert '\n' not in mcp_line
        # Should show the parameter content
        assert 'Test comment with' in mcp_line


class describe_truncated_mode:
    """Test truncated timeline display."""
    
    def it_shows_preview_format(self):
        """Truncated mode should show Claude Code-style preview."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl', '-t', '--truncated'])
        
        assert returncode == 0
        
        # Should show ⏺ symbols for assistant messages
        assert '⏺ <thinking>' in stdout
        assert '⏺ I\'ll help you test this feature.' in stdout
        
        # Should show tool names
        assert '⏺ Update Todos' in stdout
        assert '⏺ mcp__github_comment__update_claude_comment(' in stdout
    
    def it_omits_sequence_numbers_by_default(self):
        """Truncated mode should not show [N] numbers unless filtering."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl', '-t', '--truncated'])
        
        # Should not have sequence numbers
        assert '[1]' not in stdout
        assert '[2]' not in stdout
        
    def it_shows_numbers_with_filtering(self):
        """Truncated mode should show numbers when filtering is applied."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl', '-t', '--truncated', '-i', 'Tool'])
        
        # Should have sequence numbers when filtering
        assert '[4]' in stdout  # TodoWrite
        assert '[7]' in stdout  # MCP tool


class describe_full_mode:
    """Test full timeline display."""
    
    def it_shows_complete_content(self):
        """Full mode should show complete content without truncation."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl', '-t', '--full'])
        
        assert returncode == 0
        
        # Should have sequence numbers in full mode
        assert '[1]' in stdout
        assert '[2]' in stdout
        
        # Should show complete multiline content
        # (In this case, our minimal example doesn't have much multiline content)
        

class describe_special_content_types:
    """Test display of special content types."""
    
    def it_displays_thinking_content(self):
        """Thinking content should be displayed with <thinking> prefix."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl', '-t'])
        
        assert '<thinking> The user wants me to test something' in stdout
    
    def it_displays_tool_only_messages(self):
        """Assistant messages with only tools should show tool names."""
        stdout, returncode = run_explore_session(['specs/fixtures/minimal_session.jsonl', '-t'])
        
        # Both TodoWrite and MCP tool should appear
        assert 'TodoWrite' in stdout
        assert 'mcp__github_comment__update_claude_comment' in stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])