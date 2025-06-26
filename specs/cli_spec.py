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


def describe_bookminder_list_recent_with_user_parameter():
    def _run_cli_with_user(user_name):
        """Run CLI with --user parameter."""
        return subprocess.run(
            [sys.executable, "-m", "bookminder", "list", "recent", "--user", user_name],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

    def it_handles_user_who_never_opened_apple_books():
        """User without Apple Books should see helpful message."""
        result = _run_cli_with_user("never_opened_user")

        assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"
        assert (
            "Apple Books not found" in result.stdout
        ), f"Expected helpful message, got: {result.stdout}"

    def it_handles_user_with_fresh_apple_books_no_books():
        """User who just opened Apple Books but has no books."""
        result = _run_cli_with_user("fresh_books_user")

        assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"
        assert (
            "No books currently being read" in result.stdout
        ), f"Expected no books message, got: {result.stdout}"

    def it_handles_user_with_legacy_apple_books_installation():
        """User with partial/legacy Apple Books installation (missing database)."""
        result = _run_cli_with_user("legacy_books_user")

        assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"
        assert (
            "Apple Books database not found" in result.stdout
        ), f"Expected database not found message, got: {result.stdout}"

    def it_shows_books_for_user_with_reading_progress():
        """User with books in progress should see their reading list."""
        result = _run_cli_with_user("test_reader")

        assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"

        output_lines = result.stdout.strip().split("\n")
        assert len(output_lines) > 0, "Expected books in output"

        # Should have standard book format
        for line in output_lines:
            if line.strip():
                assert " - " in line, f"Expected 'Title - Author' format in: {line}"
                assert "%" in line, f"Expected progress percentage in: {line}"
