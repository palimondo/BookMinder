import pytest
from unittest.mock import Mock, patch
import json
from io import StringIO

import sys
sys.path.insert(0, '/Users/palimondo/Developer/BookMinder/claude-dev-log-diary/tools')
from explore_session import SessionExplorer


@pytest.fixture
def mock_session_data():
    """Create test session data with various message types"""
    return {
        "messages": [
            # User message
            {
                "seq": 1,
                "type": "user",
                "timestamp": "2025-01-01T10:00:00Z",
                "message": "Test user message"
            },
            # Thinking block
            {
                "seq": 2,
                "type": "assistant",
                "timestamp": "2025-01-01T10:00:01Z",
                "message": {
                    "content": [
                        {
                            "type": "thinking",
                            "text": "This is a thinking block\nwith multiple lines"
                        }
                    ]
                }
            },
            # Slash command
            {
                "seq": 3,
                "type": "user",
                "timestamp": "2025-01-01T10:00:02Z",
                "message": "//voice: voice is running…"
            },
            # Tool allowance message (after slash command)
            {
                "seq": 4,
                "type": "assistant",
                "timestamp": "2025-01-01T10:00:03Z",
                "message": {
                    "content": [
                        {"type": "text", "text": "Allowed 1 tools for this command"}
                    ]
                }
            },
            # Local bash command
            {
                "seq": 5,
                "type": "user",
                "timestamp": "2025-01-01T10:00:04Z",
                "message": "<bash-input>./explore_session.py test</bash-input>"
            },
            # Bash output
            {
                "seq": 6,
                "type": "user",
                "timestamp": "2025-01-01T10:00:05Z",
                "message": "<bash-stderr>Error: file not found</bash-stderr>"
            },
            # File reference with @
            {
                "seq": 7,
                "type": "user",
                "timestamp": "2025-01-01T10:00:06Z",
                "message": "@file.txt"
            },
            # Tool use for file read
            {
                "seq": 8,
                "type": "tool",
                "timestamp": "2025-01-01T10:00:07Z",
                "tool": {
                    "name": "Read",
                    "parameters": {"file_path": "file.txt"}
                }
            }
        ],
        "tools": {
            8: {
                "seq": 8,
                "result": "File contents here"
            }
        }
    }


class describe_thinking_block_formatting:
    @pytest.fixture
    def explorer(self, mock_session_data):
        explorer = SessionExplorer("test.jsonl")
        explorer.messages = mock_session_data["messages"]
        explorer.tools = mock_session_data["tools"]
        explorer._build_timeline()
        return explorer

    def it_should_display_thinking_with_star_symbol_in_truncated_mode(self, explorer, capsys):
        """✻ Thinking… should be displayed with star symbol, not ⏺ <thinking>"""
        explorer.show_timeline_with_filters(display_mode='truncated', indices=[2])
        captured = capsys.readouterr()
        assert "✻ Thinking…" in captured.out
        assert "⏺ <thinking>" not in captured.out

    def it_should_display_thinking_with_star_symbol_in_full_mode(self, explorer, capsys):
        """Full mode should show ✻ Thinking… followed by indented content"""
        explorer.show_timeline_with_filters(display_mode='full', indices=[2])
        captured = capsys.readouterr()
        assert "✻ Thinking…" in captured.out
        assert "  This is a thinking block" in captured.out
        assert "  with multiple lines" in captured.out

    def it_should_display_thinking_compactly_in_compact_mode(self, explorer, capsys):
        """Compact mode should show thinking on one line"""
        explorer.show_timeline_with_filters(display_mode='compact', indices=[2])
        captured = capsys.readouterr()
        assert "[2] ✻" in captured.out or "[2] ⏺ <thinking>" in captured.out


class describe_slash_command_formatting:
    @pytest.fixture
    def explorer(self, mock_session_data):
        explorer = SessionExplorer("test.jsonl")
        explorer.messages = mock_session_data["messages"]
        explorer.tools = mock_session_data["tools"]
        explorer._build_timeline()
        return explorer

    def it_should_display_single_slash_without_colon(self, explorer, capsys):
        """Slash commands should use single / and no colon"""
        explorer.show_timeline_with_filters(display_mode='truncated', indices=[3])
        captured = capsys.readouterr()
        assert "> /voice is running…" in captured.out
        assert "//voice:" not in captured.out

    def it_should_show_tool_allowance_message(self, explorer, capsys):
        """Tool allowance messages should appear after slash commands"""
        explorer.show_timeline_with_filters(display_mode='truncated', indices=[3, 4])
        captured = capsys.readouterr()
        assert "Allowed 1 tools for this command" in captured.out


class describe_local_bash_command_formatting:
    @pytest.fixture
    def explorer(self, mock_session_data):
        explorer = SessionExplorer("test.jsonl")
        explorer.messages = mock_session_data["messages"]
        explorer.tools = mock_session_data["tools"]
        explorer._build_timeline()
        return explorer

    def it_should_use_exclamation_prefix_for_local_bash(self, explorer, capsys):
        """Local bash commands should use ! prefix"""
        explorer.show_timeline_with_filters(display_mode='truncated', indices=[5, 6])
        captured = capsys.readouterr()
        assert "! ./explore_session.py test" in captured.out
        assert "<bash-input>" not in captured.out

    def it_should_indent_bash_output_properly(self, explorer, capsys):
        """Bash output should be indented under the command"""
        explorer.show_timeline_with_filters(display_mode='truncated', indices=[5, 6])
        captured = capsys.readouterr()
        assert "⎿  Error: file not found" in captured.out or "  ⎿  Error: file not found" in captured.out


class describe_file_reference_formatting:
    @pytest.fixture  
    def explorer(self, mock_session_data):
        explorer = SessionExplorer("test.jsonl")
        explorer.messages = mock_session_data["messages"]
        explorer.tools = mock_session_data["tools"]
        explorer._build_timeline()
        return explorer

    def it_should_handle_at_prefix_file_references(self, explorer, capsys):
        """@ prefix file references should be recognized"""
        explorer.show_timeline_with_filters(display_mode='truncated', indices=[7, 8])
        captured = capsys.readouterr()
        assert "> @file.txt" in captured.out
        assert "Read file.txt" in captured.out or "Read: file.txt" in captured.out


class describe_compact_mode_design_decisions:
    """Design questions for compact mode formatting"""
    
    @pytest.mark.skip(reason="Design decision needed")
    def it_should_show_thinking_blocks_compactly(self):
        """How should thinking blocks appear in compact mode?
        Options:
        1. [N] ✻ Thinking…
        2. [N] ✻ <thinking>
        3. [N] ⏺ <thinking> (current)
        """
        pass

    @pytest.mark.skip(reason="Design decision needed")
    def it_should_handle_slash_command_status(self):
        """Should 'is running...' status be shown in compact mode?
        Options:
        1. [N] > /voice is running…
        2. [N] > /voice
        3. [N] > /voice (running)
        """
        pass

    @pytest.mark.skip(reason="Design decision needed")
    def it_should_show_tool_allowance_compactly(self):
        """How to show tool allowance in compact mode?
        Options:
        1. Not shown (current)
        2. [N] > /voice is running… (+1 tool)
        3. [N] > /voice is running… | Allowed 1 tool
        """
        pass