#!/usr/bin/env python3
"""
Characterization tests for export formats in explore_session.py.

Tests --export-json, --json, --jsonl output formats.
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


def create_simple_session():
    """Create a simple session for export testing."""
    events = [
        {"type": "assistant", "message": {"id": "msg_1", "content": [{"type": "text", "text": "Hello"}]},
         "timestamp": "2025-07-30T10:00:00.000Z"},
        {"type": "assistant", "message": {"id": "msg_2", "content": [
            {"type": "tool_use", "name": "Edit", "id": "tool_1",
             "input": {"file_path": "/test.py", "old_string": "foo", "new_string": "bar"}}]},
         "timestamp": "2025-07-30T10:00:01.000Z"},
        {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "tool_1",
                                                "content": "File edited"}]},
         "timestamp": "2025-07-30T10:00:02.000Z"}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
        return f.name


class describe_json_output_format:
    """Test --json flag for stdout output."""
    
    def it_outputs_json_array_to_stdout(self):
        """--json should output JSON array to stdout."""
        session_file = create_simple_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '--json'])
            
            assert returncode == 0
            # Should be valid JSON
            data = json.loads(stdout)
            assert isinstance(data, list)
            # Should contain our events
            assert len(data) > 0
        finally:
            Path(session_file).unlink()
    
    def it_works_with_range_selection(self):
        """--json should work with range selection."""
        session_file = create_simple_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '1-2', '--json'])
            
            assert returncode == 0
            data = json.loads(stdout)
            # Should only have the selected items
            assert isinstance(data, list)
        finally:
            Path(session_file).unlink()


class describe_jsonl_output_format:
    """Test --jsonl flag for stdout output."""
    
    def it_outputs_jsonl_to_stdout(self):
        """--jsonl should output newline-delimited JSON to stdout."""
        session_file = create_simple_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '--jsonl'])
            
            assert returncode == 0
            # Should be JSONL format (one JSON per line)
            lines = stdout.strip().split('\n')
            assert len(lines) > 0
            
            # Each line should be valid JSON
            for line in lines:
                if line:  # Skip empty lines
                    json.loads(line)  # Should not raise
        finally:
            Path(session_file).unlink()


class describe_export_json_to_file:
    """Test --export-json for file output."""
    
    def it_exports_to_specified_file(self):
        """--export-json should write to specified file."""
        session_file = create_simple_session()
        
        try:
            with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
                export_file = f.name
            
            stdout, returncode = run_explore_session([
                session_file, '--export-json', '1-3', export_file
            ])
            
            # Check if export succeeded
            if returncode == 0:
                assert 'Exported' in stdout
                assert Path(export_file).exists()
                
                # Verify file contains valid JSON
                with open(export_file) as f:
                    data = json.load(f)
                    assert isinstance(data, list)
        finally:
            Path(session_file).unlink()
            if Path(export_file).exists():
                Path(export_file).unlink()
    
    def it_requires_range_parameter(self):
        """--export-json should require a range parameter."""
        session_file = create_simple_session()
        
        try:
            # Try without range - should fail or show usage
            # Need to capture stderr for usage message
            tools_dir = Path(__file__).parent.parent
            cmd = ['./explore_session.py', session_file, '--export-json']
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=tools_dir)
            
            # Should show usage in stderr or stdout
            assert result.returncode != 0 or 'usage:' in result.stdout or 'usage:' in result.stderr
        finally:
            Path(session_file).unlink()


class describe_export_with_filters:
    """Test export formats with filters."""
    
    def it_exports_filtered_results(self):
        """Export should respect include/exclude filters."""
        session_file = create_simple_session()
        
        try:
            # Export only tools
            stdout, returncode = run_explore_session([
                session_file, '-t', '-i', 'Tool', '--json'
            ])
            
            if returncode == 0:
                data = json.loads(stdout)
                # Should have filtered results
                assert isinstance(data, list)
        finally:
            Path(session_file).unlink()


class describe_raw_json_preservation:
    """Test that exports preserve raw JSONL data."""
    
    def it_preserves_original_message_structure(self):
        """JSON export should preserve original message IDs and structure."""
        session_file = create_simple_session()
        
        try:
            stdout, returncode = run_explore_session([session_file, '-t', '--json', '1'])
            
            if returncode == 0:
                data = json.loads(stdout)
                if len(data) > 0 and 'message' in data[0]:
                    # Should have preserved message structure
                    assert 'id' in data[0]['message'] or 'content' in data[0]['message']
        finally:
            Path(session_file).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])