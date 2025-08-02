import pytest
import json
import tempfile
from pathlib import Path
import subprocess


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


class describe_search_with_list_content:
    """Test search functionality with tool results that have list content."""
    
    def it_handles_list_content_in_tool_results(self):
        """Search should handle tool results with content as list (not string)."""
        # Create a session with tool result containing list content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            # Message with tool result that has list content
            tool_result_msg = {
                "type": "user",
                "message": {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "test123",
                            "content": [
                                {"type": "text", "text": "First line"},
                                {"type": "text", "text": "Second line with search term"}
                            ]
                        }
                    ]
                },
                "timestamp": "2025-01-01T10:00:00Z"
            }
            
            # Regular message to search in
            regular_msg = {
                "type": "assistant",
                "message": {
                    "role": "assistant", 
                    "content": [
                        {"type": "text", "text": "This message contains search term"}
                    ]
                },
                "timestamp": "2025-01-01T10:00:01Z"
            }
            
            f.write(json.dumps(tool_result_msg) + '\n')
            f.write(json.dumps(regular_msg) + '\n')
            
            session_file = f.name
        
        try:
            # This should trigger the AttributeError we saw
            stdout, stderr, returncode = run_explore_session(
                [session_file, '-S', 'search term'],
                capture_stderr=True
            )
            
            # Currently this will fail with AttributeError
            assert returncode == 0, f"Search failed with error: {stderr}"
            assert 'Found' in stdout
            
        finally:
            Path(session_file).unlink()
    
    def it_handles_search_with_double_dash_pattern(self):
        """Search should handle patterns with -- like '--conversation'."""
        # Create a simple session
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            msg = {
                "type": "user",
                "message": {
                    "role": "user",
                    "content": "The old --conversation flag was useful"
                },
                "timestamp": "2025-01-01T10:00:00Z"
            }
            f.write(json.dumps(msg) + '\n')
            session_file = f.name
        
        try:
            # This might fail with argument parsing error
            stdout, stderr, returncode = run_explore_session(
                [session_file, '-S', '--conversation'],
                capture_stderr=True
            )
            
            assert returncode == 0, f"Search failed: {stderr}"
            assert 'Found 1 match' in stdout
            
        finally:
            Path(session_file).unlink()