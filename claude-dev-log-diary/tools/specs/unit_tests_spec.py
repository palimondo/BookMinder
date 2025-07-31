#!/usr/bin/env python3
"""
Unit tests for JSONL parsing and timeline building in explore_session.py.

These tests isolate specific functions and components for focused testing.
"""
import json
import tempfile
from pathlib import Path
import pytest
from unittest.mock import Mock, patch
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from parse_claude_jsonl import parse_jsonl_objects
from explore_session import parse_range, parse_indices, SessionExplorer


class describe_parse_range_function:
    """Unit tests for parse_range function."""
    
    def it_parses_single_index(self):
        """Single number should return one-item range."""
        start, end = parse_range("5", 100)
        assert start == 4  # 0-based
        assert end == 5
    
    def it_parses_plus_prefix(self):
        """'+N' should return first N items."""
        start, end = parse_range("+10", 100)
        assert start == 0
        assert end == 10
    
    def it_parses_minus_prefix(self):
        """-N should return last N items."""
        start, end = parse_range("-5", 100)
        assert start == 95
        assert end == 100
    
    def it_parses_range_with_both_bounds(self):
        """'N-M' should return range from N to M."""
        start, end = parse_range("10-20", 100)
        assert start == 9  # 0-based
        assert end == 20
    
    def it_parses_open_ended_range(self):
        """'N-' and 'N+' should return from N to end."""
        # Test N-
        start, end = parse_range("50-", 100)
        assert start == 49
        assert end == 100
        
        # Test N+
        start, end = parse_range("50+", 100)
        assert start == 49
        assert end == 100
    
    def it_handles_out_of_bounds_gracefully(self):
        """Out of bounds indices should be clamped."""
        # Single index too large
        with pytest.raises(ValueError):
            parse_range("101", 100)
        
        # Range end too large - should clamp
        start, end = parse_range("90-200", 100)
        assert start == 89
        assert end == 100
        
        # Negative range larger than total
        start, end = parse_range("-200", 100)
        assert start == 0
        assert end == 100


class describe_parse_indices_function:
    """Unit tests for parse_indices function."""
    
    def it_parses_multiple_ranges(self):
        """Should combine multiple range arguments."""
        indices = parse_indices(["5", "10-12", "+3"], 100)
        assert indices == [0, 1, 2, 4, 9, 10, 11]  # 0-based, sorted, unique
    
    def it_removes_duplicates(self):
        """Overlapping ranges should not produce duplicates."""
        indices = parse_indices(["1-5", "3-7"], 100)
        assert indices == [0, 1, 2, 3, 4, 5, 6]  # No duplicates
    
    def it_returns_empty_for_no_args(self):
        """Empty args should return empty list."""
        indices = parse_indices([], 100)
        assert indices == []


class describe_parse_jsonl_objects_function:
    """Unit tests for parse_jsonl_objects parser."""
    
    def it_parses_single_line_json(self):
        """Should parse simple single-line JSON objects."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            f.write('{"type": "user", "message": "hello"}\n')
            f.write('{"type": "assistant", "message": "hi"}\n')
            temp_file = f.name
        
        try:
            objects = list(parse_jsonl_objects(temp_file))
            assert len(objects) == 2
            assert objects[0]['type'] == 'user'
            assert objects[1]['type'] == 'assistant'
        finally:
            Path(temp_file).unlink()
    
    def it_parses_multiline_json(self):
        """Should parse JSON objects spanning multiple lines."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            f.write('{\n')
            f.write('  "type": "assistant",\n')
            f.write('  "message": {\n')
            f.write('    "content": "hello"\n')
            f.write('  }\n')
            f.write('}\n')
            temp_file = f.name
        
        try:
            objects = list(parse_jsonl_objects(temp_file))
            assert len(objects) == 1
            assert objects[0]['type'] == 'assistant'
            assert objects[0]['message']['content'] == 'hello'
        finally:
            Path(temp_file).unlink()
    
    def it_handles_strings_with_braces(self):
        """Should correctly parse JSON with braces in strings."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            f.write('{"code": "if (x) { return y; }"}\n')
            temp_file = f.name
        
        try:
            objects = list(parse_jsonl_objects(temp_file))
            assert len(objects) == 1
            assert objects[0]['code'] == 'if (x) { return y; }'
        finally:
            Path(temp_file).unlink()
    
    def it_handles_escaped_quotes(self):
        """Should handle escaped quotes in strings."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            f.write('{"text": "He said \\"hello\\""}\n')
            temp_file = f.name
        
        try:
            objects = list(parse_jsonl_objects(temp_file))
            assert len(objects) == 1
            assert objects[0]['text'] == 'He said "hello"'
        finally:
            Path(temp_file).unlink()
    
    def it_handles_malformed_json_gracefully(self):
        """Should skip malformed JSON without crashing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            f.write('{"valid": "json"}\n')
            f.write('{"invalid": json"}\n')  # Missing quote
            f.write('{"also_valid": "json"}\n')
            temp_file = f.name
        
        try:
            objects = list(parse_jsonl_objects(temp_file))
            # Should parse valid objects and skip invalid
            assert len(objects) >= 1  # At least the first valid one
        finally:
            Path(temp_file).unlink()


class describe_session_explorer_parsing:
    """Unit tests for SessionExplorer parsing logic."""
    
    def it_extracts_tool_calls(self):
        """Should extract tool calls from assistant messages."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            event = {
                "type": "assistant",
                "message": {
                    "content": [{
                        "type": "tool_use",
                        "name": "Read",
                        "id": "test_1",
                        "input": {"file_path": "/test.py"}
                    }]
                },
                "timestamp": "2025-07-30T10:00:00.000Z"
            }
            f.write(json.dumps(event) + '\n')
            temp_file = f.name
        
        try:
            explorer = SessionExplorer(temp_file)
            assert len(explorer.tool_calls) == 1
            assert explorer.tool_calls[0]['name'] == 'Read'
            assert explorer.tool_calls[0]['id'] == 'test_1'
        finally:
            Path(temp_file).unlink()
    
    def it_extracts_user_messages(self):
        """Should extract user text messages."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            event = {
                "type": "user",
                "message": {
                    "content": [{
                        "type": "text",
                        "text": "Hello Claude"
                    }]
                },
                "timestamp": "2025-07-30T10:00:00.000Z"
            }
            f.write(json.dumps(event) + '\n')
            temp_file = f.name
        
        try:
            explorer = SessionExplorer(temp_file)
            assert len(explorer.messages) == 1
            assert explorer.messages[0]['text'] == 'Hello Claude'
            assert explorer.messages[0]['type'] == 'user'
        finally:
            Path(temp_file).unlink()
    
    def it_extracts_assistant_text(self):
        """Should extract assistant text messages."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            event = {
                "type": "assistant",
                "message": {
                    "content": [{
                        "type": "text",
                        "text": "I'll help with that"
                    }]
                },
                "timestamp": "2025-07-30T10:00:00.000Z"
            }
            f.write(json.dumps(event) + '\n')
            temp_file = f.name
        
        try:
            explorer = SessionExplorer(temp_file)
            assert len(explorer.messages) == 1
            assert explorer.messages[0]['text'] == "I'll help with that"
            assert explorer.messages[0]['type'] == 'assistant'
        finally:
            Path(temp_file).unlink()
    
    def it_preserves_raw_objects(self):
        """Should store raw JSONL objects for export."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            event = {
                "type": "user",
                "message": {"content": [{"type": "text", "text": "test"}]},
                "timestamp": "2025-07-30T10:00:00.000Z",
                "custom_field": "preserved"
            }
            f.write(json.dumps(event) + '\n')
            temp_file = f.name
        
        try:
            explorer = SessionExplorer(temp_file)
            assert len(explorer.raw_objects) == 1
            assert explorer.raw_objects[0]['custom_field'] == 'preserved'
        finally:
            Path(temp_file).unlink()
    
    def it_handles_tool_results(self):
        """Should handle tool result messages."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            event = {
                "type": "user",
                "message": {
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": "test_1",
                        "content": "File not found"
                    }]
                },
                "timestamp": "2025-07-30T10:00:00.000Z"
            }
            f.write(json.dumps(event) + '\n')
            temp_file = f.name
        
        try:
            explorer = SessionExplorer(temp_file)
            # Tool results are stored in messages under tool_results
            assert len(explorer.messages) == 1
            assert explorer.messages[0]['type'] == 'user'
            assert len(explorer.messages[0]['tool_results']) == 1
            assert explorer.messages[0]['tool_results'][0]['content'] == 'File not found'
        finally:
            Path(temp_file).unlink()


class describe_timeline_building:
    """Unit tests for timeline construction."""
    
    def it_creates_timeline_with_correct_indices(self):
        """Timeline items should have sequential indices."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            # Write multiple events
            for i in range(3):
                event = {
                    "type": "user",
                    "message": {"content": [{"type": "text", "text": f"Message {i}"}]},
                    "timestamp": f"2025-07-30T10:00:0{i}.000Z"
                }
                f.write(json.dumps(event) + '\n')
            temp_file = f.name
        
        try:
            explorer = SessionExplorer(temp_file)
            # Timeline is built internally, access it directly
            assert len(explorer.timeline) == 3
            for i, item in enumerate(explorer.timeline):
                assert item['seq'] == i + 1  # 1-based display indices
        finally:
            Path(temp_file).unlink()
    
    def it_preserves_chronological_order(self):
        """Timeline should maintain timestamp order."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            # Events might not be in timestamp order in file
            events = [
                {"type": "user", "message": {"content": [{"type": "text", "text": "Second"}]},
                 "timestamp": "2025-07-30T10:00:02.000Z"},
                {"type": "user", "message": {"content": [{"type": "text", "text": "First"}]},
                 "timestamp": "2025-07-30T10:00:01.000Z"},
                {"type": "user", "message": {"content": [{"type": "text", "text": "Third"}]},
                 "timestamp": "2025-07-30T10:00:03.000Z"}
            ]
            for event in events:
                f.write(json.dumps(event) + '\n')
            temp_file = f.name
        
        try:
            explorer = SessionExplorer(temp_file)
            # Timeline should be in chronological order
            assert 'First' in explorer.timeline[0]['data']['text']
            assert 'Second' in explorer.timeline[1]['data']['text']
            assert 'Third' in explorer.timeline[2]['data']['text']
        finally:
            Path(temp_file).unlink()
    
    def it_combines_messages_and_tools_in_timeline(self):
        """Timeline should include both messages and tools in chronological order."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            events = [
                {"type": "user", "message": {"content": [{"type": "text", "text": "Check file"}]},
                 "timestamp": "2025-07-30T10:00:00.000Z"},
                {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read", "id": "t1",
                                                            "input": {"file_path": "/test.py"}}]},
                 "timestamp": "2025-07-30T10:00:01.000Z"},
                {"type": "assistant", "message": {"content": [{"type": "text", "text": "File is empty"}]},
                 "timestamp": "2025-07-30T10:00:02.000Z"}
            ]
            for event in events:
                f.write(json.dumps(event) + '\n')
            temp_file = f.name
        
        try:
            explorer = SessionExplorer(temp_file)
            # The timeline actually has 4 items because assistant messages with tools
            # create both a message entry and a tool entry
            assert len(explorer.timeline) == 4
            
            # Check types are mixed correctly
            assert explorer.timeline[0]['type'] == 'message'
            assert explorer.timeline[0]['subtype'] == 'user'
            # Assistant message (contains the tool)
            assert explorer.timeline[1]['type'] == 'message'
            assert explorer.timeline[1]['subtype'] == 'assistant'
            # Tool call itself
            assert explorer.timeline[2]['type'] == 'tool'
            assert explorer.timeline[2]['subtype'] == 'Read'
            # Second assistant message
            assert explorer.timeline[3]['type'] == 'message'
            assert explorer.timeline[3]['subtype'] == 'assistant'
        finally:
            Path(temp_file).unlink()


class describe_filter_parsing:
    """Unit tests for filter parsing logic."""
    
    def it_parses_simple_tool_filter(self):
        """Should parse simple tool name filters."""
        explorer = SessionExplorer.__new__(SessionExplorer)  # Create without __init__
        
        filter_type, entity, pattern = explorer._parse_filter("Edit")
        assert filter_type == "tool"
        assert entity == "Edit"
        assert pattern is None
    
    def it_parses_tool_with_parameter_pattern(self):
        """Should parse tool filters with parameter patterns."""
        explorer = SessionExplorer.__new__(SessionExplorer)
        
        filter_type, entity, pattern = explorer._parse_filter("Bash(git *)")
        assert filter_type == "tool"
        assert entity == "Bash"
        assert pattern == "git *"
    
    def it_recognizes_virtual_entities(self):
        """Should recognize Message, Tool, User, Assistant as virtual entities."""
        explorer = SessionExplorer.__new__(SessionExplorer)
        
        for virtual in ["Message", "Tool", "User", "Assistant"]:
            filter_type, entity, pattern = explorer._parse_filter(virtual)
            assert filter_type == "virtual"
            # Entity names are normalized to lowercase
            assert entity == virtual.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])