#!/bin/bash
# xs-commits.sh - Comprehensive git command to list all commits related to the xs toolset
#
# This script identifies all commits that touch any part of the xs (explore-session) toolset,
# including precursor tools (reconstruct.jq, fetch_logs) and the complete tools directory.
#
# Usage: ./xs-commits.sh [git-log-options]
#
# Examples:
#   ./xs-commits.sh                    # List all commits with default format
#   ./xs-commits.sh --oneline          # Brief format
#   ./xs-commits.sh --stat             # With file statistics
#   ./xs-commits.sh --name-status      # With file change status

# The comprehensive path list covering all xs toolset components:
# - claude-dev-log-diary/tools/        Main toolset directory (all files)
# - claude-dev-log-diary/reconstruct.jq Original precursor (moved to tools/)
# - xs                                  Symlink to explore_session.py

git log --all "$@" -- \
    claude-dev-log-diary/tools/ \
    claude-dev-log-diary/reconstruct.jq \
    xs

# Note: Using --all ensures we see commits across all branches
# The paths are ordered to show the evolution: precursor -> tools -> symlink
