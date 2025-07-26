#!/usr/bin/env python3
"""
Interactive CLI to explore Claude session logs.
Analyze what Claude did, filter tool calls, and extract specific information.
"""
import json
import sys
import argparse
import re
import fnmatch
from pathlib import Path
from collections import defaultdict

from parse_claude_jsonl import parse_jsonl_objects

class SessionExplorer:
    def __init__(self, jsonl_file):
        self.jsonl_file = jsonl_file
        self.tool_calls = []
        self.messages = []
        self._parse_session()
    
    def _parse_session(self):
        """Parse the session file."""
        print(f"Parsing {Path(self.jsonl_file).name}...")
        
        for obj in parse_jsonl_objects(self.jsonl_file):
            if obj.get('type') == 'assistant' and 'message' in obj:
                message = obj.get('message', {})
                content = message.get('content', [])
                
                # Track assistant messages
                assistant_text = []
                tool_uses = []
                
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'text':
                                assistant_text.append(item.get('text', ''))
                            elif item.get('type') == 'tool_use':
                                tool_name = item.get('name', '')
                                if not tool_name.startswith('mcp__'):
                                    tool_uses.append(tool_name)
                                    self.tool_calls.append({
                                        'name': tool_name,
                                        'id': item.get('id', ''),
                                        'parameters': item.get('input', {}),
                                        'timestamp': obj.get('timestamp', '')
                                    })
                
                # Store assistant message with text and tool summary
                if assistant_text or tool_uses:
                    self.messages.append({
                        'type': 'assistant',
                        'text': '\n'.join(assistant_text) if assistant_text else None,
                        'tools': tool_uses,
                        'timestamp': obj.get('timestamp', '')
                    })
            
            elif obj.get('type') == 'user':
                # Track user messages
                content = obj.get('message', {}).get('content', [])
                user_text = []
                
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'text':
                            user_text.append(item.get('text', ''))
                        elif isinstance(item, str):
                            user_text.append(item)
                
                self.messages.append({
                    'type': 'user',
                    'text': '\n'.join(user_text) if user_text else '',
                    'timestamp': obj.get('timestamp', '')
                })
        
        print(f"Found {len(self.tool_calls)} tool calls\n")
    
    def show_summary(self):
        """Show session summary."""
        tool_counts = defaultdict(int)
        for tc in self.tool_calls:
            tool_counts[tc['name']] += 1
        
        print("=== SESSION SUMMARY ===")
        print(f"Total tool calls: {len(self.tool_calls)}")
        print("\nTool usage:")
        for tool, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
            print(f"  {tool:15} {count:3}")
    
    def show_timeline(self, tool_filter=None):
        """Show timeline of tool calls."""
        print("\n=== TIMELINE ===")
        for i, tc in enumerate(self.tool_calls):
            if tool_filter and tc['name'] != tool_filter:
                continue
            
            print(f"{i+1:3}. {tc['name']:12}", end='')
            
            # Show relevant parameter based on tool type
            params = tc['parameters']
            if tc['name'] in ['Edit', 'Write', 'MultiEdit']:
                path = params.get('file_path', '')
                if path:
                    print(f" → {path.split('/')[-1]}", end='')
            elif tc['name'] == 'Bash':
                cmd = params.get('command', '')[:50]
                print(f" $ {cmd}...", end='')
            elif tc['name'] == 'Read':
                path = params.get('file_path', '')
                if path:
                    print(f" ← {path.split('/')[-1]}", end='')
            
            print()
    
    def show_git_operations(self):
        """Show all git operations."""
        print("\n=== GIT OPERATIONS ===")
        for i, tc in enumerate(self.tool_calls):
            if tc['name'] == 'Bash':
                cmd = tc['parameters'].get('command', '')
                if cmd.startswith('git'):
                    print(f"{i+1:3}. {cmd[:80]}...")
    
    def show_file_changes(self):
        """Show all file modifications."""
        print("\n=== FILE CHANGES ===")
        file_changes = defaultdict(list)
        
        for i, tc in enumerate(self.tool_calls):
            if tc['name'] in ['Edit', 'Write', 'MultiEdit']:
                path = tc['parameters'].get('file_path', 'unknown')
                file_changes[path].append((i+1, tc['name']))
        
        for path, changes in sorted(file_changes.items()):
            display_path = path.split('/')[-1] if '/' in path else path
            print(f"\n{display_path}: {len(changes)} changes")
            for seq, tool in changes[:5]:  # Show first 5
                print(f"  {seq:3}. {tool}")
            if len(changes) > 5:
                print(f"  ... and {len(changes)-5} more")
    
    def show_created_files(self):
        """Show files created with Write tool."""
        print("\n=== FILES CREATED ===")
        for i, tc in enumerate(self.tool_calls):
            if tc['name'] == 'Write':
                path = tc['parameters'].get('file_path', '')
                content = tc['parameters'].get('content', '')
                if path:
                    print(f"\n{i+1}. {path.split('/')[-1]}")
                    # Show first few lines
                    lines = content.split('\n')[:5]
                    for line in lines:
                        print(f"   {line[:60]}...")
                    if len(content.split('\n')) > 5:
                        print(f"   ... ({len(content.split('\n'))} total lines)")
    
    def search_commands(self, pattern):
        """Search bash commands for pattern."""
        print(f"\n=== BASH COMMANDS CONTAINING '{pattern}' ===")
        for i, tc in enumerate(self.tool_calls):
            if tc['name'] == 'Bash':
                cmd = tc['parameters'].get('command', '')
                if pattern.lower() in cmd.lower():
                    print(f"{i+1:3}. {cmd[:100]}...")
    
    def show_conversation(self, start=None, end=None):
        """Display conversation between user and assistant."""
        print("\n=== CONVERSATION ===")
        
        messages = self.messages[start-1:end] if start and end else self.messages
        
        for i, msg in enumerate(messages, start=start or 1):
            if msg['type'] == 'user':
                print(f"\n[{i}] USER:")
                if msg.get('text'):
                    # Indent user text
                    lines = msg['text'].split('\n')
                    for line in lines[:10]:  # Show first 10 lines
                        print(f"    {line}")
                    if len(lines) > 10:
                        print(f"    ... ({len(lines)-10} more lines)")
            
            elif msg['type'] == 'assistant':
                print(f"\n[{i}] CLAUDE:")
                if msg.get('text'):
                    # Show assistant's text response
                    lines = msg['text'].split('\n')
                    for line in lines[:20]:  # Show more lines for assistant
                        print(f"    {line}")
                    if len(lines) > 20:
                        print(f"    ... ({len(lines)-20} more lines)")
                
                # Show tool usage summary
                if msg.get('tools'):
                    tool_summary = defaultdict(int)
                    for tool in msg['tools']:
                        tool_summary[tool] += 1
                    
                    tools_str = ', '.join([f"{tool}({count})" if count > 1 else tool 
                                          for tool, count in tool_summary.items()])
                    print(f"    [Used tools: {tools_str}]")
    
    def export_range(self, start, end, output_file, include_filters=None, exclude_filters=None):
        """Export a range of tool calls with optional Tool(glob) filtering."""
        selected = self.tool_calls[start-1:end]
        
        # Apply filters if provided
        if include_filters or exclude_filters:
            selected = self._apply_filters(selected, include_filters, exclude_filters)
        
        # Output to file or stdout
        if output_file == '-':
            json.dump(selected, sys.stdout, indent=2)
            sys.stdout.write('\n')
        else:
            with open(output_file, 'w') as f:
                json.dump(selected, f, indent=2)
            print(f"\nExported {len(selected)} tool calls to {output_file}")
    
    def _parse_tool_filter(self, filter_str):
        """Parse 'Tool' or 'Tool(glob)' format."""
        match = re.match(r'(\w+)\((.*)\)', filter_str)
        if match:
            return match.group(1), match.group(2)
        elif re.match(r'^\w+$', filter_str):
            return filter_str, '*'
        return None, None
    
    def _matches_filter(self, tool_call, tool_name, pattern):
        """Check if a tool call matches the filter."""
        if tool_call['name'] != tool_name:
            return False
        
        # If pattern is *, match all
        if pattern == '*':
            return True
        
        params = tool_call.get('parameters', {})
        
        # For file operations, match against file_path
        if tool_name in ['Edit', 'Write', 'MultiEdit']:
            file_path = params.get('file_path', '')
            return fnmatch.fnmatch(file_path, pattern)
        
        # For Bash, match against command
        elif tool_name == 'Bash':
            command = params.get('command', '')
            return fnmatch.fnmatch(command, pattern)
        
        return False
    
    def _apply_filters(self, tool_calls, include_filters, exclude_filters):
        """Apply include/exclude filters to tool calls."""
        filtered = []
        
        for tc in tool_calls:
            # Check includes - must match at least one
            if include_filters:
                included = False
                for inc_filter in include_filters:
                    tool, pattern = self._parse_tool_filter(inc_filter)
                    if tool and self._matches_filter(tc, tool, pattern):
                        included = True
                        break
                if not included:
                    continue
            
            # Check excludes - must not match any
            if exclude_filters:
                excluded = False
                for exc_filter in exclude_filters:
                    tool, pattern = self._parse_tool_filter(exc_filter)
                    if tool and self._matches_filter(tc, tool, pattern):
                        excluded = True
                        break
                if excluded:
                    continue
            
            filtered.append(tc)
        
        return filtered

def find_session_file(identifier):
    """Find session file by any substring match."""
    import subprocess
    
    # If it's already a valid path, return as-is
    if Path(identifier).exists():
        return identifier
    
    # Search directories in order of preference
    search_dirs = [
        Path(__file__).parent.parent / 'github',
        Path.home() / '.claude' / 'projects'
    ]
    
    matches = []
    
    # Use ripgrep to find files containing the identifier
    for search_dir in search_dirs:
        if search_dir.exists():
            result = subprocess.run(
                ['rg', '--files', '.', '--glob', '*.jsonl'],
                cwd=str(search_dir),
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line and identifier in line:
                        matches.append(search_dir / line)
    
    if not matches:
        raise FileNotFoundError(f"No session file found containing '{identifier}'")
    
    if len(matches) == 1:
        return str(matches[0])
    
    # Multiple matches - let user choose
    print(f"Found {len(matches)} matches for '{identifier}':")
    for i, match in enumerate(matches):
        # Show relative path from search directory
        for search_dir in search_dirs:
            if search_dir in match.parents:
                rel_path = match.relative_to(search_dir.parent)
                print(f"  {i+1}. {rel_path}")
                break
    
    choice = input("Select (1-N): ")
    return str(matches[int(choice)-1])

def main():
    parser = argparse.ArgumentParser(description='Explore Claude session logs')
    parser.add_argument('jsonl', help='Session file or any unique substring (issue-13, run ID, date, etc.)')
    parser.add_argument('--summary', '-s', action='store_true', help='Show summary')
    parser.add_argument('--timeline', '-t', help='Show timeline (optionally filter by tool)')
    parser.add_argument('--git', '-g', action='store_true', help='Show git operations')
    parser.add_argument('--files', '-f', action='store_true', help='Show file changes')
    parser.add_argument('--created', '-c', action='store_true', help='Show created files')
    parser.add_argument('--conversation', nargs='?', const='all', metavar='RANGE',
                        help='Show conversation (e.g., --conversation, --conversation 1-50)')
    parser.add_argument('--search', help='Search bash commands')
    parser.add_argument('--export', nargs=3, metavar=('START', 'END', 'OUTPUT'), 
                        help='Export tool calls from START to END')
    parser.add_argument('--include', metavar='FILTERS',
                        help='Include only tools matching filters, comma-separated (e.g., "Edit,Bash(git add *)")')
    parser.add_argument('--exclude', metavar='FILTERS',
                        help='Exclude tools matching filters, comma-separated')
    
    args = parser.parse_args()
    
    # Default to showing summary if no options
    if not any([args.summary, args.timeline, args.git, args.files, 
                args.created, args.conversation, args.search, args.export]):
        args.summary = True
    
    # Resolve the session file
    try:
        jsonl_file = find_session_file(args.jsonl)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    explorer = SessionExplorer(jsonl_file)
    
    if args.summary:
        explorer.show_summary()
    
    if args.timeline is not None:
        tool_filter = args.timeline if args.timeline else None
        explorer.show_timeline(tool_filter)
    
    if args.git:
        explorer.show_git_operations()
    
    if args.files:
        explorer.show_file_changes()
    
    if args.created:
        explorer.show_created_files()
    
    if args.search:
        explorer.search_commands(args.search)
    
    if args.conversation:
        if args.conversation == 'all':
            explorer.show_conversation()
        else:
            # Parse range like "1-50"
            if '-' in args.conversation:
                start, end = map(int, args.conversation.split('-'))
                explorer.show_conversation(start, end)
            else:
                print(f"Invalid range format: {args.conversation}. Use format like '1-50'")
    
    if args.export:
        start, end, output = args.export
        # Split comma-separated filters
        include_filters = args.include.split(',') if args.include else None
        exclude_filters = args.exclude.split(',') if args.exclude else None
        explorer.export_range(int(start), int(end), output, 
                            include_filters=include_filters,
                            exclude_filters=exclude_filters)

if __name__ == "__main__":
    main()