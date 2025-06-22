"""Acceptance tests for BookMinder CLI commands."""

import subprocess
import sys
from pathlib import Path


def describe_bookminder_list_recent_command():
    def it_shows_recently_read_books_with_progress():
        """When I run "bookminder list recent".

        Then I see up to 10 books
        And each book shows: Title, Author, Progress %
        And books are ordered by last read date (newest first)
        """
        # Run the CLI command
        result = subprocess.run(
            [sys.executable, "-m", "bookminder", "list", "recent"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        # Command should succeed
        assert result.returncode == 0, f"Command failed: {result.stderr}"

        # Should have output
        output_lines = result.stdout.strip().split("\n")
        assert len(output_lines) > 0, "Expected output from command"

        # Should not exceed 10 books
        assert (
            len(output_lines) <= 10
        ), f"Expected max 10 books, got {len(output_lines)}"

        # Each line should match format: "Title - Author (Progress%)"
        for line in output_lines:
            if line.strip():  # Skip empty lines
                assert " - " in line, f"Expected 'Title - Author' format in: {line}"
                assert "%" in line, f"Expected progress percentage in: {line}"
                assert (
                    "(" in line and ")" in line
                ), f"Expected parentheses around progress in: {line}"
