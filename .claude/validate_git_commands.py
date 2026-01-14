#!/usr/bin/env python3
"""Validate git commands to prevent accidental staging of large files."""

import json
import re
import sys


def main() -> None:
    """Check git commands and block dangerous bulk staging patterns."""
    try:
        input_data = json.load(sys.stdin)
        command = input_data.get("tool_input", {}).get("command", "")

        # Check for dangerous git add patterns
        dangerous_patterns = [
            r"git add \.(\s|$)",
            r"git add -A(\s|$)",
            r"git add --all(\s|$)",
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, command):
                print(
                    f"Blocked: '{pattern}' detected. Please stage files "
                    "explicitly by name to avoid accidentally committing "
                    "unintended files",
                    file=sys.stderr,
                )
                sys.exit(2)  # Exit code 2 blocks the tool call

    except Exception as e:
        print(f"Hook validation error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
