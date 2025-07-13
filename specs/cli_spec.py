import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from bookminder import BookminderError
from bookminder.apple_books.library import Book
from bookminder.cli import main


@pytest.fixture
def runner():
    return CliRunner()


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
    def it_shows_recently_read_books_with_progress(runner):
        book1 = Book(title="B1", author="A1")
        book2 = Book(title="B2", author="A2")

        with patch('bookminder.cli.list_recent_books') as mock_list_recent, \
             patch('bookminder.cli.format') as mock_format:
            mock_list_recent.return_value = [book1, book2]
            runner.invoke(main, ['list', 'recent'])

        mock_list_recent.assert_called_once_with(user=None, filter=None)
        assert mock_format.call_args_list == [((book1,),), ((book2,),)]


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
    def it_filters_by_cloud_status(runner):
        with patch('bookminder.cli.list_recent_books') as mock_list_recent:
            runner.invoke(main, ['list', 'recent', '--filter', 'cloud'])

        mock_list_recent.assert_called_once_with(user=None, filter='cloud')

    def it_excludes_cloud_books_when_filter_is_not_cloud(runner):
        with patch('bookminder.cli.list_recent_books') as mock_list_recent:
            runner.invoke(main, ['list', 'recent', '--filter', '!cloud'])

        mock_list_recent.assert_called_once_with(user=None, filter='!cloud')


def describe_bookminder_list_all_command():
    def it_shows_all_books_in_library(runner):
        book1 = Book(title="B1", author="A1")
        book2 = Book(title="B2", author="A2")

        with patch('bookminder.cli.list_all_books') as mock_list_all, \
             patch('bookminder.cli.format') as mock_format:
            mock_list_all.return_value = [book1, book2]
            runner.invoke(main, ['list', 'all'])

        mock_list_all.assert_called_once_with(user=None, filter=None)
        assert mock_format.call_args_list == [((book1,),), ((book2,),)]

    def it_filters_by_sample_status(runner):
        with patch('bookminder.cli.list_all_books') as mock_list_all:
            runner.invoke(main, ['list', 'all', '--filter', 'sample'])

        mock_list_all.assert_called_once_with(user=None, filter='sample')

    @pytest.mark.skip(reason="Implement after basic list all works")
    def it_excludes_samples_when_filter_is_not_sample():
        pass


def describe_cli_error_boundary():
    """Verify CLI properly handles errors from library layer."""

    def it_displays_library_errors_without_stack_traces(runner):
        error_message = "Something went wrong in the library"

        with patch('bookminder.cli.list_recent_books') as mock:
            mock.side_effect = BookminderError(error_message)
            result = runner.invoke(main, ['list', 'recent'])

        assert result.exit_code == 0
        assert error_message in result.output
        assert "Traceback" not in result.output

        with patch('bookminder.cli.list_all_books') as mock:
            mock.side_effect = BookminderError(error_message)
            result = runner.invoke(main, ['list', 'all'])

        assert result.exit_code == 0
        assert error_message in result.output
        assert "Traceback" not in result.output

    def it_validates_filter_values_and_shows_helpful_error(runner):
        with patch('bookminder.apple_books.library.SUPPORTED_FILTERS', {'foo', 'bar'}):
            result = runner.invoke(main, ['list', 'all', '--filter', 'baz'])

            assert result.exit_code == 1
            assert "Invalid filter: 'baz'" in result.output
            assert "Valid filters:" in result.output
            assert "foo" in result.output
            assert "bar" in result.output

