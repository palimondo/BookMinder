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
        range_str: Range string like "5", "+5", "-5", "1-50", "50-"
        total_items: Total number of items for bounds checking
        
    Returns:
        tuple: (start_idx, end_idx) as 0-based indices
    """
    # Handle single positive number as specific index
    if range_str.isdigit():
        n = int(range_str) - 1  # Convert to 0-based
        if n >= total_items:
            raise ValueError(f"Index {range_str} out of range (max {total_items})")
        return n, n + 1
    
    # Handle +N for first N items (head)
    if range_str.startswith('+') and range_str[1:].isdigit():
        n = int(range_str[1:])
        return 0, min(n, total_items)
    
    if '-' not in range_str:
        raise ValueError(f"Invalid range format: {range_str}. Use format like '5', '+5', '-5', '1-50'")
    
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
        # Silent parsing - summary will show the session file
        
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
                                        'timestamp': obj.get('timestamp')
                                    })
                
                # Store assistant message with text and tool summary
                if assistant_text or tool_uses:
                    self.messages.append({
                        'type': 'assistant',
                        'text': '\n'.join(assistant_text) if assistant_text else None,
                        'tools': tool_uses,
                        'timestamp': obj.get('timestamp')
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
        
        # Don't print redundant message during parsing
        
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
                'timestamp': msg.get('timestamp')
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
                'timestamp': tc.get('timestamp')
            })
            tool_index += 1
        
        # Sort by timestamp to get chronological order
        self.timeline.sort(key=lambda x: x['timestamp'] or '')
        
        # Reassign sequence numbers after sorting
        for i, item in enumerate(self.timeline):
            item['seq'] = i + 1
    
    def show_summary(self):
        """Show session summary in YAML-style hierarchy."""
        # Count tool calls by type
        tool_counts = defaultdict(int)
        git_operations = 0
        git_commits = 0
        
        for tc in self.tool_calls:
            tool_counts[tc['name']] += 1
            if tc['name'] == 'Bash':
                cmd = tc['parameters'].get('command', '')
                if cmd.startswith('git'):
                    git_operations += 1
                    if 'git commit' in cmd:
                        git_commits += 1
        
        # Count messages more accurately
        user_inputs = 0
        tool_results = 0
        assistant_text = 0
        assistant_tools = 0
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
                if m.get('text'):
                    assistant_text += 1
                if m.get('tools'):
                    assistant_tools += 1
        
        # Count files modified
        files_modified = set()
        for tc in self.tool_calls:
            if tc['name'] in ['Edit', 'MultiEdit', 'Write']:
                path = tc['parameters'].get('file_path', '')
                if path:
                    files_modified.add(path)
        
        # Get session time metadata
        timestamps = [item['timestamp'] for item in self.timeline if item.get('timestamp')]
        if timestamps:
            # Parse ISO timestamps
            from datetime import datetime
            try:
                start_time = datetime.fromisoformat(timestamps[0].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(timestamps[-1].replace('Z', '+00:00'))
                duration = end_time - start_time
                
                # Format duration nicely
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
        
        # Print YAML-style output
        print(f"Session: {Path(self.jsonl_file).name}")
        print()
        if start_time and end_time:
            print("Metadata:")
            print(f"  Started: {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"  Ended: {end_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"  Duration: {duration_str}")
            print()
        print(f"Timeline: {len(self.timeline)} events")
        print(f"  User inputs: {user_inputs}")
        print(f"  Tool results: {tool_results}")
        print(f"  Assistant messages: {len([m for m in self.messages if m['type'] == 'assistant'])}")
        print(f"    Text responses: {assistant_text}")
        print(f"    Tool invocations: {len(self.tool_calls)}")
        
        # Print tool breakdown with proper indentation
        for tool, count in sorted(tool_counts.items(), key=lambda x: -x[1]):
            print(f"      {tool}: {count}")
            if tool == 'Bash' and git_operations > 0:
                print(f"        Git operations: {git_operations}")
                if git_commits > 0:
                    print(f"          Commits: {git_commits}")
        
        print()
        print(f"Files modified: {len(files_modified)}")
        if user_interruptions > 0:
            print(f"User interruptions: {user_interruptions}")
    
    def filter_timeline(self, indices=None, include_filters=None, exclude_filters=None, include_tool_results=True):
        """Filter timeline based on indices and include/exclude filters.
        
        Args:
            indices: List of 0-based indices to show (if None, show all)
            include_filters: List of filter strings (e.g. ["Bash(git *)", "Edit"])
            exclude_filters: List of filter strings
            include_tool_results: When filtering for tools, also include their results (default: True)
            
        Returns:
            List of filtered timeline items
        """
        filtered_items = []
        
        for i, item in enumerate(self.timeline):
            # Skip if not in requested indices
            if indices is not None and i not in indices:
                continue
            
            # For tool items, apply include/exclude filters
            if item['type'] == 'tool':
                # Extract just the tool calls for filtering
                tool_call = item['data']
                if include_filters or exclude_filters:
                    # Use existing _apply_filters logic
                    filtered_tools = self._apply_filters([tool_call], include_filters, exclude_filters)
                    if not filtered_tools:
                        continue
            
            # For message items, check if we should include them
            elif item['type'] == 'message':
                msg = item['data']
                # Check if this is a tool result message
                is_tool_result = msg.get('tool_results', [])
                
                # If only tool filters specified, optionally include tool results
                if include_filters:
                    # Include tool results when filtering for tools if flag is set
                    if is_tool_result and include_tool_results:
                        # Check if the previous item was an included tool
                        if i > 0 and filtered_items and filtered_items[-1]['type'] == 'tool':
                            # Include this tool result
                            pass
                        else:
                            continue
                    elif is_tool_result and not include_tool_results:
                        # Skip tool results when flag is False
                        continue
                    else:
                        # Check if any filter explicitly includes messages/conversation
                        message_included = any(f.lower() in ['message', 'messages', 'conversation'] 
                                             for f in include_filters)
                        if not message_included:
                            continue
                
                # Check excludes for messages
                if exclude_filters:
                    message_excluded = any(f.lower() in ['message', 'messages', 'conversation'] 
                                         for f in exclude_filters)
                    if message_excluded:
                        continue
            
            filtered_items.append(item)
        
        return filtered_items
    
    def show_timeline_with_filters(self, indices=None, display_mode='compact', 
                                    include_filters=None, exclude_filters=None,
                                    include_tool_results=True, force_show_numbers=False):
        """Show timeline with indices and include/exclude filters.
        
        Args:
            indices: List of 0-based indices to show (if None, show all)
            display_mode: 'compact' (default), 'truncated', or 'full'
            include_filters: Comma-separated filter string (e.g. "Bash(git *),Edit")
            exclude_filters: Comma-separated filter string
            include_tool_results: Whether to include tool results when filtering
            force_show_numbers: Force showing sequence numbers in truncated mode
        """
        if display_mode != 'truncated':
            print("\n=== TIMELINE ===")
        
        # Parse filters
        include_list = include_filters.split(',') if include_filters else None
        exclude_list = exclude_filters.split(',') if exclude_filters else None
        
        # Use centralized filtering
        filtered_items = self.filter_timeline(indices, include_list, exclude_list, include_tool_results)
        
        # Determine if we should show numbers in truncated mode
        # Show numbers when: 1) filtering is applied or 2) not showing full timeline or 3) force flag
        has_filtering = indices or include_list or exclude_list
        show_numbers = display_mode == 'truncated' and (has_filtering or force_show_numbers)
        
        # Display the filtered items
        for item in filtered_items:
            self._display_timeline_item(item, display_mode, show_numbers)
    
    def show_timeline_indices(self, filter_type='all', indices=None, display_mode='compact'):
        """Show timeline with specific indices.
        
        Args:
            filter_type: 'all' (default), 'tools', 'conversation', or specific tool name
            indices: List of 0-based indices to show (if None, show all)
            display_mode: 'compact' (default), 'truncated', or 'full'
        """
        if display_mode != 'truncated':
            print("\n=== TIMELINE ===")
        
        # Use centralized filtering based on filter_type
        if filter_type == 'tools':
            # Show only tools
            filtered_items = [item for item in self.filter_timeline(indices) if item['type'] == 'tool']
        elif filter_type == 'conversation':
            # Show only messages
            filtered_items = [item for item in self.filter_timeline(indices) if item['type'] == 'message']
        elif filter_type not in ['all', 'tools', 'conversation']:
            # Specific tool filter
            include_filters = [filter_type]
            filtered_items = self.filter_timeline(indices, include_filters)
        else:
            # Show all
            filtered_items = self.filter_timeline(indices)
        
        # Show numbers in truncated mode when filtering
        has_filtering = filter_type != 'all' or indices
        show_numbers = display_mode == 'truncated' and has_filtering
        
        # Show the filtered items
        for item in filtered_items:
            self._display_timeline_item(item, display_mode, show_numbers)
    
    def _display_timeline_item(self, item, display_mode='compact', show_numbers=False):
        """Display a single timeline item based on display mode.
        
        Args:
            item: Timeline item to display
            display_mode: 'compact', 'truncated', or 'full'
            show_numbers: Force showing sequence numbers in truncated mode
        """
        if item['type'] == 'message':
            msg = item['data']
            if msg['type'] == 'user' and display_mode == 'truncated':
                # Truncated mode - reconstruct.jq style
                text = msg.get('text', '')
                tool_results = msg.get('tool_results', [])
                is_slash = msg.get('is_slash_command', False)
                slash_cmd = msg.get('slash_command', '')
                
                # Handle different user message types
                prefix = f"[{item['seq']}] " if show_numbers else ""
                if is_slash and slash_cmd:
                    print(f"{prefix}> /{slash_cmd}")
                elif text == '[Interrupted by user]':
                    print(f"{prefix}> [Request interrupted by user]")
                elif text and not tool_results:
                    # Regular user message
                    print(f"{prefix}> {text}")
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
                            
                        print("  ⎿  Waiting…\n")
                        
                        if content:
                            # Check if this is a todo result
                            if self._is_todo_result(content):
                                # Parse and format todo items
                                self._format_todo_result_truncated(content)
                            else:
                                # Format the output with truncation
                                truncated = self._format_truncated_output(content, 3)
                                # Indent each line
                                for line in truncated.split('\n'):
                                    print(f"  ⎿  {line}")
                        else:
                            # Empty result
                            print("  ⎿  (No content)")
                        print()  # Extra newline after tool results
            
            elif msg['type'] == 'assistant' and display_mode == 'truncated':
                # Assistant messages in truncated mode
                text = msg.get('text', '')
                tools = msg.get('tools', [])
                
                if text:
                    # Show full assistant text (reconstruct.jq shows all of it)
                    prefix = f"[{item['seq']}] " if show_numbers else ""
                    print(f"{prefix}⏺ {text}\n")
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
                        return
                
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
                        # Show last line too for context (same as user messages)
                        last_line = lines[-1].strip()
                        if last_line and last_line != first_line:
                            multiline = f' [...] {last_line}'
                        else:
                            multiline = ' [...]'
                    else:
                        multiline = ''
                    print(f"[{item['seq']}] ⏺ {first_line}{multiline}")
                elif tools:
                    # List tools used (tools is a list of strings)
                    print(f"[{item['seq']}] ⏺ [Used tools: {', '.join(tools)}]")
                else:
                    print(f"[{item['seq']}] ⏺ [No content]")
        
        elif item['type'] == 'tool':
            # Tool call display
            tc = item['data']
            tool_name = tc['name']
            params = tc.get('parameters', {})
            
            if display_mode == 'truncated':
                # Truncated mode matches reconstruct.jq format exactly
                prefix = f"[{item['seq']}] " if show_numbers else ""
                if tool_name == 'TodoWrite':
                    print(f"{prefix}⏺ Update Todos")
                elif tool_name == 'TodoRead':
                    print(f"{prefix}⏺ Read Todos")
                else:
                    # Standard format: ToolName(parameter)
                    # Extract the main parameter based on common patterns
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
                        # Use first string parameter or convert to string
                        for v in params.values():
                            if isinstance(v, str):
                                param_str = v
                                break
                        if not param_str and params:
                            param_str = str(list(params.values())[0])
                    
                    print(f"{prefix}⏺ {tool_name}({param_str})")
            else:
                # Compact mode - same as truncated but with sequence number and special TodoWrite handling
                if tool_name == 'TodoWrite':
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
                    # Special format for Bash: $ command
                    command = params.get('command', '')
                    # Take first line for multi-line commands
                    command = command.split('\n')[0]
                    print(f"[{item['seq']}] ⏺ Bash: $ {command}")
                elif tool_name in ['Edit', 'Write', 'MultiEdit']:
                    # Special format for file edits: → filename
                    file_path = params.get('file_path', '')
                    print(f"[{item['seq']}] ⏺ {tool_name}: → {file_path}")
                elif tool_name == 'Read':
                    # Special format for Read: ← filename
                    file_path = params.get('file_path', '')
                    print(f"[{item['seq']}] ⏺ Read: ← {file_path}")
                else:
                    # Generic format for other tools
                    param_str = ""
                    if 'command' in params:
                        param_str = params['command']
                        # Take first line for multi-line commands
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
                        # Use first string parameter or convert to string
                        for v in params.values():
                            if isinstance(v, str):
                                param_str = v
                                break
                        if not param_str and params:
                            param_str = str(list(params.values())[0])
                    
                    print(f"[{item['seq']}] ⏺ {tool_name}({param_str})")
    
    def show_timeline(self, filter_type='all', start=None, end=None, display_mode='compact'):
        """Show timeline of events.
        
        Args:
            filter_type: 'all' (default), 'tools', 'conversation', or specific tool name
            start: Starting index (1-based, inclusive)
            end: Ending index (1-based, inclusive)
            display_mode: 'compact' (default), 'truncated', or 'full'
        """
        if display_mode != 'truncated':
            print("\n=== TIMELINE ===")
        
        # Convert start/end to indices for filter_timeline
        indices = None
        if start is not None or end is not None:
            start_idx = (start - 1) if start else 0
            end_idx = end if end else len(self.timeline)
            indices = list(range(start_idx, end_idx))
        
        # Use centralized filtering based on filter_type
        if filter_type == 'tools':
            # Show only tools
            include_filters = None
            filtered_items = [item for item in self.filter_timeline(indices) if item['type'] == 'tool']
        elif filter_type == 'conversation':
            # Show only messages
            filtered_items = [item for item in self.filter_timeline(indices) if item['type'] == 'message']
        elif filter_type not in ['all', 'tools', 'conversation']:
            # Specific tool filter
            include_filters = [filter_type]
            filtered_items = self.filter_timeline(indices, include_filters)
        else:
            # Show all
            filtered_items = self.filter_timeline(indices)
        
        # Determine if we should show numbers in truncated mode
        # Show numbers when filtering is applied (not showing full timeline)
        has_filtering = filter_type != 'all' or indices is not None
        show_numbers = display_mode == 'truncated' and has_filtering
        
        # Display using the centralized display method
        for item in filtered_items:
            self._display_timeline_item(item, display_mode, show_numbers)
    
    def show_git_operations(self):
        """Show all git operations. DEPRECATED: Use -t --include 'Bash(git *)' instead."""
        print("\n=== GIT OPERATIONS ===")
        print("Note: --git is now a shortcut for: -t --include 'Bash(git *)'")
        # This method is kept for backward compatibility but the main logic
        # is now handled through the timeline filtering
    
    def show_file_changes(self):
        """Show all file modifications.
        
        DEPRECATED: Use --timeline --include "Edit,Write,MultiEdit" instead.
        """
        print("\n=== FILE CHANGES ===")
        print("Note: --files is deprecated. Use --timeline --include \"Edit,Write,MultiEdit\" instead.")
        
        # Use centralized filtering to get file editing tools
        filtered_items = self.filter_timeline(include_filters=['Edit', 'Write', 'MultiEdit'])
        
        # Group by file path
        file_changes = defaultdict(list)
        for item in filtered_items:
            if item['type'] == 'tool':
                tc = item['data']
                path = tc['parameters'].get('file_path', 'unknown')
                file_changes[path].append((item['seq'], tc['name']))
        
        # Display grouped by file
        for path, changes in sorted(file_changes.items()):
            display_path = path.split('/')[-1] if '/' in path else path
            print(f"\n{display_path}: {len(changes)} changes")
            for seq, tool in changes[:5]:  # Show first 5
                print(f"  [{seq}] ⏺ {tool}")
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
        """Display conversation between user and assistant.
        
        DEPRECATED: Use --timeline conversation instead.
        This method is kept for backward compatibility.
        """
        print("\n=== CONVERSATION ===")
        print("Note: --conversation is deprecated. Use --timeline conversation instead.")
        
        # Convert to timeline display
        self.show_timeline('conversation', start, end, display_mode='compact')
    
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
        """Parse 'Tool' or 'Tool(pattern)' format."""
        match = re.match(r'(\w+)\((.*)\)', filter_str)
        if match:
            return match.group(1), match.group(2)
        elif re.match(r'^\w+$', filter_str):
            return filter_str, None  # No pattern means match all
        return None, None
    
    def _matches_filter(self, tool_call, tool_name, pattern):
        """Check if a tool call matches the filter using glob patterns."""
        if tool_call['name'] != tool_name:
            return False
        
        # If no pattern specified, match all
        if not pattern:
            return True
        
        params = tool_call.get('parameters', {})
        
        # For file operations, match against file_path
        if tool_name in ['Edit', 'Write', 'MultiEdit', 'Read']:
            file_path = params.get('file_path', '')
            return fnmatch.fnmatch(file_path, pattern)
        
        # For Bash, match against command
        elif tool_name == 'Bash':
            command = params.get('command', '')
            # Handle exact match or glob patterns
            if '*' in pattern:
                return fnmatch.fnmatch(command, pattern)
            else:
                # Exact match (like Claude Code's "Bash(npm run build)")
                return command == pattern
        
        # For Grep, match against pattern parameter
        elif tool_name == 'Grep':
            grep_pattern = params.get('pattern', '')
            return fnmatch.fnmatch(grep_pattern, pattern)
        
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
    
    def _is_todo_result(self, content):
        """Check if content appears to be a todo result."""
        # Look for patterns that indicate todo items
        # Common patterns: "☐", "☒", "◐", "(P0)", "(P1)", "(P2)"
        todo_patterns = ['☐', '☒', '◐', '(P0)', '(P1)', '(P2)']
        return any(pattern in content for pattern in todo_patterns)
    
    def _format_todo_result_truncated(self, content):
        """Format todo result content for truncated display.
        
        Expected format based on Claude Code:
        ☒ Completed task (P0)
        ◐ In progress task (P1) 
        ☐ Pending task (P2)
        """
        # Check if this is the standard "Todos have been modified" message
        if "Todos have been modified successfully" in content:
            # Parse the actual todo list from the current todo state
            # For now, just show the success message
            print("  ⎿  ☒ Todos updated successfully")
            return
            
        # Parse todo items from the content
        lines = content.strip().split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this looks like a todo item with checkbox symbols
            if any(symbol in line for symbol in ['☐', '☒', '◐']):
                # This is a todo item - add proper spacing
                formatted_lines.append(f"     {line}")
            else:
                # Regular line - might be a header or other content
                formatted_lines.append(f"     {line}")
        
        # Print with the tool result indicator only on the first line
        if formatted_lines:
            print(f"  ⎿  {formatted_lines[0][5:]}")  # Remove the 5 spaces from first line
            for line in formatted_lines[1:]:
                print(line)

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
    parser = argparse.ArgumentParser(
        description='Explore Claude session logs. Shows summary by default.',
        epilog='Examples:\n'
               '  %(prog)s session.jsonl                    # Show summary\n'
               '  %(prog)s session.jsonl -t                 # Show full timeline\n'
               '  %(prog)s session.jsonl -t 10-20           # Show timeline items 10-20\n'
               '  %(prog)s session.jsonl -t --include "Bash(git *)"  # Show git operations\n'
               '  %(prog)s session.jsonl --git              # Shortcut for git operations\n'
               '  %(prog)s session.jsonl --files            # Show file edits summary\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('jsonl', help='Session file or any unique substring (issue-13, run ID, date, etc.)')
    parser.add_argument('--summary', '-s', action='store_true', help='Show summary')
    parser.add_argument('--timeline', '-t', action='store_true',
                        help='Show timeline')
    parser.add_argument('--git', '-g', action='store_true', help='Show git operations')
    parser.add_argument('--files', '-f', action='store_true', help='Show file changes (summary of edits per file)')
    parser.add_argument('--created', '-c', action='store_true', help='Show created files')
    parser.add_argument('--conversation', action='store_true',
                        help='Show conversation messages')
    parser.add_argument('--search', help='Search bash commands')
    parser.add_argument('--export-json', nargs=2, metavar=('RANGE', 'OUTPUT'), 
                        help='Export tool calls in RANGE as JSON. RANGE can be: 5 (single), 1-50 (range), +10 (first 10), -20 (last 20)')
    parser.add_argument('--include', metavar='FILTERS',
                        help='Include only tools matching filters, comma-separated. '
                             'Follows Claude Code syntax: "Edit,Bash(git add *)"')
    parser.add_argument('--exclude', metavar='FILTERS',
                        help='Exclude tools matching filters, comma-separated. '
                             'Follows Claude Code syntax: "TodoWrite,Bash(npm test:*)"')
    parser.add_argument('--truncated', action='store_true',
                        help='Show truncated console-style output (3-line preview)')
    parser.add_argument('--no-tool-results', action='store_true',
                        help='When filtering for tools, exclude their results (default: include results)')
    parser.add_argument('--show-numbers', action='store_true',
                        help='Show sequence numbers in truncated mode even without filtering')
    parser.add_argument('--full', action='store_true',
                        help='Show full output without truncation')
    parser.add_argument('indices', nargs='*', 
                        help='Indices/ranges: 5 (item 5), +10 (first 10), -20 (last 20), 10-30 (range)')
    
    args = parser.parse_args()
    
    # Default to showing summary if no options
    if not any([args.summary, args.timeline, args.git, args.files, 
                args.created, args.conversation, args.search, args.export_json]):
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
    
    if args.timeline:
        # Determine display mode
        display_mode = 'compact'
        if args.truncated:
            display_mode = 'truncated'
        elif args.full:
            display_mode = 'full'
        
        # Parse indices if provided
        if args.indices:
            try:
                indices = parse_indices(args.indices, len(explorer.timeline))
                explorer.show_timeline_with_filters(indices, display_mode, 
                                                    args.include, args.exclude,
                                                    not args.no_tool_results,
                                                    args.show_numbers)
            except ValueError as e:
                print(f"Error: {e}")
        else:
            # Show all items
            explorer.show_timeline_with_filters(None, display_mode,
                                              args.include, args.exclude,
                                              not args.no_tool_results,
                                              args.show_numbers)
    
    if args.git:
        # --git is a shortcut for --timeline --include "Bash(git *)"
        display_mode = 'compact'
        if args.truncated:
            display_mode = 'truncated'
        elif args.full:
            display_mode = 'full'
            
        # Parse indices if provided
        if args.indices:
            try:
                indices = parse_indices(args.indices, len(explorer.timeline))
                explorer.show_timeline_with_filters(indices, display_mode, 
                                                    "Bash(git *)", args.exclude,
                                                    not args.no_tool_results,
                                                    args.show_numbers)
            except ValueError as e:
                print(f"Error: {e}")
        else:
            explorer.show_timeline_with_filters(None, display_mode,
                                              "Bash(git *)", args.exclude,
                                              not args.no_tool_results,
                                              args.show_numbers)
    
    if args.files:
        explorer.show_file_changes()
    
    if args.created:
        explorer.show_created_files()
    
    if args.search:
        explorer.search_commands(args.search)
    
    if args.conversation:
        # --conversation is deprecated, but handle it for backward compatibility
        if args.indices:
            try:
                indices = parse_indices(args.indices, len(explorer.timeline))
                # Convert conversation to timeline with indices
                print("\n=== CONVERSATION ===")
                print("Note: --conversation is deprecated. Use --timeline conversation instead.")
                filtered_items = explorer.filter_timeline(indices)
                # Only show message items
                for item in filtered_items:
                    if item['type'] == 'message':
                        explorer._display_timeline_item(item, 'compact')
            except ValueError as e:
                print(f"Error: {e}")
        else:
            explorer.show_conversation()
    
    if args.export_json:
        range_str, output = args.export_json
        # Parse the range using our consistent syntax
        start_idx, end_idx = parse_range(range_str, len(explorer.tool_calls))
        # Split comma-separated filters
        include_filters = args.include.split(',') if args.include else None
        exclude_filters = args.exclude.split(',') if args.exclude else None
        # Export using 1-based indices for the export_range method
        explorer.export_range(start_idx + 1, end_idx, output, 
                            include_filters=include_filters,
                            exclude_filters=exclude_filters)

if __name__ == "__main__":
    main()