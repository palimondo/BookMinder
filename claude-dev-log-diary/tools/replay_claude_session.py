#!/usr/bin/env python3
"""
Replay Claude's session from JSONL log file.
Extracts tool calls and recreates the exact sequence of operations.
"""
import json
import sys
import subprocess
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ToolCall:
    """Represents a single tool call from Claude"""
    tool_name: str
    tool_id: str
    parameters: Dict[str, Any]
    timestamp: Optional[str] = None
    
@dataclass
class ToolResult:
    """Result from a tool call"""
    tool_id: str
    success: bool
    output: str = ""
    error: str = ""

@dataclass
class Commit:
    """Represents a git commit with associated changes"""
    message: str
    tool_calls: List[ToolCall]
    bash_command: Optional[str] = None

class SessionReplayer:
    def __init__(self, jsonl_file: str, dry_run: bool = True):
        self.jsonl_file = jsonl_file
        self.dry_run = dry_run
        self.tool_calls: List[ToolCall] = []
        self.commits: List[Commit] = []
        self.current_commit_tools: List[ToolCall] = []
        
    def parse_session(self):
        """Parse JSONL file and extract all tool calls"""
        print(f"Parsing session from {self.jsonl_file}...")
        
        # Read entire file and parse as JSON objects
        with open(self.jsonl_file, 'r') as f:
            content = f.read()
            
        # Split by lines and accumulate JSON objects
        lines = content.strip().split('\n')
        current_obj = []
        objects_parsed = 0
        
        for line in lines:
            current_obj.append(line)
            
            # Try to parse accumulated lines as JSON
            try:
                data = json.loads('\n'.join(current_obj))
                self._process_entry(data)
                current_obj = []
                objects_parsed += 1
                if objects_parsed % 10 == 0:
                    print(f"  Processed {objects_parsed} objects...")
            except json.JSONDecodeError:
                # Not a complete JSON object yet, continue accumulating
                continue
                    
        print(f"Parsing complete. Found {len(self.tool_calls)} tool calls in {len(self.commits)} commits.")
        
    def _process_entry(self, data: Dict[str, Any]):
        """Process a single JSONL entry"""
        # Look for assistant messages with tool use
        if data.get('role') == 'assistant' and 'content' in data:
            for content_item in data.get('content', []):
                if content_item.get('type') == 'tool_use':
                    tool_call = ToolCall(
                        tool_name=content_item.get('name', ''),
                        tool_id=content_item.get('id', ''),
                        parameters=content_item.get('input', {}),
                        timestamp=data.get('timestamp')
                    )
                    
                    self.tool_calls.append(tool_call)
                    
                    # Check if this is a file modification
                    if tool_call.tool_name in ['Edit', 'MultiEdit', 'Write']:
                        self.current_commit_tools.append(tool_call)
                    
                    # Check if this is a git commit
                    elif tool_call.tool_name == 'Bash':
                        command = tool_call.parameters.get('command', '')
                        if 'git commit' in command and self.current_commit_tools:
                            # Extract commit message
                            import re
                            msg_match = re.search(r'-m\s*"([^"]+)"', command)
                            if not msg_match:
                                # Try heredoc format
                                msg_match = re.search(r"cat <<'EOF'(.+?)EOF", command, re.DOTALL)
                            
                            if msg_match:
                                commit = Commit(
                                    message=msg_match.group(1).strip(),
                                    tool_calls=self.current_commit_tools.copy(),
                                    bash_command=command
                                )
                                self.commits.append(commit)
                                self.current_commit_tools = []
    
    def display_plan(self):
        """Display the replay plan"""
        print("\n" + "="*80)
        print("REPLAY PLAN")
        print("="*80)
        
        for i, commit in enumerate(self.commits, 1):
            print(f"\nCommit {i}: {commit.message[:60]}...")
            print(f"  Total changes: {len(commit.tool_calls)}")
            
            for j, tool in enumerate(commit.tool_calls, 1):
                if tool.tool_name == 'Write':
                    print(f"    {j}. Write: {tool.parameters.get('file_path')}")
                elif tool.tool_name == 'Edit':
                    print(f"    {j}. Edit: {tool.parameters.get('file_path')}")
                    old = tool.parameters.get('old_string', '')[:50]
                    if len(tool.parameters.get('old_string', '')) > 50:
                        old += '...'
                    print(f"       Replace: {old}")
                elif tool.tool_name == 'MultiEdit':
                    print(f"    {j}. MultiEdit: {tool.parameters.get('file_path')}")
                    print(f"       {len(tool.parameters.get('edits', []))} edits")
    
    def execute_replay(self, start_commit: int = 1, end_commit: Optional[int] = None):
        """Execute the replay plan"""
        if end_commit is None:
            end_commit = len(self.commits)
            
        print(f"\n{'DRY RUN' if self.dry_run else 'EXECUTING'} commits {start_commit} to {end_commit}")
        
        for i in range(start_commit - 1, end_commit):
            commit = self.commits[i]
            print(f"\n--- Commit {i+1}/{len(self.commits)} ---")
            print(f"Message: {commit.message[:80]}...")
            
            if not self.dry_run:
                # Execute the tool calls
                for tool in commit.tool_calls:
                    self._execute_tool_call(tool)
                
                # Execute the commit
                if commit.bash_command:
                    print(f"Executing: git commit...")
                    result = subprocess.run(
                        commit.bash_command,
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode != 0:
                        print(f"ERROR: Commit failed: {result.stderr}")
                        if input("Continue? (y/n): ").lower() != 'y':
                            break
    
    def _execute_tool_call(self, tool: ToolCall):
        """Execute a single tool call"""
        print(f"  Executing {tool.tool_name}: {tool.parameters.get('file_path', 'N/A')}")
        # Here we would implement the actual tool execution
        # For now, this is a placeholder
        pass

def main():
    if len(sys.argv) < 2:
        print("Usage: python replay_claude_session.py <jsonl_file> [--execute] [--start N] [--end M]")
        sys.exit(1)
    
    jsonl_file = sys.argv[1]
    dry_run = '--execute' not in sys.argv
    
    # Parse start/end commits
    start_commit = 1
    end_commit = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--start' and i + 1 < len(sys.argv):
            start_commit = int(sys.argv[i + 1])
        elif arg == '--end' and i + 1 < len(sys.argv):
            end_commit = int(sys.argv[i + 1])
    
    replayer = SessionReplayer(jsonl_file, dry_run)
    replayer.parse_session()
    replayer.display_plan()
    
    if input("\nProceed with replay? (y/n): ").lower() == 'y':
        replayer.execute_replay(start_commit, end_commit)

if __name__ == "__main__":
    main()