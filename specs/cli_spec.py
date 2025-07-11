import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from bookminder import BookminderError
from bookminder.apple_books.library import Book
from bookminder.cli import main


def _run_cli_with_user(user_name, use_fixture=True, subcommand="recent", filter=None):
    if use_fixture:
        user_arg = str(Path(__file__).parent / "apple_books/fixtures/users" / user_name)
    else:
        user_arg = user_name

    command = [
        sys.executable,
        "-m",
        "bookminder",
        "list",
        subcommand,
        "--user",
        user_arg,
    ]

    if filter:
        command.extend(["--filter", filter])

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )
    assert result.returncode == 0, \
        f"Expected exit code 0, got {result.returncode}: {result.stderr}"
    return result


def describe_bookminder_list_recent_command():
    def it_shows_recently_read_books_with_progress():
        runner = CliRunner()

        # Mock data that matches the test fixture expectations
        test_books = [
            Book(
                title="Extreme Programming Explained",
                author="Kent Beck",
                reading_progress_percentage=69,
            ),
            Book(
                title="The Left Hand of Darkness",
                author="Ursula K. Le Guin",
                reading_progress_percentage=32,
            ),
            Book(
                title="Lao Tzu: Tao Te Ching",
                author="Ursula K. Le Guin",
                reading_progress_percentage=8,
                is_cloud=True,
            ),
        ]

        with patch('bookminder.cli.list_recent_books') as mock:
            mock.return_value = test_books
            result = runner.invoke(main, ['list', 'recent'])

        assert result.exit_code == 0
        output_lines = result.output.strip().split("\n")
        assert len(output_lines) > 0, "Expected output from command"

        assert len(output_lines) <= 10, (
            f"Expected max 10 books, got {len(output_lines)}"
        )

        for line in output_lines:
            if line.strip():
                assert " - " in line, f"Expected 'Title - Author' format in: {line}"
                assert "%" in line, f"Expected progress percentage in: {line}"
                assert "(" in line and ")" in line, (
                    f"Expected parentheses around progress in: {line}"
                )

        # Assert ordering
        assert "Extreme Programming Explained" in output_lines[0]
        assert "The Left Hand of Darkness" in output_lines[1]


def describe_bookminder_list_recent_integration():
    def it_shows_books_for_user_with_reading_progress():
        """Integration test: verify full stack works with real fixture."""
        result = _run_cli_with_user("test_reader")

        output_lines = result.stdout.strip().split("\n")
        assert len(output_lines) > 0, "Expected books in output"

        for line in output_lines:
            if line.strip():
                assert " - " in line, f"Expected 'Title - Author' format in: {line}"
                assert "%" in line, f"Expected progress percentage in: {line}"


def describe_bookminder_list_with_filter():
    def it_filters_by_cloud_status():
        result = _run_cli_with_user("test_reader", subcommand="recent", filter="cloud")
        assert "Lao Tzu: Tao Te Ching" in result.stdout
        assert "☁️" in result.stdout
        # Should not show local books
        assert "Extreme Programming Explained" not in result.stdout
        assert "The Left Hand of Darkness" not in result.stdout

    def it_excludes_cloud_books_when_filter_is_not_cloud():
        result = _run_cli_with_user("test_reader", subcommand="recent", filter="!cloud")
        assert len(result.stdout) > 0
        assert "☁️" not in result.stdout


def describe_bookminder_list_all_command():
    def it_shows_all_books_in_library():
        result = _run_cli_with_user("test_reader", subcommand="all")
        # Should show books with and without progress
        assert "Extreme Programming Explained" in result.stdout
        assert "Snow Crash" in result.stdout
        assert "Tiny Experiments" in result.stdout

    def it_filters_by_sample_status():
        result = _run_cli_with_user("test_reader", subcommand="all", filter="sample")

        output_lines = [line for line in result.stdout.strip().split('\n') if line]
        assert len(output_lines) >= 3, "Expected at least 3 sample books"

        for line in output_lines:
            assert " • Sample" in line, f"Expected sample indicator in: {line}"

        assert " • Sample ☁️" in result.stdout, \
            "Sample indicator should appear before Cloud"
        assert "Extreme Programming Explained" not in result.stdout

    @pytest.mark.skip(reason="Implement after basic list all works")
    def it_excludes_samples_when_filter_is_not_sample():
        pass


def describe_cli_error_boundary():
    """Verify CLI properly handles errors from library layer."""

    def it_displays_library_errors_without_stack_traces():
        from unittest.mock import patch

        from click.testing import CliRunner

        from bookminder.cli import main

        runner = CliRunner()
        error_message = "Something went wrong in the library"

        # Test that recent command handles library errors gracefully
        with patch('bookminder.cli.list_recent_books') as mock:
            mock.side_effect = BookminderError(error_message)
            result = runner.invoke(main, ['list', 'recent'])

        assert result.exit_code == 0  # No crash
        assert error_message in result.output
        assert "Traceback" not in result.output  # No stack trace leaked

        # Test that all command handles library errors gracefully
        with patch('bookminder.cli.list_all_books') as mock:
            mock.side_effect = BookminderError(error_message)
            result = runner.invoke(main, ['list', 'all'])

        assert result.exit_code == 0  # No crash
        assert error_message in result.output
        assert "Traceback" not in result.output  # No stack trace leaked

