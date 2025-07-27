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


def parse_range(range_str, total_items):
    """Parse range string into start and end indices.
    
    Args:
        range_str: Range string like "1-50", "-50", "50-"
        total_items: Total number of items for bounds checking
        
    Returns:
        tuple: (start_idx, end_idx) as 0-based indices
    """
    if '-' not in range_str:
        raise ValueError(f"Invalid range format: {range_str}. Use format like '1-50' or '-50'")
    
    parts = range_str.split('-', 1)
    
    if parts[0] == '':  # Format: "-N" (last N items)
        n = int(parts[1])
        return max(0, total_items - n), total_items
    elif parts[1] == '':  # Format: "N-" (from N to end)
        start = int(parts[0]) - 1  # Convert to 0-based
        return start, total_items
    else:  # Format: "M-N"
        start = int(parts[0]) - 1  # Convert to 0-based
        end = int(parts[1])
        return start, min(end, total_items)


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
                tool_results = []
                is_slash_command = False
                slash_command = ''
                is_meta = obj.get('isMeta', False)
                
                # Handle string content (slash commands)
                if isinstance(content, str):
                    if '<command-name>' in content and '<command-message>' in content:
                        # Extract slash command
                        match = re.search(r'<command-message>([^<]+)</command-message>', content)
                        if match:
                            slash_command = match.group(1)
                            is_slash_command = True
                    else:
                        user_text.append(content)
                        
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'text':
                                text = item.get('text', '')
                                # Check for interrupted requests
                                if '[Request interrupted by user' in text:
                                    user_text.append('[Interrupted by user]')
                                else:
                                    user_text.append(text)
                            elif item.get('type') == 'tool_result':
                                tool_results.append({
                                    'tool_use_id': item.get('tool_use_id', ''),
                                    'content': item.get('content', '')
                                })
                        elif isinstance(item, str):
                            user_text.append(item)
                
                self.messages.append({
                    'type': 'user',
                    'text': '\n'.join(user_text) if user_text else '',
                    'tool_results': tool_results,
                    'is_slash_command': is_slash_command,
                    'slash_command': slash_command,
                    'is_meta': is_meta,
                    'timestamp': obj.get('timestamp', '')
                })
        
        print(f"Found {len(self.tool_calls)} tool calls\n")
        
        # Build unified timeline
        self._build_timeline()
    
    def _format_truncated_output(self, text, max_lines=3):
        """Format output in truncated style like reconstruct.jq.
        
        Args:
            text: The text to format
            max_lines: Maximum number of lines to show (default 3)
            
        Returns:
            Formatted string with truncation indicator if needed
        """
        if not text:
            return ""
            
        lines = text.split('\n')
        if len(lines) <= max_lines:
            return text
        
        # Show first max_lines lines and add truncation indicator
        truncated = '\n'.join(lines[:max_lines])
        remaining = len(lines) - max_lines
        return f"{truncated}\n       … +{remaining} lines"
    
    def _build_timeline(self):
        """Build a unified timeline of all events (messages and tool calls)."""
        self.timeline = []
        
        # Add all messages with their sequence numbers
        msg_index = 0
        for msg in self.messages:
            self.timeline.append({
                'seq': msg_index + 1,
                'type': 'message',
                'subtype': msg['type'],  # 'user' or 'assistant'
                'data': msg,
                'timestamp': msg.get('timestamp', '')
            })
            msg_index += 1
        
        # Add all tool calls with their sequence numbers
        tool_index = 0
        for tc in self.tool_calls:
            self.timeline.append({
                'seq': tool_index + 1,
                'type': 'tool',
                'subtype': tc['name'],
                'data': tc,
                'timestamp': tc.get('timestamp', '')
            })
            tool_index += 1
        
        # Sort by timestamp to get chronological order
        self.timeline.sort(key=lambda x: x['timestamp'])
        
        # Reassign sequence numbers after sorting
        for i, item in enumerate(self.timeline):
            item['seq'] = i + 1
    
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
    
    def show_timeline(self, filter_type='all', start=None, end=None, display_mode='compact'):
        """Show timeline of events.
        
        Args:
            filter_type: 'all' (default), 'tools', 'conversation', or specific tool name
            start: Starting index (1-based, inclusive)
            end: Ending index (1-based, inclusive)
            display_mode: 'compact' (default), 'truncated', or 'full'
        """
        print("\n=== TIMELINE ===")
        
        # Apply range filtering
        items = self.timeline
        if start is not None or end is not None:
            start_idx = (start - 1) if start else 0
            end_idx = end if end else len(items)
            items = items[start_idx:end_idx]
        
        for item in items:
            # Apply filtering
            if filter_type == 'tools' and item['type'] != 'tool':
                continue
            elif filter_type == 'conversation' and item['type'] != 'message':
                continue
            elif filter_type not in ['all', 'tools', 'conversation'] and item['type'] == 'tool' and item['subtype'] != filter_type:
                continue
            
            # Format based on type
            if item['type'] == 'message':
                msg = item['data']
                if msg['type'] == 'user' and display_mode == 'truncated':
                    # Truncated mode - reconstruct.jq style (NO sequence numbers)
                    text = msg.get('text', '')
                    tool_results = msg.get('tool_results', [])
                    is_slash = msg.get('is_slash_command', False)
                    slash_cmd = msg.get('slash_command', '')
                    
                    # Handle different user message types
                    if is_slash and slash_cmd:
                        print(f"> /{slash_cmd}")
                    elif text == '[Interrupted by user]':
                        print("> [Request interrupted by user]")
                    elif text and not tool_results:
                        # Regular user message
                        print(f"> {text}")
                    elif tool_results:
                        # This is a tool result - format like reconstruct.jq
                        for result in tool_results:
                            content = result.get('content', '')
                            
                            # Skip internal messages
                            if any(phrase in content for phrase in [
                                "Todos have been modified successfully",
                                "completed successfully"
                            ]):
                                continue
                                
                            if content:
                                print("  ⎿  Waiting…\n")
                                # Format the output with truncation
                                truncated = self._format_truncated_output(content, 3)
                                # Indent each line
                                for line in truncated.split('\n'):
                                    print(f"  ⎿  {line}")
                                print()  # Extra newline after tool results
                
                elif msg['type'] == 'assistant' and display_mode == 'truncated':
                    # Assistant messages in truncated mode
                    text = msg.get('text', '')
                    tools = msg.get('tools', [])
                    
                    if text:
                        # Show full assistant text (reconstruct.jq shows all of it)
                        print(f"⏺ {text}\n")
                    # Tool uses are handled separately as 'tool' items
                    
                elif msg['type'] == 'user':
                    text = msg.get('text', '')
                    tool_results = msg.get('tool_results', [])
                    is_slash = msg.get('is_slash_command', False)
                    slash_cmd = msg.get('slash_command', '')
                    is_meta = msg.get('is_meta', False)
                    
                    # Check if this is an internal message to skip
                    if tool_results and tool_results[0].get('content', ''):
                        content = tool_results[0].get('content', '')
                        if any(phrase in content for phrase in [
                            "Todos have been modified successfully",
                            "completed successfully"  # System messages
                        ]):
                            # Skip these internal messages entirely
                            continue
                    
                    if is_meta and text.startswith('Caveat:'):
                        # Show caveat message (meta)
                        print(f"[{item['seq']}] [META] {text[:50]}...")
                    elif is_slash and slash_cmd:
                        # Show slash command (no prefix - it's a command)
                        print(f"[{item['seq']}] /{slash_cmd}")
                    elif text == '[Interrupted by user]':
                        # Show interrupted request (no prefix - it's a protocol message)
                        print(f"[{item['seq']}] [Interrupted by user]")
                    elif text:
                        # Show full first line of user message
                        lines = text.split('\n')
                        first_line = lines[0]
                        if len(lines) > 1:
                            # Show last line too for context
                            last_line = lines[-1].strip()
                            if last_line and last_line != first_line:
                                multiline = f' [...] {last_line}'
                            else:
                                multiline = ' [...]'
                        else:
                            multiline = ''
                        print(f"[{item['seq']}] > {first_line}{multiline}")
                    elif tool_results:
                        # This is a tool result message
                        content = tool_results[0].get('content', '')
                        
                        # Handle interrupted tools specially
                        if "doesn't want to proceed" in content:
                            print(f"[{item['seq']}] ⎿  [Tool rejected]")
                        else:
                            # Show actual tool results
                            lines = content.split('\n')
                            first_line = lines[0]
                            if len(lines) > 1:
                                # Show last line too for context
                                last_line = lines[-1].strip()
                                if last_line and last_line != first_line:
                                    multiline = f' [...] {last_line}'
                                else:
                                    multiline = ' [...]'
                            else:
                                multiline = ''
                            print(f"[{item['seq']}] ⎿  {first_line}{multiline}")
                    else:
                        # Empty user message (rare but possible)
                        print(f"[{item['seq']}] > [empty]")
                elif msg['type'] == 'assistant':
                    # Show assistant text or tool usage
                    text = msg.get('text', '')
                    tools = msg.get('tools', [])
                    if text:
                        lines = text.split('\n')
                        first_line = lines[0]
                        if len(lines) > 1:
                            # Show last line too for context
                            last_line = lines[-1].strip()
                            if last_line and last_line != first_line:
                                multiline = f' [...] {last_line}'
                            else:
                                multiline = ' [...]'
                        else:
                            multiline = ''
                        print(f"[{item['seq']}] • {first_line}{multiline}")
                    elif tools:
                        print(f"[{item['seq']}] • [Used tools: {', '.join(tools)}]")
                    else:
                        # Empty assistant message (rare but possible)
                        print(f"[{item['seq']}] • [empty]")
            
            elif item['type'] == 'tool':
                tc = item['data']
                
                if display_mode == 'truncated':
                    # Console-style output like reconstruct.jq
                    # Format tool input based on tool type (matching format_tool_input logic)
                    params = tc['parameters']
                    param_str = ""
                    
                    if tc['name'] == 'TodoWrite':
                        # Special case for TodoWrite
                        print("⏺ Update Todos")
                    elif tc['name'] == 'TodoRead':
                        # Special case for TodoRead
                        print("⏺ Read Todos")
                    else:
                        # Standard format: ToolName(parameter)
                        if 'command' in params:
                            param_str = params['command']
                        elif 'file_path' in params:
                            param_str = params['file_path']
                        elif 'path' in params:
                            param_str = params['path']
                        elif 'pattern' in params:
                            param_str = params['pattern']
                        else:
                            # Use first string parameter or convert to string
                            for v in params.values():
                                if isinstance(v, str):
                                    param_str = v
                                    break
                            if not param_str and params:
                                param_str = str(list(params.values())[0])
                        
                        print(f"⏺ {tc['name']}({param_str})")
                    
                    # Tool results will be shown as part of user messages with tool_result type
                    # We just show the tool call here
                    
                else:
                    # Compact mode (existing logic)
                    print(f"[{item['seq']}] {tc['name']:12}", end='')
                    
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
                    elif tc['name'] == 'Grep':
                        pattern = params.get('pattern', '')
                        path = params.get('path', '.')
                        if pattern:
                            print(f' "{pattern}" in {path}', end='')
                    elif tc['name'] == 'TodoWrite':
                        todos = params.get('todos', [])
                        if todos:
                            # Count todo statuses
                            status_counts = defaultdict(int)
                            for todo in todos:
                                status = todo.get('status', 'unknown')
                                status_counts[status] += 1
                            
                            # Format summary
                            total = len(todos)
                            status_parts = []
                            for status in ['completed', 'in_progress', 'pending']:
                                if status in status_counts:
                                    status_parts.append(f"{status_counts[status]} {status}")
                            
                            if status_parts:
                                print(f" Updated {total} todos ({', '.join(status_parts)})", end='')
                            else:
                                print(f" Updated {total} todos", end='')
                    
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
    parser.add_argument('--timeline', '-t', nargs='?', const='all', 
                        help='Show timeline (e.g., --timeline, --timeline tools, --timeline 1-50)')
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
    parser.add_argument('--truncated', action='store_true',
                        help='Show truncated console-style output (3-line preview)')
    parser.add_argument('--full', action='store_true',
                        help='Show full output without truncation')
    
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
        # Handle the different timeline modes
        timeline_arg = args.timeline if args.timeline != True else 'all'
        
        # Determine display mode
        display_mode = 'compact'
        if args.truncated:
            display_mode = 'truncated'
        elif args.full:
            display_mode = 'full'
        
        # Check if it's a range
        if '-' in timeline_arg:
            try:
                start_idx, end_idx = parse_range(timeline_arg, len(explorer.timeline))
                explorer.show_timeline('all', start_idx + 1, end_idx, display_mode)  # Convert to 1-based
            except ValueError as e:
                print(f"Error: {e}")
        else:
            # It's a filter type (all, tools, conversation, or tool name)
            explorer.show_timeline(timeline_arg, display_mode=display_mode)
    
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
            # Parse range using utility function
            try:
                start_idx, end_idx = parse_range(args.conversation, len(explorer.messages))
                explorer.show_conversation(start_idx + 1, end_idx)  # Convert back to 1-based for method
            except ValueError as e:
                print(f"Error: {e}")
    
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