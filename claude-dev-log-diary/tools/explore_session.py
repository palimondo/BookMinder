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
import signal

from parse_claude_jsonl import parse_jsonl_objects

# Handle SIGPIPE gracefully when piping to head/tail
try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except AttributeError:
    # SIGPIPE doesn't exist on Windows
    pass


def parse_indices(args, total_items):
    """Parse multiple index/range arguments into a list of indices.
    
    Args:
        args: List of strings like ["5", "+10", "-5", "20-30"]
        total_items: Total number of items for bounds checking
        
    Returns:
        sorted list of unique 0-based indices
    """
    indices = set()
    
    for arg in args:
        start, end = parse_range(arg, total_items)
        indices.update(range(start, end))
    
    return sorted(indices)


def parse_range(range_str, total_items):
    """Parse range string into start and end indices.
    
    Args:
        range_str: Range string like "5", "+5", "-5", "1-50", "50-", "50+"
        total_items: Total number of items for bounds checking
        
    Returns:
        tuple: (start_idx, end_idx) as 0-based indices
    """
    if range_str.isdigit():
        n = int(range_str) - 1  # Convert to 0-based
        if n >= total_items:
            raise ValueError(f"Index {range_str} out of range (max {total_items})")
        return n, n + 1
    
    if range_str.startswith('+') and range_str[1:].isdigit():
        n = int(range_str[1:])
        return 0, min(n, total_items)
    
    # Handle "60+" format (from 60 onwards)
    if range_str.endswith('+') and range_str[:-1].isdigit():
        start = int(range_str[:-1]) - 1  # Convert to 0-based
        return start, total_items
    
    if '-' not in range_str:
        raise ValueError(f"Invalid range format: {range_str}. Use format like '5', '+5', '-5', '1-50', '50+', '50-'")
    
    parts = range_str.split('-', 1)
    
    if parts[0] == '':
        n = int(parts[1])
        return max(0, total_items - n), total_items
    elif parts[1] == '':
        start = int(parts[0]) - 1  # Convert to 0-based
        return start, total_items
    else:
        start = int(parts[0]) - 1  # Convert to 0-based
        end = int(parts[1])
        return start, min(end, total_items)


class SessionExplorer:
    def __init__(self, jsonl_file):
        self.jsonl_file = jsonl_file
        self.tool_calls = []
        self.messages = []
        self.raw_objects = []  # Store original JSONL objects
        self._parse_session()
    
    def _parse_session(self):
        """Parse the session file."""
        
        for obj in parse_jsonl_objects(self.jsonl_file):
            # Store the raw object with its index
            obj_index = len(self.raw_objects)
            self.raw_objects.append(obj)
            if obj.get('type') == 'assistant' and 'message' in obj:
                message = obj.get('message', {})
                content = message.get('content', [])
                
                assistant_text = []
                tool_uses = []
                thinking_text = []
                
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'text':
                                assistant_text.append(item.get('text', ''))
                            elif item.get('type') == 'thinking':
                                thinking_text.append(item.get('thinking', ''))
                            elif item.get('type') == 'tool_use':
                                tool_name = item.get('name', '')
                                tool_uses.append(tool_name)
                                self.tool_calls.append({
                                    'name': tool_name,
                                    'id': item.get('id', ''),
                                    'parameters': item.get('input', {}),
                                    'timestamp': obj.get('timestamp')
                                })
                
                if assistant_text or tool_uses or thinking_text:
                    self.messages.append({
                        'type': 'assistant',
                        'text': '\n'.join(assistant_text) if assistant_text else None,
                        'thinking': '\n'.join(thinking_text) if thinking_text else None,
                        'tools': tool_uses,
                        'timestamp': obj.get('timestamp'),
                        'raw_index': obj_index  # Link to raw object
                    })
            
            elif obj.get('type') == 'user':
                content = obj.get('message', {}).get('content', [])
                user_text = []
                tool_results = []
                is_slash_command = False
                slash_command = ''
                is_meta = obj.get('isMeta', False)
                
                if isinstance(content, str):
                    if '<command-name>' in content and '<command-message>' in content:
                        # Extract command name for display
                        cmd_match = re.search(r'<command-name>([^<]+)</command-name>', content)
                        msg_match = re.search(r'<command-message>([^<]+)</command-message>', content)
                        if cmd_match:
                            slash_command = cmd_match.group(1)
                            is_slash_command = True
                            # Also store the message part as text
                            if msg_match:
                                user_text.append(msg_match.group(1))
                    else:
                        user_text.append(content)
                        
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'text':
                                text = item.get('text', '')
                                if '[Request interrupted by user' in text:
                                    user_text.append('[Interrupted by user]')
                                elif '<command-name>' in text and '<command-message>' in text:
                                    # Handle slash commands in list format
                                    cmd_match = re.search(r'<command-name>([^<]+)</command-name>', text)
                                    msg_match = re.search(r'<command-message>([^<]+)</command-message>', text)
                                    if cmd_match:
                                        slash_command = cmd_match.group(1)
                                        is_slash_command = True
                                        if msg_match:
                                            user_text.append(msg_match.group(1))
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
                    'timestamp': obj.get('timestamp', ''),
                    'raw_index': obj_index  # Link to raw object
                })
        
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
        
        # Handle both string and list inputs
        if isinstance(text, list):
            # Join list items as they would appear in output
            text = '\n'.join(str(item) for item in text)
            
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
        
        msg_index = 0
        for msg in self.messages:
            self.timeline.append({
                'seq': msg_index + 1,
                'type': 'message',
                'subtype': msg['type'],  # 'user' or 'assistant'
                'data': msg,
                'timestamp': msg.get('timestamp'),
                'raw_index': msg.get('raw_index')  # Preserve link to raw object
            })
            msg_index += 1
        
        tool_index = 0
        for tc in self.tool_calls:
            self.timeline.append({
                'seq': tool_index + 1,
                'type': 'tool',
                'subtype': tc['name'],
                'data': tc,
                'timestamp': tc.get('timestamp')
            })
            tool_index += 1
        
        self.timeline.sort(key=lambda x: x['timestamp'] or '')
        
        for i, item in enumerate(self.timeline):
            item['seq'] = i + 1
    
    def show_summary(self):
        """Show session summary in YAML-style hierarchy."""
        # Count tools by name
        tool_counts = defaultdict(int)
        mcp_tools = defaultdict(lambda: defaultdict(int))
        git_operations = 0
        git_commits = 0
        
        for tc in self.tool_calls:
            tool_name = tc['name']
            tool_counts[tool_name] += 1
            
            # MCP tool detection
            if tool_name.startswith('mcp__'):
                parts = tool_name.split('__')
                if len(parts) >= 2:
                    server = parts[1]
                    mcp_tools[server][tool_name] += 1
            
            # Git operations
            elif tool_name == 'Bash':
                cmd = tc['parameters'].get('command', '')
                if cmd.startswith('git'):
                    git_operations += 1
                    if 'git commit' in cmd:
                        git_commits += 1
        
        # Count messages
        user_inputs = 0
        tool_results = 0
        assistant_messages = 0
        assistant_text_only = 0
        assistant_with_tools = 0
        user_interruptions = 0
        
        for m in self.messages:
            if m['type'] == 'user':
                if m.get('tool_results'):
                    tool_results += 1
                elif m.get('text') or m.get('is_slash_command'):
                    user_inputs += 1
                    if '[Interrupted by user]' in m.get('text', ''):
                        user_interruptions += 1
            elif m['type'] == 'assistant':
                assistant_messages += 1
                has_text = bool(m.get('text'))
                has_tools = bool(m.get('tools'))
                if has_text and not has_tools:
                    assistant_text_only += 1
                    # Also check for interruptions in assistant messages
                    if '[Request interrupted by user]' in m.get('text', ''):
                        user_interruptions += 1
                elif has_tools:
                    assistant_with_tools += 1
        
        # Count files modified
        files_modified = set()
        for tc in self.tool_calls:
            if tc['name'] in ['Edit', 'MultiEdit', 'Write']:
                path = tc['parameters'].get('file_path', '')
                if path:
                    files_modified.add(path)
        
        # Get timestamps
        timestamps = [item['timestamp'] for item in self.timeline if item.get('timestamp')]
        if timestamps:
            from datetime import datetime
            try:
                start_time = datetime.fromisoformat(timestamps[0].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(timestamps[-1].replace('Z', '+00:00'))
                duration = end_time - start_time
                
                hours, remainder = divmod(duration.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                if hours > 0:
                    duration_str = f"{hours}h {minutes}m {seconds}s"
                elif minutes > 0:
                    duration_str = f"{minutes}m {seconds}s"
                else:
                    duration_str = f"{seconds}s"
            except:
                start_time = end_time = duration_str = None
        else:
            start_time = end_time = duration_str = None
        
        # Print formatted output
        print(f"Session: {Path(self.jsonl_file).name}")
        print()
        if start_time and end_time:
            print("Metadata:")
            print(f"  Started: {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"  Ended: {end_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"  Duration: {duration_str}")
            print("                            # Use filter params and options below")
        # Fixed column position for comments
        comment_col = 30
        
        print(f"Timeline:{' ' * (comment_col - 9)}# to show specific event types:")
        print(f"  Events: {len(self.timeline)}".ljust(comment_col) + "# -t")
        print(f"  User inputs: {user_inputs}".ljust(comment_col) + "# -U")
        if user_interruptions > 0:
            print(f"    Interrupted: {user_interruptions}")
        print(f"  Tool results: {tool_results}".ljust(comment_col) + "# (shown after -T events, use --no-tool-results to exclude)")
        print(f"  Assistant: {assistant_messages}".ljust(comment_col) + "# -a")
        print("  Assistant messages:")
        print(f"    Text: {assistant_text_only}".ljust(comment_col) + "# -a -x Tool")
        print(f"    Tool: {len(self.tool_calls)}".ljust(comment_col) + "# -T")
        
        if self.tool_calls:
            print("    Tool calls:")
            
            # Group MCP tools
            total_mcp = sum(sum(tools.values()) for tools in mcp_tools.values())
            if total_mcp > 0:
                print(f"      MCP: {total_mcp:<18} # -i Tool(mcp__*)")
                print("      MCP tools:")
                # Sort MCP servers by total count
                for server, tools in sorted(mcp_tools.items(), 
                                          key=lambda x: sum(x[1].values()), 
                                          reverse=True):
                    server_total = sum(tools.values())
                    print(f"          {server.title()}: {server_total:<10} # -i Tool(mcp__{server}*)")
            
            # Regular tools (non-MCP), sorted by count
            regular_tools = [(name, count) for name, count in tool_counts.items() 
                           if not name.startswith('mcp__')]
            
            # Identify "other" tools (those with few occurrences)
            threshold = 3  # Tools with less than this count go to "Other"
            main_tools = []
            other_tools = []
            
            for name, count in sorted(regular_tools, key=lambda x: -x[1]):
                if count >= threshold or name in ['Edit', 'Read', 'Bash', 'Write', 'Grep']:
                    main_tools.append((name, count))
                else:
                    other_tools.append((name, count))
            
            # Print main tools
            for tool, count in main_tools:
                if tool == 'Bash':
                    print(f"      {tool}: {count:<18} # -i {tool}")
                    if git_commits > 0:
                        print("      Git:")
                        print(f"        Commits: {git_commits:<12} # -i Bash(git commit *)")
                        print(f"        Operations: {git_operations:<9} # --git")
                else:
                    print(f"      {tool}: {count:<18} # -i {tool}")
            
            # Print other tools as a group
            if other_tools:
                other_count = sum(count for _, count in other_tools)
                other_names = ','.join(name for name, _ in other_tools)
                print(f"      Other: {other_count:<17} # -i {other_names}")
        
        print()
        print(f"Files modified: {len(files_modified):<12} # --files")
        
        print()
        print("# Practical debugging examples:")
        print("# - Find where Claude got confused:")
        print("#   explore_session.py session.jsonl -S \"error\" -a -C 3")
        print("# - Show git commits with their edits:")
        print("#   explore_session.py session.jsonl -i \"Bash(git commit*),Edit\"")
        print("# - Debug a specific range after user correction:")
        print("#   explore_session.py session.jsonl -U -A 5 250-300")
    
    def _matches_timeline_filter(self, item, filter_str):
        """Check if a timeline item matches a filter string."""
        filter_type, entity_name, pattern = self._parse_filter(filter_str)
        
        if not filter_type:
            return False
        
        if filter_type == 'virtual':
            if entity_name == 'message' and item['type'] == 'message':
                return True
            elif entity_name == 'tool' and item['type'] == 'tool':
                return True
            elif entity_name == 'user' and item['type'] == 'message':
                return item['data']['type'] == 'user'
            elif entity_name == 'assistant' and item['type'] == 'message':
                return item['data']['type'] == 'assistant'
        
        elif filter_type == 'tool' and item['type'] == 'tool':
            tool_call = item['data']
            return self._matches_filter(tool_call, entity_name, pattern)
        
        return False
    
    def filter_timeline(self, indices=None, include_filters=None, exclude_filters=None, 
                       include_tool_results=True, before_context=0, after_context=0):
        """Filter timeline based on indices and include/exclude filters.
        
        Args:
            indices: List of 0-based indices to show (if None, show all)
            include_filters: List of filter strings (e.g. ["Bash(git *)", "Edit", "Message"])
            exclude_filters: List of filter strings
            include_tool_results: When filtering for tools, also include their results (default: True)
            before_context: Number of items to show before each match
            after_context: Number of items to show after each match
            
        Returns:
            List of filtered timeline items
        """
        # First pass: find matching items
        matched_indices = set()
        
        for i, item in enumerate(self.timeline):
            if indices is not None and i not in indices:
                continue
            
            # Check includes - must match at least one
            if include_filters:
                # Special handling for tool results
                is_tool_result = (item['type'] == 'message' and 
                                item['data'].get('tool_results', []))
                
                if is_tool_result:
                    # Include tool results if flag is set and previous item was a tool
                    if include_tool_results and i > 0 and (i-1) in matched_indices:
                        matched_indices.add(i)
                else:
                    # Check if item matches any include filter
                    if any(self._matches_timeline_filter(item, f) for f in include_filters):
                        # Check excludes before adding
                        if not exclude_filters or not any(self._matches_timeline_filter(item, f) for f in exclude_filters):
                            matched_indices.add(i)
            else:
                # No include filters, check excludes only
                if not exclude_filters or not any(self._matches_timeline_filter(item, f) for f in exclude_filters):
                    matched_indices.add(i)
        
        # Second pass: add context lines
        if before_context > 0 or after_context > 0:
            context_indices = set()
            for idx in matched_indices:
                # Add before context
                for j in range(max(0, idx - before_context), idx):
                    context_indices.add(j)
                # Add after context
                for j in range(idx + 1, min(len(self.timeline), idx + after_context + 1)):
                    context_indices.add(j)
            matched_indices.update(context_indices)
        
        # Third pass: build filtered items in order
        filtered_items = []
        for i, item in enumerate(self.timeline):
            if i in matched_indices:
                filtered_items.append(item)
        
        return filtered_items
    
    def show_timeline_with_filters(self, indices=None, display_mode='compact', 
                                    include_filters=None, exclude_filters=None,
                                    include_tool_results=True, force_show_numbers=False,
                                    json_output=False, jsonl_output=False,
                                    before_context=0, after_context=0):
        """Show timeline with indices and include/exclude filters.
        
        Args:
            indices: List of 0-based indices to show (if None, show all)
            display_mode: 'compact' (default), 'truncated', or 'full'
            include_filters: Comma-separated filter string (e.g. "Bash(git *),Edit")
            exclude_filters: Comma-separated filter string
            include_tool_results: Whether to include tool results when filtering
            force_show_numbers: Force showing sequence numbers in truncated mode
            json_output: Output as JSON array to stdout
            jsonl_output: Output as JSONL (newline-delimited JSON) to stdout
            before_context: Number of items to show before each match
            after_context: Number of items to show after each match
        """
        include_list = include_filters.split(',') if include_filters else None
        exclude_list = exclude_filters.split(',') if exclude_filters else None
        
        filtered_items = self.filter_timeline(indices, include_list, exclude_list, 
                                            include_tool_results, before_context, after_context)
        
        if json_output or jsonl_output:
            json_items = []
            for item in filtered_items:
                # Get the raw JSONL object if available
                raw_index = item.get('raw_index')
                if raw_index is not None and raw_index < len(self.raw_objects):
                    # Output the original JSONL object
                    json_item = self.raw_objects[raw_index]
                else:
                    # Fallback to timeline structure for tool events (they don't have raw objects)
                    json_item = {
                        'seq': item['seq'],
                        'type': item['type'],
                        'timestamp': item.get('timestamp')
                    }
                    if item['type'] == 'tool':
                        tc = item['data']
                        json_item['tool'] = {
                            'name': tc['name'],
                            'parameters': tc.get('parameters', {})
                        }
                
                if jsonl_output:
                    json.dump(json_item, sys.stdout)
                    sys.stdout.write('\n')
                else:
                    json_items.append(json_item)
            
            if json_output:
                json.dump(json_items, sys.stdout, indent=2)
                sys.stdout.write('\n')
        else:
            
            # Show numbers when: 1) filtering is applied or 2) not showing full timeline or 3) force flag or 4) full mode
            has_filtering = indices or include_list or exclude_list
            show_numbers = (display_mode == 'truncated' and (has_filtering or force_show_numbers)) or display_mode == 'full'
            
            prev_seq = None
            for item in filtered_items:
                # Add visual separator for gaps in sequence
                if prev_seq is not None and item['seq'] > prev_seq + 1:
                    print("--")  # Separator like grep
                self._display_timeline_item(item, display_mode, show_numbers, exclude_list)
                prev_seq = item['seq']
    
    def show_timeline_indices(self, filter_type='all', indices=None, display_mode='compact'):
        """Show timeline with specific indices.
        
        Args:
            filter_type: 'all' (default), 'tools', or specific tool name
            indices: List of 0-based indices to show (if None, show all)
            display_mode: 'compact' (default), 'truncated', or 'full'
        """
        if filter_type == 'tools':
            filtered_items = [item for item in self.filter_timeline(indices) if item['type'] == 'tool']
        elif filter_type not in ['all', 'tools']:
            # filter_type is a specific tool name (e.g., 'Edit', 'Bash')
            include_filters = [filter_type]
            filtered_items = self.filter_timeline(indices, include_filters)
        else:
            filtered_items = self.filter_timeline(indices)
        
        # Show numbers in truncated mode when filtering or always in full mode
        has_filtering = filter_type != 'all' or indices
        show_numbers = (display_mode == 'truncated' and has_filtering) or display_mode == 'full'
        
        prev_seq = None
        for item in filtered_items:
            # Add visual separator for gaps in sequence
            if prev_seq is not None and item['seq'] > prev_seq + 1:
                print("--")  # Separator like grep
            self._display_timeline_item(item, display_mode, show_numbers, None)
            prev_seq = item['seq']
    
    def _display_timeline_item(self, item, display_mode='compact', show_numbers=False, exclude_filters=None):
        """Display a single timeline item based on display mode.
        
        Args:
            item: Timeline item to display
            display_mode: 'compact', 'truncated', or 'full'
            show_numbers: Force showing sequence numbers in truncated mode
            exclude_filters: List of filters to exclude (e.g., ['Tool'])
        """
        if item['type'] == 'message':
            msg = item['data']
            if msg['type'] == 'user' and display_mode in ['truncated', 'full']:
                # Truncated mode - reconstruct.jq style
                text = msg.get('text', '')
                tool_results = msg.get('tool_results', [])
                is_slash = msg.get('is_slash_command', False)
                slash_cmd = msg.get('slash_command', '')
                
                # Handle different user message types
                prefix = f"[{item['seq']}] " if show_numbers or display_mode == 'full' else ""
                if is_slash and slash_cmd:
                    if text:
                        print(f"{prefix}> /{slash_cmd} {text}")
                    else:
                        print(f"{prefix}> /{slash_cmd}")
                elif text == '[Interrupted by user]':
                    print(f"{prefix}> [Request interrupted by user]")
                elif text and not tool_results:
                    # Check for bash command tags in truncated mode
                    if '<bash-input>' in text:
                        # Extract bash command
                        bash_match = re.search(r'<bash-input>([^<]+)</bash-input>', text)
                        if bash_match:
                            command = bash_match.group(1)
                            print(f"{prefix}! {command}")
                    elif '<bash-stdout>' in text or '<bash-stderr>' in text:
                        # Extract bash output
                        stdout_match = re.search(r'<bash-stdout>([^<]*)</bash-stdout>', text)
                        stderr_match = re.search(r'<bash-stderr>([^<]*)</bash-stderr>', text)
                        
                        output_parts = []
                        if stdout_match and stdout_match.group(1):
                            output_parts.append(stdout_match.group(1))
                        if stderr_match and stderr_match.group(1):
                            output_parts.append(stderr_match.group(1))
                        
                        if output_parts:
                            output = '\n'.join(output_parts)
                            # Show indented output with proper prefix alignment
                            indent = "  " if not prefix else " " * len(prefix) + "  "
                            first = True
                            for line in output.split('\n'):
                                if line.strip():
                                    if first:
                                        print(f"{indent}⎿  {line}")
                                        first = False
                                    else:
                                        print(f"{indent}   {line}")
                    else:
                        print(f"{prefix}> {text}")
                elif tool_results:
                    for result in tool_results:
                        content = result.get('content', '')
                        
                        if any(phrase in content for phrase in [
                            "Todos have been modified successfully",
                            "completed successfully"
                        ]):
                            continue
                            
                        print("  ⎿  Waiting…\n")
                        
                        if content:
                            if self._is_todo_result(content):
                                self._format_todo_result_truncated(content)
                            else:
                                if display_mode == 'full':
                                    # Full mode: show complete output
                                    for line in content.split('\n'):
                                        print(f"  ⎿  {line}")
                                else:
                                    # Truncated mode: show first 3 lines
                                    truncated = self._format_truncated_output(content, 3)
                                    # Indent each line
                                    for line in truncated.split('\n'):
                                        print(f"  ⎿  {line}")
                        else:
                            print("  ⎿  (No content)")
                        print()  # Extra newline after tool results
            
            elif msg['type'] == 'assistant' and display_mode in ['truncated', 'full']:
                # Assistant messages in truncated/full mode
                text = msg.get('text', '')
                thinking = msg.get('thinking', '')
                tools = msg.get('tools', [])
                
                if text:
                    # Show full assistant text
                    prefix = f"[{item['seq']}] " if show_numbers or display_mode == 'full' else ""
                    if display_mode == 'full':
                        print(f"{prefix}⏺ {text}\n")
                    else:  # truncated
                        truncated = self._format_truncated_output(text, 3)
                        for line in truncated.split('\n'):
                            print(f"{prefix}⏺ {line}")
                        print()
                elif thinking:
                    prefix = f"[{item['seq']}] " if show_numbers or display_mode == 'full' else ""
                    if display_mode == 'full':
                        # Show full thinking in full mode
                        print(f"{prefix}✻ Thinking…\n")
                        for line in thinking.split('\n'):
                            print(f"  {line}")
                        print()
                    else:  # truncated
                        # Show abbreviated thinking in truncated mode
                        print(f"{prefix}✻ Thinking…\n")
                        lines = thinking.split('\n')
                        # Show first 5-6 lines
                        for i, line in enumerate(lines[:6]):
                            print(f"  {line}")
                        if len(lines) > 6:
                            print(f"  … +{len(lines) - 6} lines")
                # Tool uses are handled separately as 'tool' items
                
            elif msg['type'] == 'user':
                text = msg.get('text', '')
                tool_results = msg.get('tool_results', [])
                is_slash = msg.get('is_slash_command', False)
                slash_cmd = msg.get('slash_command', '')
                is_meta = msg.get('is_meta', False)
                
                # Don't display todo success messages in compact mode
                # (They're noisy and not useful)
                
                if is_meta and text.startswith('Caveat:'):
                    # Show caveat message (meta) with consistent truncation
                    lines = text.split('\n')
                    first_line = lines[0]
                    if len(lines) > 1:
                        last_line = lines[-1].strip()
                        if last_line and last_line != first_line:
                            display_text = f'{first_line} [...] {last_line}'
                        else:
                            display_text = f'{first_line} [...]'
                    else:
                        # Single line - show what we can
                        display_text = first_line
                    print(f"[{item['seq']}] [META] {display_text}")
                elif is_slash and slash_cmd:
                    # Show slash command with message if available
                    if text:
                        print(f"[{item['seq']}] > /{slash_cmd} {text}")
                    else:
                        print(f"[{item['seq']}] > /{slash_cmd}")
                elif text == '[Interrupted by user]':
                    # Show interrupted request (no prefix - it's a protocol message)
                    print(f"[{item['seq']}] [Interrupted by user]")
                elif text:
                    # Check for bash command tags
                    if '<bash-input>' in text:
                        # Extract bash command
                        bash_match = re.search(r'<bash-input>([^<]+)</bash-input>', text)
                        if bash_match:
                            command = bash_match.group(1)
                            print(f"[{item['seq']}] ! {command}")
                    elif '<bash-stdout>' in text or '<bash-stderr>' in text:
                        # Extract bash output
                        stdout_match = re.search(r'<bash-stdout>([^<]*)</bash-stdout>', text)
                        stderr_match = re.search(r'<bash-stderr>([^<]*)</bash-stderr>', text)
                        
                        output_parts = []
                        if stdout_match and stdout_match.group(1):
                            output_parts.append(stdout_match.group(1))
                        if stderr_match and stderr_match.group(1):
                            output_parts.append(stderr_match.group(1))
                        
                        if output_parts:
                            output = '\n'.join(output_parts)
                            # Show indented output
                            for line in output.split('\n'):
                                if line.strip():
                                    print(f"  ⎿  {line}")
                        # Skip empty output
                    else:
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
                    content = tool_results[0].get('content', '')
                    
                    if isinstance(content, list):
                        texts = []
                        for content_item in content:
                            if isinstance(content_item, dict) and 'text' in content_item:
                                texts.append(content_item['text'])
                            else:
                                texts.append(str(content_item))
                        content = '\n'.join(texts)
                    elif isinstance(content, dict):
                        content = content.get('text', str(content))
                    
                    if "doesn't want to proceed" in content:
                        print(f"[{item['seq']}] ⎿  [Tool rejected]")
                    else:
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
                    print(f"[{item['seq']}] > [empty]")
            elif msg['type'] == 'assistant':
                # Show assistant text or tool usage
                text = msg.get('text', '')
                thinking = msg.get('thinking', '')
                tools = msg.get('tools', [])
                if text:
                    lines = text.split('\n')
                    first_line = lines[0]
                    if len(lines) > 1:
                        # Show last line too for context (same as user messages)
                        last_line = lines[-1].strip()
                        if last_line and last_line != first_line:
                            multiline = f' [...] {last_line}'
                        else:
                            multiline = ' [...]'
                    else:
                        multiline = ''
                    print(f"[{item['seq']}] ⏺ {first_line}{multiline}")
                elif thinking:
                    # Show thinking content with first [...] last pattern
                    lines = thinking.split('\n')
                    first_line = lines[0]
                    
                    if len(lines) > 1:
                        # Show last line too for context
                        last_line = lines[-1].strip()
                        if last_line and last_line != first_line:
                            display_text = f'{first_line} [...] {last_line}'
                        else:
                            display_text = f'{first_line} [...]'
                    else:
                        display_text = first_line
                    
                    print(f"[{item['seq']}] ✻ Thinking… {display_text}")
                elif tools:
                    # Check if tools should be excluded
                    if exclude_filters and 'Tool' in exclude_filters:
                        # Skip tool announcement when tools are excluded
                        pass
                    else:
                        # Show tool invocations
                        tool_summary = ', '.join(tools)
                        # Show all tools - they're important context
                        print(f"[{item['seq']}] ⏺ [Tools: {tool_summary}]")
                else:
                    print(f"[{item['seq']}] ⏺ [No content]")
        
        elif item['type'] == 'tool':
            # Tool call display
            tc = item['data']
            tool_name = tc['name']
            params = tc.get('parameters', {})
            
            if display_mode in ['truncated', 'full']:
                # Truncated/Full mode matches reconstruct.jq format
                prefix = f"[{item['seq']}] " if show_numbers or display_mode == 'full' else ""
                if tool_name == 'TodoWrite':
                    print(f"{prefix}⏺ Update Todos")
                elif tool_name == 'TodoRead':
                    print(f"{prefix}⏺ Read Todos")
                else:
                    param_str = ""
                    if 'command' in params:
                        param_str = params['command']
                    elif 'file_path' in params:
                        param_str = params['file_path']
                    elif 'path' in params:
                        param_str = params['path']
                    elif 'pattern' in params:
                        param_str = params['pattern']
                    elif 'query' in params:
                        param_str = params['query']
                    elif 'url' in params:
                        param_str = params['url']
                    elif 'description' in params:
                        param_str = params['description']
                    else:
                        for v in params.values():
                            if isinstance(v, str):
                                param_str = v
                                break
                        if not param_str and params:
                            param_str = str(list(params.values())[0])
                    
                    if display_mode == 'full' and 'command' in params:
                        print(f"{prefix}⏺ {tool_name}({params['command']})")
                    else:
                        print(f"{prefix}⏺ {tool_name}({param_str})")
            else:
                # Compact mode - same as truncated but with sequence number and special TodoWrite handling
                if tool_name == 'TodoWrite':
                    todos = params.get('todos', [])
                    if todos:
                        status_counts = defaultdict(int)
                        for todo in todos:
                            status = todo.get('status', 'unknown')
                            status_counts[status] += 1
                        
                        total = len(todos)
                        status_parts = []
                        for status in ['completed', 'in_progress', 'pending']:
                            if status in status_counts:
                                status_parts.append(f"{status_counts[status]} {status}")
                        
                        if status_parts:
                            print(f"[{item['seq']}] ⏺ TodoWrite: Updated {total} todos ({', '.join(status_parts)})")
                        else:
                            print(f"[{item['seq']}] ⏺ TodoWrite: Updated {total} todos")
                    else:
                        print(f"[{item['seq']}] ⏺ TodoWrite: Updated 0 todos")
                elif tool_name == 'TodoRead':
                    print(f"[{item['seq']}] ⏺ Read Todos")
                elif tool_name == 'Grep':
                    # Special format for Grep: "pattern" in path
                    pattern = params.get('pattern', '')
                    path = params.get('path', '.')
                    print(f"[{item['seq']}] ⏺ Grep: \"{pattern}\" in {path}")
                elif tool_name == 'LS':
                    # Show path for LS
                    path = params.get('path', '.')
                    print(f"[{item['seq']}] ⏺ LS: {path}")
                elif tool_name == 'Glob':
                    # Show pattern for Glob
                    pattern = params.get('pattern', '')
                    path = params.get('path', '.')
                    print(f"[{item['seq']}] ⏺ Glob: {pattern} in {path}")
                elif tool_name == 'Task':
                    # Show description for Task
                    description = params.get('description', '')
                    print(f"[{item['seq']}] ⏺ Task: \"{description}\"")
                elif tool_name == 'WebFetch':
                    # Show URL for WebFetch
                    url = params.get('url', '')
                    print(f"[{item['seq']}] ⏺ WebFetch: {url}")
                elif tool_name == 'WebSearch':
                    # Show query for WebSearch
                    query = params.get('query', '')
                    print(f"[{item['seq']}] ⏺ WebSearch: \"{query}\"")
                elif tool_name == 'Bash':
                    # Format like Claude Code: Bash(command)
                    command = params.get('command', '')
                    command = command.split('\n')[0]
                    print(f"[{item['seq']}] ⏺ Bash({command})")
                elif tool_name in ['Edit', 'Write', 'MultiEdit']:
                    # Format like Claude Code: Tool(filename)
                    file_path = params.get('file_path', '')
                    print(f"[{item['seq']}] ⏺ {tool_name}({file_path})")
                elif tool_name == 'Read':
                    # Format like Claude Code: Read(filename)
                    file_path = params.get('file_path', '')
                    print(f"[{item['seq']}] ⏺ Read({file_path})")
                else:
                    param_str = ""
                    if 'command' in params:
                        param_str = params['command']
                        param_str = param_str.split('\n')[0]
                    elif 'file_path' in params:
                        param_str = params['file_path']
                    elif 'path' in params:
                        param_str = params['path']
                    elif 'pattern' in params:
                        param_str = params['pattern']
                    elif 'query' in params:
                        param_str = params['query']
                    elif 'url' in params:
                        param_str = params['url']
                    elif 'description' in params:
                        param_str = params['description']
                    else:
                        for v in params.values():
                            if isinstance(v, str):
                                param_str = v
                                break
                        if not param_str and params:
                            param_str = str(list(params.values())[0])
                    
                    # Handle multiline parameters consistently with other displays
                    lines = param_str.split('\n')
                    first_line = lines[0].strip()
                    
                    if len(lines) > 1:
                        # Show first [...] last pattern like other multiline content
                        last_line = lines[-1].strip()
                        if last_line and last_line != first_line:
                            param_display = f'{first_line} [...] {last_line}'
                        else:
                            param_display = f'{first_line} [...]'
                    else:
                        # Single line - just use it
                        param_display = first_line
                    
                    # Truncate very long single lines
                    if len(param_display) > 80:
                        param_display = param_display[:77] + ' [...]'
                    
                    print(f"[{item['seq']}] ⏺ {tool_name}({param_display})")
    
    def show_file_changes(self):
        """Show all file modifications grouped by file."""
        filtered_items = self.filter_timeline(include_filters=['Edit', 'Write', 'MultiEdit'])
        
        file_changes = defaultdict(list)
        for item in filtered_items:
            if item['type'] == 'tool':
                tc = item['data']
                path = tc['parameters'].get('file_path', 'unknown')
                file_changes[path].append((item['seq'], tc['name']))
        
        for path, changes in sorted(file_changes.items()):
            display_path = path.split('/')[-1] if '/' in path else path
            print(f"\n{display_path}: {len(changes)} changes")
            for seq, tool in changes[:5]:  # Show first 5
                print(f"  [{seq}] ⏺ {tool}")
            if len(changes) > 5:
                print(f"  ... and {len(changes)-5} more")
    
    def show_created_files(self):
        """Show files created with Write tool."""
        filtered_items = self.filter_timeline(include_filters=['Write'])
        
        for item in filtered_items:
            if item['type'] == 'tool':
                tc = item['data']
                path = tc['parameters'].get('file_path', '')
                content = tc['parameters'].get('content', '')
                if path:
                    print(f"\n[{item['seq']}] {path.split('/')[-1]}")
                    lines = content.split('\n')
                    # Show first few lines with proper truncation
                    for i, line in enumerate(lines[:5]):
                        if i == 0 and len(lines) > 1:
                            # First line of multiline content
                            print(f"   {line}")
                        elif i == 4 and len(lines) > 5:
                            # Last visible line when there's more
                            print(f"   [...] ({len(lines)} total lines)")
                            break
                        else:
                            print(f"   {line}")
    
    def search_timeline(self, pattern, case_sensitive=False):
        """Full text search across all timeline content.
        
        Args:
            pattern: Text to search for
            case_sensitive: Whether search is case sensitive (default: False)
            
        Returns:
            List of matching timeline indices (0-based)
        """
        matches = []
        search_pattern = pattern if case_sensitive else pattern.lower()
        
        for i, item in enumerate(self.timeline):
            found = False
            
            if item['type'] == 'message':
                msg = item['data']
                # Search in message text
                if msg.get('text'):
                    text = msg['text'] if case_sensitive else msg['text'].lower()
                    if search_pattern in text:
                        found = True
                
                # Search in tool results
                for result in msg.get('tool_results', []):
                    content = result.get('content', '')
                    
                    # Handle content that might be a list
                    if isinstance(content, list):
                        # Convert list to searchable text
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict) and 'text' in item:
                                text_parts.append(item['text'])
                            else:
                                text_parts.append(str(item))
                        content = '\n'.join(text_parts)
                    
                    content = content if case_sensitive else content.lower()
                    if search_pattern in content:
                        found = True
                        break
                        
            elif item['type'] == 'tool':
                tc = item['data']
                # Search in tool parameters
                params = tc.get('parameters', {})
                for key, value in params.items():
                    if isinstance(value, str):
                        value = value if case_sensitive else value.lower()
                        if search_pattern in value:
                            found = True
                            break
            
            if found:
                matches.append(i)
        
        return matches
    
    
    def export_range(self, start, end, output_file, include_filters=None, exclude_filters=None):
        """Export a range of events from timeline with optional filtering."""
        # Build full timeline
        timeline = self._build_timeline()
        
        # Create indices list for the specified range
        indices = list(range(start, end + 1))
        
        # Get filtered items using the same logic as show_timeline_with_filters
        include_list = include_filters if include_filters else None
        exclude_list = exclude_filters if exclude_filters else None
        
        filtered_items = self.filter_timeline(indices, include_list, exclude_list, 
                                            include_tool_results=True)
        
        # Export raw JSONL objects
        json_items = []
        for item in filtered_items:
            raw_index = item.get('raw_index')
            if raw_index is not None and raw_index < len(self.raw_objects):
                # Output the original JSONL object
                json_items.append(self.raw_objects[raw_index])
            else:
                # For tool results (which don't have raw objects), create a minimal representation
                if item['type'] == 'tool':
                    tc = item['data']
                    json_item = {
                        'type': 'tool',
                        'name': tc['name'],
                        'parameters': tc.get('parameters', {}),
                        'timestamp': item.get('timestamp')
                    }
                    json_items.append(json_item)
        
        if output_file == '-':
            json.dump(json_items, sys.stdout, indent=2)
            sys.stdout.write('\n')
        else:
            with open(output_file, 'w') as f:
                json.dump(json_items, f, indent=2)
            print(f"\nExported {len(json_items)} events to {output_file}")
    
    def _parse_filter(self, filter_str):
        """Parse filter string supporting both tools and virtual entities.
        
        Formats:
        - Virtual entities: Message, Tool, User, Assistant
        - Tool filters: Edit, Bash(git *), Read(*.py)
        
        Returns:
            tuple: (filter_type, entity_name, pattern)
            filter_type: 'virtual' or 'tool'
            entity_name: Name of entity/tool
            pattern: Optional pattern for tools
        """
        # Virtual entities (case-insensitive)
        virtual_entities = {
            'message': 'message',
            'messages': 'message',
            'tool': 'tool', 
            'tools': 'tool',
            'user': 'user',
            'assistant': 'assistant'
        }
        
        filter_lower = filter_str.lower()
        if filter_lower in virtual_entities:
            return 'virtual', virtual_entities[filter_lower], None
        
        # Check for Tool(pattern) syntax specifically
        match = re.match(r'(\w+)\((.*)\)', filter_str)
        if match:
            entity = match.group(1)
            pattern = match.group(2)
            # Tool(pattern) is a special case for matching tool names
            if entity == 'Tool':
                return 'tool', 'Tool', pattern
            else:
                # Regular tool filters like Bash(git *)
                return 'tool', entity, pattern
        elif re.match(r'^\w+$', filter_str):
            return 'tool', filter_str, None
        
        return None, None, None
    
    def _parse_tool_filter(self, filter_str):
        """Parse 'Tool' or 'Tool(pattern)' format."""
        # Keep for backward compatibility
        match = re.match(r'(\w+)\((.*)\)', filter_str)
        if match:
            return match.group(1), match.group(2)
        elif re.match(r'^\w+$', filter_str):
            return filter_str, None  # No pattern means match all
        return None, None
    
    def _matches_filter(self, tool_call, tool_name, pattern):
        """Check if a tool call matches the filter using glob patterns."""
        # Special case for "Tool" meta-filter with pattern
        if tool_name == 'Tool' and pattern:
            # Match pattern against tool name itself
            return fnmatch.fnmatch(tool_call['name'], pattern)
        
        if tool_call['name'] != tool_name:
            return False
        
        if not pattern:
            return True
        
        params = tool_call.get('parameters', {})
        
        if tool_name in ['Edit', 'Write', 'MultiEdit', 'Read']:
            file_path = params.get('file_path', '')
            return fnmatch.fnmatch(file_path, pattern)
        
        elif tool_name == 'Bash':
            command = params.get('command', '')
            if '*' in pattern:
                return fnmatch.fnmatch(command, pattern)
            else:
                return command == pattern
        
        elif tool_name == 'Grep':
            grep_pattern = params.get('pattern', '')
            return fnmatch.fnmatch(grep_pattern, pattern)
        
        return False
    
    def _apply_filters(self, tool_calls, include_filters, exclude_filters):
        """Apply include/exclude filters to tool calls."""
        filtered = []
        
        for tc in tool_calls:
            if include_filters:
                included = False
                for inc_filter in include_filters:
                    tool, pattern = self._parse_tool_filter(inc_filter)
                    if tool and self._matches_filter(tc, tool, pattern):
                        included = True
                        break
                if not included:
                    continue
            
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
    
    def _is_todo_result(self, content):
        """Check if content appears to be a todo result."""
        todo_patterns = ['☐', '☒', '◐', '(P0)', '(P1)', '(P2)']
        return any(pattern in content for pattern in todo_patterns)
    
    def _format_todo_result_truncated(self, content):
        """Format todo result content for truncated display.
        
        Expected format based on Claude Code:
        ☒ Completed task (P0)
        ◐ In progress task (P1) 
        ☐ Pending task (P2)
        """
        if "Todos have been modified successfully" in content:
            print("  ⎿  ☒ Todos updated successfully")
            return
            
        lines = content.strip().split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if any(symbol in line for symbol in ['☐', '☒', '◐']):
                formatted_lines.append(f"     {line}")
            else:
                formatted_lines.append(f"     {line}")
        
        if formatted_lines:
            print(f"  ⎿  {formatted_lines[0][5:]}")
            for line in formatted_lines[1:]:
                print(line)

def find_session_file(identifier):
    """Find session file by any substring match."""
    import subprocess
    
    if Path(identifier).exists():
        return identifier
    
    search_dirs = [
        Path(__file__).parent.parent / 'github',
        Path.home() / '.claude' / 'projects'
    ]
    
    matches = []
    
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
    
    print(f"Found {len(matches)} matches for '{identifier}':")
    for i, match in enumerate(matches):
        for search_dir in search_dirs:
            if search_dir in match.parents:
                rel_path = match.relative_to(search_dir.parent)
                print(f"  {i+1}. {rel_path}")
                break
    
    choice = input("Select (1-N): ")
    return str(matches[int(choice)-1])

def main():
    parser = argparse.ArgumentParser(
        description='Explore Claude session logs. Shows summary by default.',
        epilog='Examples:\n'
               '  %(prog)s session.jsonl                    # Show summary\n'
               '  %(prog)s session.jsonl -t                 # Show full timeline\n'
               '  %(prog)s session.jsonl -t 10-20           # Show timeline items 10-20\n'
               '  %(prog)s session.jsonl -t -m              # Show all messages\n'
               '  %(prog)s session.jsonl -t -u              # Show user messages only\n'
               '  %(prog)s session.jsonl -t -T --no-tool-results  # Show tools without output\n'
               '  %(prog)s session.jsonl -t -i "Bash(git *)"  # Show git operations\n'
               '  %(prog)s session.jsonl --git              # Shortcut for git operations\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('session', help='Session file or any unique substring (issue-13, run ID, date, etc.)')
    parser.add_argument('-s', '--summary', action='store_true', help='Show summary')
    parser.add_argument('-t', '--timeline', action='store_true',
                        help='Show timeline')
    parser.add_argument('-g', '--git', action='store_true', help='Show git operations')
    parser.add_argument('-f', '--files', action='store_true', help='Show file changes (summary of edits per file)')
    parser.add_argument('-c', '--created', action='store_true', help='Show created files')
    parser.add_argument('-S', '--search', help='Full text search across all content (simple substring match). For patterns starting with --, use -S=pattern or --search=pattern')
    parser.add_argument('--export-json', nargs=2, metavar=('RANGE', 'OUTPUT'), 
                        help='Export tool calls in RANGE as JSON to FILE. RANGE can be: 5 (single), 1-50 (range), +10 (first 10), -20 (last 20)')
    parser.add_argument('--json', action='store_true',
                        help='Output timeline as JSON array to stdout (use with -t/--timeline)')
    parser.add_argument('--jsonl', action='store_true',
                        help='Output timeline as JSONL (newline-delimited JSON) to stdout (use with -t/--timeline)')
    parser.add_argument('-i', '--include', metavar='FILTERS',
                        help='Include filters: tools (Edit,Bash(git *)) or '
                             'virtual entities (Message,Tool,User,Assistant)')
    parser.add_argument('-x', '--exclude', metavar='FILTERS',
                        help='Exclude filters: tools or virtual entities')
    parser.add_argument('--truncated', action='store_true',
                        help='Show truncated console-style output (3-line preview)')
    parser.add_argument('--full', action='store_true',
                        help='Show full output without truncation')
    parser.add_argument('--no-tool-results', action='store_true',
                        help='When filtering for tools, exclude their results (default: include results)')
    parser.add_argument('--show-numbers', action='store_true',
                        help='Show sequence numbers in truncated mode even without filtering')
    
    # Context lines (like grep)
    parser.add_argument('-A', '--after-context', type=int, metavar='NUM',
                        help='Show NUM lines after each match')
    parser.add_argument('-B', '--before-context', type=int, metavar='NUM',
                        help='Show NUM lines before each match')
    parser.add_argument('-C', '--context', type=int, metavar='NUM',
                        help='Show NUM lines before and after each match')
    
    # Virtual entity shortcuts
    parser.add_argument('-M', dest='include_message', action='store_true',
                        help='Include all messages (shortcut for -i Message)')
    parser.add_argument('-U', dest='include_user', action='store_true',
                        help='Include user messages (shortcut for -i User)')
    parser.add_argument('-a', dest='include_assistant', action='store_true',
                        help='Include assistant messages (shortcut for -i Assistant)')
    parser.add_argument('-T', dest='include_tool', action='store_true',
                        help='Include all tools (shortcut for -i Tool)')
    
    parser.add_argument('indices', nargs='*', 
                        help='Indices/ranges: 5 (item 5), +10 (first 10), -20 (last 20), 10-30 (range), 60+ (from 60 onwards)')
    
    args = parser.parse_args()
    
    # Determine if timeline should be implicit
    has_filter_shortcuts = any([args.include_message, args.include_user, 
                               args.include_assistant, args.include_tool])
    has_filters = bool(args.include or args.exclude or has_filter_shortcuts)
    has_indices = bool(args.indices)
    
    # Timeline is implicit when using filters or ranges (but not with search)
    # Search handles its own display
    implicit_timeline = (has_filters or has_indices) and not args.search
    
    # Default to summary if no action specified
    if not any([args.summary, args.timeline, args.git, args.files, 
                args.created, args.search, args.export_json,
                implicit_timeline]):
        args.summary = True
    
    try:
        jsonl_file = find_session_file(args.session)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    explorer = SessionExplorer(jsonl_file)
    
    if args.summary:
        explorer.show_summary()
    
    # Show timeline if explicit -t or implicit (filters/ranges)
    if args.timeline or implicit_timeline:
        display_mode = 'compact'
        if args.truncated:
            display_mode = 'truncated'
        elif args.full:
            display_mode = 'full'
        
        # Parse indices if provided
        indices = None
        if args.indices:
            try:
                indices = parse_indices(args.indices, len(explorer.timeline))
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)
        
        # Build include filters from shortcuts
        include_filters = []
        if args.include:
            include_filters.extend(args.include.split(','))
        if args.include_message:
            include_filters.append('Message')
        if args.include_user:
            include_filters.append('User')
        if args.include_assistant:
            include_filters.append('Assistant')
        if args.include_tool:
            include_filters.append('Tool')
        
        # Join filters back into comma-separated string
        include_str = ','.join(include_filters) if include_filters else None
        
        # Handle context arguments
        before_context = args.before_context or 0
        after_context = args.after_context or 0
        if args.context:
            before_context = args.context
            after_context = args.context
        
        # Use show_timeline_with_filters for all timeline operations
        explorer.show_timeline_with_filters(indices, display_mode,
                                          include_str, args.exclude,
                                          not args.no_tool_results,
                                          args.show_numbers,
                                          args.json, args.jsonl,
                                          before_context, after_context)
    
    if args.git:
        display_mode = 'compact'
        if args.truncated:
            display_mode = 'truncated'
        elif args.full:
            display_mode = 'full'
        
        # Handle context arguments
        before_context = args.before_context or 0
        after_context = args.after_context or 0
        if args.context:
            before_context = args.context
            after_context = args.context
            
        if args.indices:
            try:
                indices = parse_indices(args.indices, len(explorer.timeline))
                explorer.show_timeline_with_filters(indices, display_mode, 
                                                    "Bash(git *)", args.exclude,
                                                    not args.no_tool_results,
                                                    args.show_numbers,
                                                    args.json, args.jsonl,
                                                    before_context, after_context)
            except ValueError as e:
                print(f"Error: {e}")
        else:
            explorer.show_timeline_with_filters(None, display_mode,
                                              "Bash(git *)", args.exclude,
                                              not args.no_tool_results,
                                              args.show_numbers,
                                              args.json, args.jsonl,
                                              before_context, after_context)
    
    if args.files:
        explorer.show_file_changes()
    
    if args.created:
        explorer.show_created_files()
    
    if args.search:
        # Parse indices if provided to filter search results
        indices = None
        if args.indices:
            try:
                indices = parse_indices(args.indices, len(explorer.timeline))
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)
        
        # Build include filters from shortcuts and args
        include_filters = []
        if args.include:
            include_filters.extend(args.include.split(','))
        if args.include_message:
            include_filters.append('Message')
        if args.include_user:
            include_filters.append('User')
        if args.include_assistant:
            include_filters.append('Assistant')
        if args.include_tool:
            include_filters.append('Tool')
        
        # Join filters back into comma-separated string
        include_str = ','.join(include_filters) if include_filters else None
        
        # Search and show results with context
        matches = explorer.search_timeline(args.search)
        
        # Filter matches by indices if provided
        if indices is not None:
            matches = [m for m in matches if m in indices]
        
        if matches:
            print(f"Found {len(matches)} matches for '{args.search}':")
            
            # Handle context arguments
            before_context = args.before_context or 0
            after_context = args.after_context or 0
            if args.context:
                before_context = args.context
                after_context = args.context
            
            # Convert matches to indices parameter for filter_timeline
            # and show with context, applying include/exclude filters
            explorer.show_timeline_with_filters(
                indices=matches, 
                display_mode='truncated' if args.truncated else ('full' if args.full else 'compact'),
                include_filters=include_str,
                exclude_filters=args.exclude,
                include_tool_results=not args.no_tool_results,
                force_show_numbers=True,
                json_output=args.json,
                jsonl_output=args.jsonl,
                before_context=before_context,
                after_context=after_context
            )
        else:
            if indices is not None:
                print(f"No matches found for '{args.search}' in the specified range")
            else:
                print(f"No matches found for '{args.search}'")
    
    if args.export_json:
        range_str, output = args.export_json
        start_idx, end_idx = parse_range(range_str, len(explorer.tool_calls))
        include_filters = args.include.split(',') if args.include else None
        exclude_filters = args.exclude.split(',') if args.exclude else None
        explorer.export_range(start_idx + 1, end_idx, output, 
                            include_filters=include_filters,
                            exclude_filters=exclude_filters)

if __name__ == "__main__":
    main()