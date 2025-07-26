#!/bin/bash
# Extract commits from Claude's session log

echo "Extracting commits from Claude's session..."

# Find all git commit commands
echo -e "\n=== Git Commits ==="
grep -n '"name": "Bash"' "$1" | while read -r line; do
    line_num=$(echo "$line" | cut -d: -f1)
    # Get context around the Bash command
    sed -n "$((line_num-5)),$((line_num+15))p" "$1" | grep -A10 -B5 "git commit" | head -20
done | grep -E "(git commit|input|command)" | sed 's/^[ ]*//'

# Find all Edit/Write tool calls
echo -e "\n\n=== File Modifications ==="
grep -n '"name": "Edit"' "$1" | head -10 | while read -r line; do
    line_num=$(echo "$line" | cut -d: -f1)
    echo "Edit at line $line_num:"
    sed -n "$((line_num)),$((line_num+5))p" "$1" | grep -E "(file_path|old_string|new_string)" | head -3
    echo ""
done

grep -n '"name": "Write"' "$1" | head -10 | while read -r line; do
    line_num=$(echo "$line" | cut -d: -f1)
    echo "Write at line $line_num:"
    sed -n "$((line_num)),$((line_num+3))p" "$1" | grep "file_path" | head -1
    echo ""
done

# Count totals
echo -e "\n=== Totals ==="
echo "Total Edits: $(grep -c '"name": "Edit"' "$1")"
echo "Total Writes: $(grep -c '"name": "Write"' "$1")"
echo "Total MultiEdits: $(grep -c '"name": "MultiEdit"' "$1")"
echo "Total git commits: $(grep '"name": "Bash"' "$1" | grep -c "git commit")"