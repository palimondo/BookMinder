import subprocess
import sys
from pathlib import Path

import pytest


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
        result = _run_cli_with_user("test_reader")

        output_lines = result.stdout.strip().split("\n")
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


def describe_bookminder_list_recent_with_user_parameter():
    def it_handles_user_who_never_opened_apple_books():
        result = _run_cli_with_user("never_opened_user")

        assert "Apple Books database not found" in result.stdout, (
            f"Expected helpful message, got: {result.stdout}"
        )

    def it_handles_fresh_apple_books_user_with_no_books():
        result = _run_cli_with_user("fresh_books_user")

        assert "No books currently being read" in result.stdout, (
            f"Expected no books message, got: {result.stdout}"
        )

    def it_handles_user_with_legacy_apple_books_installation():
        result = _run_cli_with_user("legacy_books_user")  # missing database

        assert "Apple Books database not found" in result.stdout, (
            f"Expected database not found message, got: {result.stdout}"
        )

    def it_shows_books_for_user_with_reading_progress():
        result = _run_cli_with_user("test_reader")

        output_lines = result.stdout.strip().split("\n")
        assert len(output_lines) > 0, "Expected books in output"

        for line in output_lines:
            if line.strip():
                assert " - " in line, f"Expected 'Title - Author' format in: {line}"
                assert "%" in line, f"Expected progress percentage in: {line}"

    def it_handles_user_with_corrupted_apple_books_database():
        result = _run_cli_with_user("corrupted_db_user")

        assert "Error reading Apple Books database:" in result.stdout, (
            f"Expected error message, got: {result.stdout}"
        )

    def it_handles_non_existent_relative_user_path():
        user_name = "non_existent_user"
        result = _run_cli_with_user(user_name, use_fixture=False)

        assert (
            f"BKLibrary directory not found: "
            f"/Users/{user_name}/Library/Containers/com.apple.iBooksX/"
            "Data/Documents/BKLibrary. Apple Books database not found." in result.stdout
        ), f"Expected FileNotFoundError message with path, got: {result.stdout}"


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

        assert "Extreme Programming Explained" not in result.stdout

    @pytest.mark.skip(reason="Implement after basic list all works")
    def it_excludes_samples_when_filter_is_not_sample():
        pass

