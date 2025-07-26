from unittest.mock import patch

import pytest
from click.testing import CliRunner

from bookminder import BookminderError
from bookminder.apple_books.library import Book
from bookminder.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def describe_bookminder_list_commands():
    def it_shows_recently_read_books_with_progress(runner):
        book1 = Book(title="B1", author="A1")
        book2 = Book(title="B2", author="A2")

        with patch('bookminder.cli.list_recent_books') as mock_list_recent, \
             patch('bookminder.cli.format') as mock_format:
            mock_list_recent.return_value = [book1, book2]
            runner.invoke(main, ['list', 'recent'])

        mock_list_recent.assert_called_once_with(user=None, filter=None)
        assert mock_format.call_args_list == [((book1,),), ((book2,),)]

    def it_shows_all_books_in_library(runner):
        book1 = Book(title="B1", author="A1")
        book2 = Book(title="B2", author="A2")

        with patch('bookminder.cli.list_all_books') as mock_list_all, \
             patch('bookminder.cli.format') as mock_format:
            mock_list_all.return_value = [book1, book2]
            runner.invoke(main, ['list', 'all'])

        mock_list_all.assert_called_once_with(user=None, filter=None)
        assert mock_format.call_args_list == [((book1,),), ((book2,),)]


def describe_bookminder_filter_passthrough():
    @pytest.mark.parametrize("command,library_function", [
        ("recent", "list_recent_books"),
        ("all", "list_all_books"),
    ])
    @pytest.mark.parametrize("filter_value", [
        "cloud", "!cloud", "sample", "!sample"
    ])
    def it_passes_filters_to_library_function(
        command, library_function, filter_value, runner
    ):
        with patch(f'bookminder.cli.{library_function}') as mock:
            runner.invoke(main, ['list', command, '--filter', filter_value])
        mock.assert_called_once_with(user=None, filter=filter_value)


def describe_cli_validation():
    def it_validates_filter_values(runner):
        result = runner.invoke(main, ['list', 'recent', '--filter', 'invalid'])

        assert result.exit_code == 1
        assert "Invalid filter: 'invalid'" in result.output
        assert "Valid filters:" in result.output

    def it_validates_filter_values_and_shows_helpful_error(runner):
        with patch('bookminder.cli.SUPPORTED_FILTERS', {'foo', 'bar'}):
            result = runner.invoke(main, ['list', 'all', '--filter', 'baz'])

            assert result.exit_code == 1
            assert "Invalid filter: 'baz'" in result.output
            assert "Valid filters:" in result.output
            assert "foo" in result.output
            assert "bar" in result.output


def describe_cli_error_boundary():
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


def describe_bookminder_acceptance():
    def it_filters_recent_books_by_sample_status(runner):
        """Verify sample filter is passed correctly and output is formatted."""
        sample_book = Book(
            title="Sample Book",
            author="Sample Author",
            reading_progress_percentage=30,
            is_sample=True,
        )

        with patch('bookminder.cli.list_recent_books') as mock_list:
            mock_list.return_value = [sample_book]
            result = runner.invoke(main, ['list', 'recent', '--filter', 'sample'])

            mock_list.assert_called_once_with(user=None, filter="sample")
            assert "Sample Book - Sample Author (30%) • Sample" in result.output

    def it_excludes_samples_from_recent_books(runner):
        """Verify !sample filter is passed correctly and samples are excluded."""
        regular_book = Book(
            title="Regular Book",
            author="Regular Author",
            reading_progress_percentage=50,
            is_sample=False,
        )

        with patch('bookminder.cli.list_recent_books') as mock_list:
            mock_list.return_value = [regular_book]
            result = runner.invoke(main, ['list', 'recent', '--filter', '!sample'])

            mock_list.assert_called_once_with(user=None, filter="!sample")
            assert "Regular Book - Regular Author (50%)" in result.output
            assert "Sample" not in result.output


def describe_reading_status_filtering():
    """Filter by Reading Status Story - ATDD Implementation."""

    def it_lists_finished_books(runner):
        """Scenario: List finished books
        When: I run "bookminder list --filter finished"
        Then:
          - I see only books marked as complete
          - Each book shows: Title, Author, (Finished) status
          - (Finished) status takes precedence over progress percentage
        """
        finished_book = Book(
            title="Finished Book",
            author="Author Name",
            reading_progress_percentage=100,
            is_finished=True,
        )

        with patch('bookminder.cli.list_all_books') as mock_list:
            mock_list.return_value = [finished_book]
            result = runner.invoke(main, ['list', 'all', '--filter', 'finished'])

        mock_list.assert_called_once_with(user=None, filter="finished")
        assert result.exit_code == 0
        assert "Finished Book - Author Name (Finished)" in result.output

    def it_lists_unread_books(runner):
        """Scenario: List unread books
        When: I run "bookminder list --filter unread"
        Then:
          - I see only books with 0% reading progress and not marked as finished
          - Each book shows: Title, Author, (Unread) status
        """
        unread_book = Book(
            title="Unread Book",
            author="Author Name",
            reading_progress_percentage=0,
            is_finished=False,
            is_unread=True,
        )

        with patch('bookminder.cli.list_all_books') as mock_list:
            mock_list.return_value = [unread_book]
            result = runner.invoke(main, ['list', 'all', '--filter', 'unread'])

        mock_list.assert_called_once_with(user=None, filter="unread")
        assert result.exit_code == 0
        assert "Unread Book - Author Name (Unread)" in result.output

    def it_lists_books_in_progress(runner):
        """Scenario: List books in progress
        When: I run "bookminder list --filter in-progress"
        Then:
          - I see only books with 1-99% reading progress and not marked as finished
          - Each book shows: Title, Author, Progress %
        """
        in_progress_book = Book(
            title="In Progress Book",
            author="Author Name",
            reading_progress_percentage=45,
            is_finished=False,
            is_unread=False,
        )

        with patch('bookminder.cli.list_all_books') as mock_list:
            mock_list.return_value = [in_progress_book]
            result = runner.invoke(main, ['list', 'all', '--filter', 'in-progress'])

        mock_list.assert_called_once_with(user=None, filter="in-progress")
        assert result.exit_code == 0
        assert "In Progress Book - Author Name (45%)" in result.output
