#!/usr/bin/env python3
"""
Extract tool calls from Claude's JSONL session log.
Handles the multi-line JSON format efficiently.
"""
import json
import sys
from typing import Iterator, Dict, Any

def parse_jsonl_objects(filename: str) -> Iterator[Dict[str, Any]]:
    """Parse multi-line JSON objects from file"""
    with open(filename, 'r') as f:
        buffer = []
        brace_count = 0
        in_string = False
        escape_next = False
        
        for line in f:
            buffer.append(line)
            
            # Count braces to detect complete JSON objects
            for char in line:
                if escape_next:
                    escape_next = False
                    continue
                    
                if char == '\\':
                    escape_next = True
                    continue
                    
                if char == '"' and not escape_next:
                    in_string = not in_string
                    
                if not in_string:
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        
            # Complete object found
            if brace_count == 0 and buffer:
                try:
                    obj = json.loads(''.join(buffer))
                    yield obj
                    buffer = []
                except json.JSONDecodeError as e:
                    print(f"Failed to parse object: {e}", file=sys.stderr)
                    buffer = []

def extract_tool_calls(filename: str):
    """Extract and display tool calls from session"""
    tool_calls = []
    commits = []
    current_changes = []
    
    print("Scanning for tool calls...")
    
    obj_count = 0
    for obj in parse_jsonl_objects(filename):
        obj_count += 1
        if obj_count % 10 == 0:
            print(f"  Processed {obj_count} objects...", file=sys.stderr)
        if obj.get('role') == 'assistant' and 'content' in obj:
            content = obj.get('content', [])
            
            # Handle both string and array content
            if isinstance(content, str):
                continue
                
            for item in content:
                if isinstance(item, dict) and item.get('type') == 'tool_use':
                    tool_name = item.get('name', '')
                    tool_id = item.get('id', '')
                    params = item.get('input', {})
                    
                    # Skip MCP tools
                    if tool_name.startswith('mcp__'):
                        continue
                    
                    tool_call = {
                        'name': tool_name,
                        'id': tool_id,
                        'params': params
                    }
                    
                    tool_calls.append(tool_call)
                    
                    # Track file changes
                    if tool_name in ['Edit', 'MultiEdit', 'Write']:
                        current_changes.append(tool_call)
                        
                    # Detect commits
                    elif tool_name == 'Bash':
                        cmd = params.get('command', '')
                        if 'git commit' in cmd and current_changes:
                            commits.append({
                                'command': cmd,
                                'changes': current_changes.copy()
                            })
                            current_changes = []
    
    # Print summary
    print(f"\nProcessed {obj_count} total objects")
    print(f"Found {len(tool_calls)} total tool calls")
    print(f"Found {len(commits)} commits")
    
    # Print commit details
    for i, commit in enumerate(commits, 1):
        print(f"\n{'='*60}")
        print(f"Commit {i}:")
        
        # Extract commit message
        import re
        cmd = commit['command']
        msg_match = re.search(r'-m\s*"([^"]+)"', cmd)
        if not msg_match:
            msg_match = re.search(r"cat <<'EOF'\n(.+?)\nEOF", cmd, re.DOTALL)
        
        if msg_match:
            print(f"Message: {msg_match.group(1).strip()[:80]}...")
        
        print(f"Files changed: {len(commit['changes'])}")
        
        for change in commit['changes']:
            tool = change['name']
            params = change['params']
            
            if tool == 'Write':
                print(f"  - Write: {params.get('file_path')}")
            elif tool == 'Edit':
                print(f"  - Edit: {params.get('file_path')}")
            elif tool == 'MultiEdit':
                print(f"  - MultiEdit: {params.get('file_path')} ({len(params.get('edits', []))} edits)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_claude_jsonl.py <jsonl_file>")
        sys.exit(1)
        
    extract_tool_calls(sys.argv[1])