from unittest.mock import patch

import pytest
from click.testing import CliRunner

from bookminder import BookminderError
from bookminder.apple_books.library import Book
from bookminder.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def describe_bookminder_list_recent_command():
    def it_shows_recently_read_books_with_progress(runner):
        book1 = Book(title="B1", author="A1")
        book2 = Book(title="B2", author="A2")

        with (
            patch("bookminder.cli.list_recent_books") as mock_list_recent,
            patch("bookminder.cli.format") as mock_format,
        ):
            mock_list_recent.return_value = [book1, book2]
            runner.invoke(main, ["list", "recent"])

        mock_list_recent.assert_called_once_with(user=None, filter=None)
        assert mock_format.call_args_list == [((book1,),), ((book2,),)]


def describe_bookminder_list_with_filter():
    def it_filters_by_cloud_status(runner):
        with patch("bookminder.cli.list_recent_books") as mock_list_recent:
            runner.invoke(main, ["list", "recent", "--filter", "cloud"])

        mock_list_recent.assert_called_once_with(user=None, filter="cloud")

    def it_excludes_cloud_books_when_filter_is_not_cloud(runner):
        with patch("bookminder.cli.list_recent_books") as mock_list_recent:
            runner.invoke(main, ["list", "recent", "--filter", "!cloud"])

        mock_list_recent.assert_called_once_with(user=None, filter="!cloud")


def describe_bookminder_list_all_command():
    def it_shows_all_books_in_library(runner):
        book1 = Book(title="B1", author="A1")
        book2 = Book(title="B2", author="A2")

        with (
            patch("bookminder.cli.list_all_books") as mock_list_all,
            patch("bookminder.cli.format") as mock_format,
        ):
            mock_list_all.return_value = [book1, book2]
            runner.invoke(main, ["list", "all"])

        mock_list_all.assert_called_once_with(user=None, filter=None)
        assert mock_format.call_args_list == [((book1,),), ((book2,),)]

    def it_filters_by_sample_status(runner):
        with patch("bookminder.cli.list_all_books") as mock_list_all:
            runner.invoke(main, ["list", "all", "--filter", "sample"])

        mock_list_all.assert_called_once_with(user=None, filter="sample")

    @pytest.mark.skip(reason="Implement after basic list all works")
    def it_excludes_samples_when_filter_is_not_sample():
        pass


def describe_cli_error_boundary():
    """Verify CLI properly handles errors from library layer."""

    def it_displays_library_errors_without_stack_traces(runner):
        error_message = "Something went wrong in the library"

        with patch("bookminder.cli.list_recent_books") as mock:
            mock.side_effect = BookminderError(error_message)
            result = runner.invoke(main, ["list", "recent"])

        assert result.exit_code == 0
        assert error_message in result.output
        assert "Traceback" not in result.output

        with patch("bookminder.cli.list_all_books") as mock:
            mock.side_effect = BookminderError(error_message)
            result = runner.invoke(main, ["list", "all"])

        assert result.exit_code == 0
        assert error_message in result.output
        assert "Traceback" not in result.output
