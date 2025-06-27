import subprocess
import sys
from pathlib import Path


def _run_cli_with_user(user_name, use_fixture=True):
    if use_fixture:
        user_arg = str(Path(__file__).parent / "apple_books/fixtures/users" / user_name)
    else:
        user_arg = user_name

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "bookminder",
            "list",
            "recent",
            "--user",
            user_arg,
        ],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
    )


def describe_bookminder_list_recent_command():
    def it_shows_recently_read_books_with_progress():
        """Feature: List recent books
  Scenario: Show recently read books
    When I run "bookminder list recent"
    Then I see up to 10 books
    And each book shows: Title, Author, Progress %
    And books are ordered by last read date (newest first)
        """
        result = _run_cli_with_user("test_reader")

        assert result.returncode == 0, f"Command failed: {result.stderr}"

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


def describe_bookminder_list_recent_with_user_parameter():
    def it_handles_user_who_never_opened_apple_books():
        """Feature: Access other users' Apple Books libraries
  Scenario: User who never opened Apple Books
    When I run "bookminder list recent --user never_opened_user"
    Then I see "Apple Books not found. Has it been opened on this account?"
        """
        result = _run_cli_with_user("never_opened_user")

        assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"
        assert "Apple Books database not found" in result.stdout, (
            f"Expected helpful message, got: {result.stdout}"
        )

    def it_handles_user_with_fresh_apple_books_no_books():
        """Feature: Access other users' Apple Books libraries
  Scenario: User with empty library
    When I run "bookminder list recent --user fresh_books_user"
    Then I see "No books currently being read"
        """
        result = _run_cli_with_user("fresh_books_user")

        assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"
        assert "No books currently being read" in result.stdout, (
            f"Expected no books message, got: {result.stdout}"
        )

    def it_handles_user_with_legacy_apple_books_installation():
        """Feature: Access other users' Apple Books libraries
  Scenario: User with partial/legacy Apple Books installation (missing database)
    When I run "bookminder list recent --user legacy_books_user"
    Then I see "Apple Books database not found."
        """
        result = _run_cli_with_user("legacy_books_user")

        assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"
        assert "Apple Books database not found" in result.stdout, (
            f"Expected database not found message, got: {result.stdout}"
        )

    def it_shows_books_for_user_with_reading_progress():
        """Feature: Access other users' Apple Books libraries
  Scenario: Admin examines another user's books
    When I run "bookminder list recent --user alice"
    Then I see alice's recently read books
        """
        result = _run_cli_with_user("test_reader")

        assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"

        output_lines = result.stdout.strip().split("\n")
        assert len(output_lines) > 0, "Expected books in output"

        for line in output_lines:
            if line.strip():
                assert " - " in line, f"Expected 'Title - Author' format in: {line}"
                assert "%" in line, f"Expected progress percentage in: {line}"

    def it_handles_user_with_corrupted_apple_books_database():
        """Feature: Handle missing Apple Books gracefully
  Scenario: User with corrupted Apple Books database
    Given the Apple Books database is corrupted
    When I run "bookminder list recent"
    Then I see a helpful message "Error reading Apple Books database"
    And the exit code is 0
        """
        result = _run_cli_with_user("corrupted_db_user")

        assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"
        assert (
            "Error reading Apple Books: Error reading Apple Books database:"
            in result.stdout
        ), f"Expected error message, got: {result.stdout}"

    def it_handles_non_existent_relative_user_path():
        """Feature: Handle missing Apple Books gracefully
  Scenario: User without Apple Books installed
    Given the Apple Books database does not exist
    When I run "bookminder list recent"
    Then I see a helpful message "No Apple Books database found"
    And the exit code is 0
        """
        user_name = "non_existent_user"
        result = _run_cli_with_user(user_name, use_fixture=False)

        assert result.returncode == 0, f"Command failed: {result.stderr}"
        assert (
            f"Error reading Apple Books: BKLibrary directory not found: "
            f"/Users/{user_name}/Library/Containers/com.apple.iBooksX/"
            "Data/Documents/BKLibrary. Apple Books database not found." in result.stdout
        ), f"Expected FileNotFoundError message with path, got: {result.stdout}"
