#!/bin/bash
# fetch_logs.sh - Extract JSONL from GitHub Action workflow logs for Claude Code runs
#
# This script retrieves workflow run logs and metadata from GitHub Actions
# and stores them in a structured format for analysis and preservation.

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GITHUB_DIR="${SCRIPT_DIR}/github"

# AWK script for extracting content and metadata
AWK_SCRIPT='
BEGIN { 
    found_start = 0
    is_pr = ""
    issue_num = ""
    pr_num = ""
    session_id = ""
    prefix_len = 0
}

# Extract metadata using simple string operations
/<is_pr>/ && is_pr == "" {
    split($0, a, "<is_pr>")
    split(a[2], b, "</is_pr>")
    is_pr = b[1]
}

/<issue_number>/ && issue_num == "" {
    split($0, a, "<issue_number>")
    split(a[2], b, "</issue_number>")
    issue_num = b[1]
}

/<pr_number>/ && pr_num == "" {
    split($0, a, "<pr_number>")
    split(a[2], b, "</pr_number>")
    pr_num = b[1]
}

# Start/end markers and content extraction
index($0, "Running Claude with prompt from file:") && found_start == 0 { 
    found_start = 1
    
    # The line format is: claude\t{step}\t{timestamp}Z {rest of line}
    # Find where the timestamp starts (after 2nd tab) and ends (at Z)
    tab_count = 0
    timestamp_start = 0
    
    for (i = 1; i <= length($0); i++) {
        if (substr($0, i, 1) == "\t") {
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
            prefix_len = timestamp_start + z_pos  # Position after Z
        }
    }
    
    # Extract date and time parts for filename
    date_part = substr(start_time, 1, 10)
    gsub("-", "", date_part)  # 20250722
    hour_min = substr(start_time, 12, 5)
    gsub(":", "", hour_min)   # 0229
    next 
}

index($0, "Log saved to") { 
    # Same logic for end timestamp
    tab_count = 0
    timestamp_start = 0
    
    for (i = 1; i <= length($0); i++) {
        if (substr($0, i, 1) == "\t") {
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
    
    # Output all metadata to stderr
    print "START_TIME:" start_time > "/dev/stderr"
    print "END_TIME:" end_time > "/dev/stderr"
    print "DATE_STR:" date_part > "/dev/stderr"
    print "TIME_STR:" hour_min > "/dev/stderr"
    print "IS_PR:" is_pr > "/dev/stderr"
    print "ISSUE_NUM:" issue_num > "/dev/stderr"
    print "PR_NUM:" pr_num > "/dev/stderr"
    exit 
}

found_start && prefix_len > 0 && substr($0, 1, 6) == "claude" {
    # Skip the prefix and extract JSON
    if (length($0) > prefix_len) {
        line = substr($0, prefix_len + 1)
        print line
        # Extract session_id from first few lines
        if (session_id == "" && index(line, "\"session_id\"")) {
            split(line, a, "\"session_id\"")
            if (length(a) > 1) {
                split(a[2], b, "\"")
                if (length(b) > 2) {
                    session_id = b[2]
                    print "SESSION_ID:" session_id > "/dev/stderr"
                }
            }
        }
    }
}
'

# Helper functions
error() {
    echo "Error: $1" >&2
    exit 1
}

info() {
    echo "$1"
}

# Get existing run IDs from archived files
get_existing_run_ids() {
    local github_dir="$1"
    local existing_runs=""
    
    if [[ -d "$github_dir" ]]; then
        # Extract run IDs from filenames: *_run-{run_id}_session-*.jsonl
        for file in "$github_dir"/*_run-*_session-*.jsonl; do
            if [[ -f "$file" ]]; then
                # Extract run ID using bash string manipulation
                local filename=$(basename "$file")
                local run_part="${filename#*_run-}"
                local run_id="${run_part%%_session-*}"
                existing_runs="${existing_runs}${run_id} "
            fi
        done
    fi
    
    echo "$existing_runs"
}

# Run GitHub CLI command
run_gh() {
    if ! gh "$@"; then
        error "Failed to run: gh $*"
    fi
}

# Get workflow runs
get_workflow_runs() {
    local limit="${1:-20}"
    info "Fetching $limit recent workflow runs..." >&2
    
    run_gh run list \
        --workflow=claude.yml \
        --status=success \
        --json 'databaseId,number,status,conclusion,createdAt,headBranch,event,displayTitle' \
        --limit "$limit"
}

# Get workflow logs
get_workflow_logs() {
    local run_id="$1"
    info "Fetching logs for run $run_id..." >&2
    
    if ! gh run view "$run_id" --log 2>/dev/null; then
        info "  Warning: Could not fetch logs for run $run_id (may be expired)" >&2
        return 1
    fi
}

# Get run metadata
get_run_metadata() {
    local run_id="$1"
    info "Fetching metadata for run $run_id..." >&2
    
    run_gh run view "$run_id" \
        --json 'databaseId,number,status,conclusion,createdAt,updatedAt,headBranch,event,displayTitle,url,jobs'
}

# Extract and save workflow data
save_workflow_data() {
    local run_metadata="$1"
    local logs="$2"
    local save_raw_logs="${3:-false}"
    
    # Parse run metadata
    local run_id=$(echo "$run_metadata" | jq -r '.databaseId | tostring')
    local created_at=$(echo "$run_metadata" | jq -r '.createdAt // ""')
    local conclusion=$(echo "$run_metadata" | jq -r '.conclusion // ""')
    
    # We now only get successful runs, but keep this check for safety
    if [[ "$conclusion" != "success" ]]; then
        info "  Unexpected $conclusion run $run_id"
        return
    fi
    
    if [[ -z "$logs" ]]; then
        info "  No logs available for run $run_id"
        return
    fi
    
    # Create temp files for AWK output
    local temp_jsonl=$(mktemp)
    local temp_metadata=$(mktemp)
    trap "rm -f $temp_jsonl $temp_metadata" EXIT
    
    # Extract JSONL and metadata using AWK
    echo "$logs" | awk "$AWK_SCRIPT" > "$temp_jsonl" 2> "$temp_metadata"
    
    # Parse metadata
    local start_time end_time date_str time_str is_pr issue_num pr_num session_id
    while IFS=: read -r key value; do
        case "$key" in
            START_TIME) start_time="$value" ;;
            END_TIME) end_time="$value" ;;
            DATE_STR) date_str="$value" ;;
            TIME_STR) time_str="$value" ;;
            IS_PR) is_pr="$value" ;;
            ISSUE_NUM) issue_num="$value" ;;
            PR_NUM) pr_num="$value" ;;
            SESSION_ID) session_id="$value" ;;
        esac
    done < "$temp_metadata"
    
    # Check if we have all required data
    if [[ -z "$session_id" || -z "$date_str" || -z "$time_str" ]]; then
        info "  Failed to extract required data from run $run_id"
        if [[ "$save_raw_logs" == "true" ]]; then
            # Save raw log for debugging
            mkdir -p "$GITHUB_DIR"
            local log_file="${GITHUB_DIR}/${created_at:0:10}-${created_at:11:2}${created_at:14:2}-run-${run_id}.log"
            echo "$logs" > "$log_file"
            info "    Saved raw log to $log_file"
        fi
        return
    fi
    
    # Determine issue/PR type and number
    local type_num
    if [[ "$is_pr" == "false" && -n "$issue_num" ]]; then
        type_num="issue-${issue_num}"
    elif [[ "$is_pr" == "true" && -n "$pr_num" ]]; then
        type_num="pr-${pr_num}"
    else
        info "  Could not determine issue/PR type for run $run_id"
        return
    fi
    
    # Build filename
    local filename="${date_str}-${time_str}-${type_num}_run-${run_id}_session-${session_id}.jsonl"
    
    # Create directory and save file
    mkdir -p "$GITHUB_DIR"
    local jsonl_file="${GITHUB_DIR}/${filename}"
    mv "$temp_jsonl" "$jsonl_file"
    
    # Set file timestamps
    if [[ -n "$start_time" && -n "$end_time" ]]; then
        # Convert ISO timestamps to formats needed by macOS commands
        # Format for SetFile: MM/DD/YYYY HH:MM:SS
        # Format for touch: YYYYMMDDHHMM.SS
        
        # Parse timestamps
        local start_year="${start_time:0:4}"
        local start_month="${start_time:5:2}"
        local start_day="${start_time:8:2}"
        local start_hour="${start_time:11:2}"
        local start_min="${start_time:14:2}"
        local start_sec="${start_time:17:2}"
        
        local end_year="${end_time:0:4}"
        local end_month="${end_time:5:2}"
        local end_day="${end_time:8:2}"
        local end_hour="${end_time:11:2}"
        local end_min="${end_time:14:2}"
        local end_sec="${end_time:17:2}"
        
        # Try to set creation time with SetFile (macOS only)
        if command -v SetFile >/dev/null 2>&1; then
            local setfile_date="${start_month}/${start_day}/${start_year} ${start_hour}:${start_min}:${start_sec}"
            SetFile -d "$setfile_date" "$jsonl_file" 2>/dev/null || true
        fi
        
        # Set modification time with touch
        local touch_time="${end_year}${end_month}${end_day}${end_hour}${end_min}.${end_sec}"
        touch -t "$touch_time" "$jsonl_file"
        
        # Calculate and display session duration
        local start_epoch=$(date -u -j -f "%Y-%m-%dT%H:%M:%S" "${start_time:0:19}" "+%s" 2>/dev/null || echo 0)
        local end_epoch=$(date -u -j -f "%Y-%m-%dT%H:%M:%S" "${end_time:0:19}" "+%s" 2>/dev/null || echo 0)
        if [[ $start_epoch -gt 0 && $end_epoch -gt 0 ]]; then
            local duration=$((end_epoch - start_epoch))
            info "    Session duration: ${duration} seconds"
        fi
    fi
    
    info "  Saved JSONL to $jsonl_file"
}

# Process single run
process_run() {
    local run_id="$1"
    local save_raw_logs="${2:-false}"
    
    info "Processing run $run_id"
    
    # Get metadata
    local metadata=$(get_run_metadata "$run_id")
    
    # Get logs
    local logs=$(get_workflow_logs "$run_id")
    
    # Save data
    save_workflow_data "$metadata" "$logs" "$save_raw_logs"
}

# Main function
main() {
    local limit=20
    local run_id=""
    local save_raw_logs=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --limit)
                limit="$2"
                shift 2
                ;;
            --run-id)
                run_id="$2"
                shift 2
                ;;
            --save-raw-logs)
                save_raw_logs=true
                shift
                ;;
            -h|--help)
                cat <<EOF
Usage: $0 [OPTIONS]

Extract JSONL from GitHub workflow logs for Claude Code runs.

Options:
  --limit N           Number of recent runs to fetch (default: 20)
  --run-id ID         Specific run ID to archive
  --save-raw-logs     Save raw logs for failed extractions (for debugging)
  -h, --help          Show this help message

Examples:
  $0                           # Fetch 20 most recent runs
  $0 --limit 50                # Fetch 50 most recent runs
  $0 --run-id 16433029102      # Fetch specific run
  $0 --save-raw-logs           # Save raw logs when extraction fails
EOF
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done
    
    # Check if gh is available
    if ! command -v gh >/dev/null 2>&1; then
        error "GitHub CLI (gh) is required but not installed"
    fi
    
    # Process runs
    if [[ -n "$run_id" ]]; then
        # Process specific run
        info "Archiving specific run $run_id"
        process_run "$run_id" "$save_raw_logs"
        info "Specific run archiving complete!"
    else
        # Get existing run IDs
        local existing_runs=$(get_existing_run_ids "$GITHUB_DIR")
        local existing_count=$(echo "$existing_runs" | wc -w | tr -d ' ')
        if [[ "$existing_count" -gt 0 ]]; then
            info "Found $existing_count existing archived runs"
        fi
        
        # Process recent runs
        local runs=$(get_workflow_runs "$limit")
        local run_count=$(echo "$runs" | jq 'length')
        
        if [[ "$run_count" -eq 0 ]]; then
            info "No workflow runs found."
            exit 0
        fi
        
        info "Found $run_count workflow runs"
        
        # Process each run, skipping already archived ones
        local skipped_runs=0
        local processed_runs=0
        
        # Use process substitution to avoid subshell
        while IFS= read -r run_info; do
            local run_id=$(echo "$run_info" | jq -r '.databaseId | tostring')
            local title=$(echo "$run_info" | jq -r '.displayTitle // "Unknown"')
            
            # Check if already archived
            if [[ " $existing_runs " =~ " $run_id " ]]; then
                ((skipped_runs++))
                continue
            fi
            
            ((processed_runs++))
            echo
            info "Processing run $run_id: $title"
            process_run "$run_id" "$save_raw_logs"
        done < <(echo "$runs" | jq -c '.[]')
        
        if [[ "$skipped_runs" -gt 0 ]]; then
            info "Skipped $skipped_runs already archived runs"
        fi
        
        if [[ "$processed_runs" -eq 0 && "$skipped_runs" -gt 0 ]]; then
            info "No new runs to archive."
        fi
        
        echo
        info "Log archiving complete!"
    fi
}

# Run main function
main "$@"