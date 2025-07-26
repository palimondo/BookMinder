#!/usr/bin/env python3
"""Fetch and archive GitHub Action workflow logs for Claude Code runs.

This script retrieves workflow run logs and metadata from GitHub Actions
and stores them in a structured format for analysis and preservation.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_gh_command(command: list[str]) -> str:
    """Run a GitHub CLI command and return the output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)


def get_workflow_runs(limit: int = 20) -> list[dict]:
    """Fetch recent workflow runs for the Claude Code workflow."""
    print(f"Fetching {limit} recent workflow runs...")

    # Get workflow runs as JSON
    output = run_gh_command([
        'gh', 'run', 'list',
        '--workflow=claude.yml',
        '--status=success',
        '--json',
        'databaseId,number,status,conclusion,createdAt,headBranch,event,displayTitle',
        '--limit', str(limit)
    ])

    return json.loads(output)  # type: ignore[no-any-return]


def get_workflow_logs(run_id: str) -> str:
    """Fetch logs for a specific workflow run."""
    print(f"Fetching logs for run {run_id}...")

    try:
        return run_gh_command(['gh', 'run', 'view', run_id, '--log'])
    except subprocess.CalledProcessError:
        print(f"Warning: Could not fetch logs for run {run_id} (may be expired)")
        return ""


def get_run_metadata(run_id: str) -> dict:
    """Fetch detailed metadata for a specific workflow run."""
    print(f"Fetching metadata for run {run_id}...")

    output = run_gh_command([
        'gh', 'run', 'view', run_id,
        '--json',
        'databaseId,number,status,conclusion,createdAt,updatedAt,headBranch,event,'
        'displayTitle,url,jobs'
    ])

    return json.loads(output)  # type: ignore[no-any-return]




def extract_issue_or_pr_from_log(log_content: str) -> tuple[str | None, int | None]:
    """Extract issue or PR number from log XML tags.

    Returns:
        tuple of (type, number) where type is 'issue' or 'pr'

    """
    import re

    # Check if it's a PR
    if re.search(r'<is_pr>true</is_pr>', log_content):
        # Extract PR number
        pr_match = re.search(r'<pr_number>(\d+)</pr_number>', log_content)
        if pr_match:
            return ('pr', int(pr_match.group(1)))
    else:
        # It's an issue (is_pr=false)
        issue_match = re.search(r'<issue_number>(\d+)</issue_number>', log_content)
        if issue_match:
            return ('issue', int(issue_match.group(1)))

    return (None, None)


def extract_jsonl_from_logs(
    log_content: str,
) -> tuple[str, str | None, str | None, str | None, str | None, str | None]:
    """Extract JSONL content from Claude execution logs using optimized AWK.

    Returns:
        tuple of (jsonl_content, session_id, start_timestamp,
               end_timestamp, date_str, time_str)

    """
    # Use subprocess to leverage AWK's optimized text processing
    # Extract JSONL content AND timestamps in a single pass
    # Now also extracts formatted date/time for filename
    awk_script = '''
    BEGIN {
        found_start = 0
        prefix_len = 0
        prompt_file = "/Users/runner/work/_temp/claude-prompts/claude-prompt.txt"
    }
    index($0, "Running Claude with prompt from file: " prompt_file) && \
          found_start == 0 {
        found_start = 1

        # The line format is: claude\\t{step}\\t{timestamp}Z {rest of line}
        # Find where the timestamp starts (after 2nd tab) and ends (at 'Z ')
        tab_count = 0
        timestamp_start = 0

        for (i = 1; i <= length($0); i++) {
            if (substr($0, i, 1) == "\\t") {
                tab_count++
                if (tab_count == 2) {
                    timestamp_start = i + 1
                    break
                }
            }
        }

        if (timestamp_start > 0) {
            # Find the Z that ends the timestamp
            z_pos = index(substr($0, timestamp_start), "Z")
            if (z_pos > 0) {
                start_time = substr($0, timestamp_start, z_pos - 1)
                prefix_len = timestamp_start + z_pos  # Position after 'Z '
            }
        }

        # Extract date and time parts for filename
        date_part = substr(start_time, 1, 10)
        gsub("-", "", date_part)  # 20250722
        hour_min = substr(start_time, 12, 5)
        gsub(":", "", hour_min)   # 0229
        next
    }
    index($0, "Log saved to /Users/runner/work/_temp/claude-execution-output.json") {
        # Same logic for end timestamp
        tab_count = 0
        timestamp_start = 0

        for (i = 1; i <= length($0); i++) {
            if (substr($0, i, 1) == "\\t") {
                tab_count++
                if (tab_count == 2) {
                    timestamp_start = i + 1
                    break
                }
            }
        }

        if (timestamp_start > 0) {
            z_pos = index(substr($0, timestamp_start), "Z")
            if (z_pos > 0) {
                end_time = substr($0, timestamp_start, z_pos - 1)
            }
        }

        print "METADATA:" start_time "|" end_time "|" date_part "|" hour_min
        exit
    }
    found_start && prefix_len > 0 && substr($0, 1, 6) == "claude" {
        # Skip the prefix and extract JSON
        if (length($0) > prefix_len) {
            print substr($0, prefix_len + 1)
        }
    }
    '''

    result = subprocess.run(
        ['awk', awk_script],
        input=log_content,
        capture_output=True,
        text=True
    )

    output_lines = result.stdout.strip().split('\n')

    # Extract metadata if present
    start_timestamp = None
    end_timestamp = None
    date_str = None
    time_str = None
    jsonl_lines = output_lines

    if output_lines and output_lines[-1].startswith('METADATA:'):
        metadata = output_lines[-1][9:]  # Skip "METADATA:"
        parts = metadata.split('|')
        if len(parts) == 4:
            start_timestamp = parts[0] if parts[0] else None
            end_timestamp = parts[1] if parts[1] else None
            date_str = parts[2] if parts[2] else None
            time_str = parts[3] if parts[3] else None
        jsonl_lines = output_lines[:-1]  # Exclude metadata line

    jsonl_content = '\n'.join(jsonl_lines)

    # Extract session ID from first few lines of JSONL
    session_id = None
    if jsonl_lines:
        # Check first 10 lines for session_id
        import re
        for line in jsonl_lines[:10]:
            match = re.search(r'"session_id":\s*"([^"]+)"', line)
            if match:
                session_id = match.group(1)
                break

    return jsonl_content, session_id, start_timestamp, end_timestamp, date_str, time_str


def ensure_directory(path: Path) -> None:
    """Ensure directory exists, creating it if necessary."""
    path.mkdir(parents=True, exist_ok=True)


def get_existing_run_ids(github_dir: Path) -> set[str]:
    """Extract run IDs from existing JSONL files in the github directory."""
    existing_runs = set()

    if not github_dir.exists():
        return existing_runs

    # Pattern: *_run-{run_id}_session-*.jsonl
    for file in github_dir.glob("*_run-*_session-*.jsonl"):
        # Extract run ID from filename
        parts = file.stem.split("_run-")
        if len(parts) > 1:
            run_id_part = parts[1].split("_session-")[0]
            existing_runs.add(run_id_part)

    return existing_runs


def set_file_timestamps(
    file_path: Path, start_timestamp: str, end_timestamp: str
) -> None:
    """Set file creation and modification timestamps.

    On macOS, uses SetFile for creation time and touch for modification time.
    On other systems, falls back to os.utime for access/modification times.
    """
    try:
        # Parse the timestamps
        start_dt = datetime.fromisoformat(start_timestamp.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_timestamp.replace('Z', '+00:00'))

        # Try to set creation time on macOS
        if sys.platform == 'darwin':
            try:
                # Format for SetFile: MM/DD/YYYY HH:MM:SS
                setfile_date = start_dt.strftime('%m/%d/%Y %H:%M:%S')
                subprocess.run(
                    ['SetFile', '-d', setfile_date, str(file_path)],
                    check=True,
                    capture_output=True
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                # SetFile not available or failed
                pass

        # Set modification time (and access time as a side effect)
        os.utime(file_path, (start_dt.timestamp(), end_dt.timestamp()))

        # Log session duration
        duration = (end_dt - start_dt).total_seconds()
        print(f"    Session duration: {duration:.1f} seconds")

    except (ValueError, OSError) as e:
        print(f"    Warning: Could not set session timestamps: {e}")


def save_workflow_data(
    run_metadata: dict, logs: str, base_dir: Path, save_raw_logs: bool = False
) -> None:
    """Extract and save JSONL from workflow logs."""
    run_id = str(run_metadata['databaseId'])
    created_at = run_metadata.get('createdAt', '')
    conclusion = run_metadata.get('conclusion', '')

    # We now only get successful runs, but keep this check for safety
    if conclusion != 'success':
        print(f"  Unexpected {conclusion} run {run_id}")
        return

    if not logs:
        print(f"  No logs available for run {run_id}")
        return

    # Extract everything from logs
    (jsonl_content, session_id, start_timestamp,
     end_timestamp, date_str, time_str) = extract_jsonl_from_logs(logs)
    log_type, log_number = extract_issue_or_pr_from_log(logs)

    # Create github directory
    github_dir = base_dir / "github"
    ensure_directory(github_dir)

    # Only proceed if we have all the data we need
    if not (jsonl_content and session_id and log_type
            and log_number and date_str and time_str):
        print(f"  Failed to extract JSONL data from run {run_id}")
        if save_raw_logs:
            # Parse timestamp for naming
            timestamp = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            date_str_fallback = timestamp.strftime('%Y%m%d')
            time_str_fallback = timestamp.strftime('%H%M')
            # Save raw log in same flat directory
            log_filename = f"{date_str_fallback}-{time_str_fallback}-run-{run_id}.log"
            log_file = github_dir / log_filename
            with open(log_file, 'w') as f:
                f.write(logs)
            print(f"    Saved raw log to {log_file}")
        return

    # Build filename with new format
    jsonl_filename = (f"{date_str}-{time_str}-{log_type}-{log_number}_"
                      f"run-{run_id}_session-{session_id}.jsonl")
    jsonl_file = github_dir / jsonl_filename
    with open(jsonl_file, 'w') as f:
        f.write(jsonl_content)

    # Set file timestamps to match actual Claude session start/end times
    if start_timestamp and end_timestamp:
        set_file_timestamps(jsonl_file, start_timestamp, end_timestamp)
    else:
        # Use workflow timestamp if session times not found
        timestamp_seconds = datetime.fromisoformat(
            created_at.replace('Z', '+00:00')
        ).timestamp()
        os.utime(jsonl_file, (timestamp_seconds, timestamp_seconds))

    print(f"  Saved JSONL to {jsonl_file}")


def main() -> None:
    """Execute log archiving based on command line arguments."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Extract JSONL from GitHub workflow logs'
    )
    parser.add_argument('--limit', type=int, default=20,
                      help='Number of recent runs to fetch (default: 20)')
    parser.add_argument('--run-id', type=str,
                      help='Specific run ID to archive')
    parser.add_argument('--save-raw-logs', action='store_true',
                      help='Save raw logs for failed extractions (for debugging)')

    args = parser.parse_args()

    # Setup base directory (parent of tools directory)
    base_dir = Path(__file__).parent.parent

    if args.run_id:
        # Archive specific run
        print(f"Archiving specific run {args.run_id}")
        metadata = get_run_metadata(args.run_id)
        logs = get_workflow_logs(args.run_id)
        save_workflow_data(metadata, logs, base_dir, args.save_raw_logs)
        print("Specific run archiving complete!")
        return

    # Get existing run IDs to avoid re-downloading
    github_dir = base_dir / "github"
    existing_runs = get_existing_run_ids(github_dir)
    if existing_runs:
        print(f"Found {len(existing_runs)} existing archived runs")

    # Fetch workflow runs
    runs = get_workflow_runs(args.limit)

    if not runs:
        print("No workflow runs found.")
        return

    print(f"Found {len(runs)} workflow runs")

    # Filter out already downloaded runs
    new_runs = []
    skipped_count = 0
    for run_info in runs:
        run_id = str(run_info['databaseId'])
        if run_id in existing_runs:
            skipped_count += 1
        else:
            new_runs.append(run_info)

    if skipped_count > 0:
        print(f"Skipping {skipped_count} already archived runs")

    if not new_runs:
        print("No new runs to archive.")
        return

    # Process each new run
    for run_info in new_runs:
        run_id = str(run_info['databaseId'])
        title = run_info.get('displayTitle', 'Unknown')

        print(f"\nProcessing run {run_id}: {title}")

        # Get detailed metadata
        metadata = get_run_metadata(run_id)

        # Get logs
        logs = get_workflow_logs(run_id)

        # Save data
        save_workflow_data(metadata, logs, base_dir, args.save_raw_logs)

    print("\nLog archiving complete!")


if __name__ == "__main__":
    main()
