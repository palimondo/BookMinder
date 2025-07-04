import subprocess
import sys
from pathlib import Path


def _run_cli_with_user(user_name, use_fixture=True):
    if use_fixture:
        user_arg = str(Path(__file__).parent / "apple_books/fixtures/users" / user_name)
    else:
        user_arg = user_name

    result = subprocess.run(
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
    assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}"
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
