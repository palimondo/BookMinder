"""Tests for CLI formatting functions."""

from bookminder.apple_books.library import Book
from bookminder.cli import _format_book_output, format_book_list


def describe_format_book_output():
    def it_formats_book_with_no_attributes():
        book = Book(
            title="Test Book",
            author="Test Author",
            path="",
            updated=None,
        )
        result = _format_book_output(book)
        assert result == "Test Book - Test Author"

    def it_formats_book_with_progress():
        book = Book(
            title="Test Book",
            author="Test Author",
            path="",
            updated=None,
            reading_progress_percentage=42,
        )
        result = _format_book_output(book)
        assert result == "Test Book - Test Author (42%)"

    def it_formats_book_with_sample_status():
        book = Book(
            title="Test Book",
            author="Test Author",
            path="",
            updated=None,
            is_sample=True,
        )
        result = _format_book_output(book)
        assert result == "Test Book - Test Author • Sample"

    def it_formats_book_with_cloud_status():
        book = Book(
            title="Test Book",
            author="Test Author",
            path="",
            updated=None,
            is_cloud=True,
        )
        result = _format_book_output(book)
        assert result == "Test Book - Test Author ☁️"

    def it_formats_book_with_all_attributes():
        book = Book(
            title="Test Book",
            author="Test Author",
            path="",
            updated=None,
            reading_progress_percentage=42,
            is_sample=True,
            is_cloud=True,
        )
        result = _format_book_output(book)
        assert result == "Test Book - Test Author (42%) • Sample ☁️"

    def it_ensures_sample_indicator_appears_before_cloud():
        book = Book(
            title="Test Book",
            author="Test Author",
            path="",
            updated=None,
            is_sample=True,
            is_cloud=True,
        )
        result = _format_book_output(book)
        assert result.index("• Sample") < result.index("☁️")


def describe_format_book_list():
    def it_returns_empty_message_when_no_books():
        result = format_book_list([])
        assert result == "No books found"

    def it_uses_custom_empty_message():
        result = format_book_list([], empty_message="No books currently being read")
        assert result == "No books currently being read"

    def it_formats_single_book():
        books = [
            Book(title="Book 1", author="Author 1", path="", updated=None),
        ]
        result = format_book_list(books)
        assert result == "Book 1 - Author 1"

    def it_formats_multiple_books():
        books = [
            Book(title="Book 1", author="Author 1", path="", updated=None),
            Book(title="Book 2", author="Author 2", path="", updated=None),
        ]
        result = format_book_list(books)
        assert result == "Book 1 - Author 1\nBook 2 - Author 2"

    def it_formats_books_with_mixed_attributes():
        books = [
            Book(
                title="Book 1",
                author="Author 1",
                path="",
                updated=None,
                reading_progress_percentage=50,
            ),
            Book(
                title="Book 2",
                author="Author 2",
                path="",
                updated=None,
                is_sample=True,
            ),
            Book(
                title="Book 3",
                author="Author 3",
                path="",
                updated=None,
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
