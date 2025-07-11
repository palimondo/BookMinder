"""Unit tests for CLI with mocked library functions."""

from unittest.mock import patch

from click.testing import CliRunner

from bookminder.apple_books.library import Book
from bookminder.cli import main


def test_books():
    """Create test books for mocking."""
    return [
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
        Book(
            title="The Beginning of Infinity",
            author="David Deutsch",
            reading_progress_percentage=59,
        ),
    ]


def sample_books():
    """Create sample books for mocking."""
    return [
        Book(
            title="Snow Crash",
            author="Neal Stephenson",
            is_sample=True,
        ),
        Book(
            title="Tiny Experiments",
            author="Anne-Laure Le Cunff",
            reading_progress_percentage=1,
            is_sample=True,
        ),
    ]


def describe_bookminder_list_recent_command():

    def it_shows_recently_read_books_with_progress():
        runner = CliRunner()
        books = test_books()

        with patch('bookminder.cli.list_recent_books') as mock:
            mock.return_value = books
            result = runner.invoke(main, ['list', 'recent'])

        assert result.exit_code == 0
        output_lines = result.output.strip().split("\n")

        # Should show all 3 books
        assert len(output_lines) == 3

        # Check each book is formatted correctly
        assert "The Left Hand of Darkness - Ursula K. Le Guin (32%)" in result.output
        assert "Lao Tzu: Tao Te Ching - Ursula K. Le Guin (8%) ☁️" in result.output
        assert "The Beginning of Infinity - David Deutsch (59%)" in result.output

    def it_handles_empty_recent_books():
        runner = CliRunner()

        with patch('bookminder.cli.list_recent_books') as mock:
            mock.return_value = []
            result = runner.invoke(main, ['list', 'recent'])

        assert result.exit_code == 0
        assert "No books currently being read" in result.output

    def it_passes_user_parameter():
        runner = CliRunner()
        test_user = "test_reader"

        with patch('bookminder.cli.list_recent_books') as mock:
            mock.return_value = test_books()[:1]
            result = runner.invoke(main, ['list', 'recent', '--user', test_user])

        assert result.exit_code == 0
        mock.assert_called_once_with(user=test_user, filter=None)

    def it_passes_filter_parameter():
        runner = CliRunner()

        with patch('bookminder.cli.list_recent_books') as mock:
            # Return only cloud books when cloud filter is applied
            mock.return_value = [b for b in test_books() if b.get("is_cloud")]
            result = runner.invoke(main, ['list', 'recent', '--filter', 'cloud'])

        assert result.exit_code == 0
        mock.assert_called_once_with(user=None, filter='cloud')
        assert "Lao Tzu: Tao Te Ching" in result.output
        assert "The Left Hand of Darkness" not in result.output


def describe_bookminder_list_all_command():

    def it_shows_all_books_in_library():
        runner = CliRunner()
        all_books = test_books() + sample_books()

        with patch('bookminder.cli.list_all_books') as mock:
            mock.return_value = all_books
            result = runner.invoke(main, ['list', 'all'])

        assert result.exit_code == 0

        # Check all books appear
        for book in all_books:
            assert book["title"] in result.output

    def it_filters_by_sample_status():
        runner = CliRunner()

        with patch('bookminder.cli.list_all_books') as mock:
            mock.return_value = sample_books()
            result = runner.invoke(main, ['list', 'all', '--filter', 'sample'])

        assert result.exit_code == 0
        mock.assert_called_once_with(user=None, filter='sample')

        # Check sample books appear with indicator
        assert "Snow Crash - Neal Stephenson • Sample" in result.output
        assert "Tiny Experiments - Anne-Laure Le Cunff (1%) • Sample" in result.output

    def it_handles_empty_library():
        runner = CliRunner()

        with patch('bookminder.cli.list_all_books') as mock:
            mock.return_value = []
            result = runner.invoke(main, ['list', 'all'])

        assert result.exit_code == 0
        assert "No books found" in result.output


def describe_bookminder_list_with_filter():

    def it_filters_by_cloud_status():
        runner = CliRunner()
        cloud_books = [b for b in test_books() if b.get("is_cloud")]

        with patch('bookminder.cli.list_recent_books') as mock:
            mock.return_value = cloud_books
            result = runner.invoke(main, ['list', 'recent', '--filter', 'cloud'])

        assert result.exit_code == 0
        assert "Lao Tzu: Tao Te Ching" in result.output
        assert len(result.output.strip().split("\n")) == 1

    def it_excludes_cloud_books_when_filter_is_not_cloud():
        runner = CliRunner()
        non_cloud_books = [b for b in test_books() if not b.get("is_cloud")]

        with patch('bookminder.cli.list_recent_books') as mock:
            mock.return_value = non_cloud_books
            result = runner.invoke(main, ['list', 'recent', '--filter', '!cloud'])

        assert result.exit_code == 0
        assert "The Left Hand of Darkness" in result.output
        assert "The Beginning of Infinity" in result.output
        assert "Lao Tzu: Tao Te Ching" not in result.output
