#!/usr/bin/env python3
import json
import sys
from typing import Dict, List, Any

def extract_tool_calls(file_path: str) -> None:
    commits = []
    current_commit_edits = []
    current_commit_message = None
    
    with open(file_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                
                # Check for tool use
                if data.get('type') == 'assistant' and 'message' in data:
                    content = data['message'].get('content', [])
                    for item in content:
                        if item.get('type') == 'tool_use':
                            tool_name = item.get('name')
                            tool_input = item.get('input', {})
                            
                            if tool_name in ['Edit', 'MultiEdit', 'Write']:
                                edit_info = {
                                    'tool': tool_name,
                                    'file_path': tool_input.get('file_path'),
                                    'tool_use_id': item.get('id')
                                }
                                
                                if tool_name == 'Edit':
                                    edit_info['old_string'] = tool_input.get('old_string', '')[:100] + '...' if len(tool_input.get('old_string', '')) > 100 else tool_input.get('old_string', '')
                                    edit_info['new_string'] = tool_input.get('new_string', '')[:100] + '...' if len(tool_input.get('new_string', '')) > 100 else tool_input.get('new_string', '')
                                    edit_info['replace_all'] = tool_input.get('replace_all', False)
                                elif tool_name == 'MultiEdit':
                                    edit_info['edits_count'] = len(tool_input.get('edits', []))
                                    edit_info['edits'] = []
                                    for e in tool_input.get('edits', []):
                                        edit_info['edits'].append({
                                            'old': (e.get('old_string', '')[:50] + '...') if len(e.get('old_string', '')) > 50 else e.get('old_string', ''),
                                            'new': (e.get('new_string', '')[:50] + '...') if len(e.get('new_string', '')) > 50 else e.get('new_string', ''),
                                            'replace_all': e.get('replace_all', False)
                                        })
                                elif tool_name == 'Write':
                                    edit_info['content_preview'] = tool_input.get('content', '')[:200] + '...' if len(tool_input.get('content', '')) > 200 else tool_input.get('content', '')
                                
                                current_commit_edits.append(edit_info)
                            
                            # Check for git commit commands
                            elif tool_name == 'Bash':
                                command = tool_input.get('command', '')
                                if 'git commit' in command and current_commit_edits:
                                    # Extract commit message
                                    import re
                                    match = re.search(r'-m\s*"([^"]+)"', command)
                                    if not match:
                                        match = re.search(r"cat <<'EOF'(.+?)EOF", command, re.DOTALL)
                                    
                                    if match:
                                        commit_msg = match.group(1).strip()
                                        commits.append({
                                            'message': commit_msg,
                                            'edits': current_commit_edits.copy()
                                        })
                                        current_commit_edits = []
                
            except json.JSONDecodeError:
                continue
    
    # Print results
    print(f"Found {sum(len(c['edits']) for c in commits)} tool calls across {len(commits)} commits\n")
    
    for i, commit in enumerate(commits, 1):
        print(f"\n{'='*80}")
        print(f"COMMIT {i}: {commit['message'][:100]}...")
        print(f"{'='*80}")
        print(f"Total edits in this commit: {len(commit['edits'])}\n")
        
        for j, edit in enumerate(commit['edits'], 1):
            print(f"  {j}. {edit['tool']} - {edit['file_path']}")
            if edit['tool'] == 'Edit':
                print(f"     Old: {edit['old_string']}")
                print(f"     New: {edit['new_string']}")
                if edit.get('replace_all'):
                    print(f"     Replace all: True")
            elif edit['tool'] == 'MultiEdit':
                print(f"     Number of edits: {edit['edits_count']}")
                for k, e in enumerate(edit['edits'], 1):
                    print(f"     Edit {k}:")
                    print(f"       Old: {e['old']}")
                    print(f"       New: {e['new']}")
                    if e.get('replace_all'):
                        print(f"       Replace all: True")
            elif edit['tool'] == 'Write':
                print(f"     Content preview: {edit['content_preview']}")
            print()

if __name__ == "__main__":
    extract_tool_calls("claude-dev-log-diary/github/20250723-2239-issue-13_run-16483315365_session-8eb20bb1-d6aa-45f3-b2c7-4b7f3f40c11e.jsonl")