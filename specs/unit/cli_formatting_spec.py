"""Tests for CLI formatting functions."""

from bookminder.apple_books.library import Book
from bookminder.cli import format, format_book_list


def _book(**kwargs):
    """Create a test book with default values."""
    defaults = {"title": "Test Book", "author": "Test Author"}
    defaults.update(kwargs)
    return Book(**defaults)


def describe_format():
    def it_formats_book_with_no_attributes():
        assert format(_book()) == "Test Book - Test Author"

    def it_formats_book_with_progress():
        result = format(_book(reading_progress_percentage=42))
        assert result == "Test Book - Test Author (42%)"

    def it_formats_book_with_sample_status():
        result = format(_book(is_sample=True))
        assert result == "Test Book - Test Author • Sample"

    def it_formats_book_with_cloud_status():
        result = format(_book(is_cloud=True))
        assert result == "Test Book - Test Author ☁️"

    def it_formats_book_with_all_attributes():
        book = _book(
            reading_progress_percentage=42,
            is_sample=True,
            is_cloud=True,
        )
        result = format(book)
        assert result == "Test Book - Test Author (42%) • Sample ☁️"


def describe_format_book_list():
    def it_returns_empty_message_when_no_books():
        result = format_book_list([])
        assert result == "No books found"

    def it_uses_custom_empty_message():
        result = format_book_list([], empty_message="No books currently being read")
        assert result == "No books currently being read"

    def it_formats_single_book():
        books = [
            Book(title="Book 1", author="Author 1"),
        ]
        result = format_book_list(books)
        assert result == "Book 1 - Author 1"

    def it_formats_multiple_books():
        books = [
            Book(title="Book 1", author="Author 1"),
            Book(title="Book 2", author="Author 2"),
        ]
        result = format_book_list(books)
        assert result == "Book 1 - Author 1\nBook 2 - Author 2"

    def it_formats_books_with_mixed_attributes():
        books = [
            Book(
                title="Book 1",
                author="Author 1",
                reading_progress_percentage=50,
            ),
            Book(
                title="Book 2",
                author="Author 2",
                is_sample=True,
            ),
            Book(
                title="Book 3",
                author="Author 3",
                is_cloud=True,
            ),
        ]
        result = format_book_list(books)
        expected = (
            "Book 1 - Author 1 (50%)\n"
            "Book 2 - Author 2 • Sample\n"
            "Book 3 - Author 3 ☁️"
        )
        assert result == expected
